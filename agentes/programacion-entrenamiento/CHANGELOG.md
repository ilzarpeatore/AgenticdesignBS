# Changelog — Asistente de Programación de Entrenamiento

## v0.24.0 — 2026-09-29

El usuario pidió, en otra sesión de trabajo (repo `bsa`, el backend/app real de BeFit), diseñar macrociclos de 6 meses para cinco clientes reales -- **Arafa El Harrak Moumen #107, Carlos Palomar #110, Josu Mauricio #109, Ayoub Ghamari #102 y Anas Benaissa #128** -- resolviendo todo directamente contra la base de datos por SSH/`tinker` con un pipeline propio (`docs/AGENTE PROGRAMACION/` en `bsa`, con su propio documento de reglas y su propio validador `validar_progresion.py`), sin pasar por este agente en absoluto. Después pidió explícitamente **reconciliar lo aprendido en esos cinco casos con este repo**, "para que el agente se ajuste a lo que has estado haciendo en esta sesión" -- este changelog documenta esa reconciliación.

**Lo más importante que expusieron esos casos, y que no existía como regla ni como código aquí:** un macrociclo puede tener la estructura y la onda intra-mesociclo perfectas (RIR undulando, deload presente, todo lo que ya comprobaba este agente) y aun así **no progresar realmente de un mesociclo al siguiente** -- el volumen semanal total se queda plano o incluso baja mes a mes. El primer caso real (Arafa) lo hizo evidente: `88 → 100 → 103 → 103 → 114 → 102` series/semana en 6 mesociclos, y 0 de ~22 ejercicios de progresión cambiaban de rango de reps entre semanas de carga. Nada mecánico lo detectaba -- `progresion-carga.md` y `biomecanica-programacion-hipertrofia.md` sección 9 solo cubrían la progresión DENTRO de un mesociclo, nunca la comparación entre mesociclos.

Un segundo hallazgo, más sutil (caso Josu): incluso cuando la base (semana 1) de un grupo muscular SÍ sube de un mesociclo al siguiente, el **pico** semanal de ese grupo puede retroceder si la onda intra-mesociclo (`+1-2 series` en semanas intermedias) se aplica de forma inconsistente entre mesociclos -- en ese caso, 8 de 10 grupos musculares tenían un pico de mesociclo 2 por debajo del pico de mesociclo 1, pese a que la base subía. Ningún chequeo existente, en ningún repo, comprobaba esto.

Un tercer hallazgo, de individualización más que de progresión (caso Anas vs. Ayoub, avisado por el usuario): dos clientes que se conocen y comparten gimnasio recibieron macrociclos casi idénticos -- 45 de 50 ejercicios coincidían, incluidas las 10 anclas -- pese a que cada uno, por separado, cumplía perfectamente las reglas de progresión. Ningún módulo de intake preguntaba ni comprobaba esto.

**Cambios en este repo:**

- **`modulos/biomecanica-programacion-hipertrofia.md` (v0.3.0):** nueva sección 9bis, "Progresión de volumen ENTRE mesociclos" -- la base de cada grupo muscular debe subir de mesociclo a mesociclo (no solo dentro de uno), y el pico semanal tampoco debe retroceder aunque la base suba, aplicando la misma regla de onda de forma consistente en todos los mesociclos del macrociclo. Generalizada como regla operativa, sin ningún número concreto de ningún cliente (mismo criterio que ya fijó v0.2.1 de `progresion-carga.md`).
- **Nuevo `validador/validar_macrociclo.py`:** validador determinista, mismo contrato JSON (`aprobado`/`errores`/`advertencias`) que `validar_programa.py`, pero opera sobre el CONJUNTO de `.xlsx` de un macrociclo en vez de uno solo. Comprueba V1 (base sube), V2b (pico no retrocede), V2 (descarga real por mesociclo) y V3 (las reps cambian de rango semana a semana, con ambos sentidos representados por sesión), más un V4 opcional (mínimos de reps/RIR para un patrón de ejercicio pasado por `--patron-seguro`, sin ninguna lista hardcodeada). Probado con `tests/test_validar_macrociclo.py` (8 pruebas, fixtures sintéticas generadas con `openpyxl` -- no hay individualización de cliente que justifique un fixture real aquí, a diferencia de `validar_programa.py`) y, durante el desarrollo, contra los macrociclos reales completos de los 5 clientes de esta reconciliación (sin adjuntarlos a este repo). `system-prompt.md` sección 6 lo referencia: se corre además de `validar_programa.py` cuando se generan o revisan dos o más mesociclos seguidos del mismo cliente.
- **`modulos/seleccion-ejercicios-sustitucion-lesion.md` (v0.3.0):** dos patrones nuevos a partir del caso de Anas (rotura de tríceps antigua, `cronica_controlada`, objetivo secundario de igualar fuerza entre lados). **(1)** Reintroducción progresiva de intensidad: la zona lesionada lleva una rampa de RIR más conservadora que el resto del programa durante los primeros mesociclos, convergiendo con la intensidad general en un mesociclo concreto decidido por el Productor -- nunca una excepción permanente ni un número fijo de "2 meses" para todos los casos. **(2)** Ejercicio unilateral por anotación en `notas` cuando el catálogo no tiene variante explícita ("a un brazo"): el lado afectado progresa a su propio RIR real, nunca al peso absoluto del lado sano.
- **`formato-salida/formato-excel.md`:** pasa de 19 a **21 columnas** -- documenta `tecnica`/`tecnica_series`, que el importador real de BeFit (`Bckbs::database/data/programs/EXCEL_FORMAT.md`) ya soporta desde antes de esta fecha y este documento nunca reflejó. Sin este campo, el Productor no tenía forma de prescribir una técnica de intensidad (rest-pause, drop sets, myo-reps...) de forma estructurada -- solo como texto libre en `notas`, que el importador no interpreta.
- **`formato-salida/formato-excel-detallado.md`:** resuelve la "Limitación conocida" de la hoja `📊 DASHBOARD` (v0.21.0): `openpyxl` sí genera gráficos nativos de Excel (`LineChart`/`BarChart`/`RadarChart`) sin construir OOXML a mano -- basta con volcar los datos a celdas normales y apuntar el gráfico con `Reference`. Documenta la estructura recomendada de esa hoja (KPIs, línea de volumen semanal completo, barras por mesociclo, radar por grupo muscular, tabla de progresión con color condicional, antes/después si aplica), probada en los 5 macrociclos reales de esta reconciliación.
- **`system-prompt.md` (v0.24.0):** nuevo apartado 5bis del Paso 1 -- si el cliente conoce a otro cliente ya programado, comprobar el solapamiento de ejercicios (sobre todo anclas) antes de fijar el roster. Sección 6 actualizada para referenciar `validar_macrociclo.py`.

