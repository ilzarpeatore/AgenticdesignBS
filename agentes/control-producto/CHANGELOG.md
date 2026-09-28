# Changelog — Agente de Control Producto (revisión de cierre de mesociclo, entrenamiento)

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
