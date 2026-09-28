# Organigrama completo de agentes — director, controles, operativos

> Documento de referencia arquitectónica, compartido por el usuario el 2026-09-27. Describe el organigrama completo al que el sistema podría escalar (nivel M2), y la secuencia de implementación recomendada para llegar ahí sin construir por completitud especulativa. **No implica que los 20 agentes se construyan ya** — el `docs/roadmap.md` (mesociclo actual: M1) sigue marcando el ritmo real: un agente operativo nuevo a la vez, priorizado por impacto en tiempo ahorrado, con su control correspondiente solo cuando el operativo ya funciona sin supervisión constante. Ver `docs/TAREAS_PENDIENTES.md` para qué agente concreto se está construyendo ahora mismo dentro de este organigrama.

## Contexto de negocio

- Servicio de asesoría de entrenamiento online profesional.
- Facturación real: **menos de 1.000€/mes** (el ejemplo de 10.000€/mes usado en el diseño original era solo para ilustrar la estructura completa; el objetivo es replicar el sistema con presupuesto ajustado).
- Objetivo: automatizar progresivamente las tareas de un equipo pequeño mediante agentes de IA, empezando por el agente que más tiempo consume hoy y escalando por fases.

---

## Estructura general (3 niveles)

1. **Agente director** — supervisión global del sistema.
2. **6 agentes de control** — uno por área, auditan a los agentes operativos de su área.
3. **13 agentes operativos** — ejecutan las tareas día a día. De estos, 3 ya existen y se diseñaron antes de este documento: el **Asistente de Programación de Entrenamiento**, el **Agente Importador de Programas** y el **Asistente de Programación de Nutrición** (área producto) — ver `docs/roadmap.md`, sección "Agentes existentes". Los 10 restantes son candidatos, no construidos todavía.

---

## Nivel 1 — Agente director

**Características:**
- Tono ejecutivo, orientado a resumen y priorización.
- No interactúa con clientes finales.
- Frecuencia de trabajo semanal (no tiempo real).

**Funciones:**
- Recopila los informes de los 6 agentes de control.
- Detecta patrones cruzados entre áreas (ej. quejas de soporte coincidiendo con una campaña de ads mal targetizada).
- Genera un resumen semanal con: alertas críticas, tendencias, recomendaciones.
- Escala al humano cuando un control reporta el mismo fallo 3+ veces seguidas.
- No corrige nada directamente — solo informa y prioriza.

---

## Nivel 2 — Agentes de control (uno por área)

### Control ventas
- **Características:** tono exigente pero justo; revisa contra guion de ventas y política de precios; acceso a transcripciones/logs del Closer y al CRM.
- **Funciones:** verifica que no se prometan resultados no garantizados; comprueba que precio/condiciones coincidan con la política vigente; revisa que los leads calientes no queden sin seguimiento +24h; marca conversaciones con riesgo de reclamación.

### Control soporte
- **Características:** sensible a tono emocional; prioriza detección de riesgo sobre precisión formal.
- **Funciones:** detecta respuestas genéricas que no responden a la pregunta real; identifica señales de posible baja (frustración, mención de "cancelar", falta de resultados); verifica tiempos de primera respuesta y tickets abandonados; revisa cumplimiento del proceso de onboarding.

### Control contenido
- **Características:** referencia = guía de marca/tono; revisa coherencia, no creatividad.
- **Funciones:** valida que el copy no tenga afirmaciones médicas/salud no verificadas; revisa consistencia de tono entre canales; comprueba que no se reciclen ideas recientes; verifica cumplimiento del calendario de publicación.

### Control producto (entrenamiento/nutrición)
- **Características:** el más sensible del sistema — errores afectan la salud del cliente; requiere supervisión humana obligatoria en casos límite.
- **Funciones:** revisa progresiones de carga/volumen peligrosas; verifica que los planes nutricionales no den consejos clínicos sin derivar a profesional; comprueba adaptación al nivel/objetivo del cliente; bloquea automáticamente outputs sobre medicación, suplementación de riesgo o restricciones calóricas extremas y deriva a revisión humana.

### Control operaciones
- **Características:** orientado a procesos, no a personas; revisa consistencia y cumplimiento de plazos.
- **Funciones:** verifica tareas administrativas al día; comprueba que los informes sean coherentes con datos reales (sin cifras inventadas); detecta tareas duplicadas/solapadas entre agentes; alerta si un agente lleva X horas sin actividad esperada.

### Control marketing
- **Características:** orientado a rendimiento y cumplimiento normativo (publicidad engañosa).
- **Funciones:** verifica que los anuncios cumplan políticas de plataforma y no prometan resultados poco realistas; revisa coherencia entre anuncio y producto; comprueba errores de personalización en email (nombres, links rotos); marca campañas con bajo rendimiento sostenido.