**Pendiente, no resuelto en esta versión:** ninguno de los 5 casos reales se persistió en `bstronger-memoria-clientes` (ni `plan-macro.json` ni `log-registro.json` con el `razonamiento` del Paso 2) -- se trabajaron con el pipeline operativo de `bsa`, no con este agente. Si el coach quiere ese historial disponible para este agente en el futuro (por ejemplo, para que un ciclo posterior de esos mismos clientes SÍ pase por aquí y pueda leer memoria episódica real), habría que reconstruirlo retroactivamente a partir de lo que ya existe en `bsa` -- no se ha hecho en esta versión, y no se ha decidido si merece la pena para casos ya cerrados.

## v0.23.0 — 2026-09-27

El usuario quiere montar en el panel admin un check-in de satisfacción con el programa cada 15 días (qué ejercicio cuesta más, qué sesión se complica). El Agente de Soporte / Customer Success ya vigila esas respuestas vía `GET admin-form-submission-list` de Bckbs (`agentes/soporte-customer-success/modulos/checkin-satisfaccion.md`, nuevo) — este agente debe leer la misma fuente, no solo el agente que vigila.

- Sección "Memoria del cliente" (Paso 1) gana `GET admin-form-submission-list` como fuente a consultar antes de generar, cuando el coach tenga ese check-in configurado para el cliente.
- No se duplica en `bstronger-memoria-clientes`: Bckbs ya es la fuente real de esas respuestas.
- El Agente de Soporte solo vigila y escala si hay una señal de seguridad o insatisfacción — nunca decide programación; eso sigue siendo trabajo de este agente.

## v0.22.0 — 2026-09-27

El usuario pidió calibrar el Agente de Soporte / Customer Success (`agentes/soporte-customer-success/`) a un servicio premium de ~300€/mes, siguiendo prácticas reales de coaching de alto contacto (investigación de mercado): la pieza de mayor impacto identificada es un check-in semanal estructurado y fijo — algo que este agente ya necesitaba (`bienestar_diario` existe en `log-registro.schema.json` desde antes, pero nada lo recogía en la práctica).

- **`esquemas/log-registro.schema.json` gana `origen: "checkin_soporte"`** (mismo patrón que `checkpoint-fisico.schema.json` con `sync_automatico`, 2026-09-20): una entrada con este origen solo exige `bienestar_diario`, nunca `modulos_activos`/`razonamiento`/`confianza`/`requiere_revision` — no tiene sentido simular el razonamiento de una generación que no ocurrió. El comportamiento para entradas sin `origen` (todas las anteriores a esta fecha) o con `origen: "generacion"` no cambia.
- **Sección "Memoria del cliente" (Paso 1)** actualizada para leer también estas entradas — es la misma serie temporal de bienestar que antes, con una fuente nueva.
- Diseño completo del check-in (cadencia, preguntas, quién lo recoge) vive en `agentes/soporte-customer-success/modulos/checkin-semanal.md` — este documento no lo duplica.

## v0.21.0 — 2026-09-27

El usuario pidió ver los 6 mesociclos de Carlos Palomar (110) "en el excel para poder revisar todo" y adjuntó como referencia el Excel real de un cliente de Be Stronger (`Porgramación 6 meses.xlsx`) que ya se había mencionado en v0.16.0. Al comparar el entregable generado (formato plano de `formato-excel.md`, pensado para importar) contra esa referencia, quedó claro que el coach esperaba el formato rico de revisión -- hojas por mesociclo con semanas en columnas, clasificación ancla/variable/nuevo, RPE/RIR por semana, patrones de reps. v0.16.0 había registrado ese formato como "servicio individualizado... no se generaliza a ningún módulo, cada cliente puede requerir indicaciones distintas".

**Decisión explícita del usuario, con una corrección importante el mismo día:** se generaliza la **tabla/formato** (hojas por mesociclo, semanas en columnas, clasificación ancla/variable/nuevo, columnas Sets×Reps/RIR/Nota técnica) -- pero **NO los valores numéricos concretos de progresión, regresión o descarga** de ese cliente original (RPE exacto por semana, %, qué ejercicios son "seguros"). Esos siguen siendo individualizados por cliente y mesociclo, decisión del Productor, igual que ya lo es la duración de cada mesociclo (`periodizacion-por-calendario.md` v0.3.0). La primera versión de este cambio (v0.2.0 de `progresion-carga.md`, corregida en el mismo día a v0.2.1) generalizaba también los números por error.

- **`modulos/progresion-carga.md` (v0.2.1):** nuevo "Esquema de especificación detallada de mesociclo" -- clasificación ancla/variable/nuevo, patrones de reps A (descendente)/B (ascendente)/C (fijo), que exista una progresión de RPE semana a semana con deload, sistema de RIR según nº de series y si el ejercicio se trata como "seguro" para ese cliente. Los números concretos del caso real (RPE 7-7.5 en S1, +5%, -30% en deload, la lista de ejercicios "seguros" de ese cliente) quedan como **ejemplo ilustrativo explícito**, no como valor por defecto. El contenido específico del cliente original (2 ejercicios excluidos permanentemente) tampoco se traslada.
- **Nuevo `formato-salida/formato-excel-detallado.md`:** especifica el `.xlsx` de revisión (hoja `Mn` por mesociclo, `Visión general` cruzando todos los mesociclos, `Leyenda y metodología`). Es un documento distinto de `formato-excel.md` -- se genera primero para que el coach lo revise, y solo tras su aprobación se traduce (sin reinventar contenido) al formato de importación de siempre. Limitación conocida y documentada: no genera gráficos embebidos (la referencia real tenía una hoja `DASHBOARD` con gráficos) -- requeriría construir a mano las partes OOXML de `xl/charts/`, fuera de alcance de esta versión.
- **`system-prompt.md` (v0.21.0):** sección 7 pasa de tres a cuatro formatos de salida; apartado 4bis del Paso 2 actualizado para reflejar el nuevo paso intermedio.
- **Carlos Palomar (110):** su Excel de 5 mesociclos se regenera en este formato nuevo (hojas `Mn` + `Visión general` + `Leyenda y metodología`, sustituyendo la tabla plana anterior), aplicando la clasificación ancla/variable a su roster de 22 ejercicios con una progresión de RPE/RIR decidida específicamente para su caso (técnica autoevaluada baja, nivel intermedio provisional, precaución reforzada por su historial de TCA superado) -- no copiada del cliente original. Ver `bstronger-memoria-clientes/clientes/110-carlos-palomar-dominguez/log-registro.json` para el razonamiento completo.

