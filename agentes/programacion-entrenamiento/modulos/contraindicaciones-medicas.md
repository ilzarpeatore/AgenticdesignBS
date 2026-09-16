# Módulo: Contraindicaciones médicas y derivación profesional

**Tipo:** General — capa de seguridad transversal, no un módulo de contenido de entrenamiento
**Se activa cuando:** siempre. Se consulta **antes que cualquier otro módulo**, como parte obligatoria del Paso 1 (validación de entrada). Si detecta una contraindicación absoluta, el pipeline se detiene ahí: no se selecciona ningún módulo de contenido (Paso 0), no se genera ningún borrador.
**Versión:** 0.3.0 · **Última actualización:** 2026-09-16
**Procedencia:** ACSM (contraindicaciones a la prueba de esfuerzo y al ejercicio), PAR-Q+ (cribado estándar internacional), ACOG (contraindicaciones al ejercicio en el embarazo), guías de RED-S/trastornos de conducta alimentaria. v0.2.0: el cribado de la sección 1 estaba escrito en teoría desde v0.1.0 sin contrastar contra el onboarding real de Bckbs — al hacerlo se encontró que las preguntas 6-8 (embarazo, RED-S, trastorno alimentario) nunca se preguntaban en producción; se añadieron a `par_q_answers` (Bckbs) esa misma fecha. v0.3.0 (mismo día): decisión de producto del usuario — embarazo/RED-S solo se preguntan a perfil `mujer`, no a hombre/otro; ver `esquemas/perfil-cliente.schema.json` (nuevo campo `genero`) y la tabla de mapeo actualizada.

> Este módulo es más estricto que `seleccion-ejercicios-sustitucion-lesion.md`: aquel adapta el ejercicio ante una limitación física manejable (sustituir manteniendo patrón y vector). Este módulo cubre condiciones donde **no se programa nada** hasta que exista autorización médica explícita, o donde se deriva directamente sin programar.

## 1. Cribado obligatorio (Paso 1, estilo PAR-Q+)

Antes de generar cualquier borrador para un cliente nuevo, o ante cualquier cambio relevante de salud de uno existente, pregunta explícitamente:

1. ¿Sientes dolor en el pecho en reposo o durante actividad física?
2. ¿Has perdido el conocimiento o el equilibrio de forma inexplicada en el último año?
3. ¿Tienes un diagnóstico cardíaco, pulmonar o metabólico conocido (incluida diabetes)?
4. ¿Tomas medicación regular? ¿Cuál?
5. ¿Has tenido una cirugía, fractura o lesión importante en los últimos 3 meses?
6. ¿Estás embarazada o existe la posibilidad?
7. ¿Has perdido la menstruación de forma inesperada, o has tenido una fractura por estrés? (cribado de baja disponibilidad energética / RED-S)
8. ¿Tienes o has tenido un trastorno de la conducta alimentaria?

Cualquier "sí" activa la contraindicación correspondiente de las secciones 2 o 3 — no se decide con una respuesta vaga; si la respuesta no es clara, se pide especificidad antes de continuar (mismo principio que `seleccion-ejercicios-sustitucion-lesion.md`).

### Mapeo con el onboarding real (`par_q_answers` en Bckbs)

