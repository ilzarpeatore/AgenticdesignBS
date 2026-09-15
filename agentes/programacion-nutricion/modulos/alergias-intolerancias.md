# Módulo: Alergias e intolerancias alimentarias

**Tipo:** General — capa de seguridad transversal
**Se activa cuando:** siempre, primero — antes del Paso 0. Se consulta contra `restricciones_dieteticas` en `agentes/programacion-entrenamiento/esquemas/perfil-cliente.schema.json` (campo compartido entre agentes, no se duplica el intake).
**Versión:** 0.1.0 · **Última actualización:** 2026-09-15
**Procedencia:** primer módulo del Agente de Programación de Nutrición, escrito aplicando directamente la lección del intake de lesiones del Asistente de Programación de Entrenamiento (`seleccion-ejercicios-sustitucion-lesion.md`, v0.2.0) — una descripción vaga de un riesgo de seguridad no es un dato provisional a mejorar más adelante, es un bloqueo hasta que se resuelve.

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

## Conflictos conocidos con otros módulos

- **Con cualquier módulo de objetivo nutricional:** esta regla tiene prioridad 1 de la jerarquía universal (`system-prompt.md`, sección 5) sobre cualquier rango de macros, timing o preferencia que pida otro módulo.
- **Con el módulo de coordinación con el entrenamiento** (Paso 1, apartado 1 del `system-prompt.md`): una alergia grave puede limitar qué alimentos post-entreno son viables para el timing recomendado — la exclusión de seguridad nunca cede ante la conveniencia del timing; se busca una alternativa segura, no se relaja la exclusión.

## Referencias

Sin deep-search todavía — este módulo parte de la lección arquitectónica del propio proyecto (intake bloqueante ante datos de seguridad ambiguos), no de una revisión de evidencia clínica sobre alergias alimentarias. Pendiente: revisar guías clínicas reales de manejo dietético de alergias/intolerancias (ej. criterios de contaminación cruzada por alérgeno) antes de tratar este módulo como completo — ver `CONTRIBUTING.md` para el proceso de incorporar evidencia nueva.
