# Módulo: Hipertrofia y recomposición corporal

**Tipo:** Específico
**Se activa cuando:** el objetivo del cliente incluye reducir grasa corporal manteniendo o aumentando masa muscular (recomposición corporal), o hipertrofia como fin en sí mismo. **Se activa siempre junto con `biomecanica-programacion-hipertrofia.md`** — ese módulo aporta el "cómo" a nivel de ejercicio/serie (RIR, ROM, descansos, orden), este módulo aporta el "cuánto y en qué contexto energético".
**Versión:** 0.2.0 · **Última actualización:** 2026-09-14
**Procedencia:** primer módulo escrito desde cero (no existía playbook previo). Síntesis de revisiones y meta-análisis recientes — ver referencias al final de cada bloque.

> Este módulo cubre las **condiciones de entrenamiento en contexto de déficit/recomposición**. Las cifras de déficit calórico, proteína y macros son datos que necesita el Productor para dimensionar el volumen y ajustar expectativas — su prescripción exacta al cliente sigue siendo competencia del Agente Nutricional (ver guardrail de alcance en `system-prompt.md`). La biomecánica y programación fina de la hipertrofia en sí (RIR, rango de movimiento, descansos) vive en `biomecanica-programacion-hipertrofia.md` — no se duplica aquí.

## 1. Viabilidad según nivel de entrenamiento

La recomposición simultánea (perder grasa Y ganar músculo a la vez) no es igual de realista para todos — es la variable que más debe ajustar las expectativas que se comunican al cliente:

- **Principiante / con sobrepeso:** ocurre casi automáticamente con entrenamiento de fuerza + proteína adecuada, incluso en déficit calórico moderado ("ganancias de novato"). Rango orientativo a 6-12 meses: +3-5 kg de músculo, -4-6 kg de grasa, peso corporal casi estable.
- **Intermedio:** posible pero más lento y sensible a la dosificación — requiere volumen suficiente, proteína en el rango alto, y un déficit no severo.
- **Avanzado (3+ años de entrenamiento serio):** el margen real de ganancia muscular es pequeño (≈0.1-0.2 kg/mes). Intentar ganar músculo en déficit suele estancar ambos objetivos a la vez. Para este nivel, la literatura respalda mejor **bloques dedicados alternos** (superávit pequeño ~250 kcal/día para ganar, déficit moderado ~500 kcal/día para perder) que una recomposición continua — a menos que el cliente entienda y acepte explícitamente el ritmo lento de la vía simultánea.

**Guardrail de expectativas:** con un cliente avanzado que pide recomposición simultánea, el borrador debe dejar explícito el ritmo de progreso realista según esta evidencia — nunca prometer una velocidad de cambio propia de un principiante. Esto conecta directamente con la política de "no prometer resultados no garantizados" del resto del sistema.

**Guardrail de seguridad (precede a todo lo anterior):** este módulo no se activa en absoluto si el cribado de `contraindicaciones-medicas.md` detecta un trastorno de conducta alimentaria activo o señales de baja disponibilidad energética/RED-S (amenorrea, fractura por estrés, pérdida de peso rápida no intencionada). En esos casos no se prescribe ningún déficit calórico ni se programa recomposición — se deriva a evaluación médica/nutricional clínica.

*(Barakat et al., 2020, NSCA Strength & Conditioning Journal; editorial Frontiers in Physiology, 2024, sobre recomposición en poblaciones no entrenadas, entrenadas y muy entrenadas)*

## 2. Condiciones energéticas y proteicas (para dimensionar el entrenamiento)

