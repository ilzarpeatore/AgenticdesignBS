# Módulo: Selección de ejercicios y sustitución por lesión

**Tipo:** General
**Se activa cuando:** existe una restricción física declarada por el cliente clasificada como `lesion_localizada` (ver `contraindicaciones-medicas.md` para las categorías `contraindicacion_relativa`/`contraindicacion_absoluta`, que se resuelven antes y de forma distinta), o una limitación de material/instalaciones. Condición casi universal — revisar en cada intake.
**Versión:** 0.3.0 · **Última actualización:** 2026-09-29
**Procedencia:** adaptado de los "principios generales" de la sección 3.4 del agente original de fuerza/pliometría para media maratón. v0.3.0: dos patrones nuevos a partir de un caso real (lesión de tríceps `cronica_controlada`, objetivo secundario de igualar fuerza entre lados) — reintroducción progresiva de intensidad por mesociclo para una zona con lesión antigua mientras el resto del programa entrena a intensidad plena, y ejercicio unilateral por anotación cuando el catálogo no tiene variante explícita. Ver `CHANGELOG.md` v0.24.0.

## Regla operativa

- Ante dolor, lesión o limitación: identifica (a) el patrón de movimiento, (b) el vector de resistencia y (c) el rango donde ocurre el dolor o la limitación. Sustituye manteniendo (a) y (b), evitando (c). **No elimines el patrón completo** salvo indicación explícita — mantener el patrón y cambiar la ejecución suele ser suficiente.
- Ante falta de material: mancuernas, bandas o el propio peso corporal permiten mantener casi cualquier patrón (empuje, tracción, bisagra de cadera, sentadilla, unilateral) cambiando solo la herramienta — no es motivo para vaciar el programa de patrones clave.
- Ante información vaga sobre una molestia ("me duele X a veces"): **bloqueante, no un matiz a resolver mientras se genera.** Exige antes de programar nada: qué gesto la provoca (`gesto_doloroso`), si es aguda/en recuperación/crónica controlada (`fase`), y si empeora con la actividad principal o con impacto (`empeora_con_actividad_o_impacto`) — campos obligatorios de `esquemas/perfil-cliente.schema.json` para toda `restriccion_salud` de categoría `lesion_localizada`. **Nunca decidas con datos insuficientes**, ni hacia el lado conservador (excluir de más) ni hacia el permisivo (adaptar algo que debía excluirse).

## Guardrail duro

Ante una lesión declarada con `fase: aguda`: excluye por completo el grupo muscular o patrón de movimiento afectado de toda la programación, y exige `autorizacion_profesional` antes de continuar. No lo "adaptas con cuidado" — lo excluyes y marcas el caso para revisión humana explicando qué excluiste y por qué. `en_recuperacion` y `cronica_controlada` sí admiten adaptación (mantener patrón, evitar el rango doloroso, regla operativa de arriba) — pero solo cuando `fase` está declarada explícitamente, nunca por defecto ante una descripción ambigua.

**Lección de un caso real:** una lesión de manguito rotador declarada sin `fase` ni `gesto_doloroso` forzó al Productor a decidir entre adaptar y excluir por juicio propio, en tensión directa con este guardrail — exactamente el escenario que estos campos obligatorios existen para evitar.

## Reintroducción progresiva de intensidad (lesión `cronica_controlada`/`en_recuperacion`, cliente que entrena fuerte)

Un caso distinto del guardrail duro de arriba: el cliente tiene una lesión antigua en el grupo muscular o patrón
de movimiento afectado ya **`cronica_controlada`** (no `aguda`, admite adaptación) y además pide intensidad alta
en general (`progresion-carga.md`: RIR bajo, cerca del fallo en los ejercicios que se tratan como seguros). No
es correcto ni excluir el patrón (eso es solo para `fase: aguda`) ni tratarlo con la misma intensidad agresiva
que el resto del cuerpo desde la semana 1 — la zona afectada necesita reintroducir la carga con un margen extra
de seguridad, aunque el cliente en conjunto pueda entrenar fuerte.

