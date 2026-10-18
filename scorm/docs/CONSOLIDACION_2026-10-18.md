# Consolidación de paquetes SCORM del 18 de octubre de 2026

Los doce ejercicios están aprobados, cargados en el módulo de Moodle y con QA completado, según la confirmación del equipo del proyecto del 18 de octubre de 2026.

Esta actualización incorpora **once archivos ZIP recuperados**, sus fuentes extraídas sin cambios y los nombres canónicos de distribución. C-1-1 V4 y C-2-1 V2 ya estaban en la rama; se conservan sus bytes. Las demás versiones recuperadas actualizan los cortes anteriores. Los nombres canónicos `C1-1_SCORM_1.2.zip`, etc. apuntan a los mismos bytes que el ZIP versionado indicado en el inventario.

## Diferencia de trazabilidad para C-2-3

C-2-3 está aprobado y en Moodle. No se recuperó el ZIP de ese último corte durante esta consolidación. Se conserva el código y el ZIP histórico ya existentes en GitHub, sin renombrarlos como una nueva versión ni afirmar equivalencia con la entrega aprobada en Moodle. La publicación del archivo exacto de ese corte queda pendiente de recuperación; esto no cambia su aprobación funcional.

## Inventario de los archivos recuperados

| Ejercicio | Archivo | SHA-256 |
| --- | --- | --- |
| C-1-1 | `C-1-1_SCORM_1.2_V4_QA_AJUSTADO.zip` | `90eb004a248b3daa78c7a19c6144e143141cfe4948133a15fb3aeaa1daf8298a` |
| C-1-2 | `C-1-2_SCORM_1.2_V2_QA.zip` | `90ed42915d8ac0cb7bd489e199ffac907363118da5308f27724c2080334b4846` |
| C-1-3 | `C-1-3_SCORM_1.2_V2_QA.zip` | `aa90b159b0c73671b74e63629973cb32f0f8daf81c81cc4602bb2e554e31a3e5` |
| C-1-4 | `C-1-4_SCORM_1.2_V6.zip` | `f85cb2d1ab0c9fa963672f66a11cc28b548e80eda0d4145736f92d7902107057` |
| C-2-1 | `C-2-1_SCORM_1.2_V2_QA.zip` | `24f18feabfa22b3addbf3ce499c03b2fb696177cc490b50d7b574f6534812acd` |
| C-2-2 | `C-2-2_SCORM_1.2_V4_QA.zip` | `803c219c76ee90f834d15fb925b245b88e723d57ec3a1a71b3ce0d28e3d8b932` |
| C-2-4 | `C-2-4_SCORM_1.2_V7_QA.zip` | `47fe6af38c93fd3e131be24a016f46631103fdf35eba7df5413f017d8a2239cd` |
| C-3-1 | `C-3-1_SCORM_1.2_V12_QA.zip` | `a2f4fe544fb42d1148759674216f814c9fabc039d2f19a30566657bde30e979a` |
| C-3-2 | `C-3-2_SCORM_1.2_V5_QA.zip` | `313755111ea28aeb4212c12249f78a115b853343d532656a8a77a2827b5259a6` |
| C-3-3 | `C-3-3_SCORM_1.2_V16_QA.zip` | `c5807da02471227f9ad45a4f4149907761e018991b40d2874e9f5ac2bae34ffa` |
| C-3-4 | `C-3-4_SCORM_1.2_V4_QA.zip` | `3335925eb5673575f434e73c8e26e8fd92e40469b6e3b63226d5d49c272ecf08` |

## Verificación de esta consolidación

Se comprobó la integridad ZIP, la presencia de las referencias del manifiesto y la sintaxis de los archivos JavaScript de los once paquetes. No se modificó su lógica ni se repitió la aplicación con estudiantes. Estas comprobaciones de distribución no sustituyen el QA ya completado en Moodle.

- C-1-3: ZIP íntegro; referencias de manifiesto presentes; sintaxis JavaScript correcta.
- C-1-1: ZIP íntegro; referencias de manifiesto presentes; sintaxis JavaScript correcta.
- C-1-2: ZIP íntegro; referencias de manifiesto presentes; sintaxis JavaScript correcta.
- C-2-1: ZIP íntegro; referencias de manifiesto presentes; sintaxis JavaScript correcta.
- C-1-4: ZIP íntegro; referencias de manifiesto presentes; sintaxis JavaScript correcta.
- C-2-2: ZIP íntegro; referencias de manifiesto presentes; sintaxis JavaScript correcta.
- C-2-4: ZIP íntegro; referencias de manifiesto presentes; sintaxis JavaScript correcta.
- C-3-3: ZIP íntegro; referencias de manifiesto presentes; sintaxis JavaScript correcta.
- C-3-1: ZIP íntegro; referencias de manifiesto presentes; sintaxis JavaScript correcta.
- C-3-2: ZIP íntegro; referencias de manifiesto presentes; sintaxis JavaScript correcta.
- C-3-4: ZIP íntegro; referencias de manifiesto presentes; sintaxis JavaScript correcta.

## Evaluación y audio

El estándar de cierre usa veinte puntos internos, conversión a 0–100 y aprobación desde 60. No se aplicó una conversión adicional al libro de calificaciones. El laboratorio de voz no modifica la nota y el audio se procesa temporalmente en el navegador. Los bancos varían por archivo: no se declara que todos tengan quince preguntas. En C-1-4 V6 se conservan los once ítems presentes en el ZIP inspeccionado.

## Uso académico

La monografía describe la arquitectura y la implementación de los doce ejercicios en el capítulo 3. El capítulo 4 separa los resultados del QA del piloto pedagógico de C-1-1. Este registro y el inventario permiten vincular los archivos de entrega con el código sin publicar datos de estudiantes.