## v0.20.0 — 2026-09-27

Cierra el hueco que la propia v0.18.0 ya había dejado anotado ("no existe todavía una plantilla formal para este nivel de detalle"): pedido explícito del usuario tras comprobar que pedir "el plan semestral de un cliente" no devolvía ningún `.xlsx` — el agente no tenía ningún formato registrado para ese nivel, solo para un mesociclo individual.

- **Nuevo `esquemas/plan-macro.schema.json`:** esqueleto de varios meses (nivel Macrociclo/Bloque de `modulos/periodizacion-por-calendario.md`) — lista de mesociclos con `numero`, `semanas`, `objetivo_principal`, `modulos_previstos`, `semana_deload` y `estado` (`planificado`/`generado`/`entregado`/`completado`). Sin detalle semana a semana ni columnas de ejercicio/series/reps — eso lo sigue cubriendo, sin cambios, `formato-salida/formato-excel.md` para cada mesociclo cuando le toca generarse.
- **`system-prompt.md` (v0.20.0):** nuevo punto 0 (condicional) en el razonamiento del Paso 2 y nuevo apartado 4bis que describe el flujo en dos fases — generar/leer el esqueleto primero, luego el `.xlsx` de cada mesociclo cuando llega su turno, releyendo siempre la memoria episódica real del mesociclo anterior antes de fijar la progresión (no se trata el esqueleto como un contrato fijo, mismo criterio que ya fijaba v0.16.0 para el detalle completo por adelantado). "Memoria del cliente" del Paso 1 pasa a leer también `plan-macro.json` si existe. Formato de salida (sección 7) pasa de dos a tres formatos.
- **Persistencia:** `plan-macro.json` vive en `bstronger-memoria-clientes/clientes/<cliente_id>/`, mismo patrón que el resto de memoria de cliente — repo editable a mano por el coach, revisado en el mismo Paso 5 que cualquier otro borrador.
- No se ha tocado `formato-salida/formato-excel.md` en su contenido (solo una nota cruzada al principio) ni `validador/validar_programa.py` — el esqueleto no pasa por ese validador, solo el `.xlsx` de cada mesociclo.

## v0.19.0 — 2026-09-27

- **Cabecera de `system-prompt.md` sincronizada** — se había quedado en v0.12.0 (19/09) mientras este changelog ya iba por v0.18.0, por trabajo concurrente de varias sesiones sin actualizar el encabezado a la vez.
- **`formato-salida/catalogo-ejercicios.xlsx` refrescado por el usuario** — el anterior (14/09, 1505 ejercicios) llevaba dos semanas desactualizado: el usuario reportó que el Productor no seleccionaba bien los ejercicios de la BD real, y se confirmó que el catálogo consultado no reflejaba las importaciones reales desde entonces (Nerea/Toni/Osas, 17-20/09). El nuevo archivo (1520 ejercicios) se exportó hoy **después de borrar del catálogo real los duplicados** que causaba el bug ya documentado en `agentes/importador-programas/CHANGELOG.md` v0.4.1 (mismo ejercicio creado una vez por semana).
- **Riesgo real sin verificar todavía:** borrar ejercicios duplicados de la BD puede dejar referencias rotas en programas que ya apuntaban a esos ids — ya pasó una vez antes (ver `Bckbs::app/Services/ExerciseMatcher/ExerciseMatcher.php`, comentario sobre una limpieza de catálogo del 2026-09-01 que rompió 4 referencias). Los 3 Mesociclo 1 ya asignados a clientes reales (Nerea `#65`, Toni `#64`, Osas `#66`, ver v0.18.0) son los que más importa verificar. Nuevo ítem en `docs/TAREAS_PENDIENTES.md`: correr `programs:check-integrity` contra el VPS real para confirmarlo.

## v0.18.0 — 2026-09-20

Primer Mesociclo 1 real ejecutado end-to-end para **3 clientes simultáneos** (Nerea, Toni, Osas) — hasta ahora el único caso real completo era Toni (v0.9.0, Septiembre). Pedido explícito del coach. No se descubrió ninguna regla nueva ni se tocó ningún módulo de contenido — el pipeline (Paso 1 intake → Paso 0 selección de módulos → Paso 2 Productor con razonamiento → Paso 3 validador determinista → import a biblioteca) se siguió tal cual estaba especificado, primera vez que se ejercita de principio a fin para 3 perfiles distintos a la vez (fuerza/potencia+pliometría, hipertrofia con lesión de hombro, recomposición con antecedente de rodilla/cadera).