**Patrón operativo (general, sin números por defecto — los decide el Productor para ese cliente y esa lesión):**

1. Da a los ejercicios de ese grupo/patrón una progresión de RIR **más conservadora** que el resto del programa
   durante los primeros 1-2 mesociclos del macrociclo (RIR más alto en cada semana equivalente) — no un RIR fijo
   para siempre, una rampa que converge con la intensidad general en un mesociclo concreto, decidido según el
   historial y la fase de la lesión, no una regla universal de "2 meses".
2. Desde el mesociclo en el que converge, esos ejercicios pasan al mismo esquema de RIR que el resto del
   programa (`progresion-carga.md`) — la reintroducción es temporal, no una excepción permanente salvo que la
   lesión siga activa.
3. Si el objetivo del cliente incluye igualar fuerza/hipertrofia entre dos lados de una asimetría (ej. una
   lesión unilateral antigua), añade volumen extra de ese grupo trabajado en **unilateral** (ver la sección
   siguiente) — cada lado progresa a su propio RIR real, nunca al mismo peso absoluto que el lado no afectado.
4. Documéntalo explícitamente en la nota de esos ejercicios (qué semana/mesociclo se reintroduce la intensidad
   plena) y en el razonamiento del Paso 2 — no debe quedar implícito en los números, alguien que revise el
   programa después tiene que poder ver por qué esa zona progresa más despacio que el resto.

**Precedencia:** esto sigue siendo prioridad 1 de la jerarquía universal (seguridad) — si en cualquier momento
aparece dolor, chasquido o pérdida de fuerza notable durante la reintroducción, se detiene la progresión de esa
zona y se marca para revisión, independientemente del mesociclo en el que esté.

## Ejercicio unilateral cuando el catálogo no tiene variante

Para trabajo asimétrico (asimetría de fuerza declarada, o preferencia del cliente por más unilateral en una
zona concreta), busca primero en el catálogo una variante explícitamente unilateral ("a un brazo", "a una
pierna", "una mano"). Si no existe ninguna razonablemente cercana para ese ejercicio concreto:

- Usa el ejercicio bilateral estándar del catálogo (mancuerna o barra, nunca máquina guiada bilateral, que no
  admite ejecución unilateral real) y añade en `notas` la instrucción explícita: hacerlo un lado cada vez, sin
  ayuda del lado contrario ni del impulso del cuerpo, empezando siempre por el lado más débil/afectado.
- El lado afectado progresa a **su** RIR real esa semana, no al peso que levante el lado sano — nunca fuerces
  igualar la carga absoluta entre lados; el objetivo es igualar el esfuerzo relativo, la carga se equipara sola
  con el tiempo si el lado afectado progresa de verdad.
- No abuses de la conversión: si la mayoría de los ejercicios de una sesión pasan a unilateral por esta vía, la
  sesión se alarga mucho y pierde variedad de estímulo — combina con ejercicios que sí tengan variante unilateral
  real en el catálogo y con trabajo bilateral, no conviertas todo el roster.
- Documenta en el razonamiento del Paso 2 qué ejercicios se convirtieron por esta vía (sin variante en catálogo)
  frente a los que ya eran unilaterales de catálogo — es información relevante si más adelante aparece una
  variante nueva en el catálogo que sustituya a la anotación manual.

## Conflictos conocidos con otros módulos

- **Con cualquier módulo de contenido:** esta regla tiene prioridad 1 de la jerarquía universal (seguridad) sobre lo que pida cualquier otro módulo — incluida la progresión de carga o las prioridades de ejercicio de un módulo específico como `running-economia-carrera.md`.
- **Con `contraindicaciones-medicas.md`:** ese módulo se consulta primero y tiene precedencia. Si una restricción de salud es una contraindicación (relativa o absoluta), no se gestiona aquí como sustitución de ejercicio — se gestiona allí como bloqueo de la programación hasta autorización, o derivación directa.
