# Continuar desde consola — 2026-09-17

> Este archivo es un mensaje de arranque para una sesión de Claude Code en consola/local con acceso real a `bestronger-vps` (SSH) y a los dos repos (`AgenticdesignBS`, `Bckbs`). Pégalo entero como primer mensaje de esa sesión.

## Contexto que ya es cierto (no re-verificar, no re-decidir)

Repo `ilzarpeatore/AgenticdesignBS`, rama `main`, commit `7469a83` ya en remoto. La única fuente de verdad de qué falta es `docs/TAREAS_PENDIENTES.md` — léelo entero antes de tocar nada, no confíes en el resumen de abajo para el detalle fino, solo para orientarte rápido.

Lo que cambió en la última sesión (mergeado limpio, sin conflictos reales):

- **Memoria persistente por cliente** (diseño nuevo, a partir de un caso real de un cliente — guideline de Borja): `perfil-cliente.schema.json` ganó `contexto_vida` (ocupación, horario laboral, sueño, estrés, historial de coaching previo). Nuevo esquema compartido `agentes/programacion-entrenamiento/esquemas/checkpoint-fisico.schema.json` (reevaluación física periódica: métricas + `observaciones_coach` en texto libre — esa es la pieza que más importa). Ambos `system-prompt.md` (entrenamiento v0.11.0, nutrición v0.6.0) ahora exigen leer las últimas entradas de `log-registro`/`log-nutricion`/`checkpoint-fisico` de ese cliente ANTES de generar, no solo escribir después. Sigue como decisión abierta (ítem **2.6**) dónde viven físicamente esos archivos reales — a propósito no viven en este repo, son datos sensibles de clientes.
- **Verificación real contra VPS** (otra sesión, mergeada): 1.2 (severidad de alergias en `client_limitations`) estaba marcada como bloqueada y en realidad **ya está aplicada en producción** — migración en estado `Ran`, columna `severity` presente, validación 422 confirmada. 1.1 se verificó parcialmente: dry-run limpio contra los 2 catálogos ya importados (`training_program #48` y `#50`, dedupe por `source_id` funciona bien), `check-integrity` sin `--fix` corrió limpio contra 207 filas reales ("sin referencias rotas"). `--confidence-gate` **no** se pudo ejercitar de verdad porque el flujo corta en "ya existe" antes de llegar a esa lógica — hace falta un `.xlsx` nuevo, no importado aún.
- **Datos reales encontrados** (ítem 2.3): 4 filas en `nutrition_questionnaire_answers.allergies_intolerances` con texto libre y sin fila estructurada en `client_limitations`. Dos son ruido (demo/test). Las dos que importan: `user_id 99` Toni Pérez Fernández ("fruta/lactosa") y `user_id 101` Borja Betanzos ("alergia a la mayoría de pieles de frutas, pero come fruta igual, no le preocupa").

## Qué puedes hacer tú (con acceso VPS que la sesión sandbox no tiene)

1. **Ítem 1.1, cerrarlo de verdad**: conseguir/generar un `.xlsx` de catálogo que NO esté ya en `storage/imports/` del VPS, correr `programs:import excel --dry-run --json --confidence-gate` contra él para ver el gate actuar de verdad con casos ambiguos, y si aparece un `review_required` concreto, llevarlo a revisión humana antes de escribir nada real (regla del proyecto: nunca escribir en producción sin que un humano vea el caso). Si todo sale bien, entonces sí ejecutar la importación real + `programs:assign-client` de punta a punta.
2. **Ítem 2.3, la parte humana**: para Toni Pérez Fernández y Borja Betanzos, decidir `type`/`severity` de sus alergias (con el coach, no automatizado) y crear las filas en `client_limitations` vía el endpoint ya existente `POST client-limitation-store`.

## Qué NO te toca decidir a ti (son del usuario, no de una sesión de consola)

- **2.4** — regla de derivación de `nivel_fuerza`: es criterio de coach.
- **2.5** — qué hacer con clientes onboarded antes del 2026-09-16 con campos `NULL`: decisión de producto.
- **2.6** — dónde viven los archivos reales de memoria por cliente: decisión operativa (¿carpeta privada? ¿tabla en Bckbs?).
- **2.7** — si se construye una capa de "hábitos prioritarios" (aparece en el caso de Borja) y en qué agente: decisión de alcance, contenido nuevo.

No resuelvas estos cuatro por tu cuenta aunque parezca obvio — están marcados 🟡 a propósito.

## Reglas de siempre en este proyecto

- Nunca escribir en producción sin caso concreto + revisión humana.
- No construir nada especulativo — si una tarea depende de una decisión del usuario, se deja marcada, no se resuelve "por si acaso".
- Datos reales de clientes (PII, salud, alergias, composición corporal) no se commitean a `AgenticdesignBS` — es un repo de diseño, no de datos.
- Actualiza `docs/TAREAS_PENDIENTES.md` según avances (fila + "Última actualización" del encabezado), commit y push a `main` cuando termines cada pieza.