- **Nerea (105-nerea-mejia):** estructura real confirmada por el coach (Fuerza + Potencia, tren inferior priorizado, + calentamiento pliométrico corto de 25min pre-carrera) sustituye el split genérico del guideline antiguo. Verificado explícitamente contra `contraindicaciones-medicas.md` antes de generar: historial de TCA (superado, no activo) y SOP no son contraindicación absoluta ni relativa de las listadas en ese módulo — se procede con precaución reforzada (volumen en rango alto, nunca usar el entrenamiento como palanca de pérdida de grasa), no con bloqueo.
- **Toni (99-toni-perez-fernandez):** `disponibilidad.dias_por_semana` actualizado de 3 a 5 y nueva `preferencia` (no le gusta pierna, 2 ejercicios/semana en 2 sesiones, sin día dedicado) — ambos confirmados directamente por el coach en conversación, no por un nuevo onboarding. Split Empuje/Tracción con mancuernas (nunca barra) por la asimetría crónica-controlada del hombro derecho.
- **Osas (103-osas-ehigiator):** split Torso/Pierna x2 + Full Body. Antecedente de cirugía de rodilla derecha/cadera izquierda (~5 años, crónica controlada, "entrena con normalidad") no activa el guardrail duro (los 3 campos obligatorios están completos y `fase` no es `aguda`) — se prioriza igualmente prensa/sentadilla en copa sobre sentadilla libre pesada como criterio conservador propio del Productor, no como bloqueo del sistema. **Pendiente de confirmar con el coach si ese criterio es adecuado o excesivamente conservador** dado que el perfil dice explícitamente que entrena con normalidad.
- Los 3 programas pasaron `validador/validar_programa.py` (`aprobado: true`, 0 errores) y se importaron a la biblioteca de Bckbs (`training_program_id` 64/65/66) vía `programs:import excel --json`, con `check-integrity` limpio inmediatamente después. **Ninguno asignado a un cliente real** — regla no negociable del agente importador, pendiente de revisión y asignación manual del coach en el panel admin.
- **Razonamiento completo del Paso 2 persistido** en `log-registro.json` de cada cliente en `bstronger-memoria-clientes` (primera entrada de los 3, no había historial previo que leer).
- **Esqueleto macro de 6 meses** (2 bloques de 3 meses, objetivos por bloque/mes) generado como `.xlsx` para los 3 clientes y entregado al coach para revisión, siguiendo la estructura que en ese momento documentaba `periodizacion-por-calendario.md` (v0.2.0) como cifra fija. **Nota post-hoc (misma fecha):** v0.3.0 de ese módulo (ver entrada inmediatamente inferior, trabajo concurrente de otra sesión) corrige que esa cifra nunca debió tratarse como fija -- el número de mesociclos y su duración dependen del cliente. Los 3 esqueletos generados aquí siguen siendo válidos como una posible estructura razonable, pero no deben tomarse como "la" plantilla obligatoria de 6 meses en ciclos futuros. Formato libre en cualquier caso -- **no existe todavía una plantilla formal para este nivel de detalle** en este repo (a diferencia del formato de entrega de Mesociclo 1, que sí está especificado en `formato-salida/formato-excel.md`).
- **Pendiente, no resuelto en esta versión:** confirmar con el coach `nivel_fuerza='avanzado'` de Nerea (sigue marcado `_provisional` en su perfil); resolver la discrepancia `duracion_sesion_preferida` de Toni (onboarding dice 45min, guideline antiguo decía 60-90min, sin tocar en esta sesión).

## v0.17.0 — 2026-09-20

Caso real: al pedir un plan nutricional para Ayoub (102-ayoub-ghamari), no había forma de calcular TDEE porque peso/altura/edad no existían en ningún sitio de `bstronger-memoria-clientes` — el volcado inicial solo leyó `par_q_answers`/`training_questionnaire_answers`/`nutrition_questionnaire_answers`, que nunca capturan estos datos. Investigación de código (no solo documentación) confirmó que sí existen en Bckbs, en la tabla `user_profiles` (columnas `weight`/`height`/`age`, texto libre, nullable), rellenadas en una etapa de registro separada (`update-profile`) del resto del onboarding v2. El usuario confirmó que el flujo actual las pide a todos los usuarios nuevos, pero el propio backend documenta fallos de red reales (`OnboardingController::complete()` no verifica esa etapa concreta) que pueden dejarla sin guardar, y las cuentas anteriores al 29-08-2026 pasaron por una pantalla de registro que no las pedía en absoluto — de ahí que sea opcional, no un error de captura.

- **Nuevo `datos_fisicos` en `esquemas/perfil-cliente.schema.json`:** objeto opcional con `peso_kg`, `altura_cm`, `edad` y `fecha_referencia`. Documentado como imprescindible para el cálculo real de TDEE (Mifflin-St Jeor, ver `agentes/programacion-nutricion/modulos/necesidades-energeticas-macronutrientes.md`) y explícitamente distinto de `checkpoint-fisico.schema.json` (historial de reevaluaciones periódicas del coach, no el snapshot de registro).
- Poblado con datos reales confirmados por el coach para 8 clientes (98, 99, 100, 101, 102, 103, 104, 105) en `bstronger-memoria-clientes`, consultando `GET admin/users/{id}` del panel admin.
- **Pendiente, no resuelto en esta versión:** `agentes/programacion-nutricion/modulos/necesidades-energeticas-macronutrientes.md` y `system-prompt.md` de ese agente (Paso 1, punto 6, "Referencias actuales") todavía no citan `datos_fisicos` explícitamente como la fuente de peso/altura/edad para el cálculo de TDEE — sigue redactado como si fuera parte de la lista de datos opcionales, cuando en realidad es bloqueante para un cálculo real (no inventado) de calorías. Corregir en la próxima revisión de ese agente.

## v0.16.0 — 2026-09-20

Corrige una contradicción real en `modulos/periodizacion-por-calendario.md`, expuesta al revisar el macrociclo real de un cliente de hipertrofia (Be Stronger, entregado como Excel de 6 meses con detalle semana a semana completo: clasificación de ejercicios ancla/variable/nuevo, patrones de reps A/B/C, esquema de RIR por seguridad, regla de progresión +5%/mantén/baja, deload -30%, valores MEV/MRV por grupo muscular).

- **`modulos/periodizacion-por-calendario.md` (v0.3.0):** la tabla de jerarquía fijaba cifras concretas (macrociclo = 6 meses, bloque/mesociclo = 3 meses × 2, mes = 1 × 3 por bloque) que contradecían el propio texto del módulo ("cada módulo de objetivo rellena este esqueleto con sus propios parámetros de duración"). Se corrige: el número de mesociclos y las semanas por mesociclo dependen del cliente (objetivo, nivel, disponibilidad) — nunca una cifra fija de plantilla. Se elimina el nivel "Mes" de la tabla (no aportaba nada que el nivel Mesociclo/Semana no cubra ya, y forzaba una cadencia calendario que no siempre aplica).
- **Cadencia de generación:** el Productor deja de estar limitado a "solo esqueleto macro + detalle mes a mes" — puede generar el detalle semana a semana de todo el macrociclo en un único pase cuando el caso lo justifique (como en el caso real que motivó este cambio). Sigue siendo un borrador vivo: se revisa mesociclo a mesociclo con la adherencia real antes de entregarse, no se convierte en contrato fijo solo por estar ya detallado.
- **Decisión explícita del usuario, sin cambios en ningún otro documento:** el contenido metodológico concreto del caso real (ancla/variable/nuevo, patrones de reps, esquema de RIR, regla de progresión, deload, MEV/MRV) es específico de ese cliente y no se generaliza a ningún módulo — es un servicio individualizado, cada cliente puede requerir indicaciones distintas. El propio Excel de ese cliente tampoco se sube a este repositorio.

## v0.15.3 — 2026-09-19

