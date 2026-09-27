# Changelog — Agente de Soporte / Customer Success

## v0.8.0 — 2026-09-27

El usuario quiere montar en el panel admin un check-in de satisfacción con el programa cada 15 días — qué ejercicio cuesta más, qué sesión se complica, cómo va la nutrición.

- **Descubierto que Bckbs ya tiene un sistema completo de Forms/Check-ins** (`Form`/`FormQuestion`/`FormAssignment`/`FormSubmission`/`FormAnswer`), no usado hasta ahora por ningún agente. A diferencia del check-in semanal (WhatsApp, sin sistema de registro propio), este lo rellena el cliente dentro de la app y Bckbs ya lo persiste correctamente — **no se duplica en `bstronger-memoria-clientes`**.
- **Nueva sección 3quater + `modulos/checkin-satisfaccion.md`:** el agente vigila `GET admin-form-submission-list` (nueva herramienta, ya existía) una vez al día, aplica el mismo cribado de seguridad de siempre si una respuesta menciona dolor (una encuesta no baja el nivel de exigencia), reconoce con calidez cuando aplica (patrón 3.8), y escala si la satisfacción es baja o se repite una queja. Los Productores de entrenamiento/nutrición deben leer esta misma fuente directamente en su "Memoria del cliente" — se documenta en sus propios `system-prompt.md`, no aquí.
- **Gap real encontrado y arreglado en Bckbs:** `Form.recurrence` solo aceptaba `daily/weekly/monthly` pese a que el comentario de la migración ya mencionaba `biweekly` como opción nunca implementada. Arreglado y pusheado (commit `435d180`, 4 tests nuevos contra MySQL real local, suite completa de Feature verde) — pendiente de desplegar al VPS antes de que el usuario pueda crear el formulario quincenal desde el panel (`docs/TAREAS_PENDIENTES.md`, ítem 2.19).
- `system-prompt.md` sube a v0.8.0.

## v0.7.0 — 2026-09-27

El usuario pidió investigar cómo operan los entrenadores online que más facturan, para que este agente lo replique. Investigación de mercado (fuentes en `docs/TAREAS_PENDIENTES.md`): la práctica con más impacto medido en retención dentro del coaching de alto contacto es un check-in semanal fijo y corto, siempre con las mismas preguntas, en un día que nunca cambia — el churn en coaching online es sobre todo un problema de comunicación inconsistente, no de calidad de programación.

- **Nueva sección 3ter + `modulos/checkin-semanal.md`:** check-in semanal, domingo por la mañana (decisión del usuario), a todos los clientes activos. Sigue el principio de "no preguntar lo que ya sabes por datos reales" — abre citando `GET client-session-feedback`/`GET client-meal-calendar` antes de preguntar, y solo pregunta lo subjetivo (`bienestar_diario`, escala 1-7 ya definida en `log-registro.schema.json`, más una nota libre de nutrición).
- **Primera vez que este agente escribe en la memoria del cliente, no solo lee:** `esquemas/log-registro.schema.json` y `esquemas/log-nutricion.schema.json` (agentes de entrenamiento y nutrición, mismo día) ganan `origen: "checkin_soporte"` — una entrada ligera que no simula un razonamiento de generación que nunca ocurrió. Tabla de herramientas de este agente actualizada para reflejar que este es el único campo/caso donde escribe, no solo lee.
- **Banda de alerta:** si fatiga/dolor/estrés vienen altos (especialmente 2 semanas seguidas), el check-in escala igual que cualquier señal de salud — nunca sugiere él mismo un ajuste de entrenamiento, eso sigue siendo del Productor de entrenamiento.
- **Cliente que no responde al check-in** es en sí misma una señal temprana de desenganche (documentada en la investigación) — se registra, no se convierte en tarea automática salvo que coincida con otra señal de escalación.
- `system-prompt.md` sube a v0.7.0.

## v0.6.0 — 2026-09-27

