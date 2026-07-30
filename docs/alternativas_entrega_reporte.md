# Alternativas para entregar y proteger el reporte docente

Este documento presenta dos rutas para revisión con los tutores. La primera
puede utilizarse en el piloto con la infraestructura disponible. La segunda
requiere alojamiento y control de acceso institucional.

## Alternativa A: PDF protegido y entrega en Moodle

Al finalizar el ejercicio, el estudiante descarga un PDF que se abre sin
contraseña y permite impresión y lectura, pero restringe la modificación. El
archivo incluye el código estudiantil, el código de sesión, los resultados por
criterio, el puntaje, la nota y un código de verificación.

El estudiante entrega el PDF en Moodle. Si existe una duda sobre el archivo, el
docente compara el código visible con el generado a partir del registro JSON
original de la sesión.

Esta protección reduce modificaciones accidentales. No constituye una firma
digital ni garantiza por sí sola la autenticidad del archivo; la comprobación
contra el registro original es el control relevante.

## Alternativa B: consulta docente por código de sesión

El sistema conserva el resultado original y el docente lo consulta mediante el
código de sesión. El PDF puede seguir disponible como copia, pero la fuente
oficial es el registro almacenado por la aplicación.

El recorrido propuesto para la interfaz docente es:

1. Ingreso con una cuenta autorizada.
2. Búsqueda por código estudiantil o código de sesión.
3. Visualización del ejercicio, RAE, puntaje, nota y resultado por criterio.
4. Descarga del reporte generado desde el registro original.
5. Registro de la fecha y del usuario que realizó la consulta.

Para convertir esta alternativa en una solución institucional se debe definir
el alojamiento, la base de datos, los perfiles autorizados, el tiempo de
conservación y el tratamiento de los datos académicos. El piloto actual no
expone una consulta docente sin autenticación.

## Comparación

| Criterio | Alternativa A: PDF + Moodle | Alternativa B: consulta por sesión |
|---|---|---|
| Seguridad | Media. Restricción de edición y verificación contra el JSON. | Alta, si se implementan autenticación y permisos institucionales. |
| Trazabilidad | Media. Moodle registra la entrega; el JSON conserva el origen. | Alta. La consulta parte del registro original y puede generar auditoría. |
| Esfuerzo técnico | Bajo. Ya funciona en el piloto. | Alto. Requiere backend, base de datos y control de acceso. |
| Costo inicial | Bajo; usa la infraestructura disponible. | Pendiente de la infraestructura que autorice la Universidad. |
| Experiencia del estudiante | Un paso adicional: descargar y subir el PDF. | Simple; el reporte queda registrado al finalizar. |
| Experiencia docente | Debe organizar archivos recibidos. | Consulta centralizada y filtrable. |
| Tiempo a valor | Inmediato para el piloto de septiembre. | Posterior al piloto y a la decisión institucional. |
| Riesgo principal | Entrega del archivo equivocado o pérdida de organización. | Acceso no autorizado si se implementa sin controles adecuados. |

## Recomendación para la tutoría

Usar la alternativa A en el primer piloto de septiembre y presentar la
alternativa B como evolución recomendada. Antes de desarrollar la consulta
docente se debe validar con los tutores si la Universidad permite almacenar los
resultados fuera de Moodle y qué mecanismo de autenticación debe utilizarse.
