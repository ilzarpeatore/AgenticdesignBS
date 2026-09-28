# Módulo: Progresión de carga

**Tipo:** General
**Se activa cuando:** cualquier módulo de fuerza o pliometría está activo.
**Versión:** 0.3.0 · **Última actualización:** 2026-09-28
**Procedencia (v0.3.0):** el usuario reportó que las programaciones reales entregadas hasta ahora mantienen el mismo número de series y repeticiones durante los 5-6 meses de un macrociclo, sin ninguna progresión — un caso real de exactamente el fallo que este módulo lleva desde v0.1.0 diciendo cómo evitar, pero sin ninguna comprobación que lo confirmara. Investigado antes de decidir: el conocimiento ya era correcto y detallado (esquema de especificación de abajo), el hueco real estaba en que nada verificaba que se aplicara. Dos cambios: **(1)** nuevo chequeo mecánico en `../validador/validar_programa.py` (ver `../validador/CHANGELOG.md`) que detecta cuando un ejercicio no progresa en NINGÚN eje (series, reps, RIR/RPE, carga) entre semanas de acumulación — mira la tupla completa, no un eje aislado, porque cuál de ellos progresa es justo la decisión que ya describía este módulo. **(2)** nueva "Checklist de verificación" al final de este documento, siguiendo el patrón que el system-prompt del agente ya prometía para cada módulo pero que este (y `biomecanica-programacion-hipertrofia.md`) no tenían todavía por escrito.
**Procedencia:** v0.1.0 adaptado de la sección 3.5 del agente original de fuerza/pliometría para media maratón. v0.2.0: formaliza como **esquema de especificación** (la forma de detallar un mesociclo -- qué dimensiones hay que decidir y cómo se documentan) la estructura que hasta ahora solo existía como un Excel individual de un cliente real de Be Stronger (citado en `CHANGELOG.md` v0.16.0). v0.2.1 (misma fecha, corrección del usuario tras revisar v0.2.0): **se generaliza la tabla/estructura de especificación, NUNCA los valores numéricos concretos de progresión/regresión/descarga de ese cliente** -- esos siguen siendo individualizados caso a caso, exactamente igual que la duración de mesociclo ya es individualizada en `periodizacion-por-calendario.md` v0.3.0 ("nunca una cifra fija de plantilla"). Los números de las tablas de abajo (RPE por semana, %, qué ejercicios son "seguros") son el **ejemplo real** que motivó este formato -- una ilustración de cómo se ve una progresión bien especificada, no un valor por defecto que se copie para otro cliente. El contenido concreto de ejercicios excluidos de ese cliente original (`Pull-through con polea`, `Curl femoral con tobillera`) tampoco se traslada -- es específico de ese cliente.

## Regla operativa (general)

- La progresión puede darse en carga, en velocidad de ejecución (más explosiva a igual carga), o en la exigencia de la variante (de bilateral a unilateral, de submáximo a drop jump) — no siempre hay que subir peso.
- Incrementos sostenibles y pequeños (ej. +2.5-5% de carga) antes que saltos grandes, y **solo cuando la técnica se mantiene limpia** — especialmente crítico en gestos pliométricos, donde una técnica de aterrizaje deficiente bajo fatiga es la vía más directa a la lesión.
- **Si hay estancamiento** (2+ sesiones sin progreso): primero descarta que la carga total combinada (todas las actividades y módulos activos) esté generando fatiga acumulada, antes de asumir que el estímulo de fuerza es insuficiente.

## Esquema de especificación detallada de mesociclo

Esto es lo que hay que **decidir y documentar explícitamente** al rellenar la hoja de detalle semana a semana de `formato-salida/formato-excel-detallado.md`, cuando el módulo de objetivo activo es `hipertrofia-recomposicion-corporal.md` o `biomecanica-programacion-hipertrofia.md`. Para otros objetivos (fuerza máxima/potencia pura, pliometría), sigue rigiendo solo la regla general de arriba.

**Importante — qué se reutiliza y qué no:** las categorías/dimensiones de abajo (clasificación ancla/variable/nuevo, patrones de reps A/B/C, que exista una progresión de RPE semana a semana, un sistema de RIR según nº de series/seguridad del ejercicio, y una regla de ajuste de carga tras cada semana) son la **forma** que se reutiliza con cualquier cliente -- es lo que hace auditable y consistente la lectura de cualquier mesociclo. Los **valores concretos** que se ven en las tablas de ejemplo (7-7.5 de RPE en S1, +5% de incremento, -30% de deload, qué ejercicios en concreto se tratan como "seguros") pertenecen al caso real que motivó este documento -- el Productor decide esos números para cada cliente y cada mesociclo según su nivel, su objetivo, su técnica y la señal de fatiga real (`monitorizacion-fatiga-bienestar.md`, `gestion-fatiga-deload.md`), nunca los copia sin más.