---

## Nivel 3 — Agentes operativos (13)

### Área ventas
- **Agente Closer/Ventas** — tono persuasivo no agresivo; conoce guion y objeciones. Cualifica leads, responde objeciones, agenda llamadas, hace seguimiento a los no cerrados, nunca cierra fuera de política de precios.
- **Agente de Leads/CRM** — analítico, sin contacto directo con cliente. Clasifica leads (frío/tibio/caliente), etiqueta en CRM, dispara secuencias de seguimiento, avisa al Closer de leads calientes desatendidos.

### Área soporte
- **Agente de Soporte/Customer Success** — empático, prioriza resolver, escala a humano en temas delicados. Responde dudas frecuentes, detecta señales de baja, sigue proactivamente a clientes inactivos.
- **Agente de Onboarding** — tono cercano y didáctico, opera solo en los primeros 7-14 días. Guía primeros pasos, envía recordatorios de bienvenida, alerta a soporte si el cliente no ha empezado.

### Área contenido
- **Agente Copywriter** — mantiene tono de marca, versátil entre formatos. Genera emails, textos de venta, guiones y posts; adapta el mismo mensaje a distintos canales.
- **Agente de Redes Sociales** — ya existe (diseñado 2026-09-28), ver `agentes/redes-sociales/system-prompt.md`. Conoce particularidades de cada plataforma. Propone calendario de contenido, adapta formato/duración, sugiere hooks, prepara descripciones y hashtags.
- **Agente de Edición/Producción** *(apoyo, no autónomo, requiere revisión humana)* — genera subtítulos, sugiere cortes/timestamps, propone descripciones de vídeo.

### Área producto
- **Agente Asistente de Programación de Entrenamientos** — ya existe, ver `agentes/programacion-entrenamiento/system-prompt.md`.
- **Agente Nutricional** — ya existe, ver `agentes/programacion-nutricion/system-prompt.md`.

### Área operaciones
- **Agente Administrativo/VA** — tareas repetitivas de bajo riesgo. Gestiona agenda, responde emails rutinarios, organiza documentos, recuerda pendientes.
- **Agente de Reporting** — solo trabaja con datos reales, nunca inventa cifras. Genera informes mensuales (ventas, churn, engagement), detecta variaciones relevantes mes a mes.

### Área marketing
- **Agente de Ads** — orientado a rendimiento, conoce políticas publicitarias. Sugiere variaciones de copy/creatividades, analiza rendimiento, alerta de campañas flojas.
- **Agente de Email Marketing** — trabaja con segmentación y automatización. Arma secuencias de nurturing, ajusta según apertura/clics, personaliza por segmento.

*(El Agente Importador de Programas no aparece en este organigrama por área de negocio porque es infraestructura técnica del área producto, no una función de negocio — sigue existiendo igual, ver `agentes/importador-programas/`.)*

---

## Flujo de comunicación entre niveles

**1. Log operativo → Control (cada acción)**

Cada agente operativo genera un registro estructurado por interacción:

```json
{
  "agente": "closer",
  "timestamp": "2026-09-14T10:32:00",
  "cliente_id": "xxxx",
  "accion": "resumen breve de qué hizo",
  "input_resumen": "qué pidió/dijo el cliente",
  "confianza": "alta/media/baja",
  "riesgo_detectado": null,
  "requiere_revision": false
}
```

El propio agente rellena `riesgo_detectado` cuando reconoce terreno delicado (promesa de resultado, salud, cliente enfadado) — así el control prioriza lo marcado en vez de auditar todo.

**2. Control → Director (informe semanal, resumen no logs en bruto)**

```json
{
  "area": "soporte",
  "periodo": "semana 37",
  "total_interacciones": 340,
  "auditadas": 45,
  "incidencias_bajas": 3,
  "incidencias_altas": 1,
  "detalle_incidencias_altas": ["..."],
  "tendencia": "aumento de quejas sobre tiempos de respuesta"
}
```

**3. Reglas de escalación**

- **Riesgo bajo** (tono raro, respuesta mejorable): el control corrige o pide reintento, queda en el log, no sube al director.
- **Riesgo alto** (salud, dinero, reclamación, promesa indebida): salta directo a **humano**, sin esperar al informe semanal; el director solo recibe la notificación.
- **Patrón repetido** (3+ incidencias del mismo tipo en una semana): el control lo marca "sistémico" y entra en el resumen semanal del director como punto a decidir (cambiar prompt, cambiar proceso, etc.).

Flujo de decisión por acción: `Acción del operativo → Log automático (JSON) → Control audita (muestreo + casos marcados) → [Todo correcto | Riesgo bajo: corrige | Riesgo alto: escala → Director/humano]`

---

## Stack técnico por presupuesto real (<1.000€/mes de facturación)

