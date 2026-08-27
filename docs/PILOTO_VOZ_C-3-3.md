# Piloto de voz del ejercicio C-3-3

## Propósito

El laboratorio incorpora una señal real de voz como aplicación complementaria
de la convolución. No reemplaza las señales sintéticas aprobadas ni modifica la
evaluación o la nota del ejercicio.

## Configuración temporal

- Ubicación: después de los cuatro pasos guiados y antes de la evaluación.
- Participación: opcional durante el piloto.
- Duración analizada: máximo cinco segundos.
- Captura: micrófono, canal mono y frecuencia de muestreo de 16 kHz.
- Procesamiento: convolución con `h[n] = [1, -1, 2]`.
- Evidencia visual: forma de onda y espectro de la voz original y procesada.
- Evidencia auditiva: reproducción temporal de ambas señales.
- Calificación: no genera puntos ni modifica la nota.
- Almacenamiento: la voz no se escribe en JSON, PDF ni carpetas del proyecto.

El registro de la sesión conserva únicamente si el laboratorio se completó,
duración, frecuencia de muestreo, número de muestras, fecha de procesamiento y
si la grabación tuvo que limitarse a cinco segundos.

## Información para estudiantes

Antes de grabar, la interfaz informa que el navegador solicitará autorización
para usar el micrófono. El estudiante confirma que comprende que el audio se
procesa durante la sesión y no se almacena. Puede omitir el laboratorio y
continuar con la evaluación sin ninguna penalización.

Esta configuración es una decisión temporal para el piloto y debe discutirse
con los tutores. No constituye todavía una política institucional definitiva.

## Alternativas que deben revisar los tutores

### Mantener el procesamiento sin almacenamiento

Ventajas:

- reduce el tratamiento de datos personales;
- evita acumular archivos de audio;
- permite demostrar, visualizar y escuchar el efecto de la convolución;
- simplifica el piloto y su posterior adaptación a Moodle.

Limitación:

- el tutor no puede escuchar nuevamente una grabación después de cerrar la
  sesión.

### Conservar los archivos de voz

Ventaja:

- permite revisar posteriormente la evidencia auditiva completa.

Requisitos antes de habilitarla:

- consentimiento específico para almacenar la voz;
- definición de responsables y personas autorizadas;
- ubicación institucional segura;
- tiempo de conservación;
- procedimiento de eliminación;
- reglas para descarga, copia y uso académico;
- verificación de las capacidades de Moodle o de la infraestructura elegida.

## Preguntas para la decisión final

1. ¿La evaluación académica necesita escuchar nuevamente la grabación?
2. ¿Quién puede acceder a los archivos?
3. ¿Dónde se almacenarían?
4. ¿Durante cuánto tiempo?
5. ¿Cómo solicita un estudiante su eliminación?
6. ¿Qué ocurre si el estudiante no autoriza guardar su voz?
7. ¿Moodle ofrece el control de acceso y eliminación requerido?
