# Módulo: Ganancia muscular — superávit calórico dedicado

**Tipo:** Específico
**Se activa cuando:** el objetivo prioritario del cliente es ganar masa muscular sin un objetivo simultáneo de pérdida de grasa relevante (a diferencia de `recomposicion-corporal-nutricion.md`, que asume déficit o mantenimiento). Coordina con `hipertrofia-recomposicion-corporal.md` y `biomecanica-programacion-hipertrofia.md` del Asistente de Programación de Entrenamiento, que fijan el volumen/frecuencia que este superávit debe sostener.
**Versión:** 0.1.0 · **Última actualización:** 2026-09-15
**Procedencia:** deep search de guías prácticas de "lean bulk" y consenso ISSN sobre proteína/grasa en superávit. Hasta ahora esto solo tenía una mención breve dentro de `recomposicion-corporal-nutricion.md`, sección 1 — este módulo le da su propio detalle porque el objetivo (ganar músculo sin maximizar pérdida de grasa) tiene una lógica de dimensionamiento distinta, no solo el signo contrario del déficit.

## 1. Tamaño del superávit — implementación práctica

**Igual que en déficit, la app calcula el superávit como porcentaje del TDEE, no como kcal fijas** (`FITNESS_GOAL`: ganancia +10/+20/+40% — ver `formato-salida/entrega-bckbs.md`, sección 5). El procedimiento:

1. Calcula el TDEE con `necesidades-energeticas-macronutrientes.md`, sección 1.
2. El tamaño de superávit recomendado depende del nivel de entrenamiento — **más superávit para principiantes, menos para avanzados**, lo contrario de lo intuitivo si se piensa solo en "cuánto músculo se puede construir":
   - **Principiante:** hasta ~500 kcal/día de superávit — el techo de síntesis proteica muscular es alto, un superávit generoso no se traduce en tanta grasa añadida como en un avanzado, y el margen de "ganancias de novato" (ver `hipertrofia-recomposicion-corporal.md`, sección 1, del agente de entrenamiento) tolera bien el exceso.
   - **Intermedio/avanzado:** 200-300 kcal/día — el margen real de ganancia muscular mensual es pequeño (≈0.1-0.5 kg/mes), así que un superávit grande en este nivel se convierte casi todo en grasa, no en músculo.
3. Traduce el porcentaje elegido a **kcal absolutas** para el TDEE real de este cliente y comprueba que el ritmo de ganancia de peso resultante (sección 2) sea coherente — si el preset más cercano se aleja demasiado del ritmo objetivo, usa `macro_type: custom` en vez de forzarlo.

## 2. Ritmo de ganancia de peso — el indicador real, no solo las kcal

El superávit en kcal es solo la estimación de partida; el dato que de verdad importa es el ritmo real de cambio de peso corporal:

- **Ritmo objetivo:** 0.25-0.5% del peso corporal por semana. Por debajo del umbral inferior el superávit probablemente es insuficiente para maximizar la ganancia muscular; por encima del superior, la proporción de grasa ganada por kg de músculo empieza a subir sin beneficio adicional de síntesis proteica.
- **Ajusta por la respuesta real, no por la cifra teórica de TDEE:** si a las 2-3 semanas el ritmo de ganancia de peso está claramente fuera de ese rango, sube o baja el superávit del cliente en vez de insistir en el porcentaje inicial — el TDEE estimado por Mifflin-St Jeor tiene un margen de error real (`necesidades-energeticas-macronutrientes.md`, sección 1), la báscula no.
- **Guardrail de expectativas:** comunica al cliente el rango de ganancia muscular realista de su nivel (ver `hipertrofia-recomposicion-corporal.md`, sección 1, del agente de entrenamiento) — un superávit más agresivo no acelera la ganancia muscular más allá de ese techo fisiológico, solo añade grasa más rápido.

## 3. Proteína y grasa en superávit

- **Proteína:** 1.6-2.2 g/kg/día — el extremo alto del rango general de `necesidades-energeticas-macronutrientes.md`, sección 2, coherente con maximizar síntesis proteica sin necesidad de las cifras más altas que solo tienen sentido en déficit (2.3-3.1 g/kg, ver `recomposicion-corporal-nutricion.md`).
- **Grasa:** 0.6-1.0 g/kg/día — por encima del mínimo de salud hormonal de `necesidades-energeticas-macronutrientes.md`, sección 3, dejando el resto del superávit disponible para carbohidrato, que es lo que sostiene el volumen/intensidad de entrenamiento que pide `hipertrofia-recomposicion-corporal.md`.
- El resto del superávit, por diferencia, va a carbohidrato — no hay un motivo en este contexto (a diferencia de recomposición) para limitarlo mientras se mantenga el mínimo de grasa.

## 4. Cuándo detener o ajustar el superávit

- Si la proporción de ganancia de grasa frente a músculo se dispara (el cliente reporta o mide un aumento de cintura/pliegues claramente desproporcionado respecto al peso ganado), reduce el superávit antes de plantear un bloque de pérdida de grasa — no dejes que la fase de superávit se alargue sin ajuste solo porque "sigue ganando peso".
- Un bloque de superávit dedicado no tiene por qué ser indefinido: para clientes intermedios/avanzados, la evidencia respalda mejor bloques alternos (superávit para ganar, déficit moderado para perder — ver `recomposicion-corporal-nutricion.md`, y la referencia cruzada ya existente en `hipertrofia-recomposicion-corporal.md`, sección 1) que un superávit sostenido durante meses sin revisión.

## Conflictos conocidos con otros módulos

- **Con `necesidades-energeticas-macronutrientes.md`:** este módulo aplica el superávit sobre el TDEE que calcula ese módulo, igual que hace `recomposicion-corporal-nutricion.md` con el déficit.
- **Con `recomposicion-corporal-nutricion.md`:** son mutuamente excluyentes para un mismo bloque — un cliente no está en superávit dedicado y en déficit de recomposición a la vez. Si el objetivo del cliente cambia de uno a otro entre ciclos, revisa qué módulo activa el Paso 0 para el ciclo actual.
- **Con `hipertrofia-recomposicion-corporal.md` (agente de entrenamiento):** ese módulo fija el volumen/frecuencia que este superávit debe sostener energéticamente, y la referencia de ganancia muscular realista por nivel que este módulo usa para dimensionar el ritmo de peso. Si una cifra cambia en uno, revisar el otro.
- **Con `timing-nutricional-entrenamiento.md`:** el carbohidrato adicional del superávit se reparte según la periodización de ese módulo (más en días de entrenamiento), no de forma plana en todos los días.
- **Con `alergias-intolerancias.md`:** las exclusiones de seguridad tienen prioridad sobre cualquier ajuste de superávit — busca fuentes alternativas de calorías/proteína, no relajes la exclusión.

## Referencias

- Guías prácticas de "lean bulk" — tamaño de superávit por nivel de entrenamiento y ritmo de ganancia de peso recomendado (0.25-0.5%/semana).
- Ver también las referencias de `hipertrofia-recomposicion-corporal.md` (agente de entrenamiento) para el techo real de ganancia muscular por nivel — no se duplican aquí.
- Jäger, R., et al. (2017). *International Society of Sports Nutrition Position Stand: protein and exercise* (rango de proteína general, aplicado aquí al extremo alto sin llegar a las cifras de déficit).
