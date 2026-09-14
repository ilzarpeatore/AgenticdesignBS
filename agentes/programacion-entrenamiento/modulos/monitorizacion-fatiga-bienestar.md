# Módulo: Monitorización de fatiga, adherencia y bienestar

**Tipo:** General
**Se activa cuando:** siempre — es el módulo que da herramientas concretas a las "señales de fatiga" que `gestion-fatiga-deload.md` menciona de forma genérica, y alimenta `historial_ciclos` (memoria episódica) con datos reales en vez de impresiones.
**Versión:** 0.1.0 · **Última actualización:** 2026-09-14
**Procedencia:** primer módulo escrito desde cero. Basado en el método session-RPE (Foster et al., 2001) y el cuestionario de bienestar de Hooper & Mackinnon (1995).

## 1. RPE de sesión (método Foster) — cuánto ha costado la sesión

- Al terminar cada sesión (10-30 minutos después, no durante — para que refleje el esfuerzo global y no solo el último ejercicio), pide al cliente un RPE de sesión en escala 0-10 (0 = nada de esfuerzo, 10 = el máximo esfuerzo posible).
- **Carga de la sesión = RPE de sesión × duración de la sesión en minutos.** El resultado es una cifra en unidades arbitrarias que permite comparar el "coste" real de sesiones distintas, no solo lo que decía el plan sobre el papel.
- Sumar la carga de todas las sesiones de la semana da la **carga semanal** — compárala con lo que `biomecanica-programacion-hipertrofia.md` (sección 9) programó en volumen: si la carga percibida sube mucho más rápido que el volumen programado, es una señal de que el MRV real de ese cliente es más bajo de lo estimado.

## 2. Cuestionario de bienestar diario (basado en Hooper-Mackinnon)

Antes de cada sesión (no después — sirve para decidir ajustes de ese día), 4 preguntas rápidas, cada una puntuada 1-7 (1 = muy bien/muy bajo, 7 = muy mal/muy alto):

1. Calidad del sueño de anoche
2. Fatiga percibida general
3. Dolor muscular / agujetas
4. Nivel de estrés percibido

(Opcional un quinto ítem de estado de ánimo, si el cliente lo acepta bien — no todos responden igual de honesto a preguntas sobre ánimo).

- Es viable y suficiente en M0 recogerlo como 2-3 preguntas rápidas por WhatsApp antes de la sesión — no hace falta ninguna app ni infraestructura para empezar el hábito.

## 3. Cómo usar estos datos para ajustar la programación

- **Un solo día malo** (mal sueño puntual, agujetas altas por la sesión anterior) → ajusta *esa sesión concreta* (baja el RIR objetivo, recorta 1-2 series), no el mesociclo completo. Un dato aislado no es una tendencia.
- **Empeoramiento sostenido varios días seguidos** en el cuestionario de bienestar, o una carga semanal (sección 1) muy por encima de lo esperado → es la señal real de fatiga que activa `gestion-fatiga-deload.md`, incluso antes de que llegue la semana de deload programada por calendario.
- **Registra ambos datos** (RPE de sesión y bienestar diario) en el log de cada sesión (`esquemas/log-registro.schema.json`) — es lo que convierte `historial_ciclos` en datos reales que el Productor puede usar en el siguiente ciclo, en vez de una casilla vacía o una suposición.

## 4. Limitaciones

- La percepción subjetiva está influida por factores no físicos (estado de ánimo, contexto social, cómo de bien durmió la noche anterior por motivos ajenos al entrenamiento) — no trates un solo valor extremo como una verdad absoluta sobre el estado físico del cliente. Busca la tendencia, no el punto aislado.
- Estos cuestionarios son una herramienta de cribado rápido, no un diagnóstico — si el patrón apunta a algo más serio que fatiga de entrenamiento (ej. sueño muy alterado de forma persistente, estrés muy elevado sostenido), se deriva según corresponda, no se sigue ajustando solo el volumen de entrenamiento.

## Conflictos conocidos con otros módulos

- **Con `gestion-fatiga-deload.md`:** este módulo aporta las herramientas de medición concretas; ese módulo decide qué hacer con la señal (adelantar el deload).
- **Con `biomecanica-programacion-hipertrofia.md` (sección 9):** la carga de sesión acumulada (sección 1) es la forma real de comprobar si el MRV estimado se está alcanzando antes o después de lo previsto.
- **Con `esquemas/log-registro.schema.json`:** añade los campos `rpe_sesion`, `carga_sesion` y `bienestar_diario` al registro de cada sesión.

## Referencias

- Foster, C., et al. (2001). *A new approach to monitoring exercise training.* Journal of Strength and Conditioning Research — método session-RPE.
- Hooper, S. L., & Mackinnon, L. T. (1995). *Monitoring overtraining in athletes.* Sports Medicine — cuestionario de bienestar (Hooper Index).
- Revisión sobre validez y fiabilidad del método session-RPE en distintas poblaciones y niveles (2017).