El usuario pidió calibrar el agente para ofrecer atención de calidad acorde a un servicio de ~300€/mes — coaching 1:1 premium, no una app masiva de bajo coste.

- **Contexto de nivel de servicio, sección 1:** nuevo párrafo explícito que fija el estándar (trato personal, nunca sensación de FAQ/bot) sin ampliar ningún límite existente — más exigencia dentro de lo ya permitido, no más alcance.
- **Nueva sección 4bis — SLA de seguimiento de tareas escaladas:** hasta ahora, escalar creaba una tarea y ahí terminaba la responsabilidad del agente. En un servicio premium, un "te lo comento con tu coach" seguido de silencio real durante horas es peor que no responder. Nueva herramienta confirmada en el código real de Bckbs: `GET task-list` (`TaskController::getList`, filtra por `client_id`+`status`) — si una tarea sigue `pending` tras un umbral (propuesta: 4h en horario laboral), el agente envía un mensaje de refuerzo al cliente (sin inventar plazos ni soluciones), pasando igual por la validación del Paso 6. Nunca sube la prioridad ni reasigna la tarea por su cuenta — el seguimiento es comunicativo, no presión sobre el trabajo del coach.
- **Nuevo patrón 3.8 en `modulos/tono-y-conocimiento-deportivo.md` (sube a v0.3.0): reconocer progreso real sin que lo pidan.** Un servicio premium no solo reacciona a problemas — nota cuando algo va bien. `GET client-session-feedback` gana un segundo uso (antes solo para detectar inactividad, ahora también para progreso: `volume_kg`, `difficulty_rating`, sesiones completadas), junto con `checkpoints-fisicos.json`/`observaciones_coach`. Guardrail explícito: nunca inventar una comparación de mejora sin tener ambos datos reales, y nunca convertirlo en diagnóstico o excusa para sugerir cambios de carga (eso sigue siendo escalación).
- `system-prompt.md` sube a v0.6.0.

## v0.5.0 — 2026-09-27

El usuario preguntó si el agente podía construir su propio banco de respuestas leyendo el historial de conversación de cada cliente, en vez de que el usuario tuviera que aportar ejemplos.

- **Aclaración necesaria antes de diseñar nada:** el historial de conversaciones que el coach ya ha tenido vive solo en su WhatsApp personal — ningún sistema de este proyecto lo captura hoy, así que el agente no puede "leerlo" aunque quisiera. El usuario aportará más adelante exportaciones de chat de WhatsApp (sin multimedia) por cliente para contrastar el módulo de tono contra casos reales, cuando le venga bien.
- **Nueva sección 8 en `system-prompt.md` (sube a v0.5.0): mejora continua del banco de respuestas, explícitamente supervisada, no automática.** A partir del despliegue, cada interacción sí queda en el log real (`esquemas/log-interaccion.schema.json`) — se formaliza una revisión periódica (semanal/quincenal al principio) de ese log para: detectar preguntas reales frecuentes sin patrón que las cubra (solo se añade patrón nuevo si se repite, no por un caso aislado); afinar las denylists de `modulos/validacion-antes-de-enviar.md` con los falsos positivos/negativos reales que vaya bloqueando; y revisar los casos marcados `confianza: "baja"`.
- **Por qué revisión humana y no autoajuste:** dejar que el agente reescriba su propio banco de respuestas sin supervisión rompería el mismo principio de control que ya aplica al resto del sistema — la revisión la hace el usuario hasta que exista el Control de Soporte (nivel 2 del organigrama), que entonces absorbe esta función.

## v0.4.0 — 2026-09-27

El usuario pidió seguir mejorando el diseño tras la primera revisión. Se identificaron 4 huecos reales; se resuelven los 3 que no dependen de material que solo el usuario tiene (el cuarto, contrastar el módulo de tono contra conversaciones reales, queda pendiente de que el usuario aporte ejemplos).

