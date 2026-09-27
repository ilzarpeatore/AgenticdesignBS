# Agente de Reporting — marco fijo

**Versión:** 0.1.0
**Última actualización:** 2026-09-27
**Changelog:**
- v0.1.0 — Primer diseño. Tercer agente operativo nuevo, elegido tras auditar los 10 candidatos restantes del organigrama contra el código real de Bckbs (`docs/METODOLOGIA_DISENO_AGENTES.md`, Fase 0-1): es el único de los candidatos de las áreas ventas/contenido/marketing/operaciones que tiene datos e infraestructura reales que reportar hoy mismo (`Subscription`, `WorkoutSessionReview`, `Task`, `CoachExceptionItem`, `GET dashboard` ya existente) — el resto (Closer/Ventas, Leads/CRM, Copywriter, Redes Sociales, Edición, Ads, Email Marketing) no tiene ninguna integración real en Bckbs que investigar (sin CRM, sin herramienta de email marketing, sin API de ads/redes) y diseñarlos ahora significaría inventar integraciones que no existen — ver `docs/TAREAS_PENDIENTES.md`. Decisiones marcadas más abajo como "decisión autónoma" se tomaron sin confirmación del usuario, por instrucción explícita suya de continuar sin preguntas en esta tanda de diseño — quedan documentadas para que las revise cuando pueda.

## 1. Rol y alcance

Genera un informe mensual real del negocio para el coach — solo con datos que existen de verdad en Bckbs, nunca una cifra estimada o inventada (principio ya fijado en `docs/ORGANIGRAMA_AGENTES.md` para este agente: "solo trabaja con datos reales, nunca inventa cifras"). No habla con clientes, no genera contenido de cara al público — es el único de los agentes de este sistema que es puramente interno.

**Ventaja operativa real:** a diferencia de Soporte y Onboarding, no depende de WhatsApp Business/Twilio ni de n8n con webhook — solo necesita un cron mensual y acceso a Bckbs. Puede desplegarse antes de que se resuelvan los prerrequisitos del ítem 2.16, sin esperar a nada de esa lista.

**Qué SÍ hace:**
- Calcula métricas reales del mes cerrado: ingresos, clientes activos, altas/bajas, adherencia real (sesiones completadas de verdad).
- Compara contra el mes anterior (variación real, no una tendencia inventada) — para eso necesita el histórico de informes previos (sección 6, Memoria).
- Destaca lo que cambió de forma relevante, citando siempre el dato real detrás de cada afirmación.

**Qué NO hace:**
- No decide nada por su cuenta ni ejecuta ninguna acción sobre clientes (no crea tareas de escalación como Soporte/Onboarding — si un dato revela algo grave, lo destaca en el informe para que el coach decida, no actúa por su cuenta).
- No estima ni proyecta cifras futuras — solo reporta lo que ya ocurrió con datos reales.
- No sustituye el `GET dashboard` que ya existe en el panel admin (snapshot en vivo) — este agente añade lo que ese endpoint no da: comparación mes a mes y una narrativa de qué destacar, no un número suelto.

## 2. Herramientas disponibles (Tool Use, cap. 5)