| Pregunta de arriba | Campo real | Nota |
|---|---|---|
| 1. Dolor en el pecho | `parq_chest_pain_activity` + `parq_chest_pain_rest_last_month` | Dos campos reales para una pregunta del módulo — cualquiera de los dos en `true` activa la contraindicación. |
| 2. Pérdida de conocimiento o equilibrio | `parq_dizziness_balance` | El campo real es más estrecho (mareo/equilibrio) — no pregunta explícitamente por pérdida de conocimiento. Trátalo como proxy razonable, no como equivalente exacto. |
| 3. Diagnóstico cardíaco/pulmonar/metabólico | `parq_heart_condition` + `parq_medical_history` (texto libre) | No hay un campo booleano de "diagnóstico pulmonar/metabólico" — puede estar mencionado en el texto libre. Léelo, no lo ignores, pero si sugiere algo relevante, confirma con el cliente en vez de decidir solo con el texto libre (ver `esquemas/perfil-cliente.schema.json`). |
| 4. Medicación regular | `parq_bp_or_heart_medication` + `parq_medical_history` | El campo booleano solo cubre medicación de tensión/corazón — otra medicación relevante, si existe, vive en el texto libre. |
| 5. Cirugía/fractura/lesión reciente | `parq_bone_joint_problem` | El campo real no acota a "últimos 3 meses" — pregunta si hace falta precisar la fecha. |
| 6. Embarazo o posibilidad | `parq_pregnant_or_possible` | Añadido a Bckbs el 2026-09-16. **Solo se pregunta a perfil `mujer`** (`perfil_cliente.genero`) — en `hombre`/`otro` es `null` porque no aplica, no lo trates como pendiente ni lo preguntes. En una clienta mujer que completó el onboarding antes del 2026-09-16, `null` sí es "sin responder" — ahí sí pregúntalo. |
| 7. Alteración menstrual / fractura por estrés (RED-S) | `parq_menstrual_change_or_stress_fracture` | Mismo criterio de género y de fecha que la anterior. |
| 8. Trastorno de conducta alimentaria | `parq_eating_disorder_history` | Aplica a **cualquier género**, siempre obligatoria. `null` solo puede significar "onboarding anterior al 2026-09-16, sin responder" — en ese caso sí pregúntalo. |

Las preguntas 6-8 ya activan `flagged_for_review` automáticamente en Bckbs si la respuesta es `true` (mismo mecanismo que las de riesgo cardíaco) — pero eso marca al cliente para revisión de un coach en el panel, no sustituye este cribado ni el bloqueo de las secciones 2-3 de este módulo. Ocultar las preguntas 6-7 en el formulario para perfiles no-mujer es responsabilidad del frontend de la app — este módulo y Bckbs ya no las exigen ni las guardan para esos géneros, pero la app decide qué muestra.

## 2. Contraindicaciones absolutas — no se programa, se deriva

Ante cualquiera de estas señales, el agente no genera ningún borrador: marca `requiere_revision: true`, riesgo **alto**, y deriva explícitamente a evaluación médica antes de cualquier programación.

- **Cardiovasculares:** infarto agudo de miocardio en los últimos 2 días, angina inestable en curso, arritmia cardíaca no controlada con compromiso hemodinámico, endocarditis activa, estenosis aórtica severa sintomática, insuficiencia cardíaca descompensada, embolia pulmonar o trombosis venosa profunda aguda, miocarditis o pericarditis aguda, disección aórtica aguda o sospechada.
- **Aneurisma intracraneal o aórtico** no tratado — ninguna carga ni maniobra de Valsalva hasta valoración médica.
- **Retinopatía proliferativa activa** — el esfuerzo de alta intensidad y la maniobra de Valsalva pueden provocar hemorragia vítrea o desprendimiento de retina.
- **Hernia abdominal o inguinal sintomática o de gran tamaño**, no reparada.
- **Fractura no consolidada** o cirugía reciente sin alta médica.
- **Embarazo con:** rotura de membranas, incompetencia cervical, sangrado persistente en 2º/3er trimestre, placenta previa después de la semana 26, riesgo de parto prematuro, preeclampsia, cardiopatía hemodinámicamente significativa, enfermedad pulmonar restrictiva, gestación múltiple con riesgo de parto prematuro.
- **Trastorno de la conducta alimentaria activo, o señales de baja disponibilidad energética / RED-S** (amenorrea de causa no aclarada, fractura por estrés, pérdida de peso rápida no intencionada): contraindicación específica para prescribir **cualquier** déficit calórico o activar `hipertrofia-recomposicion-corporal.md`. El primer paso terapéutico ante RED-S es reducir o detener el ejercicio, no programarlo — deriva a evaluación médica/nutricional clínica especializada, nunca lo gestiones como una simple restricción dietética.

## 3. Contraindicaciones relativas — requieren autorización médica antes de programar

Ante estas señales, el agente no programa hasta que `perfil_cliente.restricciones_salud[].autorizacion_profesional` sea explícitamente `true`. Con autorización, programa con las adaptaciones indicadas y mantiene `confianza: "media"`.

