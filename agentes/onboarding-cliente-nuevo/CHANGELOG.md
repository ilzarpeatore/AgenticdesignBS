# Changelog — Agente de Onboarding (cliente nuevo)

## v0.4.0 — 2026-09-27

El usuario pidió priorizar cerrar un hallazgo pendiente: el check-in semanal del Agente de Soporte y este agente no se coordinaban entre sí — un cliente nuevo podía recibir la bienvenida/toque intermedio de Onboarding **y** el check-in semanal de Soporte en la misma semana, justo el "info overload" entre dos agentes que la investigación de v0.3.0 advertía dentro de uno solo.

- `esquemas/log-interaccion.schema.json` (compartido con Soporte) gana el campo `onboarding_estado` (`activo`/`cerrado`), obligatorio en toda entrada de este agente vía `allOf`/`if`/`then` — mismo patrón condicional ya usado en `log-registro.schema.json`/`log-nutricion.schema.json` para `origen`.
- El campo `agente` del esquema pasa de `const: "soporte-customer-success"` a `enum` con los dos agentes — corrige un descuido real: este agente decía "reutilizar" el esquema desde v0.1.0, pero el `const` original solo permitía el nombre de Soporte.
- Cada entrada de este agente debe llevar `agente: "onboarding-cliente-nuevo"` y `onboarding_estado: "activo"`, salvo la entrada de cierre (Paso 3 o Paso 6), que lleva `"cerrado"`.
- El check-in semanal de Soporte lee este campo y se salta a un cliente cuyo onboarding sigue activo — sin necesidad de ningún endpoint nuevo en Bckbs, solo usando la hoja de log que ya comparten.

## v0.3.0 — 2026-09-27

El usuario pidió investigar cómo debería ser un onboarding perfecto para un servicio de +300€/mes (fuentes en `docs/TAREAS_PENDIENTES.md`). Tres hallazgos, tres cambios de diseño confirmados por el usuario:

- **El "info dump" del día 0 es el error más citado.** Nuevo Paso 2 en el flujo: un toque intermedio a los 2-3 días (un único consejo práctico, no una segunda bienvenida) — reparte lo que antes se intentaba meter todo en el mensaje de bienvenida. El Paso 1 queda limitado explícitamente a 2-3 ideas.
- **Nunca cerrar en silencio.** El cierre por primera sesión completada (antes un simple registro en el log) ahora manda un check-in breve de reconocimiento citando el dato real de la sesión. El cierre por fin de ventana a los 14 días (antes "sin acción") ahora manda un mensaje de transición y crea una tarea de baja prioridad recordando al coach el check-in de satisfacción — apuntado al día 30, no al día 14: la investigación señala el check-in de 30 días ("qué está funcionando, qué mejorarías") como el de mayor impacto en retención, no uno más temprano.
- **El vídeo de bienvenida del coach es la pieza de mayor impacto citada** — transmite que hay una persona real detrás, algo que ningún texto logra igual. Documentado con instrucciones de contenido completas en `modulos/primeros-pasos.md` (duración, qué decir, formato), marcado explícitamente como pendiente de que el usuario lo grabe — no es algo que este agente pueda generar ni decidir, y no bloquea el resto del diseño mientras tanto.

## v0.2.0 — 2026-09-27

Gap de corrección encontrado al revisar cómo seguir perfeccionando el diseño: `GET client-session-feedback` (la señal que este agente usa para decidir "el cliente ya empezó de verdad, cierro el onboarding") solo filtraba por `completed_at IS NOT NULL` — no comprobaba si la sesión tenía series realmente registradas.

- Bckbs ya tenía un servicio dedicado exactamente a este patrón de bug real (`EmptySessionAlertService`, caso Ayoub, 2026-09-25: sesiones finalizadas en verde con volumen 0 y cero filas en `client_exercise_logs`) — pero esa comprobación no llegaba a `client-session-feedback`.
- Si el primer "completado" de un cliente nuevo hubiera sido justo uno de esos casos vacíos, este agente habría cerrado el seguimiento pensando que el cliente ya había empezado — la peor falsa señal de tranquilidad posible, justo en el momento que más importa vigilar.
- **Arreglado y pusheado a Bckbs `main`** (commit `b11eb09`): nuevo campo `has_logged_sets` en la respuesta, reutilizando `EmptySessionAlertService::hasLoggedSets()` sin reimplementar la lógica. Campo aditivo — no afecta a otros consumidores del mismo endpoint (Agente de Soporte). 3 tests nuevos, suite Feature completa (133 tests) verde.
- Paso 2 del flujo actualizado: una sesión `completed_at` con `has_logged_sets: false` se trata igual que si no hubiera ninguna sesión — sigue el flujo normal del Paso 3, nunca cierra el onboarding por sí sola.

## v0.1.0 — 2026-09-27

Primer diseño. El usuario pidió empezar el siguiente agente del organigrama de M1 tras el Agente de Soporte / Customer Success; se eligió Onboarding por ser su pareja natural en el área soporte (`docs/ORGANIGRAMA_AGENTES.md` ya los marcaba juntos desde el principio) y por reutilizar casi toda la infraestructura de Soporte en vez de construir una nueva.

- **Investigado primero el código real de Bckbs** (mismo criterio que con Soporte): el flujo de intake (cuestionario PAR-Q + entrenamiento + nutrición) ya está resuelto por la propia app — `onboarding_completed_at` se marca solo cuando las 3 tablas existen de verdad (hay un fix real documentado, 2026-09-18, para un bug donde se marcaba completo sin datos). Este agente no gestiona esa parte, actúa después.
- **Disparador decidido por el usuario:** el reloj de "primeros 7-14 días" empieza con la primera asignación real de programa de entrenamiento (`ProgramClientAssignment`), no con el alta de cuenta ni con el cuestionario — se descartó "al alta" (cubriría mejor el abandono antes de tener plan, pero no hay nada que "empezar" todavía) y "al completar el cuestionario" (dejaría sin cubrir al cliente que nunca lo rellena).
- **Cierre automático por cliente:** si `GET client-session-feedback` muestra una sesión real completada antes de los 14 días, el onboarding de ese cliente termina ahí — no se acompaña un número fijo de días si el objetivo (que empiece) ya se cumplió.
- **Nuevo módulo `modulos/primeros-pasos.md`:** mensaje de bienvenida (citando algo real del cliente, nunca genérico) y aviso si no ha empezado (nunca en tono de reproche, siempre asumiendo una barrera práctica antes que falta de voluntad).
- **Reutilización explícita, no duplicación:** mismo webhook WhatsApp/Twilio, mismo `GET admin/users/lookup-by-phone`, mismo `GET client-session-feedback`, mismo `POST task-store`, mismo esquema de log de interacciones y los mismos módulos de tono/validación que el Agente de Soporte — un cambio en esos módulos compartidos afecta a los dos agentes por igual.
- **Gap real encontrado y documentado, no construido todavía:** no existe en Bckbs un endpoint que liste "clientes con primera asignación de programa reciente" — el arranque del flujo depende por ahora de que el coach lo dispare manualmente la primera vez que asigna un plan.
- **Reglas de escalación (sección 4):** idénticas a las de Soporte, sin excepción por ser "solo los primeros días" — más un caso propio (cliente sin ninguna sesión completada al llegar al umbral del Paso 4).
