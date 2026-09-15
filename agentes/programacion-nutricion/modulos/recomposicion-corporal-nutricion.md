# Módulo: Recomposición corporal — implementación nutricional

**Tipo:** Específico
**Se activa cuando:** el objetivo del cliente incluye reducir grasa manteniendo/ganando masa muscular, o pérdida de grasa con entrenamiento de fuerza activo. **Se activa siempre junto con `necesidades-energeticas-macronutrientes.md`** — este módulo aplica el déficit/superávit sobre la base que calcula aquel, no repite el cálculo.
**Versión:** 0.2.0 · **Última actualización:** 2026-09-15
**Procedencia:** deep search de guías prácticas de diet breaks/refeeds y consenso ISSN sobre proteína en déficit. Complementa, sin duplicar, `hipertrofia-recomposicion-corporal.md` del Asistente de Programación de Entrenamiento. v0.2.0: reconciliado con el cálculo real de déficit de Bckbs (`FITNESS_GOAL` es un % del TDEE, no kcal fijas) tras revisar `app/Traits/DailyPlanTrait.php` — ver `formato-salida/entrega-bckbs.md`.

> Este módulo es la contraparte nutricional de `agentes/programacion-entrenamiento/modulos/hipertrofia-recomposicion-corporal.md`. Ese módulo ya fija, del lado de entrenamiento: viabilidad por nivel, tamaño de déficit seguro (no >500 kcal/día), ritmo de pérdida de peso (0.5-0.7%/semana), rango de proteína de referencia (hasta ~2.5 g/kg/día) y volumen de entrenamiento en déficit. **No repitas esas cifras aquí como si fueran un descubrimiento nuevo** — este módulo se ocupa de cómo se implementa el lado nutricional: cuánto déficit fijar en la práctica, cómo estructurar diet breaks/refeeds, y el guardrail de disponibilidad energética.

## 1. Tamaño del déficit/superávit — implementación práctica

**La app calcula el déficit/superávit como porcentaje del TDEE, no como kcal fijas** (`FITNESS_GOAL`: mantenimiento 0%, pérdida -10/-20/-40%, ganancia +10/+20/+40% — ver `formato-salida/entrega-bckbs.md`, sección 5). El procedimiento correcto:

1. Calcula el TDEE con `necesidades-energeticas-macronutrientes.md`, sección 1.
2. Elige el preset de `FITNESS_GOAL` más cercano al ritmo de cambio deseado (pérdida de peso 0.5-0.7%/semana, o superávit pequeño si el objetivo prioritario es ganancia muscular en un cliente avanzado — ver nivel de viabilidad en `hipertrofia-recomposicion-corporal.md`, sección 1, del agente de entrenamiento) y calcula a cuántas **kcal absolutas** se traduce ese porcentaje para el TDEE real de este cliente concreto.
3. **Comprueba el límite absoluto de seguridad (nunca >500 kcal/día de déficit, sin motivo clínico explícito) sobre esa cifra ya calculada, no sobre el porcentaje.** El mismo -20% puede quedarse en 400 kcal para un cliente sedentario y superar 700 kcal para uno muy activo — si el preset más cercano al ritmo deseado se pasa del límite, usa `macro_type: custom` (o el mecanismo equivalente) para fijar un porcentaje que sí lo respete, en vez de forzar el preset.
4. Verifica además que el resultado no baje la disponibilidad energética estimada de la banda segura (`necesidades-energeticas-macronutrientes.md`, sección 5).

## 2. Proteína en déficit

Usa el extremo alto del rango del ISSN para retención de masa magra en periodos hipocalóricos: **2.3-3.1 g/kg/día**. Esto es coherente con el "hasta ~2.5 g/kg/día" que ya usa `hipertrofia-recomposicion-corporal.md` para dimensionar el entrenamiento — aquí es la cifra que efectivamente se prescribe en el plan, no solo una referencia para el otro agente.

## 3. Diet breaks y refeeds — estructura práctica

Son herramientas distintas, no sinónimos:

- **Diet break:** 1-2 semanas a calorías de mantenimiento **recalculado al peso actual** (nunca al TDEE de antes de empezar la dieta — el cliente pesa menos, su mantenimiento real es menor). Cadencia: cada 4-10 semanas de déficit continuo, más frecuente cuanto más larga sea la fase de pérdida (fases de 8-12+ semanas casi siempre se benefician de al menos un diet break).
- **Refeed:** 1-3 días a calorías más altas dentro de una fase de déficit continuo, el incremento sobre todo vía carbohidrato (proteína y grasa se mantienen). Ej.: +500 kcal/día ≈ +125 g de carbohidrato ese día. Cadencia orientativa: una vez cada 7-14 días.
- **Coordinación con entrenamiento (obligatoria, no opcional):** hazlo coincidir con la semana de deload del agente de entrenamiento cuando sea posible (`hipertrofia-recomposicion-corporal.md`, sección 7, ya lo pide desde el lado de entrenamiento) — evita que el cliente tenga la semana más dura de carga en la misma semana de mayor restricción calórica.
- Ni un diet break de 1-2 semanas a mantenimiento real ni un refeed puntual deberían producir ganancia de grasa relevante — el aumento de peso que se observe en esos días es agua/glucógeno, no tejido adiposo; comunícalo así para no generar ansiedad innecesaria en el cliente.

## 4. Guardrail de seguridad (precede a todo lo anterior)

Igual que `hipertrofia-recomposicion-corporal.md` del agente de entrenamiento: este módulo **no se activa en absoluto** si el cribado de contraindicaciones médicas detectó un trastorno de conducta alimentaria activo o señales de RED-S (amenorrea, fractura por estrés, pérdida de peso rápida no intencionada), y **nunca** programa un déficit que lleve la disponibilidad energética estimada por debajo de 30 kcal/kg de masa libre de grasa/día (`necesidades-energeticas-macronutrientes.md`, sección 5) — en esos casos, deriva a evaluación profesional en vez de ajustar el déficit "por si acaso".

## Conflictos conocidos con otros módulos

- **Con `hipertrofia-recomposicion-corporal.md` (agente de entrenamiento):** no es un conflicto — es la misma recomposición vista desde dos agentes. Este módulo implementa numéricamente lo que ese módulo usa como referencia para dimensionar el entrenamiento. Si alguna cifra cambia en uno, debe revisarse el otro.
- **Con `necesidades-energeticas-macronutrientes.md`:** este módulo aplica el déficit/superávit sobre el TDEE que calcula ese módulo, y respeta su umbral de disponibilidad energética como límite duro.
- **Con `timing-nutricional-entrenamiento.md`:** los días de refeed/diet break deben coordinarse con qué tipo de sesión toca esa semana (ver periodización de carbohidrato de ese módulo, sección 3) — un refeed no debería caer, por accidente, en el único día de descanso de la semana si el objetivo es rendir mejor en la sesión más exigente.
- **Con `alergias-intolerancias.md`:** el incremento de carbohidrato en un refeed debe seguir respetando las exclusiones — no relajar por un día "especial".

## Referencias

- Jäger, R., et al. (2017). *International Society of Sports Nutrition Position Stand: protein and exercise* (rango de proteína en periodos hipocalóricos).
- Guías prácticas sobre diet breaks y refeeds — estructura, cadencia y recálculo de mantenimiento al peso actual.
- Ver también las referencias de `hipertrofia-recomposicion-corporal.md` (agente de entrenamiento) para la evidencia de tamaño de déficit, ritmo de pérdida de peso y volumen de entrenamiento en restricción — no se duplican aquí.