Cierra el ítem 2.4 de `docs/TAREAS_PENDIENTES.md` con datos reales de 6 clientes.

- El coach confirmó `nivel_fuerza` real para Hamsa, Toni, Borja, Ayoub, Osas y Alberto. Contrastado contra la regla de derivación (2026-09-16, `experiencia_meses`/`tecnica_autoevaluada`): coincidió en 3/6 (Hamsa avanzado, Toni intermedio, Borja avanzado) y falló en 3/6 (Ayoub: la regla decía principiante por su técnica autoevaluada de 1/10, el coach lo clasifica avanzado; Osas: la regla decía avanzado, el coach dice intermedio; Alberto: la regla decía intermedio, el coach dice principiante).
- Conclusión práctica: la técnica autoevaluada por el propio cliente no es un predictor fiable por sí sola del nivel real. `nivel_fuerza` deja de derivarse siempre — ahora se lee directamente si el coach ya lo confirmó (caso normal a partir de ahora), y solo se deriva con la regla como estimación de baja confianza, marcada para confirmar, cuando un cliente nuevo todavía no tiene el dato.
- `esquemas/perfil-cliente.schema.json` (descripción de `nivel_fuerza`) y `system-prompt.md` (v0.12.0, Paso 1 punto 4) actualizados.

## v0.15.2 — 2026-09-19

Decisión del usuario: en `bstronger-memoria-clientes`, `perfil-nutricional.json` deja de ser un archivo aparte y pasa a vivir anidado bajo la clave `"nutricion"` dentro de `perfil-cliente.json` (ver CHANGELOG del agente de nutrición, v0.8.0, para el detalle completo). Sin impacto funcional en este agente — sigue leyendo un único archivo por cliente, igual que antes. `system-prompt.md` (v0.11.2), sección "Memoria del cliente", ya no cita `perfil-nutricional.json` como archivo independiente.

## v0.15.1 — 2026-09-17

Cierra el ítem 2.6 de `docs/TAREAS_PENDIENTES.md` (dónde viven físicamente los archivos reales de memoria por cliente, dejado abierto en v0.15.0).

- **Decisión:** repo privado de GitHub, **`ilzarpeatore/bstronger-memoria-clientes`** — no una tabla en Bckbs (esos campos, `observaciones_coach`/`razonamiento`, los escribe el coach a mano, igual que hoy escribe el guideline de Borja) ni Google Sheets (exigiría aplanar los esquemas anidados e integrar la API de Google, trabajo de M1 adelantado sin necesidad).
- Estructura: `clientes/<cliente_id>/` con `perfil-cliente.json`, `perfil-nutricional.json`, `checkpoints-fisicos.json`, `log-registro.json`, `log-nutricion.json` — mismos nombres que los esquemas de `AgenticdesignBS`, sin duplicar su definición. Plantilla de partida en `_plantilla/` de ese repo.
- `system-prompt.md` (v0.11.1), sección "Memoria del cliente": ahora nombra el repo y la ruta exacta en vez de dejarlo como decisión abierta.

## v0.15.0 — 2026-09-17

Memoria persistente por cliente, diseñada a partir de un documento real que el usuario comparte con sus clientes (guideline de Borja, Be Stronger, abril 2026) — el primer ejemplo concreto del "perfil vivo" que hasta ahora solo existía como concepto en la tabla de memoria de `docs/roadmap.md`.

- **Nuevo `contexto_vida` en `esquemas/perfil-cliente.schema.json`:** ocupación, horario laboral (texto libre — los horarios reales no caben en un enum), sueño (horas + regularidad), estrés percibido (1-10), coaching previo. El caso real mostró un horario nocturno de trabajo y estrés 7/10 como factores que condicionan directamente `gestion-fatiga-deload.md`/`monitorizacion-fatiga-bienestar.md`, no datos decorativos.
- **Nuevo `esquemas/checkpoint-fisico.schema.json` (compartido con nutrición):** una entrada por reevaluación física periódica (peso, % grasa, masa muscular, cargas de referencia) más `observaciones_coach` en texto libre — el campo más importante del esquema. Cierra el hueco real que exponía el caso de Borja: la mejora perceptual no se reflejaba en las métricas, y la explicación (ingesta insuficiente) solo la tenía el coach en la cabeza, sin ningún sitio donde quedara escrita de forma estructurada para el siguiente ciclo.
- **`system-prompt.md` (v0.11.0), Paso 1:** nueva sección "Memoria del cliente" — exige leer las últimas entradas de log y checkpoints de este cliente ANTES de generar. Hasta ahora la memoria episódica (`log-registro.schema.json`) era de solo escritura: se guardaba el razonamiento de cada ciclo, pero nada instruía a leerlo de vuelta. Se aclara explícitamente que los datos reales de cliente no viven en este repositorio de diseño.
- **Pendiente, no resuelto en esta versión:** el caso real de Borja incluye una capa de "hábitos prioritarios" (nutrición/estilo de vida, ordenados por impacto, con implementación muy simple) que no tiene equivalente en ningún agente hoy — ni el de entrenamiento ni el de nutrición generan este tipo de contenido. Anotado como posible pieza nueva, no construida.

## v0.14.1 — 2026-09-16

- **Embarazo/RED-S solo para perfil mujer:** decisión de producto del usuario tras v0.14.0 — `parq_pregnant_or_possible`/`parq_menstrual_change_or_stress_fracture` dejan de ser obligatorias para hombre/otro (Bckbs las guarda `null`, no `false`, para no confundir "no aplica" con "se preguntó y dijo que no"). Nuevo campo `genero` en `esquemas/perfil-cliente.schema.json`, validación condicional (`allOf`/`if`/`then`) en vez de `required` fijo. `contraindicaciones-medicas.md` sube a v0.3.0. Ocultar el campo en el formulario de la app para perfiles no-mujer queda fuera de Bckbs (frontend).

## v0.14.0 — 2026-09-16

Primera reconciliación real de `perfil-cliente.schema.json` contra el onboarding de Bckbs (antes nunca se había contrastado contra las tablas reales, solo diseñado por lógica). El usuario confirmó que el onboarding real de la app queda registrado en BD, lo que permitió comparar el esquema contra las columnas reales sin necesitar datos de ningún cliente.

