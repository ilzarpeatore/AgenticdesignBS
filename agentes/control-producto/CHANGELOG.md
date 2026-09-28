# Changelog — Agente de Control Producto (revisión de cierre de mesociclo, entrenamiento)

## v0.2.0 — 2026-09-28

El usuario preguntó qué más necesitaban este agente y el Productor para trabajar juntos lo mejor posible. Cuatro correcciones de la misma petición:

- **La más importante: se quita la dependencia dura de `plan-macro.json`.** v0.1.0 exigía un mesociclo en `estado: completado` de ese archivo para activarse — pero el propio system-prompt del Productor dice que generar mesociclos sueltos sin ese esqueleto es el patrón normal, no la excepción. Exigirlo habría dejado este Control inaplicable a la mayoría de clientes reales. Disparador ampliado: basta con que exista un mesociclo anterior entregado, visible en `log-registro.json`. `plan-macro.json` se sigue usando cuando existe (da fechas exactas), pero ya no bloquea la activación.
- **Lectura compartida del `.xlsx`**: usa `agentes/programacion-entrenamiento/validador/lectura_programa.py` (extraído del validador en la misma petición) en vez de interpretar el formato de columnas por su cuenta.
- **Paso 8 de calibración**: compara la recomendación anterior contra el resultado real del mesociclo que se acaba de cerrar — si el mismo desajuste se repite 2 veces seguidas para un cliente, se marca para recalibrar el criterio de ese cliente en concreto.
- **Nuevo `ejemplo-trabajado.md`**: un caso ilustrativo (prescrito real de Toni + ejecución inventada para el ejemplo, dejado explícito) que prueba las cuatro direcciones de la regla de decisión contra el esquema real, ya que este agente no tiene datos reales de ejecución con los que construir un fixture de verdad todavía (a diferencia del validador, que sí usa el `.xlsx` real de Toni).

## v0.1.0 — 2026-09-28

Primer diseño, a petición explícita del usuario. Segundo agente de Control del proyecto (después de `agentes/control-contenido/`), y el primero directamente activable hoy.

- **Distinto del bug de progresión plana ya corregido**: ese fue un chequeo mecánico (`validador/validar_programa.py` v0.6.0, compara el `.xlsx` contra sí mismo). Este agente compara lo prescrito contra **datos reales de ejecución** (peso, reps y RIR/RPE que el cliente registró de verdad en Bckbs) — un juicio, no una comprobación estructural, por lo que no podía vivir en el validador.
- **Por qué un agente separado y no un paso más del Productor**: el mismo día se comprobó que una instrucción de "también revisa esto" sin nada que la hiciera obligatoria no bastó para evitar el problema — pedirle al mismo paso que escribe el mesociclo que además juzgue si el anterior funcionó tiene el mismo sesgo estructural que ya evita la separación Producer-Critic (Reflection, cap. 4) del resto del sistema.
- **Por qué "Control Producto" y no un paso interno sin nombre**: coincide casi literalmente con el nivel 2 "Control producto (entrenamiento/nutrición)" ya definido en `docs/ORGANIGRAMA_AGENTES.md`. A diferencia de Control Contenido (diseñado el mismo día, marcado "no activar todavía"), el área producto lleva meses de entregas reales — cumple el criterio de secuenciación del organigrama mejor que cualquier otra área.
- **Groundeado sin backend nuevo**: `GET client-exercise-history`, `GET client-muscle-volume` y `GET client-session-feedback` ya existen en Bckbs (usados hoy por el panel admin y por el Agente de Soporte) — investigados antes de diseñar nada, no asumidos.
- **Regla de decisión explícita** (sección 4 del system-prompt): distingue "no progresó porque ya no hacía falta" (RIR real más fácil, adherencia alta → subir) de "no progresó porque los datos no son fiables" (adherencia baja → mantener con confianza baja, nunca bajar por una adherencia mala) — nunca trata ambos casos igual.
- **Reconciliación con el Productor, no un bloqueo ciego**: el Productor puede desviarse de la recomendación, pero debe justificarlo citando la jerarquía universal (sección 5 del system-prompt del Productor) — el Crítico de ese agente audita que toda desviación esté justificada, nunca silenciosa.
- **Alcance de esta v0.1.0: solo entrenamiento**, no nutrición (mismo nivel del organigrama original agrupa ambos) — sin señal real todavía de que la nutrición tenga el mismo problema.
- Nuevo esquema `esquemas/revision-cierre-mesociclo.schema.json` — salida estructurada, no prosa libre, consumible directamente por el Productor.
