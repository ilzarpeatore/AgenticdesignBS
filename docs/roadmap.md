# Roadmap del sistema de agentes

> Resumen versionado del diseño. La versión completa y navegable vive en el documento de diseño compartido (Artifact) — este archivo existe para que el diseño no dependa de una sola copia.

## Contexto de negocio

- Servicio de asesoría de entrenamiento y nutrición online.
- Hoy: servicio informal, atendido a amigos y familiares, sin apertura al mercado ni publicidad.
- Objetivo: automatizar progresivamente mediante agentes de IA, empezando por el agente que más tiempo consume hoy.

## Principio de progresión

Como en un programa de entrenamiento real: no se sube de fase por calendario, se sube cuando el criterio de progresión del ciclo anterior está cumplido.

## Los tres mesociclos

| Mesociclo | Contexto | Se automatiza | Control | Infraestructura |
|---|---|---|---|---|
| **M0 (actual)** | Amigos y familia, sin apertura al mercado | 3 agentes operativos (entrenamiento + import + nutrición) | Revisión humana al 100% | Ninguna — prompt guardado a mano, sin n8n |
| **M1** | Servicio abierto, <1.000€/mes | 2-3 agentes operativos | Revisión humana por muestreo | n8n + Google Sheets como log |
| **M2** | Ingresos recurrentes estables | 13 operativos + 6 controles + director | Un agente de control por área | n8n/Make + Airtable + Notion |

**Criterios de progresión:**
- M0 → M1: el servicio se abre al mercado con clientes de pago *y* el agente lleva varios ciclos seguidos sin correcciones mayores en revisión.
- M1 → M2: ingresos recurrentes sostenidos varios meses (~500-1.000€/mes) *y* los agentes operativos funcionan con supervisión por muestreo, no total.

## Agentes existentes

| Agente | Rol | Repo que opera | Documento |
|---|---|---|---|
| Asistente de Programación de Entrenamiento | Genera el borrador de programa (síntesis multi-módulo) | — (produce el `.xlsx` que consume Bckbs) | `agentes/programacion-entrenamiento/system-prompt.md` |
| Agente Importador de Programas | Lleva el `.xlsx` ya generado hasta la base de datos real (validar, importar, asignar, verificar) — no genera contenido ni decide programación | `ilzarpeatore/Bckbs` (Laravel, VPS `bestronger-vps`) | `agentes/importador-programas/system-prompt.md` |
| Asistente de Programación de Nutrición | Genera el plan nutricional/recetas individualizado, coordinado con el entrenamiento real del cliente — no diseña entrenamiento ni diagnostica | — (sin destino de producción todavía) | `agentes/programacion-nutricion/system-prompt.md` |

Son agentes de cadena, no independientes. El importador empieza exactamente donde termina el productor de entrenamiento (recibe un `.xlsx` ya escrito). El de nutrición es distinto: no es una cadena estrictamente secuencial de un solo sentido, sino un **sequential handoff** (Multi-Agent Collaboration, cap. 7) — lee el `perfil-cliente.schema.json` y el razonamiento del Productor de entrenamiento como entrada de contexto (qué días y qué tipo de sesión hay), sin regenerar ni cuestionar el entrenamiento en sí. `restricciones_dieteticas` vive en el esquema del agente de entrenamiento pero la gestiona por completo el de nutrición — es el primer campo genuinamente compartido entre dos agentes de este proyecto.

## Arquitectura del Asistente de Programación de Entrenamiento (M0)

No es un agente monolítico ni un router que encasilla al cliente en una categoría fija. Es un marco fijo que combina módulos de conocimiento relevantes al caso, en una cadena de 6 pasos:

0. **Selección de módulos** (Knowledge Retrieval / Agentic RAG; enrutamiento multi-etiqueta, cap. 2) — ¿qué módulos de `agentes/programacion-entrenamiento/modulos/` aplican a este cliente? Dentro de este paso, la elección de periodización (por evento vs. por calendario) es enrutamiento determinista por regla, no una decisión que el modelo deba razonar.
1. **Validación de entrada** (Exception Handling) — ¿faltan datos críticos? Si sí, se piden, no se asumen.
2. **Productor** (Planning + Prompt Chaining + Chain-of-Thought, cap. 17) — razona por escrito qué módulos están activos y cómo resuelve sus conflictos, consulta activamente el catálogo real de ejercicios (Tool Use, cap. 5) para resolver cada nombre, y solo entonces sintetiza el borrador según la jerarquía universal.
3. **Validador determinista** (Tool Use) — código, no el LLM, comprueba mecánicamente lo verificable (checklist mecánica de cada módulo).
4. **Crítico** (Reflection — patrón Productor-Crítico) — segunda pasada de LLM que revisa lo que requiere juicio.
5. **Revisión humana** (Human-in-the-Loop) — en M0, el 100% de los borradores.

