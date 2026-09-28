# Changelog — Validador determinista (Paso 3)

## v0.6.0 — 2026-09-28

El usuario reportó que todas las programaciones entregadas hasta ahora mantienen el mismo número de series y repeticiones durante los 5-6 meses de un macrociclo, sin progresión de ningún tipo — ver `../CHANGELOG.md` v0.25.0 para el diagnóstico completo (el conocimiento ya existía en `progresion-carga.md`/`biomecanica-programacion-hipertrofia.md`, el hueco real era que nada lo comprobaba).

- Nuevo chequeo: por ejercicio, compara la tupla completa (`series`, `reps`, `rir`, `rpe`, `carga_kg`, `carga_pct`) entre las semanas de acumulación del mesociclo (excluye deload). Si la tupla es idéntica en todas — ningún eje progresa — se marca. Deliberadamente NO exige que un eje concreto cambie: cuál de los seis progresa es decisión del Productor caso a caso (`progresion-carga.md`).
- **Verificado contra el fixture real de Toni antes de escribir la lógica**, no después: su programa progresa solo vía RIR (series y reps fijos las 3 semanas) — eso es válido y no debía marcarse. Si el chequeo hubiera mirado solo series o solo reps, habría marcado como fallo un programa real ya entregado a un cliente.
- Un único ejercicio sin progresión es advertencia (puede ser deliberado, ej. un ejercicio de estabilidad). Si la mitad o más de los ejercicios del programa no progresan en ningún eje, es error bloqueante — el patrón sistémico real reportado.
- Nuevo `--semanas-deload` (opcional, mismo patrón que `--semanas-esperadas`/`--excluidos`): por defecto trata la última semana vista como deload (regla universal en todos los módulos de objetivo), sin necesidad de que el Productor lo declare explícitamente salvo que el mesociclo no siga ese patrón.
- 4 tests nuevos (`TestProgresionDeVolumen`): el caso real de Toni no marca nada; una mutación completamente plana sí (error); un único ejercicio plano es solo advertencia; `--semanas-deload` explícito excluye correctamente esas semanas del juicio. Suite completa (17 tests) verde.
- **Gap real, no cerrado aquí**: este validador audita un `.xlsx` (un mesociclo) a la vez — la progresión de un ejercicio ancla entre mesociclos de un mismo macrociclo queda fuera de su alcance, depende del Crítico releyendo la memoria episódica del cliente (ver `../system-prompt.md` sección 6).

## v0.5.0 — histórico

Primera versión como código real (antes era prosa descriptiva) — ver `../CHANGELOG.md` v0.5.0 para el contexto original. Probado contra el programa real entregado a un cliente (Toni) como fixture principal.
