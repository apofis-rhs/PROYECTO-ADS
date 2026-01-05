document.addEventListener('DOMContentLoaded', function() {
    // 1. SELECTORES (Corregidos)
    const selectNivel = document.querySelector('#id_nivel') || document.querySelector('select[name="nivel"]');
    const selectGrado = document.querySelector('#id_grado') || document.querySelector('select[name="grado"]');
    const inputPeriodo = document.querySelector('#id_periodo') || document.querySelector('input[name="periodo"]');

    // CONSOLE LOG CORREGIDO (Sin el error de selectPeriodo)
    console.log("Revisión de elementos:", {
        nivel: selectNivel ? "Encontrado" : "NO ENCONTRADO",
        grado: selectGrado ? "Encontrado" : "NO ENCONTRADO",
        periodo: inputPeriodo ? "Encontrado" : "NO ENCONTRADO"
    });

    function actualizarInterfaz() {
        if (!selectNivel || !selectGrado) return;

        const nivelId = String(selectNivel.value).trim();
        console.log("Nivel detectado:", nivelId);

        // Limpiar grados
        selectGrado.innerHTML = '<option value="">Seleccionar...</option>';
        let opciones = [];

        // Lógica de grados según el ID del nivel
        switch (nivelId) {
            case "1": opciones = ["1° Kinder", "2° Kinder", "3° Kinder"]; break;
            case "2": opciones = ["1° Primaria", "2° Primaria", "3° Primaria", "4° Primaria", "5° Primaria", "6° Primaria"]; break;
            case "3": opciones = ["1° Secundaria", "2° Secundaria", "3° Secundaria"]; break;
            case "4": opciones = ["1° Semestre", "2° Semestre", "3° Semestre", "4° Semestre", "5° Semestre", "6° Semestre"]; break;
            case "5": opciones = ["1° Semestre", "2° Semestre", "3° Semestre", "4° Semestre", "5° Semestre", "6° Semestre", "7° Semestre", "8° Semestre", "9° Semestre", "10° Semestre"]; break;
        }

        if (opciones.length > 0) {
            opciones.forEach(texto => {
                const opt = document.createElement('option');
                // IMPORTANTE: Extraemos el número para el valor de la BD
                const numeroMatch = texto.match(/\d+/);
                opt.value = numeroMatch ? numeroMatch[0] : "";
                opt.textContent = texto;
                selectGrado.appendChild(opt);
            });
        }

        // Actualizar Placeholder
        if (inputPeriodo) {
            if (["4", "5"].includes(nivelId)) {
                inputPeriodo.setAttribute('placeholder', 'Ej: 2025-1');
            } else if (nivelId !== "") {
                inputPeriodo.setAttribute('placeholder', 'Ej: 2024');
            }
        }
    }

    // EVENTOS
    if (selectNivel) {
        selectNivel.addEventListener('change', () => {
            if (inputPeriodo) {
                inputPeriodo.value = "";
                inputPeriodo.classList.remove('is-invalid', 'is-valid');
            }
            actualizarInterfaz();
        });
        actualizarInterfaz();
    }

    // VALIDACIÓN VISUAL PERIODO
    if (inputPeriodo) {
        inputPeriodo.addEventListener('blur', function() {
            const nivelId = selectNivel ? String(selectNivel.value).trim() : "";
            const valor = this.value.trim();
            this.classList.remove('is-invalid', 'is-valid');

            if (valor === "") return;

            if (["1", "2", "3"].includes(nivelId)) {
                if (/^\d{4}$/.test(valor)) {
                    this.classList.add('is-valid');
                } else {
                    this.classList.add('is-invalid');
                }
            } else if (["4", "5"].includes(nivelId)) {
                if (/^(\d{4})-(1|2)$/.test(valor)) {
                    this.classList.add('is-valid');
                } else {
                    this.classList.add('is-invalid');
                }
            }
        });
    }

    // VALIDACIÓN CLAVE
    const inputClave = document.querySelector('#id_clave_grupo') || document.querySelector('input[name="clave_grupo"]');
    if (inputClave) {
        inputClave.addEventListener('input', function() {
            this.value = this.value.toUpperCase().replace(/\s/g, '');
            this.classList.remove('is-invalid', 'is-valid');
        });
        inputClave.addEventListener('blur', function() {
            const regexClave = /^[A-Z0-9-]{2,10}$/;
            if (this.value !== "") {
                if (regexClave.test(this.value)) {
                    this.classList.add('is-valid');
                } else {
                    this.classList.add('is-invalid');
                }
            }
        });
    }
});