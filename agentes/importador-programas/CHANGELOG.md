# Changelog — Agente Importador de Programas

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
