# Changelog — Agente Importador de Programas

## v0.4.3 — 2026-09-27

Auditoría del diseño contra el contenido teórico del repositorio (`Agentic-Design-Patterns`), pedida por el usuario para todos los agentes.

- Cita corregida en la sección "Flujo paso a paso": "Planning + Prompt Chaining" sin números de capítulo (inconsistente con el resto del documento) pasa a "Planning, cap. 6 + Prompt Chaining, cap. 1".
- La sección 5 (Manejo de excepciones) ya aplicaba correctamente el patrón real de Exception Handling and Recovery (cap. 12) desde antes de esta auditoría — archivo inválido, fila irreparable en `check-integrity`, ambos fallos técnicos reales, no casos de negocio. A diferencia de los otros 4 agentes del sistema, este no necesitó corrección de fondo, solo confirmación.

## v0.4.2 — 2026-09-27

Primer import real de un macrociclo completo (5 mesociclos de un mismo cliente, Carlos Palomar, en 5 archivos separados) tras formalizar el flujo de plan macro + formato de revisión detallada del agente de programación. Pedido explícito del usuario para probar el pipeline end-to-end.

- 5 `.xlsx` (formato-excel.md, uno por mesociclo, semana local 1..N) generados traduciendo el contenido ya aprobado del documento de revisión (`formato-salida/formato-excel-detallado.md`) del agente de programación -- sin inventar nada nuevo en la traducción.
- Los 5 pasaron `validador/validar_programa.py` (`aprobado: true`, 0 errores) y `--dry-run --confidence-gate` (22 ejercicios en nivel A, confianza 1.0, `review_required` vacío) antes del import real.
- Import real contra `bestronger_test` (`bestronger-vps`) con `--json --confidence-gate --check-integrity`: `training_program_id` 129-133, 624 filas de ejercicio en total, 100% nivel A (0 creados, 0 ambiguos), `check-integrity` limpio tras cada uno. Verificado por SQL: `client_id=NULL`, `is_personal=0` en los 5 -- ninguno asignado, norma no negociable de este agente.
- **Agrupación en el panel admin:** el esquema de `training_programs` no tiene ningún campo relacional de agrupación (sin `macrociclo_id`/tag) -- se logra por convención de título (`training_programs.title`, ej. "Carlos Palomar -- Macrociclo 1 -- Mesociclo 3/5 -- ..."), que ordena y agrupa visualmente en la lista del admin panel pero no es un dato estructurado. Si en el futuro se necesita agrupación real (filtrar/consultar "todos los mesociclos de este macrociclo"), haría falta una columna nueva en Bckbs -- anotado como posible mejora, no construida.

## v0.4.1 — 2026-09-27

El usuario reportó que sus planes mensuales/mesociclos generados repetían el mismo ejercicio como "nuevo" una vez por semana (ej. "sentadilla unilateral" x4), sin priorizar ejercicios ya existentes en la BD. Investigado contra el código real de Bckbs (`ilzarpeatore/bckbs`, sin tocar producción):

- **Causa raíz encontrada y ya arreglada desde el 2026-09-24, antes del reporte del usuario:** `ExerciseMatcher` cargaba las firmas de la BD una sola vez al arrancar el import (cacheadas 1h) y no veía los ejercicios que el propio import iba creando sobre la marcha — el mismo nombre repetido en la semana 2 no encontraba el que se acababa de crear en la semana 1, y lo volvía a crear. Fix real (commit `70922d0`, con test de regresión): `ExerciseMatcher::register()` da de alta cada ejercicio recién creado en caliente, y `ProgramsImporter` recuerda los ya creados en el mismo import (`createdExercises`) para reutilizar el id aunque el matcher no lo devuelva por umbral/firma.
- **Fix relacionado, mismo día:** resolver de equivalencias con IA (commit `867c053`) para nombres que son traducciones/anglicismos de ejercicios ya existentes (el matcher por reglas no los reconocía) — opcional, requiere `ANTHROPIC_API_KEY`, sin ella el comportamiento es idéntico al anterior.
- El usuario confirmó haber visto el bug **antes** del 24/09 — coincide con la fecha del fix, probablemente ya resuelto en la práctica, pero **sin verificar todavía contra un import real nuevo en el VPS** (ítem 1.5 de `docs/TAREAS_PENDIENTES.md`, nuevo).
- Ninguno de los dos fixes cambia el flujo de este agente (sección 3 de `system-prompt.md`, sube a v0.4.1) — son mejoras internas del matcher que el agente ya invocaba igual, no requieren ningún comando/parámetro nuevo.
- Hallazgo aparte, no relacionado con este bug: `formato-salida/catalogo-ejercicios.xlsx` (el catálogo que consulta el Productor de entrenamiento antes de fijar cada nombre) no se actualiza desde el 2026-09-14 — con varios mesociclos reales importados desde entonces, es una foto parcial del catálogo real. Pendiente de que el usuario aporte una exportación actualizada.