**Nivel 0 — Sin coste / mínimo coste (para empezar, = infraestructura de M1)**
- **n8n** (self-hosted gratis, o Cloud starter ~20€/mes) — orquestador que conecta los agentes, dispara logs y gestiona la lógica de escalación.
- **Google Sheets** como base de datos de logs, sin coste.
- **API de Claude o GPT (pago por uso)** — con este volumen, el gasto en tokens para varios agentes operativos suele rondar 20-60€/mes.
- **WhatsApp Business API vía Twilio (pago por uso)** o gestión manual de IG/WhatsApp si el volumen es bajo.

**Nivel 1 — Cuando haya ingresos recurrentes más estables (~500-1.000€/mes, = infraestructura de M2)**
- **Make (Integromat)** como alternativa a n8n self-hosted si se prefiere menos mantenimiento técnico (~9-16€/mes).
- **Airtable** en vez de Sheets cuando crece el volumen de datos.
- **Notion** como panel de control para que el director escriba ahí el resumen semanal.

**Lo que NO hace falta todavía**
- Frameworks de agentes complejos (LangGraph, CrewAI): añaden fricción sin beneficio real con este volumen.
- Bases de datos vectoriales, servidores dedicados, ni coste fijo mensual alto.

---

## Secuencia de implementación recomendada

1. Montar **1 solo agente operativo** — el que más tiempo consume hoy — conectado por n8n a la API de Claude/GPT.
2. Añadir su **agente de control** correspondiente solo cuando el operativo funcione sin supervisión constante.
3. El **agente director** puede sustituirse por revisión manual (leer el Sheet/Airtable una vez a la semana) hasta tener 3+ controles activos.
4. Repetir el proceso agente por agente, priorizando por impacto en tiempo ahorrado, no por completitud del organigrama.

**(2026-09-27) Primer agente operativo nuevo priorizado: Soporte/Onboarding** — ver `docs/TAREAS_PENDIENTES.md` y `agentes/` para el diseño en curso.

**(2026-09-27) Segundo: Agente de Onboarding**, diseñado justo después de Soporte por ser su pareja natural en esta misma área y reutilizar casi toda su infraestructura — ver `agentes/onboarding-cliente-nuevo/system-prompt.md`.

**Antes de diseñar el tercero**, seguir `docs/METODOLOGIA_DISENO_AGENTES.md` — el proceso real (no teórico) extraído de cómo se diseñaron los 5 agentes existentes, fase por fase: investigar el código real primero, investigar la práctica del sector cuando aplique, aislar qué decisiones son del usuario, aplicar los patrones reales del libro (no solo citarlos), comprobar solapamiento con agentes existentes, y sincronizar la documentación en el orden correcto.

**(2026-09-27) Tercero: Agente de Reporting**, elegido tras aplicar la Fase 0-1 de `docs/METODOLOGIA_DISENO_AGENTES.md` a los 10 candidatos restantes: es el único con datos e infraestructura reales que reportar hoy (`Subscription`, `client-session-feedback`, `task-list`, `GET dashboard` ya existente) — ver `agentes/reporting/system-prompt.md`. El resto de candidatos de ventas/contenido/marketing quedan documentados como no diseñables todavía en `docs/TAREAS_PENDIENTES.md` — ninguno tiene una integración real en Bckbs (CRM, email marketing, ads, redes) que investigar, y diseñarlos ahora significaría inventarla.

**(2026-09-28) Cuarto: Agente Copywriter**, a petición explícita del usuario tras corregirse el descarte inicial: investigando más a fondo apareció un blog interno completo y ya usado en Bckbs (`Post`/`BlogCategory`/`AdminPostController`, 3 categorías reales) — ver `agentes/copywriter/system-prompt.md`. Alcance reencuadrado respecto a la descripción original del organigrama (emails/ventas/multicanal, sin integración real) a lo único con base real: artículos educativos para ese blog in-app, con publicación siempre sujeta a revisión humana. Redes Sociales, Ads y Email Marketing siguen sin ninguna integración real — se mantienen sin diseñar.

**(2026-09-28) Quinto: Agente Copywriter Comercial**, a petición del usuario al identificar que el blog de la app y el de la web pública (`webbs`) estaban totalmente sincronizados, sin distinguir contenido educativo de contenido de captación. Requirió primero un cambio real de backend (`channel` en `posts`, Bckbs commit `70300b8`) — ver `agentes/copywriter-comercial/system-prompt.md`. Diseñado como agente hermano del Copywriter, no una variante: mismo patrón Productor/Crítico, pero objetivo (captar, no educar), estructura (siempre CTA en el contenido de captación) y riesgo (promesas de resultado, precio) distintos, con los guardrails de "Control ventas"/"Control marketing" (niveles todavía sin agente propio) incorporados directamente en el Crítico — incluyendo, tras una segunda ronda de investigación pedida por el usuario, su base legal real (Ley 34/1988 General de Publicidad, Directiva 2006/114/CE). Esa misma ronda añadió al Copywriter educativo un límite regulatorio equivalente para declaraciones de salud/nutrición (Reglamento 1924/2006).