### Clasificación de ejercicios: ancla / variable / nuevo

Cada ejercicio de una sesión se clasifica, no solo se elige:

- **Ancla (MAYÚSCULAS en la hoja):** ejercicio compuesto principal de ese patrón de movimiento, fijo durante todo el macrociclo (todos los mesociclos). Progresa en carga de mesociclo a mesociclo, no solo semana a semana dentro de uno. Normalmente 1-2 por sesión (el/los movimiento/s que definen esa sesión).
- **Variable (minúsculas):** mismo patrón biomecánico que un ancla o un objetivo de aislamiento concreto, pero rota ~50% de un mesociclo al siguiente (cambia de material/ángulo/variante) para gestionar monotonía e interferencia sin perder el estímulo. La mitad del roster de accesorios rota, la otra mitad se mantiene, para no perder continuidad de progresión en ninguna semana.
- **Nuevo (🆕, primera vez que aparece):** sin carga de referencia previa en ningún mesociclo anterior. Su semana 1 (S1) es siempre de exploración técnica pura (ver más abajo) — nunca se compara su carga contra mesociclos anteriores porque no los hay.

### Patrones de reps por semana (dentro de un mesociclo)

La forma general -- tres patrones posibles, elegidos por rol del ejercicio, no al azar. El Productor decide cuál usar y con qué rangos exactos de reps para cada ejercicio de cada cliente:

- **Patrón A (descendente):** reps bajan, carga sube semana a semana dentro del mesociclo. Típico del ancla principal de la sesión.
- **Patrón B (ascendente):** reps suben, acumula volumen semana a semana. Típico de un segundo ancla o accesorios orientados a elongación/hipertrofia.
- **Patrón C (fijo):** rango de reps igual todas las semanas de acumulación, solo sube la carga. Típico de gemelos, core, ejercicios de estabilidad.

*Ejemplo real (caso que motivó este formato, NO un valor por defecto):* Patrón A `12-15 → 10-12 → 8-10 → 6-8 → 5-6`, deload `12-15`. Patrón B `6-8 → 8-10 → 10-12 → 12-15 → 12-15`, deload `10-12`. Patrón C `12-15` fijo, deload `15`.

### Que exista una progresión de RPE/intensidad semana a semana (S1..Sn, la última siempre deload)

La forma general: cada mesociclo debe tener una progresión explícita de intensidad/RPE objetivo semana a semana, más una semana final de deload con intensidad y RIR claramente reducidos. **Cuántas semanas, qué RPE exacto en cada una, y cuánto baja el deload es una decisión del Productor para ese cliente y ese mesociclo concreto** -- depende del nivel, la fase del macrociclo, la fatiga real acumulada (`monitorizacion-fatiga-bienestar.md`) y la cadencia de deload que ya decide `gestion-fatiga-deload.md` (cada 3-5 semanas de acumulación) y `hipertrofia-recomposicion-corporal.md` sección 5 (4-6 semanas de mesociclo según nivel). No hay un número de RPE ni un % de deload universal correcto para todos los clientes.

*Ejemplo real (caso que motivó este formato, NO un valor por defecto):*

| Semana | RPE objetivo | Foco |
|---|---|---|
| S1 | 7-7.5 | Establece la carga base. Exploración técnica y de carga. Volumen mínimo del mesociclo. |
| S2 | 7.5-8 | +5% sobre S1. Confirma técnica. |
| S3 | 8-8.5 | +5% sobre S2. Aumenta la densidad — la técnica debe mantenerse bajo mayor fatiga. |
| S4 | 8.5-9 | +5% sobre S3. Pico de volumen del mesociclo. Concentración máxima por serie. |
| S5 | 9 | Mantén carga de la semana anterior. Intensificación — última serie al límite real (fallo o RIR 1 en ejercicios seguros). |
| S6 (deload) | 5-6 | -30% sobre la carga de S1. RIR 3 en TODAS las series, sin excepción por tipo de ejercicio. Recuperación activa. |

### Sistema de RIR dentro de cada semana, según nº de series y si el ejercicio se trata como "seguro" para ESE cliente