## v0.4.0 — 2026-09-17

Sincroniza con `docs/AGENTE_IMPORTADOR.md` (Bckbs, commit `ada8b1b`) tras verificación end-to-end real contra `bestronger-vps`: se generó un mesociclo real nuevo (`nerea-media-m1.xlsx`, 68 filas) para tener por fin un catálogo no importado antes, y `--confidence-gate` detectó correctamente un match nivel D (confianza 0.74, `Peso muerto rumano a una pierna con kettlebell` confundido con `Peso muerto rumano con barra` — unilateral/kettlebell vs. bilateral/barra) más 7 auto-creaciones.

- **Cambio de norma, decisión explícita del usuario, sustituye el principio de diseño de v0.1.0:** el import (crear el `training_program` y los ejercicios de catálogo, incluidos auto-creados y matches ambiguos nivel C/D/E) se ejecuta automáticamente — ya no hay dry-run obligatorio ni pausa por `review_required` antes de escribir. El riesgo era menor de lo que asumía el diseño original: un ejercicio mal matcheado que solo existe en el catálogo, sin cliente asignado todavía, es bajo coste y reversible.
- **La pausa humana no negociable se mueve a la asignación:** este agente nunca ejecuta `programs:assign-client`/`POST training-program-assign-client`, bajo ninguna circunstancia — es siempre una acción manual del humano en el panel admin, después de revisar el programa recién creado.
- `--confidence-gate` sigue existiendo y siendo válido, pero deja de ser el flujo por defecto de este agente.
- Import real ejecutado end-to-end sobre `nerea-media-m1.xlsx`: `training_program #55` creado, 27 ejercicios nuevos, 0 asignaciones a cliente, `check-integrity` limpio inmediatamente después.
- `system-prompt.md` sube a v0.4.0: secciones 1 (NO debes), 2 (herramientas), 3 (flujo), 4 (principio no negociable) y 5 (excepciones) reescritas.

## v0.3.0 — 2026-09-15

Cierra el último bloqueante real de `docs/AGENTE_IMPORTADOR.md` (Bckbs): el endpoint HTTP del import.

- **`system-prompt.md` (v0.3.0):** `POST program-import` (Bckbs, rama `feature/program-import-http-endpoint`) permite operar sin SSH — devuelve el mismo JSON que la CLI, mismo motor por debajo. Secciones 1-3 reescritas para presentar SSH y HTTP como vías equivalentes (import y asignación tienen ambas; integridad, de momento, solo SSH).
- De paso se corrigió un bug de regresión real en Bckbs (no en este repo): `programs:import` y `programs:assign-client` fatal en cuanto se cargaban, por un método `fail()` privado que chocaba con uno público ya definido en la clase base de Laravel — introducido y detectado en la misma sesión, arreglado antes de que nadie lo notara en producción.

## v0.2.0 — 2026-09-15

Se revisó `docs/AGENTE_IMPORTADOR.md` (Bckbs) contra el estado real del código y aparecieron dos desactualizaciones que este agente heredaba tal cual.

- **`system-prompt.md` (v0.2.0):** la asignación a cliente deja de tratarse como manual — `programs:assign-client` (nuevo comando en Bckbs, rama `feature/assign-client-command`) reutiliza la misma lógica que ya exponía el panel vía `POST training-program-assign-client`, que llevaba existiendo sin que el documento lo reflejara. `check-integrity` también deja de describirse como completamente manual: corre solo vía cron semanal desde una sesión anterior no reflejada aquí. Paso 5 del flujo actualizado para ejecutar el comando nuevo en vez de "documentar un proceso manual".

## v0.1.0 — 2026-09-15

Primer borrador, priorizado por el usuario por delante de seguir puliendo el Asistente de Programación de Entrenamiento.

- **Nuevo `system-prompt.md`:** rol y alcance (qué NO decide: ni programación de entrenamiento, ni candidato de ejercicio ante ambigüedad), herramientas disponibles (Tool Use, cap. 5) sobre `ilzarpeatore/Bckbs`, flujo paso a paso (dry-run → revisión humana obligatoria de `review_required` → import real → asignación → check-integrity → informe), el principio no negociable de nunca escribir en producción sin revisión humana de matches ambiguos/auto-creados, manejo de excepciones, y asignación de modelo.
- Se apoya en la salida `--json` de `programs:import` (implementada en el mismo turno, ver `feature/import-json-output` en `ilzarpeatore/Bckbs`), que es lo que hace operable este agente sin depender de parsear texto de consola.
- Ver `docs/AGENTE_IMPORTADOR.md` en `ilzarpeatore/Bckbs` para el diseño técnico completo del sistema que este agente opera — este documento es la capa operativa, no lo duplica.
