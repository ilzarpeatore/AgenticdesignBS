# Continuar desde consola — 2026-09-17 (actualizado)

> Mensaje de arranque para una sesión de Claude Code en consola/local con acceso real a `bestronger-vps` (SSH) y a los repos (`AgenticdesignBS`, `Bckbs`, `bstronger-memoria-clientes`). Pégalo entero como primer mensaje de esa sesión. La sesión sandbox remota no tiene salida de red hacia el VPS (verificado: sin `ssh`, sin resolución DNS de `bestronger-vps`, `curl` a `testapp.bestronger.es` bloqueado por el proxy con 403) — por eso esto tiene que salir de ahí.

## Contexto que ya es cierto (no re-verificar, no re-decidir)

Repo `ilzarpeatore/AgenticdesignBS`, rama `main`, commit `2d4afaa` ya en remoto. La única fuente de verdad de qué falta es `docs/TAREAS_PENDIENTES.md` — léelo entero antes de tocar nada.

**Ya resuelto desde el último mensaje de consola (no lo repitas):**

- **2.6 — dónde vive la memoria real de cliente:** repo privado **`ilzarpeatore/bstronger-memoria-clientes`**, `clientes/<cliente_id>/` (`perfil-cliente.json`, `perfil-nutricional.json`, `checkpoints-fisicos.json`, `log-registro.json`, `log-nutricion.json`), plantilla en `_plantilla/`. Vacío de datos reales todavía.
- **2.7 — capa de "hábitos prioritarios":** nuevo módulo `agentes/programacion-nutricion/modulos/habitos-prioritarios.md` (solo en nutrición) + campo `habitos_prioritarios` en `esquemas/log-nutricion.schema.json`. `system-prompt.md` de nutrición en v0.7.0.
- **1.2 — severidad de alergias en Bckbs:** confirmada ya aplicada en producción (migración `Ran`, columna `severity`, validación 422 funcionando).

**Quedan exactamente dos tareas técnicas abiertas, ambas necesitan tu acceso VPS real:**

### 1.1 — Cerrar la verificación de `programs:import`/`--confidence-gate` contra BD real

Ya se probó parcialmente: `--dry-run --json` corrió limpio contra los 2 catálogos ya presentes en `storage/imports/` del VPS (`mesociclo_toni.xlsx` → `training_program #48`, `BeStronger_M1_Entrenamiento.xlsx` → `#50`, dedupe por `source_id` funciona bien), y `programs:check-integrity` sin `--fix` corrió limpio contra las 207 filas reales ("sin referencias rotas"). Lo que falta:

1. Conseguir/generar un `.xlsx` de catálogo que **no** esté ya importado en el VPS.
2. Correr `programs:import excel --dry-run --json --confidence-gate` contra él — es la primera vez que el gate se ejercitaría con casos ambiguos de verdad (hasta ahora el flujo cortaba en "ya existe" antes de llegar a esa lógica).
3. Si aparece un `review_required` concreto, llévalo a revisión humana (el coach) antes de escribir nada — regla del proyecto (`Bckbs/docs/AGENTE_IMPORTADOR.md`, sección 8): nunca escribir en producción sin un caso concreto visto por un humano.
4. Solo si eso sale bien: ejecutar la importación real + `programs:assign-client` de punta a punta.

### 2.3 — Alta estructurada de alergias para Toni y Borja

Ya está el listado real (consulta de solo lectura contra `nutrition_questionnaire_answers.allergies_intolerances`, ninguna con fila en `client_limitations`):

- `user_id 99` — Toni Pérez Fernández — texto libre: "fruta/lactosa"
- `user_id 101` — Borja Betanzos — texto libre: "Tengo alergia a la mayoría de pieles de frutas, pero como igual fruta, no es una alergia preocupante"

Falta la parte humana: que el coach decida `type` (`allergy`/`intolerance`/etc.) y `severity` (`mild`/`moderate`/`severe_anaphylaxis`) para cada uno, y las crees vía el endpoint ya existente `POST client-limitation-store`. A propósito no se automatiza el parseo del texto libre — es una decisión clínica, no de formato.

## Qué NO te toca decidir a ti (son del usuario, no de una sesión de consola)

- **2.4** — regla de derivación de `nivel_fuerza`: es criterio de coach.
- **2.5** — qué hacer con clientes onboarded antes del 2026-09-16 con campos `NULL`: decisión de producto.

No los resuelvas por tu cuenta aunque parezca obvio — están marcados 🟡 a propósito.

## Reglas de siempre en este proyecto

- Nunca escribir en producción sin caso concreto + revisión humana.
- No construir nada especulativo.
- Datos reales de clientes no se commitean a `AgenticdesignBS` — van a `bstronger-memoria-clientes` (memoria de coaching) o a Bckbs (datos operativos), nunca al repo de diseño.
- Actualiza `docs/TAREAS_PENDIENTES.md` según avances (fila + "Última actualización" del encabezado), commit y push a `main` cuando termines cada pieza.
