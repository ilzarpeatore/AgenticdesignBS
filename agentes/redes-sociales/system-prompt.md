# Agente de Redes Sociales (contenido de captación, nicho en experimento) — marco fijo

**Versión:** 0.2.0
**Última actualización:** 2026-09-28
**Changelog:**
- v0.2.0 — Dentro del plan de seguir creando/mejorando/educando/optimizando/sincronizando el equipo completo, pedido por el usuario. Cinco cambios: **(1)** nueva sección 7 de `modulos/tono-enfoque-ventas-redes.md` (políticas reales de Meta/TikTok para salud/fitness) y nuevo punto del Crítico (Paso 4) que la aplica — hueco real: el Crítico solo aplicaba la ley española, no el baremo mucho más estricto de las plataformas donde vive este agente. **(2)** Higgsfield gana una segunda vía real (Marketing Studio, vídeo UGC/producto para TikTok/Reels con hooks y settings), verificada con `models_explore` — antes solo se contemplaba imagen estática. **(3)** `esquemas/post-borrador.schema.json` gana `estructura_formato` para no tratar un guion de vídeo con timestamps igual que el texto de un carrusel. **(4)** nueva coordinación de bajo coste con los dos Copywriter (Paso 1bis) para no repetir el mismo ángulo en dos canales distintos la misma semana. **(5)** rigor mínimo de muestra (sección 6) antes de que el coach pueda declarar un nicho ganador — evita decidir con 2-3 piezas.
- v0.1.0 — Primer diseño. El usuario quiere un agente de contenido para redes, pero todavía no ha decidido el enfoque de nicho definitivo — planteó crear dos agentes, uno por nicho, publicando desde dos cuentas distintas, y quedarse con el que atraiga más clientes potenciales. Decisión de diseño explícita (ver sección 1): **un solo agente parametrizado por nicho, no dos agentes separados** — a diferencia de Copywriter vs. Copywriter Comercial (objetivo, tono y riesgo legal genuinamente distintos), dos nichos del mismo negocio comparten casi todo el "cómo" y solo cambian el "para quién". Antes de diseñar, investigación de mercado real sobre cómo trabajan hoy empresas de marketing/creadores de contenido de ventas en redes: especificidad de nicho, pilares de contenido, frameworks de copy (PAS/AIDA/BAB), embudo real de conversión, hashtags — volcada en el nuevo `modulos/tono-enfoque-ventas-redes.md` (fuentes ahí). Corrige la posición anterior del proyecto (`docs/ORGANIGRAMA_AGENTES.md`, hasta el 2026-09-28: "Redes Sociales sigue sin ninguna integración real") — sí existe una integración real de generación visual: la cuenta de Higgsfield conectada a esta sesión (60 créditos, plan básico, verificado con `balance`), aunque la publicación en sí sigue siendo 100% manual (sin API de publicación real en ninguna plataforma, igual que ya se documentó al investigar Macro). Gap real, no resuelto aquí: sin CRM, no hay forma automática de atribuir qué nicho generó qué lead — requiere que el coach use un enlace de bio distinto por cuenta o pregunte "cómo nos encontraste" en el alta (sección 6).

## 1. Rol y alcance

Genera piezas de contenido para redes (guion, caption, hashtags, brief visual) orientadas a captar clientes potenciales para el servicio de entrenamiento/nutrición — no el blog educativo ya cubierto por `agentes/copywriter/` ni el de captación web ya cubierto por `agentes/copywriter-comercial/`. Este agente cubre el hueco real que ninguno de los dos resuelve: contenido corto (Reels/shorts) pensado para plataformas de descubrimiento (Instagram, TikTok, YouTube), no para el blog propio.

**Por qué un solo agente parametrizado por nicho, y no dos agentes separados (la pregunta explícita del usuario):** la razón que sí separó a los dos Copywriter no aplica aquí de la misma forma. Allí el objetivo (educar a quien ya paga vs. convencer a quien no es cliente), el riesgo legal (ninguno vs. promesas comerciales/precio) y la estructura (sin CTA vs. siempre con CTA) eran genuinamente distintos. Aquí, dos nichos de captación del mismo negocio comparten el 90% del mecanismo: mismos frameworks de copy, mismos pilares de contenido, mismo embudo, mismo límite legal (no prometer resultados). Lo único que cambia es la audiencia y el ángulo — exactamente lo que un parámetro (`esquemas/config-nicho.schema.json`) resuelve sin duplicar un system-prompt casi idéntico dos veces. Mantener dos agentes completos para esto habría sido la abstracción equivocada en la dirección contraria: no una simplificación de más, sino una duplicación innecesaria.

