# Módulo — Tono y enfoque de venta en redes

**Versión:** 0.1.0
**Última actualización:** 2026-09-28
**Procedencia:** investigación de mercado real (fuentes al final), pedida explícitamente por el usuario antes de diseñar el agente — "necesito que eduques bien con información al agente para que identifique el tipo de contenido a crear". Compartido por los dos nichos activos del experimento (`esquemas/config-nicho.schema.json`): el mecanismo de este módulo es el mismo para ambos, solo cambia la audiencia y el `positioning_statement` de cada uno.

## 1. Especificidad de nicho, no de servicio

El hallazgo más repetido en la investigación: la especificidad de audiencia predice el rendimiento mejor que cualquier otra variable de contenido. "Ayudo a profesionales ocupados de +40 a ganar fuerza sin pasar horas en el gimnasio" supera a "soy entrenador personal" en cualquier algoritmo y en la cabeza de cualquier cliente potencial — un entrenador que habla directamente a "padres de 35 años que quieren perder 20kg sin renunciar a su vida social" siempre rinde mejor que uno cuyo contenido apunta a "cualquiera que quiera ponerse en forma".

**Fórmula obligatoria de posicionamiento** (`positioning_statement` en `config-nicho.schema.json`, un campo, no una idea suelta): "Ayudo a [audiencia específica] a lograr [objetivo específico] mediante [método/enfoque propio]". Un nicho sin esta frase completa y concreta no está listo para generar contenido — el Productor la exige como precondición (Paso 1).

## 2. Pilares de contenido (rotación fija, 3-5 temas)

Un pilar de contenido es un tema recurrente que se repite en un calendario fijo en vez de partir de cero cada vez — el algoritmo de las plataformas de formato corto depende de la consistencia temática para la distribución, tanto como del contenido en sí.

Pilares por defecto de este agente (ajustables por nicho, nunca menos de 3 ni más de 5):

1. **Educación/autoridad** — un concepto real de entrenamiento/nutrición explicado con precisión (grounded en los módulos de conocimiento de `agentes/programacion-entrenamiento/modulos/` y `agentes/programacion-nutricion/modulos/`, nunca inventado).
2. **Prueba social/transformación** — solo con datos de un cliente real que haya dado consentimiento explícito confirmado por el coach (mismo guardrail ya usado por los dos Copywriter); sin eso, contenido genérico sin atribución a nadie identificable.
3. **Conexión/personalidad** — por qué este método, autenticidad real del coach (programa, PRs, contratiempos, recuperación) — la investigación señala la autenticidad de quien demuestra lo que predica como un factor real de conversión, no solo de simpatía.
4. **Conversión directa** — oferta y llamada a la acción explícitas.

**Énfasis por plataforma** (mismos 4 pilares, la mezcla cambia): Instagram Reels premia más el pilar educativo y el de prueba social que TikTok — los guardados ("saves") son una señal de ranking real, y el contenido que se guarda tiende a ser práctico y específico. TikTok premia más el pilar de personalidad y lo que está en tendencia. Por defecto: en Instagram, más peso a 1 y 2; en TikTok, más peso a 3.

## 3. Framework de copy por tipo de pieza (`framework_usado` en `post-borrador.schema.json`)

No hay un único framework — mezclar frameworks dentro del mismo embudo es señal de madurez, no de inconsistencia:

- **Hook (primeros 1-3 segundos, toda pieza sin excepción):** debe crear curiosidad, tensión o relevancia inmediata. Sin hook fuerte, el resto de la pieza no importa — es lo primero que el Crítico revisa (Paso 4bis).
- **Pilar educativo (1):** estructura hook → retención (contenido real, útil, específico) → recompensa (una idea aplicable, no un teaser vacío).
- **Pilar de conversión directa (4):** PAS (Problema → Agitar → Solución) — nombrar la frustración real del nicho, mostrar la consecuencia de no resolverla, presentar el servicio como la respuesta concreta — o AIDA (Atención → Interés → Deseo → Acción) cuando la pieza es más una pieza de anuncio que de contenido orgánico. PAS rinde mejor en formato corto/orgánico; AIDA encaja mejor si la pieza se promociona como anuncio pagado.
- **Pilar de transformación (2):** BAB (Before → After → Bridge) — el antes real del cliente, el después real, el método como puente entre ambos.

Aplicado al nicho de entrenamiento: la frustración a nombrar nunca es genérica ("ponerse en forma") sino la del `positioning_statement` de ese nicho en concreto (falta de motivación, progreso lento, dificultad para mantener la constancia son los tres patrones reales más citados) — nunca un dolor inventado que no encaje con la audiencia declarada.

## 4. Embudo real de conversión (para diseñar el CTA de cada pieza, no para automatizar nada — no hay integración de DM real)

Contenido (Reels/posts) → captura (comentario → DM) → cualificación (guion de DM) → conversión (llamada de descubrimiento) → retención. Los CTA de este agente están pensados para alimentar ese embudo manual: "comenta 'X' y te mando el enlace/guía" rinde mejor que un genérico "escríbeme" porque da al coach una señal clara de qué pieza generó el contacto — importante para el propio experimento de nicho (sección 6 del system-prompt), ya que hoy no existe ningún CRM que lo haga automáticamente.

## 5. Hashtags

El descubrimiento por interés/palabra clave pesa más que el hashtag genérico, pero la mezcla recomendada sigue siendo real: 2-3 hashtags amplios (la categoría, ej. `#entrenamientopersonal`), 4-5 de nivel medio (el nicho, ej. `#fuerzadespuesde40`), 3-4 muy específicos de nicho (la audiencia exacta del `positioning_statement`).

## 6. Formato y plataformas

Reels/shorts de 30-60 segundos; Instagram, TikTok y YouTube son las tres plataformas con más tracción para este tipo de contenido. Este agente diseña para las tres con el mismo guion base, ajustando solo énfasis de pilar (sección 2) y tono (TikTok más informal/personal, Instagram más práctico/educativo).

## Fuentes

- [Fitness Coach Instagram Content Ideas: 2026 Marketing Guide — FitBudd](https://www.fitbudd.com/academy/fitness-coach-instagram-content-ideas-guide-to-marketing-for-professionals-2026)
- [Instagram Funnel for Fitness Coaches: 2026 Playbook — Creatorflow](https://creatorflow.so/blog/instagram-funnel-fitness-coaches/)
- [Content Pillar Strategy for Short-Form Creators in 2026 — Miraflow](https://miraflow.ai/blog/content-pillar-strategy-short-form-creators-2026)
- [Social Media Content Strategy for 2026: Frameworks, Formats & Models — Teknon](https://www.teknon.io/blog/social-media-content-strategy-2026)
- [DTC Brand Instagram Strategy: How to Drive Sales in 2026 — Creatorflow](https://creatorflow.so/blog/dtc-instagram-strategy-2026/)
- [Crazy conversion hack: PAS copywriting framework — Shyam Govind](https://shyamgovind.com/blogs/pas-copywriting-framework/)
- [AIDA vs PAS vs BAB: Best Copywriting Frameworks for 2026 — SwiftCopy](https://swiftcopy.io/blog/aida-pas-bab-copywriting-frameworks)
- [13 fitness influencers coaches should study in 2026 — Coachway](https://coachway.io/articles/fitness-influencers-coaches-should-study/)
- [How to Start Online Fitness Coaching (2026) — SetSmart](https://setsmart.io/blog/how-to-start-online-fitness-coaching)
