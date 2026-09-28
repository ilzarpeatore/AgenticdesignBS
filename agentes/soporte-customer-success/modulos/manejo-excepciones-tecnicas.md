# Módulo: Manejo de excepciones técnicas (Exception Handling and Recovery, cap. 12)

**Tipo:** General — aplica a todo el flujo de ambos agentes que lo referencian (Soporte, Onboarding), no a un paso concreto
**Se activa cuando:** cualquier llamada a una herramienta (API de Claude, cualquier endpoint de Bckbs, entrega por WhatsApp/Twilio) falla de forma técnica
**Versión:** 0.1.0 · **Última actualización:** 2026-09-27
**Procedencia:** auditoría del diseño contra el contenido teórico del repositorio (`Agentic-Design-Patterns`, capítulo 12). Ambos agentes tenían una sección llamada "Manejo de excepciones" que en realidad cubre otra cosa — casos de negocio (el cliente da un dato ambiguo o contradictorio), no fallos técnicos (una herramienta cae, una API responde 500, un timeout). Son dos patrones distintos del libro y no deben confundirse: este módulo es el que corresponde de verdad al capítulo 12.

## Por qué esto no es lo mismo que "Manejo de excepciones" (sección 5/4bis de cada `system-prompt.md`)

Esa otra sección resuelve "el cliente dijo algo que no sé interpretar". Este módulo resuelve "intenté hacer algo y el sistema me lo impidió" — un fallo de infraestructura, no de contenido. Confundirlos es el error real que motivó esta auditoría: un agente que solo sabe reaccionar a datos ambiguos del cliente, pero no tiene ningún plan para cuando su propia herramienta falla, sigue siendo frágil en producción aunque su cribado de negocio sea impecable.

## Detección

Antes de asumir que una respuesta de herramienta es válida, comprueba que lo sea de verdad — no proceses una respuesta malformada como si fuera buena:

- Cualquier endpoint de Bckbs (`client-calendar-data`, `client-meal-calendar`, `client-session-feedback`, `admin/users/lookup-by-phone`, `task-store`, `admin-form-submission-list`) que devuelva un código HTTP 5xx, o un 4xx que el propio diseño de este agente no espera como caso normal (un 404 de "cliente no encontrado" ya está previsto en el flujo; un 500 no lo está).
- Un timeout de red en cualquiera de esas llamadas, o en la propia llamada a la API de Claude.
- Una respuesta que llega con código 200 pero sin la forma esperada (JSON malformado, campos que el diseño da por hechos que existen y no están).
- Un envío de WhatsApp/Twilio que Twilio marca como no entregado.

## Manejo

- **Logging:** registra el fallo en el log de interacciones (`esquemas/log-interaccion.schema.json`) igual que cualquier otra entrada, usando `accion` para dejarlo identificable sin ambigüedad — ej. `"fallo técnico: GET client-session-feedback devolvió 500"`. No lo mezcles con `riesgo_detectado`, que es para señales del cliente, no para fallos de infraestructura.
- **Reintentos:** para errores transitorios (timeout, 502/503) — configura el nodo HTTP correspondiente en n8n con 1-2 reintentos y un backoff corto (propuesta: 5-10 segundos). No reintentes en bucle indefinido, ni reintentes un 4xx que no es transitorio por naturaleza (ej. una validación rechazada no se arregla reintentando igual).
- **Fallback / degradación controlada:** si no puedes leer el contexto que necesitas (memoria del cliente, calendario real, feedback de sesiones), **no generes contenido como si el cliente no tuviera historial** — eso sería inventar una premisa falsa, no degradar con cuidado. La respuesta al cliente en ese momento debe ser honesta y breve ("dame un momento, tengo un problema técnico para consultar tu información, en breve te confirmo") — nunca una respuesta de contenido generada sin los datos reales que la sustentan.
- **Notificación:** si el fallo persiste tras los reintentos, escala exactamente igual que cualquier señal de la sección 4/Escalación — crea una tarea (`POST task-store`, `priority: high`) para que el coach lo sepa. Desde el 2026-09-27 esto ya dispara aviso activo (`TaskEscalationAlertService` en Bckbs) — un fallo técnico que te impide atender a un cliente es tan urgente como cualquier otra señal de la sección 4, porque el cliente se queda sin respuesta real si nadie actúa.

## Recuperación

- **No dejes datos a medias:** si un flujo con efectos secundarios (ej. el check-in semanal, que escribe en `log-registro.json`/`log-nutricion.json`) falla después de haber escrito parte de la entrada, no dejes una entrada parcial que parezca completa — o se completa con los campos disponibles marcando explícitamente los que faltan, o no se escribe nada. Un dato a medias sin marcar es peor que no tener el dato.
- **Distingue fallo transitorio de fallo real** antes de decidir entre reintentar y escalar — un único timeout puntual no es lo mismo que 3 fallos seguidos del mismo endpoint.
- **Escalación como último recurso:** agotados los reintentos, la tarea creada (ver "Notificación" arriba) es la recuperación — no inventes una solución alternativa por tu cuenta ni sigas intentando indefinidamente.

## Caso especial: el cliente escribe y no hay forma de generar ninguna respuesta real (la API de Claude falla del todo)

El cliente no debe quedarse sin ninguna respuesta. n8n debe tener, fuera de este agente (un nodo de código simple, no otra llamada al modelo — sería lo mismo que acaba de fallar), un mensaje de acuse de recibo fijo y pre-escrito para este caso exacto ("Recibido, en cuanto pueda te confirmo") que se envía cuando la llamada al modelo falla del todo, más la tarea de escalación de siempre. Esto no pasa por el módulo de tono (no lo genera el LLM) ni por la validación del Paso 6 (no hay contenido que validar) — es la única respuesta de este sistema que no pasa por ninguno de los dos, precisamente porque existe para el caso en que ninguno de los dos está disponible.

## Guardrail

Este módulo nunca decide contenido de programación/nutrición ni resuelve por su cuenta un fallo que requiere intervención humana real (ej. una credencial caducada, un endpoint de Bckbs caído de verdad) — su trabajo es detectar, no fingir que todo va bien, y escalar cuando corresponde. Ningún reintento ni fallback sustituye la corrección real del problema técnico subyacente.
