# Módulo: Gestión de fatiga y deload

**Tipo:** General
**Se activa cuando:** siempre — es un módulo "de fondo" que se combina con cualquier otro módulo de fuerza/pliometría activo y con cualquier actividad concurrente (carrera, otro deporte, trabajo físico exigente).
**Versión:** 0.1.0 · **Última actualización:** 2026-09-14
**Procedencia:** adaptado de la sección 3.6 del agente original de fuerza/pliometría para media maratón.

## Regla operativa

- Cada 3-5 semanas de acumulación progresiva, planificar una semana de descarga: reducir volumen de series/contactos de salto (~40-60% del habitual) e intensidad relativa.
- Si el cliente tiene un plan de otra actividad (carrera, liga, temporada) con sus propias semanas de descarga, **coordinar el deload de fuerza con esas semanas** en vez de acumular fatiga alta en ambos frentes a la vez.
- Señales para adelantar un deload: estancamiento de rendimiento (en fuerza o en la actividad principal), dolor articular/tendinoso persistente, fatiga sistémica elevada, molestias que empeoran progresivamente.
- El deload es prioritario sobre cualquier regla de progresión (jerarquía universal, punto 2 del system-prompt).

## Conflictos conocidos con otros módulos

- **Con `periodizacion-orientada-evento.md`:** si el deload cae cerca de la fecha del evento, el taper absorbe su función — no se acumulan ambos.
- **Con `hipertrofia-recomposicion-corporal.md`:** coordinar el deload de entrenamiento con los diet breaks/refeeds del plan nutricional del cliente, si los tiene — mismo principio que coordinar con las semanas de descarga de una actividad concurrente.
- **Con `biomecanica-programacion-hipertrofia.md`:** las señales de fatiga de este módulo son las que determinan cuándo se ha alcanzado el MRV real de un cliente (sección 9 de ese módulo) — el MRV teórico es solo una estimación de partida, no una cifra fija.
- **Con `monitorizacion-fatiga-bienestar.md`:** ese módulo da las herramientas concretas (RPE de sesión, cuestionario de bienestar) para detectar las señales de fatiga que aquí solo se describen de forma genérica ("estancamiento", "fatiga sistémica elevada").
