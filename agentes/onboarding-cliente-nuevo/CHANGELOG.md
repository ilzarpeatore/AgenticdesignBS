# Changelog — Agente de Onboarding (cliente nuevo)

## v0.1.0 — 2026-09-27

Primer diseño. El usuario pidió empezar el siguiente agente del organigrama de M1 tras el Agente de Soporte / Customer Success; se eligió Onboarding por ser su pareja natural en el área soporte (`docs/ORGANIGRAMA_AGENTES.md` ya los marcaba juntos desde el principio) y por reutilizar casi toda la infraestructura de Soporte en vez de construir una nueva.

- **Investigado primero el código real de Bckbs** (mismo criterio que con Soporte): el flujo de intake (cuestionario PAR-Q + entrenamiento + nutrición) ya está resuelto por la propia app — `onboarding_completed_at` se marca solo cuando las 3 tablas existen de verdad (hay un fix real documentado, 2026-09-18, para un bug donde se marcaba completo sin datos). Este agente no gestiona esa parte, actúa después.
- **Disparador decidido por el usuario:** el reloj de "primeros 7-14 días" empieza con la primera asignación real de programa de entrenamiento (`ProgramClientAssignment`), no con el alta de cuenta ni con el cuestionario — se descartó "al alta" (cubriría mejor el abandono antes de tener plan, pero no hay nada que "empezar" todavía) y "al completar el cuestionario" (dejaría sin cubrir al cliente que nunca lo rellena).
- **Cierre automático por cliente:** si `GET client-session-feedback` muestra una sesión real completada antes de los 14 días, el onboarding de ese cliente termina ahí — no se acompaña un número fijo de días si el objetivo (que empiece) ya se cumplió.
- **Nuevo módulo `modulos/primeros-pasos.md`:** mensaje de bienvenida (citando algo real del cliente, nunca genérico) y aviso si no ha empezado (nunca en tono de reproche, siempre asumiendo una barrera práctica antes que falta de voluntad).
- **Reutilización explícita, no duplicación:** mismo webhook WhatsApp/Twilio, mismo `GET admin/users/lookup-by-phone`, mismo `GET client-session-feedback`, mismo `POST task-store`, mismo esquema de log de interacciones y los mismos módulos de tono/validación que el Agente de Soporte — un cambio en esos módulos compartidos afecta a los dos agentes por igual.
- **Gap real encontrado y documentado, no construido todavía:** no existe en Bckbs un endpoint que liste "clientes con primera asignación de programa reciente" — el arranque del flujo depende por ahora de que el coach lo dispare manualmente la primera vez que asigna un plan.
- **Reglas de escalación (sección 4):** idénticas a las de Soporte, sin excepción por ser "solo los primeros días" — más un caso propio (cliente sin ninguna sesión completada al llegar al umbral del Paso 4).