- **Hipertensión no controlada** → sin autorización, no se programa fuerza de alta intensidad. Con autorización, priorizar programas moderados y supervisados; evitar picos de intensidad máxima.
- **Diabetes no controlada** → riesgo de hipoglucemia, incluida hipoglucemia tardía hasta 12-14h post-ejercicio. Si el cliente usa insulina, el trabajo de fuerza/alta intensidad es preferible por la tarde/noche (mayor estabilidad glucémica) frente a la mañana. Si hay retinopatía diabética asociada, aplica además la contraindicación absoluta de retinopatía (sección 2).
- **Osteoporosis u osteopenia significativa** → evita flexión de columna cargada (nada de crunch/abdominales con carga, remo con flexión lumbar marcada), evita la combinación de flexión + rotación con carga (el gesto que más se asocia a fractura vertebral), evita alto impacto (saltos, carrera) y evita levantamientos por encima de la cabeza con carga alta. Prioriza ejercicios de extensión de columna (seguros y protectores).
- **Hernia no complicada o antecedente de reparación** → evita maniobra de Valsalva marcada y presión intraabdominal alta hasta autorización explícita.
- **Uso de anticoagulantes** → mayor riesgo de hematoma/sangrado con alto impacto o riesgo de caída/contacto — prioriza ejercicios estables y controla el entorno.
- **Cardiopatía conocida estable o antecedente de evento cardiovascular** → requiere autorización médica; con ella, evita maniobra de Valsalva marcada y progresa de forma más conservadora que con `progresion-carga.md` por defecto.
- **Embarazo sin contraindicación absoluta** → adaptaciones básicas hasta que exista un módulo específico de entrenamiento en embarazo: evitar decúbito supino prolongado desde el 2º trimestre, evitar maniobra de Valsalva marcada, ajustar intensidad por percepción de esfuerzo en vez de por porcentajes fijos de 1RM.

## 4. Protocolo de actuación

```
Cribado (sección 1) → ¿alguna respuesta activa la sección 2?
  SÍ → no generar. requiere_revision=true, riesgo="alto". Derivar a evaluación
       médica. No se selecciona ningún módulo de contenido (Paso 0 no se ejecuta).
  NO → ¿alguna respuesta activa la sección 3?
        SÍ → ¿autorizacion_profesional == true?
              SÍ → generar con las adaptaciones de la sección 3. confianza="media".
              NO → no generar. requiere_revision=true. Pedir autorización médica
                   explícita antes de continuar.
        NO → proceder con normalidad al Paso 0 (selección de módulos).
```

## Conflictos conocidos con otros módulos

- **Con `seleccion-ejercicios-sustitucion-lesion.md`:** ese módulo adapta (sustituye un ejercicio); este módulo, cuando aplica, impide programar del todo hasta autorización o deriva sin programar. Este módulo tiene precedencia — se consulta antes.
- **Con `hipertrofia-recomposicion-corporal.md`:** el cribado de RED-S/trastorno alimentario de este módulo es previo y superior a cualquier lógica de déficit calórico de ese módulo — si se activa, `hipertrofia-recomposicion-corporal.md` no se activa en absoluto para ese cliente hasta resolución médica.
- **Con cualquier módulo de contenido:** todas las reglas de este módulo tienen la prioridad más alta de la jerarquía universal (`system-prompt.md`, sección 5, punto 1 — seguridad) y se comprueban antes de que cualquier otro módulo entre en juego.

## Referencias

- American College of Sports Medicine (ACSM). *Guidelines for Exercise Testing and Prescription* — contraindicaciones absolutas y relativas a la prueba de esfuerzo y al ejercicio.
- Physical Activity Readiness Questionnaire for Everyone (PAR-Q+) — estándar internacional de cribado previo a la participación.
- American College of Obstetricians and Gynecologists (ACOG) — contraindicaciones absolutas y relativas al ejercicio durante el embarazo.
- Mountjoy, M., et al. — Relative Energy Deficiency in Sport (RED-S): definición, cribado e indicaciones de manejo.
- Retina Today (2021) — Valsalva retinopathy y ejercicio de alta intensidad.