- **Nuevo `modulos/validacion-antes-de-enviar.md`:** este agente es el único de los 4 sin revisión humana antes de que su output llegue a producción (los otros 3 tienen validador determinista + humano al 100%). Nueva red de seguridad mecánica (nodo de código en n8n, no el LLM juzgándose a sí mismo): denylists de precio/condiciones comerciales, de prescripción de cambio de programación/nutrición, de diagnóstico médico; comprobación de coherencia con la clasificación del Paso 3 (cribado); y verificación de que cualquier dato factual citado (día, ejercicio, receta) tiene detrás una llamada real registrada a `client-calendar-data`/`client-meal-calendar` en el mismo turno, para atajar alucinaciones. Si algo no pasa, no se envía — se envía una respuesta neutra y se crea tarea con el mensaje bloqueado visible para el coach.
- **Memoria de conversación (nuevo Paso 1bis del flujo):** hasta ahora cada mensaje entrante era una ejecución aislada, sin contexto de mensajes anteriores del mismo cliente — un "¿y si en vez de eso?" no tenía forma de interpretarse. Ahora se leen las últimas interacciones (24h o últimas 10, lo que sea menos) del log antes de generar.
- **Mecanismo real de seguimiento proactivo (nueva sección 3bis):** antes el `system-prompt.md` decía "detecta clientes inactivos" sin definir cómo. Se investigó el código real de Bckbs y se encontró `GET client-session-feedback` (`ClientProfileCalendarController::getSessionFeedback`) — sesiones **realmente completadas** (`WorkoutSessionReview.completed_at`), no solo asignadas, que es la señal correcta (ya la usa el propio panel admin para mostrar feedback post-entreno). Umbral definido en función de `disponibilidad.dias_por_semana` real de cada cliente (2× su intervalo esperado entre sesiones), no un número arbitrario igual para todos. Nuevo patrón 3.7 en `modulos/tono-y-conocimiento-deportivo.md` (sube a v0.2.0): un mensaje de reenganche genérico funciona peor que uno que referencia algo real de esa persona; nunca en tono de reproche; no crea tarea automáticamente, solo si la respuesta del cliente trae señales de escalación.
- `system-prompt.md` sube a v0.4.0: nueva tabla de herramientas, flujo renumerado (7 pasos + sección 3bis).

## v0.3.0 — 2026-09-27

El usuario pidió que el agente pudiera leer entrenamiento y nutrición reales del cliente, para responder de forma aplicada cuando una duda combine ambos (ej. qué comer después de la sesión de hoy).

- **Nueva herramienta confirmada en el código real de Bckbs:** `GET client-meal-calendar` (admin, `Admin\ClientMealPlanController::getCalendar`, parámetros `user_id`+rango de fechas, máx. 62 días) — devuelve el plan de comidas real día a día con receta completa (`DailyPlan`/`DailyPlanRecipe`/`Recipe`). Es el equivalente exacto de `client-calendar-data` (que solo cubre entrenamiento) para el lado de nutrición. No se construyó nada nuevo — mismo criterio que el resto del proyecto: primero se comprobó que ya existía.
- **Memoria del cliente, alcance explícito ampliado:** antes la tabla de herramientas citaba la memoria de forma genérica; ahora nombra explícitamente `log-nutricion.json` y la clave `nutricion` de `perfil-cliente.json` (gustos, disponibilidad de cocina, hábitos prioritarios), no solo el lado de entrenamiento.
- Paso 3 del flujo (`system-prompt.md`, sube a v0.3.0) actualizado: si la pregunta combina los dos dominios, consulta ambas fuentes antes de responder, no solo una.
- **El límite no cambia:** leer los dos dominios sigue sin ser lo mismo que decidir sobre ellos — el agente sigue sin poder cambiar ni un ejercicio ni un macro, sección 1 intacta.

## v0.2.0 — 2026-09-27

El usuario pidió explícitamente que el agente no "suene a bot" — que responda con la formación real de un profesional de ciencias del deporte combinado con atención al cliente, no como un FAQ automatizado que reconoce palabras clave.