### Jerarquía universal de conflictos

1. Seguridad y ausencia de dolor
2. Carga total combinada y recuperación real observada
3. No comprometer el estímulo prioritario declarado por el cliente
4. Adherencia sostenible
5. Volumen/intensidad "óptimos" según evidencia de cada módulo
6. Preferencias del cliente

### Memoria (Memory Management)

| Tipo | Contenido | Por qué importa |
|---|---|---|
| Semántica | `perfil_cliente`: objetivo(s), deporte/actividad, restricciones — varias etiquetas | Decide qué módulos se activan |
| Procedimental | La base de conocimiento modular completa + `reglas_programa` | Sostiene el conocimiento científico y las personalizaciones del cliente |
| Episódica | `historial_ciclos`: adherencia y resultado real de cada ciclo, más el `razonamiento` (Chain-of-Thought del Paso 2) de cada generación | El ciclo N+1 depende de cómo fue realmente el ciclo N, no de una suposición; el razonamiento guardado hace que la síntesis de módulos sea auditable después, no solo mientras se genera |

### Periodización: dos anclajes posibles

- **Por evento**: existe `fecha_evento` en el perfil (carrera, competición, examen físico...). Fases contadas hacia atrás desde la fecha (módulo `periodizacion-orientada-evento.md`).
- **Por calendario**: sin fecha objetivo. Macrociclo de 6 meses en bloques de 3, mes a mes, semana a semana (módulo `periodizacion-por-calendario.md`).

### Índice de módulos (estado actual)

| Módulo | Tipo | Se activa cuando |
|---|---|---|
| `contraindicaciones-medicas.md` | General — capa de seguridad | Siempre, primero — antes del Paso 0 |
| `calentamiento-activacion.md` | General | Siempre — cada sesión |
| `monitorizacion-fatiga-bienestar.md` | General | Siempre — cada sesión y cada día |
| `fuerza-maxima-potencia.md` | General | Objetivo prioriza fuerza relativa/potencia sobre tamaño muscular |
| `pliometria-rigidez-tendinosa.md` | General | Objetivo con salto, sprint, cambio de dirección |
| `progresion-carga.md` | General | Cualquier módulo de fuerza/pliometría activo |
| `seleccion-ejercicios-sustitucion-lesion.md` | General | Restricción física declarada, o limitación de material |
| `gestion-fatiga-deload.md` | General | Siempre — módulo de fondo |
| `periodizacion-orientada-evento.md` | General, condicional | Existe `fecha_evento` |
| `periodizacion-por-calendario.md` | General, condicional | No existe `fecha_evento` |
| `biomecanica-programacion-hipertrofia.md` | General | Objetivo incluye ganancia de tamaño muscular (se activa junto con cualquier módulo de hipertrofia) |
| `hipertrofia-recomposicion-corporal.md` | Específico | Objetivo de reducir grasa manteniendo/ganando masa muscular |
| `running-economia-carrera.md` | Específico | Cliente corre/compite en fondo o medio fondo |

## Backlog abierto

- Definir el esquema real de `perfil_cliente` con datos reales de clientes actuales.
- Módulos de población/deporte específicos: solo cuando exista un cliente real que lo necesite (fútbol, embarazo, patología concreta) — explícitamente pospuestos, no se escriben por completitud especulativa.
- Agente Importador de Programas: los cinco bloqueantes originales de `docs/AGENTE_IMPORTADOR.md` (Bckbs) están ya resueltos o parcialmente cubiertos — sin ítem abierto real pendiente de este lado por ahora.
- **(2026-09-15) Verificar contra BD real** todo lo mergeado hoy a `main` de Bckbs (`--json`, `programs:assign-client`, `POST program-import`, hotfix `fail()`→`reportFailure()`): solo se comprobó sin base de datos (lint, `route:list` de las 1024 rutas de la app, `artisan list`, 15 tests unitarios puros). Falta un ciclo completo `--dry-run` → import real → `assign-client` → `check-integrity` contra el catálogo real, como el que se hizo con Toni el 2026-09-14. Requiere acceso a datos del VPS `bestronger-vps` — ver `docs/AGENTE_IMPORTADOR.md` en Bckbs, sección 6.
- **(2026-09-15) Asistente de Programación de Nutrición — recién empezado**, solo capa de seguridad (`alergias-intolerancias.md`, sin deep-search clínico todavía) y el esqueleto del `system-prompt.md`. Pendiente, en orden probable: deep-search de módulos de contenido reales (macros por objetivo, timing alrededor del entrenamiento, recomposición nutricional — mismo proceso que se siguió con hipertrofia/recomposición en el agente de entrenamiento), definir el recetario real contra el que buscar (Paso 2, Tool Use), validador determinista (Paso 3), y un caso real de principio a fin como el de Toni antes de dar por maduro el diseño.