**(2026-09-28) Primer agente de Control: Control Contenido**, a petición explícita del usuario, junto con el cierre del gap de portada de ambos Copywriter (Pexels API, gratis, sin atribución obligatoria — ver `agentes/copywriter/CHANGELOG.md` v0.4.0 para la investigación completa). Decisión de alcance real en vez de seguir el organigrama al pie de la letra: "Control ventas"/"Control marketing" no tienen ningún operativo real que auditar hoy (sin Closer/CRM/Ads/Email Marketing), así que este Control audita a los dos Copywriter juntos y absorbe el chequeo legal/comercial del Comercial — ver `agentes/control-contenido/system-prompt.md`. Es el primer punto del proyecto donde un agente compara la salida de otros dos entre sí (Multi-Agent Collaboration, cap. 7), sin ningún backend nuevo (`GET admin/posts`, ya existente). **Tensión con la "Secuencia de implementación recomendada" de este mismo documento, documentada explícitamente:** ese criterio dice que un Control se añade solo cuando el operativo funciona sin supervisión constante — ni el Copywriter ni el Comercial han corrido todavía un ciclo real. Se diseña igualmente a petición del usuario, marcado "no activar todavía" en su propio documento hasta que ambos completen 2 ciclos reales cada uno.

**(2026-09-28) Segundo agente de Control: Control Producto (entrenamiento)**, a petición del usuario tras reportar que las programaciones no muestran progresión real de series/reps/carga durante 5-6 meses de macrociclo. Dos correcciones distintas para dos problemas distintos: el síntoma mecánico (el plan escrito no varía respecto a sí mismo) se resolvió directamente en `agentes/programacion-entrenamiento/validador/validar_programa.py` v0.6.0, sin agente nuevo — es una comprobación de código, no de juicio. El problema de fondo (el plan no se ajusta según lo que el cliente hace de verdad en el gimnasio) sí justificó un agente nuevo — ver `agentes/control-producto/system-prompt.md`. Investigado antes de diseñar: `GET client-exercise-history`, `GET client-muscle-volume` y `GET client-session-feedback` de Bckbs ya exponen peso/reps/RIR reales y adherencia real, sin backend nuevo. **A diferencia de Control Contenido, este SÍ es activable ya**: el área producto (Asistente de Programación de Entrenamiento) lleva meses de entregas reales — cumple mejor que cualquier otra área el criterio de la Secuencia de implementación recomendada. Reconciliación obligatoria, no un bloqueo ciego: el Productor sigue la recomendación (subir/mantener/bajar) o justifica la desviación citando su propia jerarquía universal; el Crítico audita que ninguna quede sin justificar — mismo principio de separación de roles (Reflection, cap. 4) que ya usa el patrón Producer-Critic del resto del sistema, aplicado aquí a juzgar resultados reales en vez del propio borrador. Alcance de esta versión: solo entrenamiento, no nutrición (el organigrama original agrupa ambos bajo el mismo Control) — sin señal real todavía de que la nutrición tenga el mismo problema.

**(2026-09-28) Sexto agente operativo: Redes Sociales**, a petición del usuario, que quería contenido para redes pero todavía no ha decidido el nicho definitivo — planteó dos agentes, uno por nicho, y quedarse con el que atraiga más clientes. Se diseñó **un solo agente parametrizado por nicho** en su lugar (razonamiento completo en `agentes/redes-sociales/system-prompt.md` sección 1): dos nichos de captación del mismo negocio comparten casi todo el mecanismo real, a diferencia de Copywriter vs. Copywriter Comercial, que sí tienen objetivo/riesgo legal distintos y por eso siguen siendo agentes separados. Investigación de mercado real antes de diseñar (especificidad de nicho, pilares de contenido, frameworks PAS/AIDA/BAB, embudo de conversión) volcada en `agentes/redes-sociales/modulos/tono-enfoque-ventas-redes.md`. **Corrige la nota de este mismo documento sobre "Redes Sociales sin integración real":** sí existe una integración real de generación visual — la cuenta de Higgsfield conectada a esta sesión (60 créditos, plan básico, verificado) — aunque la publicación sigue siendo 100% manual, igual que ya se documentó para Ads/Email Marketing/Redes Sociales en general (ninguna plataforma tiene API de publicación integrada). Gap real sin resolver: sin CRM, atribuir qué nicho generó qué lead depende de que el coach use un enlace de bio distinto por cuenta o pregunte "cómo nos encontraste" — documentado como responsabilidad suya, no del agente.