- **`cribado_medico`:** cambia a los nombres de campo reales de `par_q_answers`. Se encontró que tres preguntas que el diseño ya asumía (embarazo/posibilidad, alteración menstrual/fractura por estrés, trastorno alimentario) nunca se preguntaban en el onboarding real — se añadieron a Bckbs esta misma fecha (`par_q_answers`, migración + validación + tests), y ahora también marcan `flagged_for_review`. Ver `modulos/contraindicaciones-medicas.md` v0.2.0 para el mapeo completo campo a campo.
- **`nivel_fuerza` → `experiencia_entrenamiento`:** el enum fijo (principiante/intermedio/avanzado) no existía como tal en la app — Bckbs guarda `training_experience_months`/`technique_level` (autoevaluados, con override de coach ya implementado y consumido por el motor de autorregulación vía `ConditionVariable::NIVEL_EXPERIENCIA`). El esquema ahora pide esos dos datos reales y deriva `nivel_fuerza` con una regla explícita — propuesta, pendiente de confirmar/ajustar con casos reales.
- **`disponibilidad`:** de días de la semana + minutos exactos (que el onboarding nunca preguntó así) a un conteo de días/semana + franja preestablecida de duración (`training_days_per_week`/`session_duration_preference`, los campos reales). Ahora también editable por el cliente sin repetir el onboarding completo — nuevo endpoint `POST training-availability-update` en Bckbs.
- **`system-prompt.md` (v0.10.0):** Paso 1, puntos 4 y 6, actualizados con los campos reales y la aclaración de que los días concretos de la semana los decide el Productor, no el cliente.

## v0.13.0 — 2026-09-15

Preparación para el nuevo Agente de Programación de Nutrición (`agentes/programacion-nutricion/`), que lee `restricciones_dieteticas` de este mismo esquema en vez de duplicar el intake.

- **`esquemas/perfil-cliente.schema.json`:** `restricciones_dieteticas` pasa de `string[]` a objetos estructurados con `tipo` (alergia/intolerancia/aversión/preferencia ética-religiosa) y `severidad` obligatoria cuando `tipo: alergia` — mismo patrón de bloqueo duro que ya tiene `restricciones_salud`/`lesion_localizada`, para no repetir con alergias el mismo error de ambigüedad que expuso el caso de Toni con lesiones.

## v0.12.0 — 2026-09-14

Cuarta y última fase de las mejoras identificadas tras el caso real de Toni: el razonamiento del Paso 2 pasa de narración efímera en el chat a dato persistido y auditable.

- **`esquemas/log-registro.schema.json`:** nuevo campo obligatorio `razonamiento` (texto libre, no vacío) — traza completa del Chain-of-Thought del Paso 2: módulos activos y por qué, conflictos detectados, resolución según la jerarquía universal, y la consulta del catálogo de ejercicios (Fase 3 de esta misma serie de mejoras).
- **`system-prompt.md` (v0.8.0):** el Paso 2 indica explícitamente que ese razonamiento se guarda en este campo, no solo se narra.
- **`docs/roadmap.md`:** la fila de memoria episódica menciona ahora `razonamiento` junto a `historial_ciclos`.

## v0.11.0 — 2026-09-14

Tercera fase de las mejoras identificadas tras el caso real de Toni: la consulta del catálogo de ejercicios se formaliza como paso explícito, en vez de referencia pasiva.

- **`system-prompt.md` (v0.7.0):** nuevo punto 4 dentro del razonamiento del Paso 2 (Productor) — "Consulta del catálogo de ejercicios" (Tool Use, cap. 5). Para cada ejercicio, el Productor debe documentar el nombre buscado, el título del catálogo encontrado (si lo hay) y, ante una sustitución forzada por lesión o material, qué alternativa del catálogo mantiene el mismo patrón y vector de resistencia. Refleja el uso real que ya se le dio al catálogo al generar el programa de Toni (Press banca con mancuernas, sustitución de Hack Squat por Prensa de piernas, etc.), ahora como paso explícito y no como consulta implícita sin rastro.
- **`docs/roadmap.md`:** la descripción del Paso 2 en la tabla de arquitectura menciona ahora la consulta activa del catálogo (Tool Use) junto al razonamiento Chain-of-Thought.

## v0.10.0 — 2026-09-14

Segunda fase de las mejoras identificadas tras el caso real de Toni: el intake de lesiones pasa de advisory a bloqueante.

- **`esquemas/perfil-cliente.schema.json`:** para `restricciones_salud` con `categoria: lesion_localizada`, ahora son obligatorios `gesto_doloroso`, `fase` (`aguda`/`en_recuperacion`/`cronica_controlada`) y `empeora_con_actividad_o_impacto`; `autorizacion_profesional` pasa a ser obligatorio también cuando `fase: aguda` (antes solo para `contraindicacion_relativa`). Aplicado con `if`/`then` de JSON Schema, no solo como descripción.
- **`system-prompt.md` (v0.6.0):** el Paso 1 apartado 5 y la lista "NO debes" declaran explícitamente que no se genera nada, ni siquiera un borrador preliminar, sin estos cuatro datos ante una lesión localizada. El caso límite "información vaga sobre una molestia" deja de decir "pide especificidad" (tono de recomendación) y pasa a "bloqueante, no un matiz a resolver sobre la marcha".
- **`modulos/seleccion-ejercicios-sustitucion-lesion.md` (v0.2.0):** el guardrail duro ("lesión activa → excluir por completo") se redefine en términos del campo `fase` en vez de la palabra ambigua "activa"; se documenta el caso real que expuso la tensión (lesión de manguito rotador sin especificidad forzó una decisión de juicio del Productor).

## v0.9.0 — 2026-09-14

Primera fase de las mejoras identificadas tras el caso real de Toni: el validador determinista (Paso 3) deja de ser un backlog histórico ("hoy es prosa que se lee a ojo", desde v0.1.0) y pasa a ser código real, probado contra un archivo real.

- **Nueva carpeta `validador/`:**
  - `validar_programa.py` — comprueba mecánicamente el `.xlsx` final (formato de `formato-salida/formato-excel.md`): hojas y columnas exactas, `semanas` declaradas vs. semanas realmente escritas (y sin huecos), `ejercicio`/`series`/`reps` obligatorias por fila salvo descanso, filas de descanso sin columnas de ejercicio rellenas, `nombre_dia` consistente dentro del mismo día, `dia` en rango 1-7, y una lista opcional de ejercicios excluidos por cliente (lesión, material no disponible). `rir`+`rpe` simultáneos y un ejercicio ausente del catálogo quedan como advertencia, no error, tal como ya especificaba `formato-excel.md`.
  - `tests/` — 13 pruebas. El fixture principal es el programa real entregado a Toni (`Mesociclo_1_TONI_Septiembre.xlsx`), no un ejemplo sintético; el resto son copias de ese mismo archivo mutadas para provocar cada fallo uno a uno.
  - `README.md` — qué comprueba, qué es solo advertencia y por qué, uso de la CLI.
