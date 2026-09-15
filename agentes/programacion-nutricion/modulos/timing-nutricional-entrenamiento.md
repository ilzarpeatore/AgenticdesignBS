# Módulo: Timing nutricional alrededor del entrenamiento

**Tipo:** General
**Se activa cuando:** siempre — es el módulo que materializa la coordinación con el entrenamiento real del cliente (`system-prompt.md`, Paso 1, apartado 1; Multi-Agent Collaboration, cap. 7). Sin esto, "coordinar con el entrenamiento" queda en declaración de intenciones.
**Versión:** 0.1.0 · **Última actualización:** 2026-09-15
**Procedencia:** deep search de meta-análisis sobre timing de proteína/carbohidrato y guías de hidratación (ACSM) — ver referencias al final.

## 1. No existe una "ventana anabólica" estrecha — no diseñes el plan alrededor de ese mito

La revisión de referencia (Aragon & Schoenfeld) y el meta-análisis posterior (Schoenfeld, Aragon et al.) concluyen que **la ventana real es de 4-6 horas alrededor de la sesión**, no los 30-60 minutos que popularizó el mito de la "ventana anabólica". La cantidad total de proteína diaria explica casi toda la varianza en los resultados — el momento exacto de la toma pre/post entreno tiene un efecto independiente limitado si el total diario ya es adecuado.

**Implicación operativa:** no fuerces una toma de proteína inmediatamente post-entreno si no encaja con la disponibilidad/preferencias del cliente — es más importante que la comida más cercana a la sesión (dentro de esa ventana de 4-6h) tenga una ración adecuada, y que el total diario (`necesidades-energeticas-macronutrientes.md`) se cumpla, que perseguir el minuto exacto.

*(Aragon, A.A. & Schoenfeld, B.J., 2013. Nutrient timing revisited: is there a post-exercise anabolic window? Journal of the International Society of Sports Nutrition. Schoenfeld, B.J., Aragon, A.A. & Krieger, J.W., 2013. The effect of protein timing on muscle strength and hypertrophy: a meta-analysis.)*

## 2. Distribución de proteína a lo largo del día

- **Umbral por toma:** ~0.4 g/kg de proteína de calidad por comida maximiza la respuesta de síntesis proteica muscular; por debajo de ~0.25 g/kg por toma, el estímulo es notablemente menor.
- **Reparto práctico:** repartir la proteína diaria (`necesidades-energeticas-macronutrientes.md`, sección 2) en **al menos 4 tomas de ~0.4 g/kg** cubre bien el objetivo diario sin depender de una única comida grande. 3 tomas bien dosificadas también funcionan si encajan mejor con la disponibilidad del cliente — el reparto exacto es una decisión de adherencia (jerarquía universal, punto 4), no una regla rígida.
- Al menos **una** comida del día debe alcanzar el umbral de ~0.4 g/kg, incluso si el resto del reparto es más irregular por el horario real del cliente.

*(Areta, J.L., et al. y revisiones sobre dosis-respuesta de síntesis proteica muscular por toma; revisiones sobre distribución de proteína y resultados musculares.)*

## 3. Carbohidrato según el tipo de día (periodización simple)

No es necesario un sistema de periodización de carbohidrato tan fino como el de un atleta de resistencia de competición (eso vive en `running-economia-carrera.md` del agente de entrenamiento para quien lo necesite). Para el cliente de gimnasio/fuerza habitual:

- **Días de entrenamiento (especialmente de mayor volumen/intensidad):** situar el carbohidrato diario (`necesidades-energeticas-macronutrientes.md`, sección 4) en la parte alta del rango calculado, priorizando su presencia en las comidas cercanas a la sesión (antes y en la ventana de 4-6h post).
- **Días de descanso:** puede bajar hacia la parte baja del rango calculado, redistribuyendo esas calorías hacia grasa si el objetivo calórico total debe mantenerse igual.
- **Sesiones largas o de alta intensidad (>60 min):** 1-4 g/kg de carbohidrato en las 1-4h previas ayuda a sostener el rendimiento de la sesión — relevante sobre todo si el cliente entrena en ayunas o con poco margen desde la última comida.

**Coordinación real con el entrenamiento (no genérica):** este ajuste debe basarse en lo que el Productor del agente de entrenamiento indicó para esa semana/sesión (tipo de sesión, volumen, si es semana de deload) — un deload no necesita el mismo carbohidrato "de rendimiento" que una semana de acumulación de volumen.

*(Gatorade Sports Science Institute; guías de carbohidrato pre-ejercicio para sesiones >60 min.)*

## 4. Hidratación

- **Antes:** ~500 ml de líquido unas 2 horas antes de la sesión, para empezar euhidratado.
- **Durante:** beber a intervalos regulares para reponer lo perdido por sudor, sin superar el 2% de pérdida de peso corporal por deshidratación. La variabilidad de sudoración entre personas es alta — si es relevante para el cliente (sesiones largas, calor), estimar la tasa de sudor real (peso antes/después de una sesión) es más útil que una cifra genérica.
- **Electrolitos:** relevantes en sesiones de más de 1 hora — el sodio es el electrolito dominante en el sudor (~900 mg/L de media), muy por encima de potasio (~200 mg/L) y magnesio (~8 mg/L). Para sesiones de gimnasio habituales (<60 min, intensidad moderada) esto no suele requerir más que agua; para sesiones largas o con sudoración muy abundante, considerar reposición de sodio.

*(American College of Sports Medicine, Position Stand: Exercise and Fluid Replacement.)*

## Conflictos conocidos con otros módulos

- **Con `necesidades-energeticas-macronutrientes.md`:** este módulo distribuye en el tiempo los totales diarios que fija ese módulo — no son dos fuentes de verdad distintas sobre "cuánto", solo sobre "cuándo".
- **Con `alergias-intolerancias.md`:** cualquier reparto de comidas debe respetar las exclusiones de seguridad antes que la distribución "ideal" — una toma post-entreno sin fuente de proteína seguro disponible se resuelve buscando alternativa, no relajando la exclusión.
- **Con el agente de entrenamiento (Paso 1, apartado 1 del `system-prompt.md`):** la periodización de carbohidrato de la sección 3 depende de leer el tipo de sesión real, no de asumir "día de entrenamiento genérico" — si esa información no está disponible, señálalo antes de fijar el reparto en vez de asumir intensidad media.

## Referencias

- Aragon, A.A. & Schoenfeld, B.J. (2013). *Nutrient timing revisited: is there a post-exercise anabolic window?* Journal of the International Society of Sports Nutrition.
- Schoenfeld, B.J., Aragon, A.A. & Krieger, J.W. (2013). *The effect of protein timing on muscle strength and hypertrophy: a meta-analysis.* Journal of the International Society of Sports Nutrition.
- Revisiones sobre dosis-respuesta de síntesis proteica muscular por toma y distribución de proteína a lo largo del día.
- Gatorade Sports Science Institute. *Dietary Carbohydrate and the Endurance Athlete.*
- American College of Sports Medicine (ACSM). *Position Stand: Exercise and Fluid Replacement.*