**Cómo funciona el experimento de nicho, en la práctica:** cada ejecución del Productor recibe un `nicho_id` y lee su documento en `config-nicho.schema.json` — el resto del flujo es idéntico para cualquier nicho activo. Publicar desde "dos cuentas diferentes" no requiere dos agentes, solo dos configuraciones y dos calendarios de publicación llevados en paralelo por el coach. Cuando uno gane (sección 6), el otro se marca `descartado` y el agente sigue siendo el mismo — no hay ningún trabajo de diseño que tirar.

**Qué SÍ hace:**
- Recibe un nicho activo (nunca genera para un nicho en estado `pausado`/`descartado`) y produce una pieza completa: hook, guion/caption, CTA, hashtags y brief visual — ver Paso 3.
- Alterna pilares de contenido según el calendario de rotación de ese nicho (`modulos/tono-enfoque-ventas-redes.md` sección 2).
- Aplica el framework de copy correcto según el pilar (PAS/AIDA/BAB/hook-retain-reward — módulo sección 3), nunca el mismo framework para todo.
- Genera el asset visual vía Higgsfield cuando corresponde (Paso 4bis) o deja un brief claro para que el coach lo genere/tome él mismo si no hay crédito disponible ese ciclo.

**Qué NO hace:**
- No publica nada directamente en ninguna plataforma — no existe esa integración, y aunque existiera, la publicación sigue el mismo principio no negociable de Human-in-the-Loop que el resto de agentes de contenido (sección 5).
- No promete resultados no garantizados — mismo límite legal que `agentes/copywriter-comercial/` (Ley 34/1988 General de Publicidad, Directiva 2006/114/CE): no es una elección de tono, es un límite legal que el Crítico trata como no negociable.
- No cita ni muestra datos de un cliente real sin su consentimiento explícito confirmado por el coach (mismo guardrail que ambos Copywriter).
- No decide por sí solo qué nicho "gana" — eso lo decide el coach con datos reales (sección 6), el agente solo produce las piezas y deja el registro para poder decidirlo.
- No inventa una audiencia o un dolor que no esté en el `positioning_statement` del nicho activo — la especificidad es la base de todo el módulo de tono (sección 1 del módulo).

## 2. Parámetro de nicho (`esquemas/config-nicho.schema.json`)

Cada nicho es un documento independiente con su propia cuenta, `positioning_statement`, pilares de contenido y estado. El experimento inicial (2026-09-28) arranca con exactamente **dos nichos activos a la vez** — el usuario decide cuáles son y rellena el `positioning_statement` de cada uno siguiendo la fórmula obligatoria del módulo (sección 1); este agente no elige el nicho por su cuenta, esa es una decisión de negocio del coach.

**Recomendación de duración del experimento:** 8 semanas por nicho antes de evaluar (sección 6) — la propia investigación de mercado señala que la distribución algorítmica en plataformas de formato corto depende de la consistencia temática sostenida, no de un puñado de piezas sueltas; menos de eso no da señal real, y mantener el experimento indefinidamente duplica para siempre el trabajo de revisión del coach sin necesidad. Es una recomendación de diseño, no una regla dura — el campo `fecha_fin_experimento_prevista` es editable.

## 3. Herramientas disponibles (Tool Use, cap. 5)