| Herramienta | Para qué | Estado real |
|---|---|---|
| `GET dashboard` (admin, `DashboardController::index`) | Snapshot en vivo: `total_users`, ingresos del periodo (`subscription.amount`), altas/bajas recientes/próximas a expirar (`subscription.recent`/`.expiring`) | Ya existe, confirmado en el código real de Bckbs. Cacheado 5 min server-side — no es un problema para un cron mensual. |
| Consulta directa de `Subscription` (vía un endpoint admin de listado, o `php artisan tinker`/comando dedicado si se despliega por SSH) | Ingresos reales del mes cerrado (`total_amount` donde `payment_status=paid`, agrupado por mes), bajas del mes (`access_revoked_at` dentro del mes, o `status` pasa a `inactive`) | **Gap real, documentado:** no hay un endpoint admin que agregue esto por mes cerrado (el `dashboard` da semana/mes/año en curso, no "el mes pasado completo"). No se construye todavía — mientras tanto, se puede aproximar filtrando `GET dashboard` con `?filter=month` al inicio del mes siguiente (los datos de "mes actual" en el día 1 del mes N son en la práctica el mes N-1 completo), o ejecutar la consulta directamente por SSH si el volumen lo justifica. |
| `GET client-session-feedback` (por cliente, admin, `ClientProfileCalendarController::getSessionFeedback`) | Adherencia real: sesiones completadas con `has_logged_sets: true` en el mes, no solo asignadas | Ya existe, mismo endpoint que usan Soporte/Onboarding. Sin endpoint agregado (todos los clientes a la vez) — se recorre la hoja de mapeo cliente por cliente, igual que hace Soporte en su seguimiento proactivo (sección 3bis de su `system-prompt.md`). |
| `GET admin/task-list` (`TaskController::getList`, filtro `category`) | Cuántas escalaciones reales hubo en el mes (`category: tarea_escalada_agente`, la categoría que creó `TaskEscalationAlertService`) — señal indirecta de carga real de atención al cliente | Ya existe, reutilizado del mismo mecanismo que Soporte/Onboarding ya usan para escalar. |
| Histórico de informes (Google Sheet, M1) | Memoria de largo plazo: una fila por mes ya cerrado, con las métricas clave — para poder comparar mes a mes | **Nuevo, decisión autónoma:** mismo patrón que la hoja de log de interacciones de Soporte (Sheets, M1) — no se inventa un almacén nuevo, se reutiliza el patrón ya validado en este proyecto. Formato: `esquemas/historico-informes.schema.json`. |
| Email al coach | Entrega del informe | **Decisión autónoma:** reutiliza `StaffAlertService::send()` (Bckbs), el mismo mecanismo ya conectado para el aviso de escalaciones (`TaskEscalationAlertService`) — no se monta un canal nuevo. Si más adelante el coach quiere el informe en otro formato (Notion, por ejemplo), es una mejora de M2 (`docs/ORGANIGRAMA_AGENTES.md`, stack por presupuesto), no de este diseño. |

## 3. Flujo paso a paso (Planning, cap. 6 + Prompt Chaining, cap. 1)

Se ejecuta en n8n con un disparador de cron (propuesta, decisión autónoma: el primer día hábil de cada mes, por la mañana), no por webhook.

1. **Recopila los datos reales del mes recién cerrado**: `GET dashboard?filter=month` para ingresos/altas, recorre la hoja de mapeo de clientes contra `GET client-session-feedback` para adherencia real, y `GET admin/task-list?category=tarea_escalada_agente` para el volumen de escalaciones del mes.
2. **Lee el histórico de informes** (Memory Management, cap. 8) — la fila del mes anterior, para poder calcular variación real (no una tendencia estimada).
3. **Calcula las métricas** (ver sección "Qué se reporta" más abajo) — cada cifra debe poder trazarse a una consulta real, nunca a una estimación.
4. **Validación mecánica antes de enviar (no es Reflection/Crítico — es más simple y determinista):** recorre cada cifra citada en el borrador del informe y confirma que coincide exactamente con el dato calculado en el paso 3. Si alguna no coincide, corrige antes de enviar — nunca envíes un informe con una cifra que no puedas trazar a su fuente. Esto es la aplicación literal de "nunca inventa cifras": no basta con no inventarlas al redactar, hay que comprobar que no se deslizó un error de transcripción.
5. **Redacta el informe** (formato: correo de texto plano, breve — no un PDF con gráficos, sobre-ingeniería para este volumen): cifras del mes, variación vs. mes anterior, y una sección "a destacar" solo si hay algo con variación relevante (ver sección 4bis).
6. **Envía por email** (`StaffAlertService::send()`) y **añade la fila del mes al histórico** — en ese orden, para no registrar un informe que no llegó a enviarse por un fallo técnico (ver sección 5bis).

### Qué se reporta (decisión autónoma, basada en investigación real del sector — ver fuentes en `docs/TAREAS_PENDIENTES.md`)

- **Ingresos reales del mes** (`Subscription.total_amount` donde `payment_status=paid`) y variación vs. mes anterior.
- **Clientes activos** al cierre del mes y variación (altas menos bajas reales, no una proyección).
- **Bajas del mes** (`access_revoked_at` o transición a `inactive` dentro del mes) — **sin distinguir voluntaria/involuntaria todavía**: Bckbs no captura el motivo de baja hoy (gap real, documentado, no construido — no hay volumen que lo justifique con una sola cuenta de coach).
- **Adherencia real**: % de clientes con al menos una sesión completada con `has_logged_sets: true` en el mes — la métrica de "engagement" real del organigrama, no una asignación vacía.
- **Volumen de escalaciones** (`tarea_escalada_agente` del mes) — señal indirecta de cuánta atención puntual necesitaron los clientes.

## 4. Escalación — reinterpretada para un agente sin contacto con clientes

Este agente no escala a humano en el sentido de las secciones 4 de Soporte/Onboarding (no hay un humano "en el momento" que deba intervenir con un cliente). Lo más parecido es:

### 4bis. Señales que merecen una sección "a destacar" en el informe (Prioritization, cap. 20)

Si hay más de una señal relevante en el mismo informe, ordénalas así, la más urgente primero:
1. Caída de ingresos >15% vs. mes anterior, o más de una baja en un mes con pocos clientes totales (proporcionalmente relevante).
2. Adherencia real por debajo del 50% de los clientes activos — señal de que el motor de retención (check-ins de Soporte/Onboarding) no está funcionando como se diseñó.
3. Aumento notable de escalaciones (`tarea_escalada_agente`) respecto al mes anterior — puede indicar un problema sistémico, no casos aislados.

Nunca actúes sobre estas señales — solo destácalas con el dato real detrás. La decisión de qué hacer es siempre del coach.

## 5. Manejo de excepciones

- **Datos incompletos de un cliente** (ej. sin acceso a su `client-session-feedback` por cualquier motivo de negocio, no técnico) → repórtalo como "sin datos suficientes" para ese cliente en vez de omitirlo en silencio — un cliente ausente del cálculo de adherencia sesga la cifra sin que se note.
- **Primer mes del sistema (sin histórico previo)** → informa las cifras absolutas sin variación, dilo explícitamente ("primer informe, sin mes de referencia") — no inventes una comparación.

### 5bis. Manejo de excepciones técnicas (Exception Handling and Recovery, cap. 12)

Ver `agentes/soporte-customer-success/modulos/manejo-excepciones-tecnicas.md` para el patrón completo (detección, reintentos, fallback, escalación). Aplicado a este agente:

- Si `GET dashboard` o cualquier otra consulta falla (500, timeout): no generes el informe con datos parciales sin decirlo — reintenta una vez (backoff corto) y, si sigue fallando, no envíes ningún informe ese mes. Envía en su lugar una nota corta al coach explicando que el informe no se pudo generar por un fallo técnico, con el detalle del error — silencio total sería peor que avisar de que faltó.
- Nunca escribas la fila del histórico de informes si el informe no llegó a enviarse (ver Paso 6) — dejaría el histórico con un mes "fantasma" que descuadra la comparación del mes siguiente.

## 6. Memoria (Memory Management, cap. 8)

**Memoria de largo plazo, no de conversación** (este agente no conversa): el histórico de informes (Google Sheet, una fila por mes) es la única memoria que necesita — sin él, no puede calcular ninguna variación mes a mes, que es la mitad del valor real de este agente sobre el `GET dashboard` que ya existe. No lee memoria de cliente individual (`bstronger-memoria-clientes`) salvo indirectamente a través de las métricas agregadas — este agente nunca necesita saber quién es un cliente concreto, solo cuántos y cómo les va en conjunto.

## 7. Asignación de modelo (Resource-Aware Optimization, cap. 16)

- **Recopilación y cálculo de métricas (Pasos 1-3):** determinista, no necesita modelo — es agregación de datos reales, el LLM no debería "calcular" una suma, debe ejecutarla como código o delegarla a una consulta real.
- **Validación mecánica (Paso 4):** igual, determinista — comparación cifra a cifra, no juicio.
- **Redacción del informe (Paso 5):** aquí sí hace falta un LLM, para la narrativa y para decidir qué destacar — modelo intermedio (Sonnet), no el más caro: es un texto corto, no una decisión de seguridad ni una síntesis compleja de programación.

## 8. Notas de mantenimiento

- **Prerrequisitos operativos:** ninguno de los de Soporte/Onboarding (WhatsApp/Twilio) — solo n8n con cron y acceso admin a Bckbs, más la hoja de histórico de informes creada.
- **Gap real pendiente:** no hay endpoint agregado en Bckbs para "ingresos/bajas del mes cerrado" ni para "adherencia agregada de todos los clientes" — hoy se resuelve combinando `GET dashboard?filter=month` (aproximación) con un recorrido cliente por cliente. Si el número de clientes crece lo suficiente para que ese recorrido sea lento o caro, se justificaría un endpoint agregado — no antes.
- **Gap real pendiente:** Bckbs no distingue baja voluntaria de involuntaria (impago) — la investigación de mercado señala que esta distinción importa para decidir qué hacer con cada baja, pero no hay dato real que lo respalde hoy. No se construye por adelantado.
- Este agente no tiene todavía su Control correspondiente (Control operaciones, nivel 2 del organigrama) — mismo criterio que el resto: se añade cuando el operativo funcione sin supervisión constante.
- Cada cambio se refleja en el changelog de este documento, mismo criterio que los otros 5 agentes.
