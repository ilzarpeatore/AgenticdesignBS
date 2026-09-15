# Changelog — Agente Importador de Programas

## v0.2.0 — 2026-09-15

Se revisó `docs/AGENTE_IMPORTADOR.md` (Bckbs) contra el estado real del código y aparecieron dos desactualizaciones que este agente heredaba tal cual.

- **`system-prompt.md` (v0.2.0):** la asignación a cliente deja de tratarse como manual — `programs:assign-client` (nuevo comando en Bckbs, rama `feature/assign-client-command`) reutiliza la misma lógica que ya exponía el panel vía `POST training-program-assign-client`, que llevaba existiendo sin que el documento lo reflejara. `check-integrity` también deja de describirse como completamente manual: corre solo vía cron semanal desde una sesión anterior no reflejada aquí. Paso 5 del flujo actualizado para ejecutar el comando nuevo en vez de "documentar un proceso manual".

## v0.1.0 — 2026-09-15

Primer borrador, priorizado por el usuario por delante de seguir puliendo el Asistente de Programación de Entrenamiento.

- **Nuevo `system-prompt.md`:** rol y alcance (qué NO decide: ni programación de entrenamiento, ni candidato de ejercicio ante ambigüedad), herramientas disponibles (Tool Use, cap. 5) sobre `ilzarpeatore/Bckbs`, flujo paso a paso (dry-run → revisión humana obligatoria de `review_required` → import real → asignación → check-integrity → informe), el principio no negociable de nunca escribir en producción sin revisión humana de matches ambiguos/auto-creados, manejo de excepciones, y asignación de modelo.
- Se apoya en la salida `--json` de `programs:import` (implementada en el mismo turno, ver `feature/import-json-output` en `ilzarpeatore/Bckbs`), que es lo que hace operable este agente sin depender de parsear texto de consola.
- Ver `docs/AGENTE_IMPORTADOR.md` en `ilzarpeatore/Bckbs` para el diseño técnico completo del sistema que este agente opera — este documento es la capa operativa, no lo duplica.