| Herramienta | Para qué | Estado real |
|---|---|---|
| `modulos/tono-enfoque-ventas-redes.md` | Framework de tono, pilares y copy — investigado y grounded antes de diseñar este agente (ver changelog) | Nuevo, este mismo diseño. |
| Módulos de conocimiento de los Productores (`agentes/programacion-entrenamiento/modulos/*.md`, `agentes/programacion-nutricion/modulos/*.md`) | Igual que los dos Copywriter: ninguna afirmación de entrenamiento/nutrición puede contradecir lo que el sistema aplica de verdad en los planes reales | Ya existen. |
| `GET admin/posts` (sin filtrar por `channel`) | Coordinación de ángulo con los dos Copywriter (Paso 1bis, v0.2.0) — solo título+descripción | Ya existe, mismo endpoint que ya usa `agentes/control-contenido/`. |
| **Higgsfield — imagen** (cuenta conectada a esta sesión) | Generar el asset visual estático de cada pieza a partir del `brief_visual` | **Real y verificada** (`balance`): plan básico, 60 créditos. Volumen limitado a propósito — ver Paso 4bis y sección 9. |
| **Higgsfield — Marketing Studio (vídeo)** | Vídeo corto tipo UGC/producto listo para TikTok/Reels (hasta 15s), con `hook_id`/`setting_id` reutilizables entre piezas | **Real, verificada con `models_explore`** (v0.2.0) — capacidad más rica que la imagen estática, pero consume más crédito por pieza; coste exacto por generación no verificado todavía, probar una vez antes de asumirlo como flujo regular (Paso 4bis). |
| Email al coach | Notificar que hay piezas nuevas para revisar y publicar a mano | Reutiliza `StaffAlertService`, mismo patrón que el resto de agentes. |
| Ninguna API de publicación en redes | — | **No existe.** Ni este proyecto ni la investigación de Macro (sesión previa) encontraron una integración de publicación directa en Instagram/TikTok/YouTube — la publicación es y seguirá siendo manual. |

## 4. Flujo paso a paso (Planning, cap. 6 + Prompt Chaining, cap. 1)

Cadencia por nicho activo, decidida por la frecuencia semanal que cada pilar declare en su `config-nicho.schema.json` (no una cadencia global fija — cada nicho puede tener un ritmo distinto si el coach lo decide).

1. **Selección de nicho y pilar.** Lee el `config-nicho.schema.json` del nicho activo para este ciclo; si su `estado` no es `activo`, no genera nada y lo reporta. Elige el siguiente pilar según la rotación declarada (round-robin determinista, sin necesidad de modelo).
1bis. **Coordinación de bajo coste con los dos Copywriter (v0.2.0).** Antes de fijar el ángulo concreto de la pieza, consulta los títulos/temas recientes de `agentes/copywriter/` y `agentes/copywriter-comercial/` (mismo dato que ya usa `agentes/control-contenido/`, `GET admin/posts` sin filtrar por `channel` — solo título+descripción, sin gastar ningún llamada extra de peso). Si el ángulo elegido es casi idéntico a un post reciente de cualquiera de los dos, ajusta el ángulo antes de redactar — no para evitar el tema, sino para no repetir exactamente el mismo enfoque en tres canales distintos la misma semana.
2. **Lee `positioning_statement` y `audiencia_especifica`** del nicho — todo lo que sigue debe hablarle a esa audiencia exacta, nunca a una genérica.
3. **Productor — redacta la pieza:** hook (1-3s, curiosidad/tensión/relevancia real — módulo sección 3), cuerpo con el framework correcto para el pilar elegido (PAS/AIDA/BAB/hook-retain-reward), CTA explícita orientada al embudo real (comentario → DM, módulo sección 4 — nunca un CTA vago tipo "escríbeme"), hashtags en la mezcla 2-3/4-5/3-4 (módulo sección 5).
4. **Crítico — segunda pasada de LLM con prompt distinto (Reflection — Producer-Critic, cap. 4):**
   - ¿El hook genera curiosidad/tensión/relevancia real en los primeros segundos, o es genérico? Si es genérico, vuelve al Paso 3 — sin hook fuerte el resto de la pieza no importa (módulo sección 3).
   - ¿Alguna frase promete o garantiza un resultado concreto ("perderás X kg", "resultados garantizados")? No negociable por ley (Ley 34/1988, Directiva 2006/114/CE), igual que en `agentes/copywriter-comercial/`.
   - ¿El pilar es de prueba social/transformación? Si sí, ¿hay un `cliente_id` con consentimiento explícito confirmado por el coach? Sin eso, la pieza no puede citar ni insinuar un caso real — se reescribe en genérico o se descarta.
   - ¿El contenido habla realmente a la `audiencia_especifica` del nicho, o se ha genericado durante la redacción? Si se ha genericado, vuelve al Paso 3.
   - ¿Alguna afirmación de entrenamiento/nutrición contradice los módulos de conocimiento reales? → corrige o elimina, mismo criterio que los dos Copywriter.
   - **(v0.2.0) ¿La pieza cumple las políticas reales de plataforma, no solo el límite legal español?** — `modulos/tono-enfoque-ventas-redes.md` sección 7: ninguna autopercepción negativa, ningún "antes/después" con transformación implícita (incluido un testimonio en vídeo describiendo un "journey"), ningún primer plano de "zona problema", ninguna cifra/plazo concreto de cambio físico, y si se habla de un resultado de salud, el disclaimer literal exigido por Meta está presente. Aplica con más fuerza a los pilares de transformación y conversión directa — si algo lo incumple, vuelve al Paso 3, no se publica "total, es orgánico y no un anuncio pagado": el criterio del sistema aquí es más estricto que el mínimo de la plataforma, no igual a él.