- **Nuevo `modulos/tono-y-conocimiento-deportivo.md`:** persona (cómo habla, cómo adapta cada respuesta al cliente real en vez de copiar una plantilla), principios de atención al cliente (validar antes de resolver, nunca un "no" seco, ser concreto no genérico), y un banco de **patrones** de respuesta — no plantillas de copiar/pegar — para las dudas reales más frecuentes: agujetas/DOMS (con la línea exacta que obliga a escalar en vez de tranquilizar), "no veo resultados" (reencuadre honesto con datos reales de su historial, nunca prometiendo un plazo), desliz puntual en dieta/entrenamiento (quitar presión sin sugerir "compensar"), uso de la app, bajón de motivación, y curiosidad sobre por qué su plan está diseñado así (citando el razonamiento real ya guardado, nunca inventando uno).
- **Guardrail explícito:** este módulo nunca amplía el alcance de la sección 1 del `system-prompt.md` — mejora cómo se responde dentro de lo ya permitido. Ninguno de sus patrones autoriza saltarse el cribado del Paso 2 ni la escalación de la sección 4; varios patrones incluyen explícitamente cuándo, pese a "sonar bien", hay que escalar igual (ej. si "no veo resultados" se repite, es señal de riesgo de baja, no solo una duda a resolver una vez).
- `system-prompt.md` sube a v0.2.0: sección 1 y Paso 4 del flujo referencian el nuevo módulo.

## v0.1.0 — 2026-09-27

Primer diseño. Primer agente operativo nuevo tras la transición M0→M1 (ver `docs/roadmap.md` y `docs/ORGANIGRAMA_AGENTES.md`), priorizado por el usuario sobre el Agente de Onboarding por cubrir más volumen real de trabajo hoy.

- **Investigación previa contra el código real de Bckbs** (mismo criterio que los otros 3 agentes: no inventar integraciones sin comprobar) — se encontraron dos gaps reales, ninguno bloqueante: **(1)** no existe forma de buscar un usuario por `phone_number` (`UserController::index` solo busca por nombre/email/username) — el mapeo teléfono→cliente_id vive en una hoja mantenida a mano hasta que el volumen lo justifique. **(2)** `tasks.category` no tiene un valor `soporte` (solo `entrenamiento,nutricion,revisiones,otro`) — se usa `otro` por ahora.
- **Sí existen ya, confirmado en el código real:** `GET client-calendar-data` (admin, `ClientProfileCalendarController::getMergedMonth`) para preguntas factuales sobre el plan del cliente, y `POST task-store` (`TaskController::store`) como mecanismo de escalación a humano — ambos reutilizados tal cual, sin construir nada nuevo en Bckbs.
- **Canal confirmado por el usuario:** WhatsApp (número personal/business), sin integración con Bckbs todavía — de ahí que el diseño use Twilio + n8n (infraestructura de M1) en vez de asumir un canal distinto.
- Diseño completo en `system-prompt.md`: rol/alcance (qué responde directo vs. qué escalar siempre, sin excepción — programación/nutrición, precios/cancelación, salud), flujo paso a paso, reglas de escalación en tiempo real (no espera a ningún resumen semanal, el Agente Director ni siquiera existe todavía), manejo de excepciones, asignación de modelo.
- Nuevo `esquemas/log-interaccion.schema.json` — adapta el JSON de ejemplo de `docs/ORGANIGRAMA_AGENTES.md` a los datos reales disponibles (cliente_id real, no un id genérico; task_id_creado quedando trazado si escaló).
- **No desplegable todavía** — quedan prerrequisitos puramente operativos (cuenta WhatsApp Business/Twilio, instancia n8n, hojas de mapeo y de log) documentados en `docs/TAREAS_PENDIENTES.md`, ninguno de código.
- Sin Control de Soporte todavía (nivel 2 del organigrama) — por diseño, se añade solo cuando este operativo funcione sin supervisión constante.