- **Tamaño del déficit:** deficits mayores de ~500 kcal/día perjudican las ganancias de masa magra con entrenamiento de fuerza, aunque no perjudican las ganancias de fuerza en sí. Por eso, si el dato que llega desde nutrición es un déficit más agresivo, hay que ajustar a la baja la expectativa de ganancia muscular del bloque, no el volumen de entrenamiento.
- **Ritmo de pérdida de peso:** 0.5-0.7% del peso corporal por semana preserva mejor la masa magra y el rendimiento que ritmos más rápidos (ej. 1.4%/semana) — este dato debe pedirse/conocerse como input, ya que un ritmo de pérdida más agresivo del que reporta el cliente es señal de alerta (posible pérdida de masa magra) que debe marcarse para revisión.
- **Proteína:** el consenso general sitúa el umbral de beneficio hasta ~1.6 g/kg/día para maximizar ganancias de masa libre de grasa; en contexto de recomposición específicamente, ingestas más altas (hasta ~2.5 g/kg/día) se asocian a mejores resultados simultáneos de grasa y masa magra. Es un dato de referencia para saber si el volumen de entrenamiento previsto es sostenible, no una prescripción que el agente deba dar.

*(Murphy & Koehler, 2022, Scandinavian Journal of Medicine & Science in Sports, meta-análisis y meta-regresión sobre déficit energético; Morton et al., 2018, meta-análisis de suplementación proteica; comparación de protocolos nutricionales en recomposición, European Journal of Applied Physiology)*

## 3. Volumen y frecuencia de entrenamiento en déficit

El rango base de volumen (10-20 series/grupo muscular/semana), frecuencia (≥2x/semana) y estilo de periodización vive en `biomecanica-programacion-hipertrofia.md` — aquí solo el matiz específico del **contexto de déficit calórico**:

- En déficit, programas con volumen alto (≥10 series/semana por grupo muscular) muestran poca o ninguna pérdida de masa magra — **subir el volumen durante la restricción (en vez de bajarlo, que es lo intuitivo) parece ayudar más a conservar masa magra que reducirlo.**
- No uses el déficit como motivo para bajar por defecto del rango base de volumen — solo redúcelo si `gestion-fatiga-deload.md` detecta señales reales de fatiga excesiva, nunca de forma preventiva.

*(Roth et al., 2023, Scandinavian Journal of Medicine & Science in Sports, volumen de entrenamiento y conservación de masa magra en restricción calórica)*

## 4. Progresión de carga en déficit

- La progresión de fuerza es más lenta e inconsistente en déficit calórico que en superávit o mantenimiento — no fuerces incrementos de carga tan agresivos como los que aplicaría `progresion-carga.md` en un contexto de superávit.
- Prioriza sostener el estímulo (proximidad al fallo según `biomecanica-programacion-hipertrofia.md`, sección 3) sobre la progresión lineal de peso. Un cliente que mantiene sus cargas en déficit no está estancado — está teniendo un resultado esperado.

## 5. Periodización: macrociclo, mesociclo y microciclo

Este módulo usa el esqueleto de `periodizacion-por-calendario.md` (sin fecha de evento) y lo rellena con estos parámetros específicos:

- **Macrociclo (6 meses):** horizonte mínimo recomendado para evaluar progreso real. Con un ritmo seguro de cambio (0.5-0.7%/semana de grasa, y en el mejor de los casos ~0.5-1 kg de músculo/mes en principiantes, muchísimo menos en avanzados), un mes es una ventana demasiado corta para juzgar si el enfoque funciona.
- **Mesociclos:** duración según nivel — 8-12 semanas en principiantes, 4-6 semanas en intermedios/avanzados. Cada mesociclo cierra con una **semana de deload** (reducir volumen 30-50%, mantener intensidad relativa moderada) — coordinada con `gestion-fatiga-deload.md`.
- **Microciclos (semana):** frecuencia ≥2x/semana por grupo muscular; volumen total repartido según la regla del punto 3, sin bajarlo automáticamente al detectar fatiga por el déficit — primero comprobar (según `progresion-carga.md`) si la fatiga es de recuperación, no de volumen excesivo.

## 6. Cardio y actividad concurrente