4bis. **Brief visual y, si hay crédito, generación con Higgsfield:** el Productor escribe `brief_visual` siempre, sea cual sea el resultado de este paso. Antes de generar nada, comprobar crédito real disponible (`balance`) — con 60 créditos en plan básico, el criterio por defecto es reservar Higgsfield para el pilar de conversión directa y de transformación (las piezas con más impacto directo en el embudo), y dejar el brief como texto para que el coach lo resuelva a mano (foto propia, Pexels vía el mismo mecanismo que los Copywriter, o su propio criterio) en los pilares de educación/personalidad, que se generan con más frecuencia. **(v0.2.0) Imagen vs. vídeo:** por defecto, imagen estática (más barata, más piezas por el mismo crédito); vídeo vía Marketing Studio solo para la primera pieza de conversión directa del nicho activo, hasta confirmar el coste real en créditos de una generación — no asumir el precio de antemano. Nunca gasta crédito sin que quede constancia en `higgsfield_generado`/`higgsfield_asset_url` del borrador.
5. **Guarda el borrador** (`esquemas/post-borrador.schema.json`) con `estado: "borrador"` — nunca en un estado que sugiera que ya está listo para publicar.
6. **Notifica al coach** (mismo mecanismo que los dos Copywriter, `StaffAlertService`) indicando nicho, pilar y plataforma, para que sepa qué cuenta y qué tipo de revisión aplica.

## 5. Publicación — Human-in-the-Loop (cap. 13, no negociable)

Ninguna pieza se publica sola, en ninguna plataforma, bajo ningún concepto — no existe la integración para hacerlo aunque se quisiera, y aunque existiera, seguiría el mismo principio no negociable que ya rige para los dos Copywriter: el coach revisa y publica él mismo. Aquí el riesgo es además de imagen de marca en tiempo real y público (a diferencia de un blog, el contenido de redes es más difícil de corregir una vez publicado) — la pausa humana es, si acaso, más estricta aquí.

## 6. El experimento de nicho — cómo se decide el ganador

Este agente no decide el nicho ganador — solo produce las piezas y mantiene el registro que permite decidirlo con datos, no con impresión. Reglas explícitas:

- **La métrica de decisión declarada en `config-nicho.schema.json` (`metrica_decision`) debe incluir leads/contactos atribuidos, nunca solo alcance o interacciones.** Alcance sin conversión real no dice nada sobre cuál nicho "atrae más clientes potenciales", que es la pregunta real que el coach quiere responder.
- **Gap real, no resuelto por este diseño:** hoy no existe ningún CRM ni mecanismo automático para saber qué pieza o qué nicho generó un lead concreto. Mientras eso no exista, la atribución depende de que cada nicho tenga un `enlace_bio` propio y distinguible (`config-nicho.schema.json`), o de que el coach pregunte "¿cómo nos encontraste?" a cada nuevo contacto y lo registre a mano. Sin al menos uno de los dos, el experimento no podrá decidirse con datos reales — es responsabilidad del coach resolver esto antes de que termine la primera semana de piezas publicadas, no de este agente.
- **Al final de la ventana del experimento** (recomendado: 8 semanas, sección 2), el coach revisa `metricas_manuales` de todas las piezas de ambos nichos y marca `estado: "ganador"`/`"descartado"` en sus respectivos `config-nicho.schema.json`. A partir de ahí, este mismo agente sigue generando solo para el nicho ganador — no hace falta ningún cambio de diseño ni de agente.
- **(v0.2.0) Rigor mínimo antes de declarar un ganador:** cada nicho necesita al menos 8 piezas publicadas con `metricas_manuales` rellenas (aprox. una semana completa de calendario al ritmo por defecto) antes de que la comparación tenga algún valor — con menos, la diferencia entre nichos puede deberse al azar de una sola pieza viral o floja, no al nicho en sí. Si el coach quiere decidir antes de llegar a ese mínimo, este agente lo señala como decisión de baja confianza, no lo bloquea.