- **`system-prompt.md` (v0.5.0):** el Paso 3/4 ahora referencia el código real; un borrador no avanza a Crítico/revisión humana si `validar_programa.py` devuelve errores.
- **`docs/roadmap.md`:** eliminado del backlog el ítem ya resuelto.

## v0.8.0 — 2026-09-14

Se integra el formato de entrega real hacia el sistema BeFit — hasta ahora el "formato de salida" del agente era solo interno (JSON de esquemas); ahora hay un formato de entrega final real, que es lo que de verdad se importa a producción.

- **Nueva carpeta `formato-salida/`:**
  - `formato-excel.md` — especificación completa del `.xlsx` de dos hojas (`Programa` + `Programación`), 19 columnas, reglas de días de descanso implícitos, progresión explícita semana a semana, notación de bloques/superseries.
  - `catalogo-ejercicios.xlsx` — catálogo real de 1.505 ejercicios ya existentes en la base de datos (id + título) — usar estos nombres al escribir la columna `ejercicio` siempre que exista coincidencia razonable, para que el matcher de BeFit reutilice el ejercicio en vez de crear un duplicado.
  - `ejemplo-programa.xlsx` — programa de referencia completo y correctamente relleno (hipertrofia full body, 5 sesiones, 4 semanas con deload).
- **`system-prompt.md` (v0.4.0):** el Paso 5 (revisión humana) ya no termina en el JSON interno — termina en este archivo `.xlsx`, listo para `php artisan programs:import`.

## v0.7.0 — 2026-09-14

Relectura completa de los capítulos del libro todavía no aplicados (Routing, Resource-Aware Optimization, Reasoning Techniques, Prioritization, Parallelization) y actualización del `system-prompt.md` en consecuencia (v0.3.0).

- **Nuevo Paso 2 explícito — Productor con razonamiento (Chain-of-Thought, cap. 17):** antes de generar el borrador, el Productor debe listar por escrito los módulos activos, los conflictos detectados entre ellos y cómo los resuelve según la jerarquía universal. Antes esto ocurría implícitamente sin dejar rastro auditable.
- **Precisión terminológica (Routing, cap. 2):** el Paso 0 se documenta explícitamente como enrutamiento *multi-etiqueta* (varios módulos activos a la vez), distinto del enrutamiento clásico excluyente. La elección entre `periodizacion-orientada-evento.md` y `periodizacion-por-calendario.md` se documenta como enrutamiento determinista por regla (existe `fecha_evento` o no) — nunca una decisión que el Productor deba razonar.
- **Nueva sección "Asignación de modelo por paso" (Resource-Aware Optimization, cap. 16):** modelo rápido/económico para Paso 0, Paso 1 y Paso 4 (Crítico); el modelo más capaz disponible reservado para el Paso 2 (Productor), que es donde un error cuesta más caro.
- **Regla de prioridad para `requiere_revision` concurrentes (Prioritization, cap. 20):** cuando coinciden varios motivos de revisión, se ordenan por la jerarquía universal (seguridad primero), no se mezclan sin indicar cuál es más urgente.
- **Parallelization (cap. 3):** revisado — no se encontró una aplicación real a esta escala (la cadena de 6 pasos es secuencial por dependencia; el validador determinista ya es código, no LLM). Sin cambios; se deja anotado por si Mesociclo 1 introduce generación por lotes de varios clientes a la vez.
- Referencias cruzadas de sección corregidas en todos los módulos tras la renumeración del `system-prompt.md`.

## v0.6.0 — 2026-09-14

Se pospone el módulo de embarazo (sin cliente real que lo necesite ahora) y se prioriza cerrar huecos de base que afectan a todos los clientes.

- **Nuevo módulo general:** `modulos/calentamiento-activacion.md` — protocolo RAMP, series de aproximación (3-5, cercanas al peso de trabajo cuanto más exigente la carga), estiramiento estático solo al final de la sesión (nunca antes de fuerza/potencia si supera 60s), versión reducida para sesiones con poco tiempo. Referencias: Jeffreys 2007 (RAMP); Behm et al. 2019 (estiramiento estático agudo).
- **Nuevo módulo general:** `modulos/monitorizacion-fatiga-bienestar.md` — RPE de sesión (método Foster) para calcular carga de entrenamiento real, cuestionario de bienestar diario (Hooper-Mackinnon: sueño, fatiga, dolor muscular, estrés), y cómo usar ambos para ajustar sesiones puntuales o adelantar un deload. Da herramientas concretas a las "señales de fatiga" que `gestion-fatiga-deload.md` solo describía de forma genérica.
- **`esquemas/log-registro.schema.json`:** nuevos campos `rpe_sesion`, `carga_sesion` y `bienestar_diario`.
- **Conflictos anotados** en `gestion-fatiga-deload.md`, `pliometria-rigidez-tendinosa.md`.
- **Backlog limpiado:** ítems ya resueltos eliminados de `docs/roadmap.md`; módulos de población/deporte específicos (fútbol, embarazo, patología concreta) quedan explícitamente pospuestos hasta que exista un cliente real que los necesite.

## v0.5.0 — 2026-09-14

Cierra la mitad que faltaba de "carga y volumen": `progresion-carga.md` solo cubría carga (peso); ahora `biomecanica-programacion-hipertrofia.md` añade cómo debe progresar el volumen (número de series) dentro de un mesociclo.

- **`biomecanica-programacion-hipertrofia.md` (v0.2.0):** nueva sección 9, "Progresión de volumen dentro del mesociclo" — marco MEV/MAV/MRV (Israetel/RP Strength), esquema de progresión de 1-2 series/semana, regla de no subir carga y volumen agresivamente a la vez, y nota de nivel de certeza (marco práctico de la industria, no consenso académico cerrado sobre acumulación de fatiga). Referencias añadidas: Israetel et al.; *Mesocycle Progression in Hypertrophy: Volume Versus Intensity* (S&C Journal, 2020).
- **Conflictos anotados** en `progresion-carga.md` y `gestion-fatiga-deload.md` para reflejar la interacción carga/volumen y cómo el MRV teórico se ajusta con señales reales de fatiga.

