# Módulo: Necesidades energéticas y macronutrientes

**Tipo:** General
**Se activa cuando:** siempre — es la base sobre la que se apoya cualquier otro módulo de este agente (timing, recomposición, rendimiento). Sin esto no hay forma de dimensionar ningún plan.
**Versión:** 0.2.0 · **Última actualización:** 2026-09-15
**Procedencia:** deep search de posicionamientos de sociedades científicas (ISSN, ACSM) y meta-análisis recientes — ver referencias al final. v0.2.0: confirmado que coincide con la implementación real de Bckbs (`app/Traits/DailyPlanTrait.php::calculateDailyPlan()`), no es una elección teórica sin conexión con el sistema de producción — ver `formato-salida/entrega-bckbs.md`.

## 1. Estimación del gasto energético total (GET/TDEE)

- **Metabolismo basal (BMR):** ecuación de Mifflin-St Jeor — `(10 × peso_kg) + (6.25 × altura_cm) − (5 × edad) + 5` (hombres) o `−161` (mujeres en vez de `+5`). Es la ecuación con menor margen de error de las disponibles sin calorimetría (~5%, frente a 10-15% de ecuaciones más antiguas como Harris-Benedict) — úsala como estimación por defecto, no como valor exacto. **Es literalmente la que ya usa Bckbs en producción** (`DailyPlanTrait::calculateDailyPlan()`, comentario `// BMR (Mifflin-St Jeor)`).
- **Factor de actividad:** multiplica el BMR por 1.2 (sedentario) a 1.9 (extremadamente activo) según la actividad fuera del entrenamiento programado, no solo las sesiones — un cliente con trabajo físico exigente necesita un factor mayor que uno con trabajo de oficina, aunque entrenen lo mismo. Coincide exactamente con `config('macro-nutrient.ACTIVITY_LEVEL')` en Bckbs — usa esas claves (`sedentary`, `lightly_active`, `moderate`, `very_active`, `athlete`) al fijar el perfil del cliente, no una escala inventada.
- **Esto es un punto de partida, no una prescripción cerrada:** ajusta según la respuesta real del cliente (peso/composición corporal a lo largo de 2-3 semanas), no persigas el número teórico si los datos reales dicen otra cosa.

*(Mifflin, M.D., et al., 1990; comparativas de precisión de ecuaciones de metabolismo basal)*

## 2. Proteína

Rango general para adultos que entrenan (ISSN Position Stand): **1.4-2.0 g/kg/día** es suficiente para la mayoría. Matices por contexto:

- **Fuerza/potencia:** 1.6-2.0 g/kg/día.
- **Resistencia (endurance):** 1.0-1.6 g/kg/día, según intensidad/duración y nivel de entrenamiento — más bajo que fuerza porque el estímulo de síntesis proteica es menor, aunque el gasto energético total pueda ser mayor.
- **En déficit calórico (retener masa magra):** 2.3-3.1 g/kg/día — ver también `recomposicion-corporal-nutricion.md`, que ya usa este rango para dimensionar el déficit.
- **Por ración:** ~0.25-0.4 g/kg de proteína de calidad por toma, o una dosis absoluta de 20-40 g — ver `timing-nutricional-entrenamiento.md` para cómo repartirlo a lo largo del día.

*(Jäger, R., et al., 2017. International Society of Sports Nutrition Position Stand: protein and exercise. Journal of the International Society of Sports Nutrition.)*

## 3. Grasas

- **Mínimo por salud hormonal:** no bajar de 0.5-1 g/kg/día, ni de ~20% de las calorías totales — bajar de este umbral se asocia a alteraciones hormonales (incluyendo el ciclo menstrual en mujeres) incluso sin llegar a un contexto de RED-S declarado.
- **Rango general:** 20-35% de las calorías totales. No uses la grasa como la variable que se recorta primero para "hacer sitio" a más proteína o carbohidrato sin comprobar que sigue por encima del mínimo.

*(Revisiones sobre ingesta de grasa en atletas y salud hormonal; scoping review de sociedades expertas sobre manipulación de composición corporal)*

## 4. Carbohidratos

- Se calculan **por diferencia** una vez fijadas proteína y grasa, ajustados después según la demanda real de entrenamiento — ver `timing-nutricional-entrenamiento.md` para la periodización por día de entrenamiento vs. descanso.
- Para contexto de resistencia/endurance de intensidad moderada-alta: 6-10 g/kg/día como referencia de sociedades deportivas — **esta cifra es para deportistas de resistencia, no la apliques por defecto a un cliente de gimnasio que hace fuerza sin volumen de resistencia relevante** (ver `running-economia-carrera.md` del agente de entrenamiento si el cliente sí corre/compite en fondo).

*(Gatorade Sports Science Institute, revisión sobre carbohidrato en atletas de resistencia; guías de periodización de carbohidrato)*

