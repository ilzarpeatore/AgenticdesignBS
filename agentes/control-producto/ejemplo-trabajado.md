# Ejemplo trabajado — no es un fixture real

**Esto no es lo mismo que el fixture real del validador** (`agentes/programacion-entrenamiento/validador/tests/fixtures/Mesociclo_1_TONI_Septiembre.xlsx`). Ese fixture es el programa real *prescrito* que se entregó a Toni — datos reales. Los datos de *ejecución* (qué reps/RIR registró él de verdad en cada sesión) viven en producción (Bckbs), no en este repositorio de diseño, y esta sesión no tiene acceso a ellos.

Lo que sigue usa el prescrito real de Toni (las tres semanas, tal cual está en el fixture) combinado con una **ejecución ilustrativa, inventada para este documento** — para probar que la regla de decisión (system-prompt.md sección 4) produce el resultado esperado en cada uno de sus casos, antes de que este agente corra contra un cliente real. Cuando exista una revisión real, sustitúyase este documento por un enlace a ella, no se mantiene como referencia permanente.

## Prescrito real (fixture de Toni, 3 semanas, sin semana de deload en este extracto)

| Ejercicio | Series | Reps | RIR objetivo (S1→S2→S3) |
|---|---|---|---|
| Press banca con mancuernas | 3 | 8-10 | 3-4 → 2-3 → 1-2 |
| Face Pull | 3 | 12-15 | 3 → 2 → 1-2 |
| Sentadilla en copa con mancuernas | 3 | 10-12 | 3-4 → 2-3 → 1-2 |
| Curl de bíceps con mancuernas | 3 | 12-15 | 3 → 2 → 1-2 |

## Ejecución ilustrativa (inventada para este ejemplo)

**Adherencia general:** 9 sesiones prescritas, 8 completadas con series reales registradas, 1 vacía → 88.9%, muy por encima del umbral del 60% — los cuatro hallazgos siguientes pueden usar `confianza: alta`/`media` sin degradarse por adherencia.

**Press banca con mancuernas** — completó el rango de reps las 3 semanas, y el RIR real fue siempre más fácil que el objetivo (S1 real RIR 4-5 vs. objetivo 3-4; S2 real RIR 3 vs. objetivo 2-3; S3 real RIR 2 vs. objetivo 1-2) → regla 1 de la sección 4 → **`subir`**.

**Face Pull** — no completó el rango de reps ninguna semana (hizo 10-11, luego 9-10, luego 8-9, siempre por debajo de 12-15), y el RIR real fue sistemáticamente más difícil que el objetivo (llegó a fallo antes de lo previsto) → regla 3 de la sección 4 → **`bajar`**. Sin nota de dolor/molestia técnica en las sesiones, así que no deriva a sustitución de ejercicio en este ejemplo — sería el caso distinto si las notas mencionaran una molestia.

**Sentadilla en copa con mancuernas** — completó el rango exacto las 3 semanas, y el RIR real coincidió con el objetivo cada semana → regla 2 de la sección 4 → **`mantener`**. El volumen/carga actual ya es tan exigente como se pretendía; subir ahora acumularía fatiga por encima de lo previsto.

**Curl de bíceps con mancuernas** — solo 1 de las 3 sesiones tiene series reales registradas (las otras 2 son parte de la única sesión vacía del mesociclo) → menos de 2 sesiones con datos → **`sin_historial_suficiente`**.

## Salida esperada (`revision-cierre-mesociclo.schema.json`)

```json
{
  "cliente_id": "toni-perez-fernandez-99",
  "mesociclo_numero": 1,
  "fecha": "2026-10-05T09:00:00Z",
  "periodo_analizado": { "desde": "2026-09-01", "hasta": "2026-09-21" },
  "adherencia_general": {
    "sesiones_prescritas": 9,
    "sesiones_completadas": 8,
    "porcentaje": 88.9,
    "sesiones_vacias": 1
  },
  "confianza_global": "alta",
  "hallazgos_ejercicios": [
    {
      "ejercicio": "Press banca con mancuernas",
      "direccion_recomendada": "subir",
      "eje_recomendado": ["carga", "rir_rpe"],
      "evidencia": {
        "sesiones_con_datos": 3,
        "completo_reps_prescritas": "si_consistente",
        "rir_rpe_real_vs_objetivo": "mas_facil",
        "tendencia_carga_kg": null
      },
      "confianza": "alta",
      "notas": "Sin carga_kg registrada -- progresa por RIR, igual que el patrón real de Toni en el fixture del validador."
    },
    {
      "ejercicio": "Face Pull",
      "direccion_recomendada": "bajar",
      "eje_recomendado": ["reps"],
      "evidencia": {
        "sesiones_con_datos": 3,
        "completo_reps_prescritas": "no_consistente",
        "rir_rpe_real_vs_objetivo": "mas_dificil",
        "tendencia_carga_kg": null
      },
      "confianza": "media",
      "notas": "No completó el rango prescrito ninguna semana. Sin nota de dolor/molestia en las sesiones -- si la hubiera, derivaría a seleccion-ejercicios-sustitucion-lesion.md en vez de solo bajar."
    },
    {
      "ejercicio": "Sentadilla en copa con mancuernas",
      "direccion_recomendada": "mantener",
      "eje_recomendado": ["ninguno"],
      "evidencia": {
        "sesiones_con_datos": 3,
        "completo_reps_prescritas": "si_consistente",
        "rir_rpe_real_vs_objetivo": "coincide",
        "tendencia_carga_kg": null
      },
      "confianza": "alta"
    },
    {
      "ejercicio": "Curl de bíceps con mancuernas",
      "direccion_recomendada": "sin_historial_suficiente",
      "eje_recomendado": ["ninguno"],
      "evidencia": {
        "sesiones_con_datos": 1,
        "completo_reps_prescritas": "parcial",
        "rir_rpe_real_vs_objetivo": "no_reportado",
        "tendencia_carga_kg": null
      },
      "confianza": "baja"
    }
  ],
  "hallazgos_grupos_musculares": [
    {
      "grupo_muscular": "pecho",
      "direccion_recomendada": "subir_volumen",
      "evidencia": {
        "volumen_real_series_semana": [3, 3, 3],
        "senales_fatiga_excesiva": false
      },
      "confianza": "media"
    }
  ],
  "notas_generales": "Ejemplo ilustrativo (ver ejemplo-trabajado.md) -- no corresponde a una revisión real todavía."
}
```

## Qué prueba este ejemplo

- Las cuatro direcciones posibles (`subir`, `mantener`, `bajar`, `sin_historial_suficiente`) salen de aplicar la regla de decisión tal cual está escrita, sin ajustarla para que "cuadre".
- El caso de Toni (progresión real solo vía RIR, sin `carga_kg`) no rompe nada — `tendencia_carga_kg: null` es un valor válido del esquema, y la decisión se apoya en reps/RIR igual que ya hace el validador del Productor con el mismo cliente.
- El JSON de salida valida contra `esquemas/revision-cierre-mesociclo.schema.json` sin necesitar ningún campo que no esté ya definido ahí.

**Pendiente real, no resuelto por este documento:** en cuanto exista una revisión real de un cliente real, sustitúyase este ejemplo por (o compleméntese con) esa revisión real como referencia, igual que el validador usa el fixture real de Toni en vez de un ejemplo sintético.