## v0.4.0 — 2026-09-14

Respuesta a control de calidad: el agente no bajaba a nivel de biomecánica ni de programación fina de carga/volumen para hipertrofia — solo manejaba el contexto de déficit/recomposición. Deep search y nuevo módulo general para cerrar ese hueco.

- **Nuevo módulo general:** `modulos/biomecanica-programacion-hipertrofia.md` — perfiles de resistencia (curvas de fuerza), rango de movimiento e hipertrofia mediada por estiramiento, proximidad al fallo (RIR), rango de repeticiones, descansos entre series, orden de ejercicios, enfoque atencional, peso libre vs. máquina, unilateral vs. bilateral. Referencias: Warneke et al. 2023; Schoenfeld 2021 (continuo de repeticiones); Singer/Wolf/Generoso/Schoenfeld 2024 (descansos); meta-análisis de orden de ejercicios 2020; investigación de enfoque atencional; meta-análisis peso libre vs. máquina 2023.
- **`hipertrofia-recomposicion-corporal.md` (v0.2.0):** se reorganiza para no duplicar contenido — ahora se apoya en el módulo nuevo para el "cómo" (RIR, ROM, descansos) y se queda solo con el "cuánto y en qué contexto energético" (déficit, viabilidad por nivel, periodización). Declarado que ambos módulos se activan siempre juntos.

## v0.3.0 — 2026-09-14

Integración de contraindicaciones médicas reales (ACSM, PAR-Q+, ACOG, RED-S), siguiendo el proceso de `CONTRIBUTING.md`.

- **Nuevo módulo, capa de seguridad transversal:** `modulos/contraindicaciones-medicas.md` — cribado obligatorio tipo PAR-Q+, contraindicaciones absolutas (cardiovasculares, aneurisma, retinopatía proliferativa, hernia sintomática, embarazo de riesgo, trastorno alimentario activo/RED-S) y relativas (hipertensión, diabetes no controlada, osteoporosis, anticoagulantes, cardiopatía estable, embarazo sin contraindicación absoluta) con su protocolo de actuación. Referencias: ACSM Guidelines for Exercise Testing and Prescription; PAR-Q+; ACOG; Mountjoy et al. (RED-S); Retina Today (2021).
- **`system-prompt.md` (v0.2.0):** el cribado de este módulo pasa a ser el primer paso del Paso 1, obligatorio antes de la selección de módulos (Paso 0). Si detecta contraindicación absoluta, el pipeline se detiene sin generar nada.
- **`esquemas/perfil-cliente.schema.json`:** nuevo campo obligatorio `cribado_medico` (respuestas PAR-Q+); `restricciones_salud` ahora distingue `categoria` (lesión localizada vs. contraindicación relativa/absoluta) para enrutar cada caso al módulo correcto.
- **Conflictos anotados** en `seleccion-ejercicios-sustitucion-lesion.md` (precedencia: contraindicaciones médicas se resuelven antes) y en `hipertrofia-recomposicion-corporal.md` (RED-S/trastorno alimentario bloquea la activación del módulo, no solo el déficit calórico).

## v0.2.0 — 2026-09-14

Deep search de evidencia científica para el módulo de recomposición corporal (pendiente desde v0.1.0), siguiendo el proceso de `CONTRIBUTING.md`.

- **Nuevo módulo específico:** `modulos/hipertrofia-recomposicion-corporal.md` — viabilidad por nivel de entrenamiento, condiciones energéticas/proteicas (para dimensionar el entrenamiento, no para prescribir), volumen y frecuencia, progresión de carga en déficit, periodización macro/meso/micro, cardio concurrente, coordinación con diet breaks/refeeds. Referencias: Barakat et al. 2020; Murphy & Koehler 2022; Roth et al. 2023; Schoenfeld et al. 2016/2017; Grgic et al. 2017; Morton et al. 2018; Garthe et al.; editorial Frontiers in Physiology 2024.
- **Nuevo módulo general:** `modulos/periodizacion-por-calendario.md` — formaliza como módulo independiente la estructura macro/meso/micro que hasta ahora solo vivía como tabla narrativa en `docs/roadmap.md`.
- **Conflictos anotados** en `fuerza-maxima-potencia.md`, `progresion-carga.md` y `gestion-fatiga-deload.md` para reflejar su interacción con el módulo nuevo (Paso 4 del proceso de mantenimiento).

## v0.1.0 — 2026-09-14

Importación inicial. Se parte del agente original (v1.0, 2026-09-07), especializado en fuerza/pliometría para corredores de media maratón — que a su vez era la reescritura completa de un agente anterior de hipertrofia/pérdida de grasa (ya no conservado).

Se descompone el contenido en:

- `system-prompt.md` — marco fijo generalizado: rol, alcance, protocolo de redirección y protocolo de intake, sin asumir ningún deporte u objetivo concreto.
- `modulos/fuerza-maxima-potencia.md` — general (de la sección 3.2 y 3.8 del original)
- `modulos/pliometria-rigidez-tendinosa.md` — general (sección 3.3)
- `modulos/progresion-carga.md` — general (sección 3.5)
- `modulos/seleccion-ejercicios-sustitucion-lesion.md` — general (principios de la sección 3.4)
- `modulos/gestion-fatiga-deload.md` — general (sección 3.6)
- `modulos/periodizacion-orientada-evento.md` — general, condicional a fecha de evento (sección 3.7, generalizada de "carrera" a "evento")
- `modulos/running-economia-carrera.md` — específico (sección 3.1, prioridades de la 3.4, y las notas de casos frecuentes de running)

Motivo del cambio de arquitectura: el agente original se reescribía por completo cada vez que cambiaba el tipo de cliente (un solo documento activo). Eso no escala a atender simultáneamente objetivos distintos (recomposición, rendimiento deportivo, patología). La base de conocimiento modular permite que el Productor combine varios módulos por cliente sin encasillarlo en una categoría fija.

**Pendiente:**
- Módulo de Hipertrofia y recomposición corporal (no existe versión previa — se escribe de cero).
- Revisar si parte de las "prioridades de selección de ejercicios" de `running-economia-carrera.md` debería extraerse a un módulo general de demandas de tren inferior en deportes de impacto/cambio de dirección.
- Automatizar la checklist "verificable mecánicamente" de cada módulo como validador determinista real (hoy es una lista que se lee a ojo).
