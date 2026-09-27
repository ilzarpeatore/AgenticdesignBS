# Módulo: Validación determinista antes de enviar

**Tipo:** General — capa de seguridad transversal, mecánica (no la aplica el LLM sobre sí mismo)
**Se activa cuando:** siempre, sobre cada mensaje saliente generado, antes de que n8n lo envíe por Twilio
**Versión:** 0.1.0 · **Última actualización:** 2026-09-27
**Procedencia:** los 3 agentes de M0 tienen un validador determinista (Paso 3/4, código no LLM) antes de que nada llegue a producción, revisado además por un humano al 100%. Este agente no tiene ninguna de las dos cosas — el mensaje sale directo al cliente real en cuanto se genera. Este módulo es el único filtro mecánico que le queda; no sustituye la revisión humana, reduce el coste de que un fallo del LLM (no seguir el cribado del Paso 2, alucinar un dato) llegue sin ningún control a un cliente real.

## Por qué existe

El cribado del Paso 2 de `system-prompt.md` vive dentro del propio prompt — depende de que el LLM lo siga bien turno a turno, sin ningún humano revisando antes de enviar (a diferencia de entrenamiento/nutrición/importador). Este módulo es una segunda capa, mecánica y barata, que no razona: solo comprueba patrones explícitos en el texto ya generado. No decide si el contenido es bueno — decide si es lo bastante sospechoso como para no enviarlo sin que alguien lo mire primero.

## Implementación (nodo de código en n8n, después de la llamada a Claude, antes del nodo de envío por Twilio)

Comprueba el mensaje generado contra estas reglas, en orden. Si cualquiera se cumple, **no se envía el mensaje generado**: se envía en su lugar una respuesta neutra fija ("Un segundo que te confirmo esto y te escribo 🙂") y se crea una tarea (`POST task-store`, `priority: high`, `category: otro`, `description` incluye el mensaje del cliente Y el mensaje bloqueado, para que el coach vea exactamente qué iba a salir).

1. **Denylist de precio/condiciones comerciales** — el mensaje generado contiene alguno de: `€`, `eur`, `precio`, `tarifa`, `descuento`, `oferta`, `reembolso`, `devoluc`, `cancela`, `dar de baja`, `cuota`, `mensualidad`. Regla de fondo: si Paso 2 clasificó correctamente, el mensaje nunca debería llegar aquí conteniendo esto — que aparezca es la señal de que el cribado falló, no una casualidad a ignorar.
2. **Denylist de prescripción de cambio de programación/nutrición** — el mensaje generado contiene patrones tipo `cambia a`, `sustituye por`, `haz en su lugar`, `en vez de haz`, `te recomiendo hacer X series/repeticiones/kg`, o cualquier número de series/repeticiones/carga distinto al que ya existe en el plan real consultado. El agente puede **citar** el plan real (sección 2), nunca **prescribir** uno nuevo.
3. **Denylist de diagnóstico médico** — patrones tipo `tienes una`, `es una lesión de`, `podría ser un/una` seguido de término clínico (tendinitis, desgarro, hernia, rotura, esguince...). Explicar DOMS/agujetas normales (patrón 3.1 de `tono-y-conocimiento-deportivo.md`) está permitido; diagnosticar no.
4. **Coherencia con el Paso 2** — si el turno se clasificó para escalar (sección 4 de `system-prompt.md`), el mensaje generado debe ser corto (< 200 caracteres aprox.) y no puede contener información sustantiva nueva — si es largo/elaborado, algo falló y se bloquea igual, aunque no matchee ninguna denylist de arriba.
5. **Verificación de dato real citado** — si el mensaje menciona un día concreto, un ejercicio concreto, o una receta concreta (afirmaciones factuales sobre el plan del cliente), debe existir en el log de este mismo turno una llamada real a `client-calendar-data` y/o `client-meal-calendar` que la respalde. Sin esa llamada registrada, es una alucinación — se bloquea.

## Guardrail

Este módulo nunca decide qué SÍ se puede enviar — solo qué NO. Que un mensaje pase estas 5 comprobaciones no lo exime de las reglas de `system-prompt.md` ni de `tono-y-conocimiento-deportivo.md`; es una red adicional, no un sustituto de seguirlas bien desde el principio.

## Pendiente de calibrar con uso real

Las denylists de arriba son un punto de partida razonable, no una lista cerrada — cuando el agente esté en producción, revisa periódicamente los casos que este módulo bloqueó (quedan documentados en la tarea creada) para afinar falsos positivos (bloquea de más) y falsos negativos (deja pasar algo que no debería) según lo que realmente escriban tus clientes.