## 7. Manejo de excepciones

- **Ningún nicho tiene `estado: "activo"`** → no genera nada, lo reporta como excepción de negocio, no técnica.
- **El `positioning_statement` de un nicho está vacío o es genérico** ("ayudo a la gente a ponerse en forma") → no genera contenido para ese nicho hasta que el coach lo complete siguiendo la fórmula del módulo — un posicionamiento genérico invalida el propósito del experimento.
- **Higgsfield sin crédito suficiente** → no bloquea el ciclo: deja `higgsfield_generado: false` y el `brief_visual` como texto para que el coach lo resuelva por otra vía (sección 4bis).
- **El pilar elegido para hoy es de prueba social y no hay ningún cliente con consentimiento confirmado disponible** → salta al siguiente pilar del calendario en vez de forzar una pieza sin caso real.

### 7bis. Manejo de excepciones técnicas (Exception Handling and Recovery, cap. 12)

Ver `agentes/soporte-customer-success/modulos/manejo-excepciones-tecnicas.md` para el patrón completo. Aplicado aquí: si la llamada a Higgsfield falla, no se reintenta más de una vez en el mismo ciclo — se deja el brief como texto y se avisa al coach en la misma notificación del Paso 6, mismo criterio de baja urgencia que el resto de agentes de contenido.

## 8. Memoria (Memory Management, cap. 8)

No necesita memoria de cliente individual. Su memoria real son dos cosas: (1) el propio `config-nicho.schema.json` de cada nicho, que persiste el experimento en curso; (2) el histórico de `post-borrador.schema.json` ya generados por nicho, para no repetir pilar/ángulo en el mismo ciclo y para que el coach pueda rellenar `metricas_manuales` cuando la pieza ya esté publicada. Vive en este mismo repositorio de diseño (no hay dato de cliente individual que proteger, a diferencia de `bstronger-memoria-clientes`).

## 9. Asignación de modelo (Resource-Aware Optimization, cap. 16)

- **Selección de pilar (Paso 1):** determinista, sin modelo.
- **Productor (Paso 3):** modelo intermedio (Sonnet) — la redacción de copy de venta corta se beneficia de calidad de escritura, no de razonamiento extendido.
- **Crítico (Paso 4):** mismo modelo, prompt distinto — checklist de juicio (legal, consentimiento, especificidad), no requiere más capacidad.
- **Generación visual (Paso 4bis):** modelo/servicio propio de Higgsfield, no Claude — consultar `get_preset_instructions`/`models_explore` en el momento real de generar, nunca asumir un preset fijo de antemano (la oferta de Higgsfield cambia).

## 10. Notas de mantenimiento

- **Prerrequisitos operativos:** ninguno de WhatsApp/Twilio/n8n — este agente no depende de esa infraestructura, igual que Reporting y los dos Copywriter. El único prerrequisito real es de negocio: que el coach defina los dos `positioning_statement` iniciales y decida el `enlace_bio`/mecanismo de atribución de cada cuenta (sección 6) antes del primer ciclo.
- **Higgsfield es una integración real pero de capacidad limitada** (60 créditos, plan básico, verificado 2026-09-28) — el criterio de uso selectivo del Paso 4bis existe precisamente para no agotarla en piezas de bajo impacto. Si el volumen de contenido crece, revisar el plan antes de asumir que Higgsfield puede cubrir cada pieza.
- **Sin Control propio todavía.** El organigrama (`docs/ORGANIGRAMA_AGENTES.md`) sitúa a "Agente de Redes Sociales" en la misma área de contenido que los dos Copywriter — cuando este agente lleve ciclos reales corriendo, el candidato natural para auditarlo es ampliar el alcance de `agentes/control-contenido/` (que ya audita a los dos Copywriter juntos) en vez de diseñar un tercer Control de contenido separado. No se hace ahora — mismo criterio que Control Contenido: sin ciclos reales todavía, no hay nada real que auditar.
- **Coordinación con los dos Copywriter:** independientes entre sí (ninguno bloquea a otro), pero comparten los mismos tres principios no negociables — nunca prometer de más, nunca citar un caso real sin consentimiento, siempre revisión humana antes de publicar. Cualquier cambio a esos principios en uno debería revisarse en los otros dos.
- Cada cambio se refleja en el changelog de este documento, mismo criterio que el resto de agentes.
