# academico/services.py

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import Dict, Iterable, List, NamedTuple, Optional, Tuple
import random

from django.db import transaction

from .models import (
    DisponibilidadDocente,
    Grupo,
    Horario,
    Materia,
    NivelEducativo,
    ReglaHorario,
)


class ResultadoGeneracion(NamedTuple):
    """
    Resultado de una ejecucion del generador de horarios.

    Atributos:
        es_valido:
            True si las asignaciones pasan la validacion y se persisten;
            False si hubo errores de contexto o validacion.
        errores:
            Lista de mensajes de error (si es_valido = False).
        total_asignaciones:
            Numero total de bloques horario asignados a grupos.
    """

    es_valido: bool
    errores: List[str]
    total_asignaciones: int


@dataclass(frozen=True)
class Slot:
    """
    Representa un bloque horario generico dentro de un dia.

    Atributos:
        dia_semana:
            Entero 1..7 (1 = Lunes, 7 = Domingo).
        hora_inicio:
            Hora de inicio del bloque.
        hora_fin:
            Hora de fin del bloque.
        numero_bloque:
            Indice del bloque dentro del dia (1, 2, 3, ...).
    """

    dia_semana: int
    hora_inicio: time
    hora_fin: time
    numero_bloque: int


class HorarioGenerator:
    """
    Servicio para generar horarios a partir de:
      - Nivel educativo
      - Periodo
      - Grado (kinder–prepa) o semestre (universidad)
      - Tipo de alumno (regular/irregular, etc.)
      - Carrera (en niveles universitarios, si aplica)

    Se apoya en:
        - ReglaHorario:
            Define duracion de bloque, maximo de materias por dia, descansos, etc.
        - Materia.sesiones_por_semana:
            Cuantos bloques a la semana requiere cada materia.
        - Grupo:
            Cada grupo representa una combinacion salon + materia + docente + periodo.
        - DisponibilidadDocente:
            Franja horaria en la que el docente puede impartir clase.
    """

    # ------------------------------------------------------------------
    # Inicializacion
    # ------------------------------------------------------------------
    def __init__(
        self,
        periodo: str,
        id_nivel: int | str,
        grado: Optional[int | str] = None,
        semestre: Optional[int | str] = None,
        tipo_alumno: Optional[str] = None,
        id_carrera: Optional[int | str] = None,
    ) -> None:
        # Normalizamos tipos basicos
        self.periodo: str = periodo
        self.id_nivel: Optional[int] = int(id_nivel) if id_nivel is not None else None
        self.grado: Optional[int] = (
            int(grado) if grado not in (None, "", "0") else None
        )
        self.semestre: Optional[int] = (
            int(semestre) if semestre not in (None, "", "0") else None
        )
        self.tipo_alumno: Optional[str] = tipo_alumno or None
        self.id_carrera: Optional[int] = (
            int(id_carrera) if id_carrera not in (None, "", "0") else None
        )

        # Lista opcional de IDs de Grupo a incluir en la generacion.
        # Se rellena desde la vista, para permitir "generar solo para estos grupos".
        self.grupos_ids_seleccionados: Optional[List[int]] = None

    # ------------------------------------------------------------------
    # API principal
    # ------------------------------------------------------------------
    def generar(self) -> ResultadoGeneracion:
        """
        Orquesta el flujo completo de generacion:

        1) Obtiene el nivel educativo.
        2) Busca la ReglaHorario activa para ese nivel y filtros.
        3) Obtiene los grupos (segun nivel, grado/semestre, carrera, periodo).
        4) Genera los slots (bloques horarios) a partir de la regla.
        5) Asigna slots a grupos respetando restricciones de:
           - sesiones por semana
           - maximo por dia
           - choques por grupo, docente y salon
           - disponibilidad del docente
        6) Valida el resultado.
        7) Si es valido, persiste en la tabla Horario.

        Retorna:
            ResultadoGeneracion con detalle de exito/errores.
        """
        errores: List[str] = []

        # Validacion minima de parametros
        if not self.periodo or not self.id_nivel:
            return ResultadoGeneracion(
                es_valido=False,
                errores=["Debes indicar al menos periodo e id_nivel."],
                total_asignaciones=0,
            )

        # 1) Nivel educativo
        nivel = self._obtener_nivel()
        if nivel is None:
            return ResultadoGeneracion(
                es_valido=False,
                errores=[f"No existe el nivel educativo con id={self.id_nivel}"],
                total_asignaciones=0,
            )

        # 2) Regla de horario
        regla = self._obtener_regla(nivel)
        if regla is None:
            return ResultadoGeneracion(
                es_valido=False,
                errores=["No hay ReglaHorario activa para los filtros indicados."],
                total_asignaciones=0,
            )

        # 3) Grupos a programar
        grupos = self._obtener_grupos(nivel)
        if not grupos:
            return ResultadoGeneracion(
                es_valido=False,
                errores=[
                    "No se encontraron grupos para el nivel / grado / semestre / "
                    "periodo indicados."
                ],
                total_asignaciones=0,
            )

        # 4) Slots (bloques horarios) disponibles
        slots = self._generar_slots(regla)
        if not slots:
            return ResultadoGeneracion(
                es_valido=False,
                errores=["La regla seleccionada no genera ningun bloque horario."],
                total_asignaciones=0,
            )

        # 5) Asignacion de slots a grupos
        asignaciones = self._asignar_slots(grupos, slots, regla)

        # 6) Validacion de las asignaciones generadas
        errores_validacion = self._validar_asignaciones(asignaciones, regla)
        if errores_validacion:
            return ResultadoGeneracion(
                es_valido=False,
                errores=errores_validacion,
                total_asignaciones=len(asignaciones),
            )

        # 7) Persistencia en BD
        self._persistir_asignaciones(asignaciones)

        return ResultadoGeneracion(
            es_valido=True,
            errores=[],
            total_asignaciones=len(asignaciones),
        )

    # ------------------------------------------------------------------
    # 1. Contexto: nivel, regla, grupos
    # ------------------------------------------------------------------
    def _obtener_nivel(self) -> Optional[NivelEducativo]:
        """
        Devuelve el objeto NivelEducativo correspondiente a self.id_nivel,
        o None si no existe.
        """
        if self.id_nivel is None:
            return None
        try:
            return NivelEducativo.objects.get(pk=self.id_nivel)
        except NivelEducativo.DoesNotExist:
            return None

    def _es_universidad(self, nivel: NivelEducativo) -> bool:
        """
        Heuristica simple para distinguir niveles universitarios.

        Puedes ajustar esta logica (por ejemplo, agregar un campo booleano
        'es_universidad' en el modelo NivelEducativo y consultarlo aqui).
        """
        nombre = (nivel.nombre or "").strip().lower()
        return nombre in {"universidad", "licenciatura", "universitario"}

    def _obtener_regla(self, nivel: NivelEducativo) -> Optional[ReglaHorario]:
        """
        Obtiene la ReglaHorario activa para el nivel.

        Regla GLOBAL:
        - Si el nivel no tiene regla propia, se usa la regla activa de Kínder.
        - Si tampoco existe, se usa la primera regla activa del sistema.
        """

        # 1) Intento normal: regla del nivel seleccionado
        qs = ReglaHorario.objects.filter(nivel=nivel, activo=True)

        if self._es_universidad(nivel):
            if self.semestre is not None:
                qs = qs.filter(semestre=self.semestre)
            if self.tipo_alumno:
                qs = qs.filter(tipo_alumno=self.tipo_alumno)
        else:
            qs = qs.filter(semestre__isnull=True, tipo_alumno__isnull=True)

        regla = qs.order_by("id_regla").first()
        if regla:
            return regla

        # 2) Fallback: usar regla de Kínder como GLOBAL
        regla_kinder = (
            ReglaHorario.objects
            .filter(activo=True, nivel__nombre__icontains="kinder")
            .order_by("id_regla")
            .first()
        )
        if regla_kinder:
            return regla_kinder

        # 3) Último recurso: cualquier regla activa
        return ReglaHorario.objects.filter(activo=True).order_by("id_regla").first()




    def _obtener_grupos(self, nivel: NivelEducativo) -> List[Grupo]:
        """
        Obtiene la lista de grupos (salon + materia + docente) a programar.

        - Para Kinder–Prepa se filtra por 'grado' usando Materia.nivel_sugerido.
        - Para universidad se filtra por 'semestre' usando Materia.nivel_sugerido.
        - Si se indica id_carrera, se filtra tambien por carrera de la materia.
        - Siempre se filtra por nivel educativo y periodo.
        - Si self.grupos_ids_seleccionados no es None, se restringe a ese subconjunto.
        """
        # 1) Materias del nivel
        materias_qs = Materia.objects.filter(nivel_educativo=nivel)

        # Carrera (tipicamente para universidad)
        if self.id_carrera:
            materias_qs = materias_qs.filter(carrera_id=self.id_carrera)

        # Filtro por nivel sugerido (grado/semestre)
        if self._es_universidad(nivel):
            if self.semestre:
                materias_qs = materias_qs.filter(nivel_sugerido=self.semestre)
        else:
            if self.grado:
                materias_qs = materias_qs.filter(nivel_sugerido=self.grado)

        materias_ids = list(materias_qs.values_list("id_materia", flat=True))
        if not materias_ids:
            return []

        # 2) Grupos del nivel, periodo, y materias resultantes
        grupos_qs = Grupo.objects.filter(
            nivel=nivel,
            periodo=self.periodo,
            materia_id__in=materias_ids,
        )

        # Subconjunto explicito de grupos (checklist en la vista)
        if self.grupos_ids_seleccionados:
            grupos_qs = grupos_qs.filter(id_grupo__in=self.grupos_ids_seleccionados)

        # Para Kinder–Prepa, si tenemos grado se vuelve a aplicar como filtro
        if self.grado:
            grupos_qs = grupos_qs.filter(grado=self.grado)

        # Evitar N+1: cargamos materia y docente
        grupos_qs = grupos_qs.select_related("materia", "docente")

        return list(grupos_qs)

    # ------------------------------------------------------------------
    # 2. Generacion de slots (bloques horarios)
    # ------------------------------------------------------------------
    def _generar_slots(self, regla: ReglaHorario) -> List[Slot]:
        """
        Genera la lista de bloques horarios (Slot) en base a la ReglaHorario:

        - Usa un horario base (por defecto 07:00).
        - Genera 'materias_max_por_dia' bloques por dia (Lunes–Viernes).
        - Inserta un descanso despues de 'descanso_despues_bloque' si la regla lo define.
        """
        slots: List[Slot] = []

        hora_inicio_base = time(7, 0)  # Podrias parametrizar esto en la regla
        duracion_bloque = timedelta(minutes=regla.duracion_bloque_min)
        descanso = timedelta(minutes=regla.descanso_duracion_min)

        # Dias 1..5 = Lunes..Viernes
        for dia in range(1, 6):
            current = datetime.combine(datetime.today(), hora_inicio_base)
            numero_bloque = 1

            for _ in range(regla.materias_max_por_dia):
                # Insertar descanso despues del bloque indicado
                if (
                    regla.descanso_despues_bloque
                    and numero_bloque == regla.descanso_despues_bloque + 1
                ):
                    current += descanso

                inicio = current
                fin = inicio + duracion_bloque

                slots.append(
                    Slot(
                        dia_semana=dia,
                        hora_inicio=inicio.time(),
                        hora_fin=fin.time(),
                        numero_bloque=numero_bloque,
                    )
                )

                current = fin
                numero_bloque += 1

        return slots

    # ------------------------------------------------------------------
    # 2.b Validacion de asignaciones de profes
    # ------------------------------------------------------------------
    def _precargar_ocupacion_docentes(self, grupos_ids_generando: set[int]) -> dict[int, list[Slot]]:
        """
        Precarga la ocupación real de docentes desde la BD para el periodo actual,
        excluyendo los grupos que se van a regenerar (porque esos se borrarán y recrearán).

        Devuelve:
            {docente_id: [Slot, Slot, ...]}
        """
        horario_docente: dict[int, list[Slot]] = {}

        qs = (
            Horario.objects
            .select_related("grupo")
            .filter(grupo__periodo=self.periodo, grupo__docente__isnull=False)
            .exclude(grupo_id__in=grupos_ids_generando)
            .only("dia_semana", "hora_inicio", "hora_fin", "grupo__docente")
        )

        for h in qs:
            docente_id = h.grupo.docente_id
            if not docente_id:
                continue
            slot = Slot(
                dia_semana=h.dia_semana,
                hora_inicio=h.hora_inicio,
                hora_fin=h.hora_fin,
                numero_bloque=0,
            )
            horario_docente.setdefault(docente_id, []).append(slot)

        return horario_docente



    # ------------------------------------------------------------------
    # 3. Asignacion de slots a grupos
    # ------------------------------------------------------------------
    def _asignar_slots(
        self,
        grupos: List[Grupo],
        slots: List[Slot],
        regla: ReglaHorario,
    ) -> List[Dict]:
        """
        Asigna bloques a grupos usando una estrategia greedy con reparto equilibrado:

        - Cada grupo (grupo + materia) necesita 'sesiones_por_semana' bloques.
        - Se calcula cuantas sesiones por dia deberia tener cada grupo para repartir
          su carga lo mas uniforme posible a lo largo de la semana.
        - Se recorre la lista de slots en orden aleatorio y, para cada slot, se busca
          el primer grupo que cumpla:

            * Todavia tiene sesiones pendientes en la semana.
            * No ha alcanzado su maximo de sesiones ese dia.
            * No tiene ya una clase a la misma hora (evita choques por grupo).
            * Su salon (nivel + periodo + grado + clave_grupo) no tiene otra
              materia en esa misma franja (evita choques por salon).
            * Su docente esta disponible y libre en ese slot (evita choques
              por docente + respeta disponibilidad).
        """
        if not slots or not grupos:
            return []

        # 0) Dias distintos presentes en los slots
        dias_disponibles = sorted({s.dia_semana for s in slots})
        num_dias = len(dias_disponibles) or 1

        # 1) Sesiones totales por grupo y maximo por dia (reparto equilibrado)
        sesiones_pendientes: Dict[int, int] = {}
        max_sesiones_por_dia: Dict[int, int] = {}

        for g in grupos:
            total_semana = getattr(g.materia, "sesiones_por_semana", 1) or 1
            sesiones_pendientes[g.id_grupo] = total_semana

            # Ejemplos:
            #   3 sesiones en 5 dias -> 1 por dia
            #   6 sesiones en 5 dias -> 2 por dia
            equilibrio = max(1, (total_semana + num_dias - 1) // num_dias)

            # Respeta el limite global por dia definido en la regla (si existe)
            limite_regla = regla.materias_max_por_dia or equilibrio
            max_sesiones_por_dia[g.id_grupo] = min(equilibrio, limite_regla)

        # 2) Control de ocupacion: grupo, docente, salon, sesiones por dia
        horario_grupo: Dict[int, List[Slot]] = {g.id_grupo: [] for g in grupos}
        # Precarga ocupación real desde BD (para evitar choques con horarios ya existentes) CAMBIO --> HOY
        grupos_ids_generando = {g.id_grupo for g in grupos}
        horario_docente: Dict[int, List[Slot]] = self._precargar_ocupacion_docentes(grupos_ids_generando)

        sesiones_por_grupo_dia: Dict[int, Dict[int, int]] = defaultdict(
            lambda: defaultdict(int)
        )

        # Mapa de salon: (id_nivel, periodo, grado, clave_grupo)
        salon_por_grupo: Dict[int, Tuple[int, str, Optional[int], str]] = {}
        horario_salon: Dict[
            Tuple[int, str, Optional[int], str], List[Slot]
        ] = defaultdict(list)

        for g in grupos:
            salon_key = (g.nivel_id, g.periodo, g.grado, g.clave_grupo)
            salon_por_grupo[g.id_grupo] = salon_key

        # 3) Disponibilidad de docentes precargada
        disponibilidad_docente = self._cargar_disponibilidad_docentes(grupos)

        asignaciones: List[Dict] = []

        # 4) Barajamos los slots para no generar siempre el mismo patron
        slots_ordenados = sorted(slots, key=lambda s: (s.dia_semana, s.hora_inicio))
        random_slots = list(slots_ordenados)
        random.shuffle(random_slots)

        # 5) Asignacion greedy
        for slot in random_slots:
            # Tambien barajamos el orden de grupos para este slot
            grupos_shuffled = list(grupos)
            random.shuffle(grupos_shuffled)

            for g in grupos_shuffled:
                gid = g.id_grupo

                # 5.1) Si ya no necesita mas sesiones en la semana, saltamos
                if sesiones_pendientes[gid] <= 0:
                    continue

                # 5.2) Limite de sesiones por dia para este grupo
                if (
                    sesiones_por_grupo_dia[gid][slot.dia_semana]
                    >= max_sesiones_por_dia[gid]
                ):
                    continue

                # 5.3) Verificar que el grupo no tenga otra clase en este rango
                if self._tiene_traslape(horario_grupo[gid], slot):
                    continue

                # 5.3 bis) Verificar que el salon no tenga otra materia en este rango
                salon_key = salon_por_grupo[gid]
                if self._tiene_traslape(horario_salon[salon_key], slot):
                    continue

                # 5.4) Verificar docente (disponibilidad + no traslape)
                docente_id = g.docente_id
                if docente_id:
                    # a) Disponibilidad declarada
                    if not self._docente_esta_disponible(
                        docente_id, slot, disponibilidad_docente
                    ):
                        continue

                    # b) No esta ya asignado en otro grupo en la misma franja
                    slots_docente = horario_docente.setdefault(docente_id, [])
                    if self._tiene_traslape(slots_docente, slot):
                        continue

                # 5.5) Llegados aqui, se asigna el slot al grupo
                asignaciones.append(
                    {
                        "id_grupo": gid,
                        "dia_semana": slot.dia_semana,
                        "hora_inicio": slot.hora_inicio,
                        "hora_fin": slot.hora_fin,
                        "aula": None,
                    }
                )

                # Actualizamos contadores y ocupaciones
                sesiones_pendientes[gid] -= 1
                sesiones_por_grupo_dia[gid][slot.dia_semana] += 1
                horario_grupo[gid].append(slot)
                horario_salon[salon_key].append(slot)

                if docente_id:
                    horario_docente.setdefault(docente_id, []).append(slot)

                # 5.6) Si todos los grupos han completado sus sesiones, terminamos
                if all(v <= 0 for v in sesiones_pendientes.values()):
                    return asignaciones

        return asignaciones

    # ------------------------------------------------------------------
    # 3.bis. Utilidades de disponibilidad y traslapes
    # ------------------------------------------------------------------
    def _cargar_disponibilidad_docentes(
        self,
        grupos: Iterable[Grupo],
    ) -> Dict[int, Dict[int, List[Tuple[time, time]]]]:
        """
        Construye un diccionario de disponibilidad de docentes:

        {
          id_docente: {
            dia_semana: [(hora_inicio, hora_fin), ...]
          }
        }

        Solo carga la disponibilidad de los docentes que aparecen
        en la lista de grupos recibida.
        """
        docentes_ids = {g.docente_id for g in grupos if g.docente_id}
        if not docentes_ids:
            return {}

        disponibilidad: Dict[int, Dict[int, List[Tuple[time, time]]]] = {}

        for d in DisponibilidadDocente.objects.filter(docente_id__in=docentes_ids):
            por_docente = disponibilidad.setdefault(d.docente_id, {})
            rangos_dia = por_docente.setdefault(d.dia_semana, [])
            rangos_dia.append((d.hora_inicio, d.hora_fin))

        return disponibilidad

    def _docente_esta_disponible(
        self,
        docente_id: int,
        slot: Slot,
        disponibilidad: Dict[int, Dict[int, List[Tuple[time, time]]]],
    ) -> bool:
        """
        Verifica si el docente esta disponible para el 'slot' indicado.

        Regla de negocio actual:
          - Si el docente NO tiene registro en DisponibilidadDocente,
            se asume que esta disponible siempre.
          - Si tiene registros, solo se considera disponible en los rangos
            donde (hora_inicio_slot, hora_fin_slot) este totalmente contenido.
        """
        por_docente = disponibilidad.get(docente_id)
        if not por_docente:
            # Sin restricciones declaradas → disponible siempre
            return True

        rangos_dia = por_docente.get(slot.dia_semana, [])
        if not rangos_dia:
            # Tiene disponibilidad declarada, pero no para ese dia
            return False

        for inicio, fin in rangos_dia:
            if inicio <= slot.hora_inicio and slot.hora_fin <= fin:
                return True

        return False

    @staticmethod
    def _tiene_traslape(slots_existentes: List[Slot], nuevo: Slot) -> bool:
        """
        Indica si 'nuevo' se traslapa con alguno de los slots de 'slots_existentes'
        en el mismo dia.

        Condicion de traslape:
            nuevo.inicio < existente.fin  y  nuevo.fin > existente.inicio
        """
        for s in slots_existentes:
            if s.dia_semana != nuevo.dia_semana:
                continue
            if nuevo.hora_inicio < s.hora_fin and nuevo.hora_fin > s.hora_inicio:
                return True
        return False

    # ------------------------------------------------------------------
    # 4. Validacion final (por dia, por grupo, etc.)
    # ------------------------------------------------------------------
    def _validar_asignaciones(
        self,
        asignaciones: List[Dict],
        regla: ReglaHorario,
    ) -> List[str]:
        """
        Aplica validaciones de consistencia sobre las asignaciones generadas:

        - Que exista al menos una asignacion.
        - Que ningun grupo exceda materias_max_por_dia en un mismo dia.
        - Que cada grupo tenga asignadas todas sus sesiones_por_semana.
        """
        errores: List[str] = []
        if not asignaciones:
            errores.append("No se genero ninguna asignacion de horario.")
            return errores

        # 1) Conteo de sesiones por grupo y dia
        sesiones_por_grupo_dia: Dict[int, Dict[int, int]] = {}
        # 2) Conteo de sesiones totales por grupo en la semana
        sesiones_por_grupo_total: Dict[int, int] = {}

        for a in asignaciones:
            id_grupo = a["id_grupo"]
            dia = a["dia_semana"]

            # Por dia
            sesiones_dia = sesiones_por_grupo_dia.setdefault(id_grupo, {})
            sesiones_dia[dia] = sesiones_dia.get(dia, 0) + 1

            # Total semanal
            sesiones_por_grupo_total[id_grupo] = (
                sesiones_por_grupo_total.get(id_grupo, 0) + 1
            )

        # 3) Validar maximo por dia (segun regla)
        max_por_dia = regla.materias_max_por_dia or 1

        for id_grupo, por_dia in sesiones_por_grupo_dia.items():
            for dia, total in por_dia.items():
                if total > max_por_dia:
                    errores.append(
                        f"El grupo {id_grupo} tiene {total} sesiones el dia {dia}, "
                        f"mas que el maximo permitido ({max_por_dia})."
                    )

        # 4) Validar sesiones_por_semana vs asignadas
        grupos_ids = list(sesiones_por_grupo_total.keys())
        grupos = Grupo.objects.filter(pk__in=grupos_ids).select_related("materia")

        for g in grupos:
            requeridas = getattr(g.materia, "sesiones_por_semana", 1) or 1
            asignadas = sesiones_por_grupo_total.get(g.id_grupo, 0)

            if asignadas < requeridas:
                errores.append(
                    f"El grupo {g.id_grupo} ({g.materia.nombre}) solo tiene "
                    f"{asignadas} sesiones asignadas, pero requiere {requeridas}."
                )

        return errores

    # ------------------------------------------------------------------
    # 5. Persistencia
    # ------------------------------------------------------------------
    def _persistir_asignaciones(self, asignaciones: List[Dict]) -> None:
        """
        Persiste las asignaciones en la tabla Horario.

        Estrategia:
            - Se borran primero todos los horarios existentes de los grupos
              involucrados.
            - Se hace un bulk_create con las nuevas asignaciones.
            - Todo se ejecuta dentro de una transaccion atomica.
        """
        if not asignaciones:
            return

        grupos_ids = {a["id_grupo"] for a in asignaciones}

        with transaction.atomic():
            # 1) Borrar horarios previos de estos grupos
            Horario.objects.filter(grupo_id__in=grupos_ids).delete()

            # 2) Crear nuevos registros
            objetos = [
                Horario(
                    dia_semana=a["dia_semana"],
                    hora_inicio=a["hora_inicio"],
                    hora_fin=a["hora_fin"],
                    aula=a["aula"],
                    grupo_id=a["id_grupo"],
                )
                for a in asignaciones
            ]
            Horario.objects.bulk_create(objetos)
