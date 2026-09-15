# Módulo: Alergias e intolerancias alimentarias

**Tipo:** General — capa de seguridad transversal
**Se activa cuando:** siempre, primero — antes del Paso 0. Se consulta contra `restricciones_dieteticas` en `agentes/programacion-entrenamiento/esquemas/perfil-cliente.schema.json` (campo compartido entre agentes, no se duplica el intake).
**Versión:** 0.2.0 · **Última actualización:** 2026-09-15
**Procedencia:** primer módulo del Agente de Programación de Nutrición, escrito aplicando directamente la lección del intake de lesiones del Asistente de Programación de Entrenamiento (`seleccion-ejercicios-sustitucion-lesion.md`, v0.2.0) — una descripción vaga de un riesgo de seguridad no es un dato provisional a mejorar más adelante, es un bloqueo hasta que se resuelve. v0.2.0: incorpora deep search de evidencia clínica real (lista de alérgenos mayores FDA/NIAID, contaminación cruzada, síndrome de alergia oral, fuentes ocultas de alérgenos) — ver referencias al final.

## Regla operativa

Para cada entrada de `restricciones_dieteticas`:

- **`tipo: alergia` sin `severidad`** → bloqueante. No generes ni un borrador preliminar. Pregunta la severidad explícitamente (leve / moderada / grave con riesgo de anafilaxia) antes de continuar. No asumas el lado conservador ni el permisivo — pregunta.
- **`tipo: alergia`, `severidad: leve` o `moderada`** → excluye el ingrediente y sus derivados directos evidentes (ej. "alergia a la lactosa" excluye leche, nata, quesos no curados — no hace falta perseguir trazas mínimas en productos horneados salvo que el cliente indique lo contrario).
- **`tipo: alergia`, `severidad: grave_anafilaxia`** → exclusión total, incluyendo:
  - El ingrediente y todos sus derivados, sin excepción.
  - Recetas del recetario que declaren riesgo de contaminación cruzada con ese alérgeno (frutos secos, marisco, gluten son los casos más frecuentes de contaminación cruzada en cocina compartida).
  - Marca el borrador para revisión humana obligatoria siempre que aparezca esta severidad, no solo la primera vez que se genera el plan — un error aquí no es "el cliente entrena mal", es un riesgo físico real y potencialmente grave.
- **`tipo: intolerancia`** → excluye o limita según el umbral que el cliente declare (muchas intolerancias son de dosis, no absolutas — ej. intolerancia a la lactosa leve puede tolerar quesos curados). Si no se declaró un umbral, trata como exclusión total hasta que se aclare — no asumas tolerancia parcial sin que el cliente lo haya dicho.
- **`tipo: aversion`** → no es una cuestión de seguridad, es de adherencia (jerarquía universal, punto 4 del `system-prompt.md`). Evita el alimento por preferencia, sin necesidad de buscar sustitutos nutricionalmente equivalentes con el mismo rigor que una alergia.
- **`tipo: preferencia_etica_religiosa`** → exclusión completa de la categoría declarada (ej. vegetariano estricto: ningún producto cárnico, sin margen de interpretación).

## Guardrail duro

Ante cualquier `tipo: alergia` con `severidad` ausente, ambigua, o descrita en términos vagos ("a veces me sienta mal X", "creo que soy un poco intolerante a Y"): **no programes nada**, ni siquiera una versión conservadora "por si acaso". Pide la especificidad mínima primero. Esto es exactamente lo que el módulo equivalente de entrenamiento (`seleccion-ejercicios-sustitucion-lesion.md`) tuvo que aprender de un caso real después de haber generado ya un programa — aquí se aplica desde el primer borrador, no después de un incidente.

## 1. Los alérgenos mayores — prioridad de cribado

La FDA (bajo la FASTER Act) y organismos equivalentes reconocen **nueve alérgenos alimentarios mayores**, responsables de la gran mayoría de reacciones graves: leche, huevo, pescado, marisco crustáceo, frutos secos de árbol, cacahuete, trigo, soja y sésamo (el sésamo se sumó a la lista en 2023 — trátalo con el mismo rigor que los otros ocho, no como una incorporación menor). Cuando el cliente declare alergia a cualquiera de estos nueve, aplica el nivel de exhaustividad más alto de este módulo por defecto, incluso si la severidad declarada es "leve" — son los alérgenos con mayor tasa de reacciones graves y de contaminación cruzada accidental en cocina no especializada.

*(FDA/FASTER Act 2021; NIAID, Guidelines for the Diagnosis and Management of Food Allergy.)*

## 2. Contaminación cruzada — reglas prácticas para severidad grave

Para `severidad: grave_anafilaxia`, la exclusión del ingrediente en la receta no es suficiente — el riesgo real más frecuente en cocina doméstica/compartida es la contaminación cruzada, no el ingrediente declarado en la receta en sí:

- **Utensilios y superficies:** cualquier receta que comparta utensilios, tablas de cortar o superficies de preparación con el alérgeno (sin lavado completo entre usos) se considera contaminada — no distingas entre "el alérgeno está en la receta" y "el alérgeno estuvo en la cocina donde se preparó", ambos son el mismo riesgo para severidad grave.
- **Orden de preparación:** si el recetario o las notas de preparación no garantizan que el plato del cliente se prepara antes que cualquier plato con el alérgeno (o con utensilios ya limpiados a fondo), márcalo como riesgo de contaminación cruzada, no lo asumas resuelto por defecto.
- **Almacenamiento:** alimentos almacenados en el mismo recipiente, estantería sin separación, o expuestos a derrames de un producto con el alérgeno, se tratan igual que si el alérgeno estuviera en la receta.
- Estas reglas se aplican tanto si el cliente cocina en casa (advertencias en las instrucciones de la receta) como si el recetario de Bckbs declara explícitamente el riesgo — ver limitación real en `formato-salida/entrega-bckbs.md`, sección 4: hoy no hay etiquetado de alérgenos por ingrediente en la base de datos, así que el cribado automático es solo por coincidencia de texto y estas reglas de contaminación cruzada dependen en parte de que el Productor las aplique al redactar las instrucciones, no solo de filtrar el recetario.

*(Guías clínicas de manejo dietético de alergias alimentarias — prevención de contaminación cruzada en preparación doméstica.)*

## 3. Síndrome de alergia oral / reactividad cruzada polen-alimento

Un cliente con alergia diagnosticada a un polen específico puede reaccionar a alimentos vegetales con proteínas similares, aunque nunca haya declarado alergia a esos alimentos concretos — pregúntalo explícitamente si el cliente menciona alergia estacional/al polen, no asumas que solo aplica su lista de alimentos ya declarada:

- **Alergia al abedul (birch):** posible reactividad cruzada con manzana, y frutas de hueso (melocotón, ciruela, cereza).
- **Alergia a la ambrosía (ragweed):** posible reactividad cruzada con plátano, melón, calabacín y pepino.
- Estas reacciones suelen ser más leves que una alergia alimentaria primaria (picor/hinchazón bucal, no siempre sistémica), pero no las descartes sin preguntar — si el cliente confirma que ya le pasa con alguno de estos alimentos, trátalo como una exclusión de tipo alergia normal, con la severidad que el cliente reporte.

*(Literatura clínica sobre síndrome de alergia oral y reactividad cruzada polen-alimento.)*

## 4. Fuentes ocultas de alérgenos

No te fíes solo del nombre evidente del alimento — algunos alérgenos mayores aparecen en productos donde no se esperan, y el recetario de Bckbs no los etiqueta automáticamente (misma limitación que la sección 2):

- **Soja:** lecitina de soja, frecuente en productos horneados, chocolate y aliños, sin que "soja" aparezca en el nombre del plato.
- **Trigo/gluten:** presente en salsas espesadas con harina, rebozados, y algunos caldos/preparados industriales.
- Cuando generes o selecciones una receta para un cliente con alergia grave a soja o trigo, revisa los ingredientes secundarios (salsas, aliños, espesantes) con el mismo rigor que el ingrediente principal — no asumas que un plato "sin soja" en el título está libre de lecitina de soja como aditivo.

*(FDA/NIAID — fuentes ocultas de alérgenos mayores en alimentos procesados y preparados.)*

## Conflictos conocidos con otros módulos

- **Con cualquier módulo de objetivo nutricional:** esta regla tiene prioridad 1 de la jerarquía universal (`system-prompt.md`, sección 5) sobre cualquier rango de macros, timing o preferencia que pida otro módulo.
- **Con el módulo de coordinación con el entrenamiento** (Paso 1, apartado 1 del `system-prompt.md`): una alergia grave puede limitar qué alimentos post-entreno son viables para el timing recomendado — la exclusión de seguridad nunca cede ante la conveniencia del timing; se busca una alternativa segura, no se relaja la exclusión.

## Referencias

- FDA (2021). *Food Allergy Safety, Treatment, Education, and Research (FASTER) Act* — lista de los nueve alérgenos alimentarios mayores, incluida la incorporación del sésamo.
- NIAID (National Institute of Allergy and Infectious Diseases). *Guidelines for the Diagnosis and Management of Food Allergy in the United States.*
- Guías clínicas de manejo dietético de alergias alimentarias — prevención de contaminación cruzada en preparación de alimentos.
- Literatura clínica sobre síndrome de alergia oral (oral allergy syndrome) y reactividad cruzada polen-alimento (abedul↔manzana/frutas de hueso; ambrosía↔plátano/melón/calabacín/pepino).
- FDA/NIAID — fuentes ocultas de alérgenos mayores en productos procesados (lecitina de soja, derivados de trigo).
