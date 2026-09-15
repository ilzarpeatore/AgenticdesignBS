# Módulo: Rendimiento deportivo y resistencia

**Tipo:** Específico
**Se activa cuando:** el cliente entrena o compite en una actividad de resistencia (running, ciclismo, triatlón...) y el objetivo nutricional prioritario es el rendimiento en esa actividad — no un cliente de gimnasio genérico que además hace algo de cardio. Coordina con `running-economia-carrera.md` del Asistente de Programación de Entrenamiento si el cliente corre/compite en fondo.
**Versión:** 0.1.0 · **Última actualización:** 2026-09-15
**Procedencia:** deep search de guías de carga de carbohidrato y fueling de competición — ver referencias al final. Complementa, sin repetir, la nota de `necesidades-energeticas-macronutrientes.md` sección 4 de que las cifras de endurance (6-10 g/kg/día) no se aplican por defecto a un cliente de fuerza sin este perfil.

## 1. Carga de carbohidrato antes de un evento (>90 minutos)

- **Protocolo estándar:** 8-12 g/kg/día de carbohidrato durante 1-3 días antes del evento, combinado con reducción de la carga de entrenamiento (taper) — coordina esto con la fase de taper que ya programa `periodizacion-orientada-evento.md` del agente de entrenamiento, no lo trates como un ajuste nutricional aislado.
- **Deportistas ya entrenados:** no hace falta la "fase de depleción" clásica (agotar glucógeno antes de cargar) — pueden ir directos a la fase de carga alta en carbohidrato con volumen de entrenamiento bajo.
- Solo tiene sentido para eventos de **más de 90 minutos** — no apliques carga de carbohidrato antes de una sesión o competición corta, no aporta beneficio y puede generar malestar digestivo innecesario.

*(Guías de carbohidrato para deportistas de resistencia; revisiones sobre protocolos de carga de carbohidrato.)*

## 2. Fueling antes del evento (día de la prueba)

- **1-4 horas antes:** 1-4 g/kg de carbohidrato — cantidad más conservadora cuanto más cerca del inicio, para evitar malestar digestivo.
- No pruebes nada nuevo el día del evento — cualquier estrategia de fueling debe haberse ensayado antes, en sesiones de entrenamiento largas equivalentes (esto es una regla de gestión de riesgo, no solo de rendimiento).

## 3. Fueling durante el evento

- **30-60 g de carbohidrato por hora** para eventos largos, empezando pronto (a los 60-90 minutos, no esperar a notar fatiga) — empezar tarde reduce el beneficio incluso si la cantidad total es correcta.
- Para intensidades muy altas o eventos muy largos, tasas más altas (>60 g/h) requieren mezclas de carbohidratos con distintos transportadores intestinales (glucosa+fructosa) para poder absorberse sin malestar — no subas la cantidad de un solo tipo de carbohidrato esperando más beneficio, el cuello de botella es la absorción, no la disponibilidad.
- Hidratación y electrolitos durante el evento: ver `timing-nutricional-entrenamiento.md`, sección 4 — las cifras de sodio en sudor son especialmente relevantes aquí, a diferencia de una sesión de gimnasio corta.

*(Gatorade Sports Science Institute; revisiones sobre estrategias de fueling en competición y absorción de carbohidratos mixtos.)*

## 4. Beneficio esperado y expectativas realistas

La carga de carbohidrato y el fueling correcto durante el evento se asocian a mejoras de rendimiento del orden de 2-3% — relevante en competición, pero no una transformación radical. Comunica esto como una optimización sobre una base de entrenamiento sólida, no como sustituto de ella.

## Conflictos conocidos con otros módulos

- **Con `necesidades-energeticas-macronutrientes.md`:** este módulo sustituye temporalmente el rango de carbohidrato de ese módulo en los días cercanos al evento — no es un conflicto, es una excepción programada y con fecha de fin.
- **Con `periodizacion-orientada-evento.md` (agente de entrenamiento):** el taper de entrenamiento y la carga de carbohidrato deben coordinarse en el tiempo — ambos módulos reducen la carga de entrenamiento/aumentan el carbohidrato en la misma ventana final antes del evento.
- **Con `timing-nutricional-entrenamiento.md`:** la hidratación/electrolitos durante el evento usa las mismas cifras de ese módulo, con mayor relevancia práctica dado la duración.
- **Con `running-economia-carrera.md` (agente de entrenamiento):** si el cliente corre/compite en fondo, ese módulo gestiona la actividad principal en sí; este módulo gestiona la nutrición alrededor de ella. No se solapan, se complementan.

## Referencias

- Gatorade Sports Science Institute. *Dietary Carbohydrate and the Endurance Athlete.*
- Revisiones sobre protocolos de carga de carbohidrato (carbohydrate loading) y su evolución desde el protocolo clásico de depleción.
- Guías de fueling pre-evento e intra-evento para deportes de resistencia — tasas de carbohidrato por hora y mezclas de carbohidratos múltiples para maximizar absorción.
