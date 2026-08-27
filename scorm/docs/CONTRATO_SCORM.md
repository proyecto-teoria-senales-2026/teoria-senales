# Contrato técnico de cada paquete SCORM 1.2

Cada ejercicio se publica como un ZIP independiente. El archivo
`imsmanifest.xml` va en la raíz del ZIP y declara `index.html` como SCO.

## Datos enviados a Moodle

- `cmi.core.lesson_status`: `incomplete`, `passed` o `failed`.
- `cmi.core.score.min`, `max` y `raw`: escala institucional directa de `0` a
  `5` en todos los ejercicios, con aprobación desde `3`.
- `cmi.core.lesson_location`: porcentaje de avance.
- `cmi.suspend_data`: progreso mínimo para reanudar la actividad.
- `cmi.interactions`: identificador, tipo, respuesta, resultado y ponderación
  de las preguntas objetivas.
- `cmi.core.session_time`: duración de la sesión.

La nota visual institucional coincide con el valor enviado a Moodle. Los
resultados por criterio se conservan en escala porcentual de 0 a 100 dentro de
`cmi.objectives`.

## Límites y decisiones

`suspend_data` se reserva para estado compacto: etapa, selección aleatoria,
respuestas y avance. No guarda reportes PDF ni evidencia extensa. Cada paquete
corresponde a un ejercicio precisamente para mantener este estado reducido.

El registro de interacciones se usará para las preguntas objetivas que Moodle
puede mostrar al docente. Las respuestas numéricas se registran como `fill-in`
para conservar la secuencia ingresada; los detalles del procedimiento guiado se
mantienen además en el estado del intento y en la lógica propia de cada
actividad.

El paquete no requiere acceso a Internet ni carga bibliotecas desde CDNs.