- Combinar cardio y fuerza en el mismo programa no compromete de forma relevante la fuerza máxima ni la hipertrofia, siempre que las sesiones no se acumulen en exceso ni se hagan sin separación.
- Si hay que elegir modalidad de cardio para minimizar cualquier interferencia residual, la bicicleta interfiere menos que correr con las ganancias de fuerza/hipertrofia del tren inferior (ver también `running-economia-carrera.md` si el cliente además corre).
- El cardio, en el contexto de recomposición, es una herramienta para aumentar el gasto calórico sin tener que profundizar más el déficit dietético — lo que ayuda indirectamente a sostener el volumen de fuerza y la proteína disponible para conservar masa magra.

## 7. Diet breaks y refeeds (coordinación, no prescripción)

- Periodos de 1-2 semanas a mantenimiento calórico ("diet break") cada 6-12 semanas de déficit continuo ayudan a preservar masa magra, rendimiento en el gimnasio y adherencia a largo plazo, frente a un déficit ininterrumpido.
- Si el plan nutricional del cliente (gestionado por el Agente Nutricional) incluye diet breaks o refeeds, **coordina el deload de entrenamiento con esas semanas** en vez de que caigan en momentos distintos — mismo principio que ya aplica `running-economia-carrera.md` con las semanas de descarga de un plan de carrera.

## Conflictos conocidos con otros módulos

- **Con `biomecanica-programacion-hipertrofia.md`:** no es un conflicto, es una activación conjunta obligatoria — ese módulo aporta el "cómo" (RIR, ROM, descansos), este el "cuánto y en qué contexto energético".
- **Con `fuerza-maxima-potencia.md`:** comparten ejercicios ancla, pero difieren en el rango de repeticiones objetivo (este módulo, vía `biomecanica-programacion-hipertrofia.md`, usa rangos orientados a hipertrofia cerca del fallo; `fuerza-maxima-potencia.md` prioriza cargas altas y rangos bajos). Se arbitra por el objetivo primario declarado (jerarquía universal, punto 3 del `system-prompt.md`).
- **Con `progresion-carga.md`:** en déficit, la progresión de carga es más lenta de lo que ese módulo asumiría por defecto — no interpretar el mantenimiento de carga como estancamiento real.
- **Con `gestion-fatiga-deload.md`:** coordinar el deload de entrenamiento con los diet breaks/refeeds del plan nutricional, si el cliente los tiene (igual que running coordina con las semanas de descarga del plan de carrera).
- **Con `running-economia-carrera.md` (u otro módulo de actividad concurrente):** si el cliente combina recomposición con una actividad de resistencia, preferir cardio en bicicleta sobre correr para minimizar interferencia en el tren inferior.

## Referencias

- Barakat, C., et al. (2020). *Body Recomposition: Can Trained Individuals Build Muscle and Lose Fat at the Same Time?* Strength & Conditioning Journal.
- Murphy, C., & Koehler, K. (2022). *Energy deficiency impairs resistance training gains in lean mass but not strength: A meta-analysis and meta-regression.* Scandinavian Journal of Medicine & Science in Sports.
- Roth, C., et al. (2023). *Lean mass sparing in resistance-trained athletes during caloric restriction: the role of resistance training volume.* Scandinavian Journal of Medicine & Science in Sports.
- Schoenfeld, B., et al. (2016). *Effects of Resistance Training Frequency on Measures of Muscle Hypertrophy: A Systematic Review and Meta-Analysis.*
- Grgic, J., et al. (2017). *Effects of linear and daily undulating periodized resistance training programs on measures of muscle hypertrophy: a systematic review and meta-analysis.* PeerJ.
- Morton, R. W., et al. (2018). *A systematic review, meta-analysis and meta-regression of the effect of protein supplementation on resistance training-induced gains in muscle mass and strength in healthy adults.*
- Garthe, I., et al. *Effect of two different weight-loss rates on body composition and strength and power-related performance in elite athletes.*
- Editorial (2024). *New insights and advances in body recomposition.* Frontiers in Physiology.