Forma general: dentro de una semana, el RIR baja serie a serie hasta un tope -- y ese tope depende de si el ejercicio se trata como uno donde SÍ tiene sentido llegar al fallo muscular real, o uno donde el coste técnico/articular de perder la forma bajo fallo es demasiado alto (normalmente compuestos pesados de barra/máquina guiada) y se limita a RIR 1 como máximo, nunca fallo real. **Qué ejercicios concretos son "seguros" para un cliente dado depende de su técnica, su historial de lesiones y el material real disponible -- no es una lista fija que se aplica igual a todos.** Un cliente con técnica autoevaluada baja puede necesitar tratar como "no seguro" (nunca cerca del fallo) incluso ejercicios que para otro cliente sí lo serían.

*Ejemplo real (caso que motivó este formato, NO una lista por defecto):*

- Ejercicio NO seguro, 4 series: RIR 3 → RIR 2 → RIR 1 → FALLO.
- Ejercicio NO seguro, 3 series: RIR 3 → RIR 2-1 → FALLO.
- Ejercicio SEGURO, 4 series: RIR 3 → RIR 2 → RIR 1 → RIR 1 (nunca fallo real).
- Ese cliente concreto trataba como "seguros" sus compuestos pesados guiados (sentadilla, peso muerto, press con barra/máquina guiada, remo con barra, dominada, hip thrust, prensa, máquina Smith/pendulum/belt squat) y como "no seguros" el aislamiento con mancuerna/polea/máquina de un solo grupo.
- Semana de deload: RIR 3 en TODAS las series, de TODOS los ejercicios, sin excepción.

### Regla de ajuste de carga tras cada semana (relativa, no cifras absolutas)

Esta parte sí es razonablemente general como heurística de autorregulación (patrón común de progresión doble/RPE), pero el **% exacto de subida y de bajada en el deload lo decide el Productor para cada cliente**, no es un 5%/30% fijo:

- **Completa todos los sets al RPE objetivo de esa semana** → sube la carga la siguiente semana (el caso real que motivó este formato usaba +5%; otro cliente puede necesitar un incremento distinto).
- **No completa todos los sets programados** → mantén la misma carga la siguiente semana. No subas hasta completar el volumen programado.
- **Fallo técnico** (pierde la forma antes de completar el rango) → baja la carga. La técnica es prioritaria sobre el peso, siempre.
- **Ejercicio nuevo (🆕) en su S1, o cliente sin ninguna carga de referencia conocida** (`referencias_carga` vacío en el perfil): S1 es siempre de exploración técnica pura -- nunca se compara contra mesociclos anteriores porque no existen. Mismo criterio que el caso límite ya documentado en `system-prompt.md` ("no sabe su 1RM" → semana de calibración).

## Conflictos conocidos con otros módulos

- **Con `gestion-fatiga-deload.md`:** un estancamiento nunca se resuelve subiendo volumen o intensidad sin descartar fatiga acumulada primero (jerarquía universal, punto 2 del system-prompt).
- **Con `hipertrofia-recomposicion-corporal.md`:** en déficit calórico, la progresión de carga es más lenta e inconsistente de lo que este módulo asumiría por defecto — mantener la carga en ese contexto no es estancamiento real.
- **Con `biomecanica-programacion-hipertrofia.md`:** este módulo cubre la progresión de **carga** (peso); ese módulo cubre además la progresión de **volumen** (número de series, sección 9). No subir ambas variables de forma agresiva la misma semana.

## Checklist de verificación

- **Verificable mecánicamente** (`validador/validar_programa.py`, sin llamada al modelo): ¿algún ejercicio mantiene series, reps, RIR/RPE y carga idénticos en todas las semanas de acumulación del mesociclo? Un único ejercicio así es advertencia (puede ser deliberado); si son la mitad o más del programa, es error bloqueante — no se avanza al Crítico ni al coach con ese resultado.
- **Requiere juicio del Crítico** (no lo cubre el validador, porque exige valorar si el ritmo es "razonable", no solo si "algo" cambia):
  - ¿La progresión elegida por ejercicio (carga, patrón de reps A/B/C, RIR/RPE, o series según `biomecanica-programacion-hipertrofia.md` sección 9) es coherente con el nivel del cliente y la fase del mesociclo, o es tan tímida que equivale en la práctica a no progresar?
  - ¿El mesociclo cierra con una semana de deload reconocible (intensidad y/o volumen claramente reducidos), no solo "una semana más" con el mismo patrón?
  - ¿Hay algún ejercicio ancla (fijo durante todo el macrociclo) cuya progresión de carga entre mesociclos consecutivos también sea plana, no solo dentro de uno? El validador solo mira un `.xlsx` (un mesociclo) a la vez — esta comparación cruzada solo la puede hacer el Crítico o el coach releyendo la memoria episódica del cliente.