**Traducción a los presets reales de Bckbs (`config('macro-nutrient.MACRO_RATIO')`):** una vez fijados los gramos de proteína (sección 2) y grasa (sección 3), conviértelos a % de calorías totales y compara con los presets ya disponibles (`balanced` 40/30/30 carbs/proteína/grasa, `low_fat` 40/40/20, `high_protein` 20/50/30, `high_carb` 55/25/20, `keto` 5/25/70) — usa el que más se acerque, o `macro_type: custom` con `protein_pct`/`carbs_pct`/`fat_pct` exactos si ninguno encaja bien. No inventes un sexto preset ni lo dejes en gramos sueltos sin traducir a lo que el sistema real espera.

## 5. Umbral de seguridad: disponibilidad energética (Low Energy Availability / RED-S)

Disponibilidad energética = (ingesta calórica − gasto energético del ejercicio) / masa libre de grasa (kg).

| Disponibilidad energética | Interpretación |
|---|---|
| >45 kcal/kg FFM/día | Sostiene ganancia de peso y función fisiológica normal |
| ~45 kcal/kg FFM/día | Óptimo para mantenimiento de peso y función normal |
| 30-45 kcal/kg FFM/día | Subóptimo — riesgo de función fisiológica reducida |
| ≤30 kcal/kg FFM/día | Baja disponibilidad energética — aparecen efectos negativos reales |

**Guardrail duro:** nunca diseñes un déficit que lleve la disponibilidad energética estimada por debajo de 30 kcal/kg FFM/día, y sé prudente ya en la banda 30-45. Esto es la versión operacional, del lado de nutrición, del mismo cribado que `contraindicaciones-medicas.md` aplica en el agente de entrenamiento (RED-S, trastorno de conducta alimentaria) — si ese cribado ya detectó una señal de alarma, este módulo ni se activa (ver guardrail de `recomposicion-corporal-nutricion.md`).

*(Loucks, A.B. y revisiones sobre disponibilidad energética baja en atletas; nótese que el punto de corte de 30 kcal/kg FFM está mejor validado en mujeres — en hombres la evidencia sugiere que el umbral real podría ser más bajo, así que trata 30-45 con la misma cautela en ambos sexos en vez de asumir que el hombre tiene más margen.)*

## 6. Micronutrientes — señales de alerta, no un plan de suplementación

No es competencia de este agente diagnosticar una deficiencia (eso es analítica clínica), pero sí señalar cuándo el patrón de riesgo está presente para recomendar valoración profesional:

- **Hierro:** riesgo notablemente mayor en mujeres (15-35%) que en hombres (3-11%) que entrenan con regularidad.
- **Vitamina D y calcio:** ingesta insuficiente es frecuente incluso en deportistas con dieta por lo demás adecuada — más relevante si hay poca exposición solar o restricción de lácteos.
- **Fibra:** frecuentemente insuficiente cuando el volumen de comida se recorta para ajustar calorías en déficit — no sacrifiques verdura/fibra al recortar calorías, sacrifica antes densidad calórica de otros alimentos.

Si el cliente combina alto volumen de entrenamiento + dieta restrictiva (vegana/vegetariana sin planificación, o historial de baja ingesta) + alguno de estos riesgos, señala la conveniencia de una analítica, no prescribas suplementación a ciegas.

*(Revisiones sobre micronutrientes en deportistas; datos de ingesta en atletas de élite y sub-élite holandeses)*

## Conflictos conocidos con otros módulos

- **Con `alergias-intolerancias.md`:** la exclusión de un alérgeno/intolerancia (jerarquía universal, punto 1) puede limitar las fuentes de proteína/grasa disponibles — recalcula con las fuentes permitidas, no relajes el objetivo de macros para compensar.
- **Con `recomposicion-corporal-nutricion.md`:** este módulo aporta el TDEE base y los rangos de macros; ese módulo aplica el déficit/superávit sobre esta base y comprueba el guardrail de disponibilidad energética de la sección 5.
- **Con `timing-nutricional-entrenamiento.md`:** los totales diarios de este módulo se distribuyen en el tiempo según ese módulo — no son dos fuentes de verdad distintas.

## Referencias

- Jäger, R., et al. (2017). *International Society of Sports Nutrition Position Stand: protein and exercise.* Journal of the International Society of Sports Nutrition, 14:20.
- Mifflin, M.D., et al. (1990). *A new predictive equation for resting energy expenditure in healthy individuals.* American Journal of Clinical Nutrition.
- Gatorade Sports Science Institute. *Dietary Carbohydrate and the Endurance Athlete: Contemporary Perspectives.*
- Loucks, A.B., et al. Revisiones sobre disponibilidad energética baja (Low Energy Availability) y RED-S.
- Scoping review sobre manipulación de masa y composición corporal en atletas — consensos y position stands de grupos expertos internacionales.
