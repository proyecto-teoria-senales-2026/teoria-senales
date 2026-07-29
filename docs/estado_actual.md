# Decisiones y estado actual

Este documento deja por escrito qué se mantiene del planteamiento aprobado, qué partes ya funcionan en el piloto y cuáles decisiones técnicas siguen abiertas.

## Lo que se mantiene

1. El módulo conserva doce ejercicios, organizados en tres grupos de cuatro.
2. La voz se incorpora dentro de los cuatro ejercicios del Componente 3. No crea ejercicios adicionales ni reemplaza el trabajo con señales sintéticas.
3. El piloto corresponde al ejercicio C3-3 de convolución y conserva `x[n] = {1, 2, 1}`, `h[n] = {1, -1, 2}`, `N = 3` y `N = 5`.
4. El estudiante desarrolla el procedimiento y explica los resultados. La herramienta se utiliza para visualizar, verificar y comparar.
5. Los intentos, las correcciones y las ayudas se registran por cada paso.
6. Al finalizar el ejercicio se genera un reporte PDF. El estudiante no debe preparar otro archivo.
7. La evaluación del C3-3 utiliza cuatro preguntas autocalificables: dos
   numéricas, una de selección múltiple y una de verdadero/falso.
8. Las cuatro preguntas suman nueve puntos y producen una nota automática de
   `0,0` a `5,0`.

## Lo que ya funciona

- Cálculo de la convolución lineal.
- Verificación mediante DFT/FFT para `N = 3` y `N = 5`.
- Validación de cuatro pasos numéricos.
- Registro de la sesión en formato JSON.
- Seguimiento de intentos, correcciones y ayudas.
- Evaluación automática de cuatro preguntas sobre nueve puntos.
- Registro de las respuestas, el puntaje, la nota y los resultados por criterio.
- Pantalla inicial en Streamlit con ingreso del código estudiantil.
- Creación y conservación de la sesión durante la navegación.
- Guardado automático de la sesión al iniciar, responder o consultar una ayuda.
- Archivo independiente por intento, incluso cuando se repite el código
  estudiantil.
- Confirmación y guardado antes de volver a la pantalla inicial.
- Validación técnica del código estudiantil, sin asumir un formato
  institucional.
- Recuperación de la última sesión incompleta o creación voluntaria de un nuevo
  intento.
- Visualización numérica y gráfica de las señales `x[n]` y `h[n]`.
- Primer paso guiado para identificar `Lx`, `Lh` y `Ly`, con verificación,
  retroalimentación y registro de ayudas e intentos.
- Segundo paso guiado para calcular y comprobar la convolución lineal.
- Tercer paso guiado para verificar mediante DFT/FFT el caso `N = 3` y
  reconocer el solapamiento circular.
- Cuarto paso guiado para verificar mediante DFT/FFT el caso `N = 5` y
  comparar su resultado con la convolución lineal.
- Quinto paso integrado con las cuatro preguntas autocalificables, puntaje sobre
  nueve y nota automática de `0,0` a `5,0`.
- Cierre de la sesión al enviar la evaluación, con una sola evidencia por
  pregunta y resultado por criterio.
- Recuperación en pantalla de las respuestas, intentos y ayudas de los cuatro
  pasos numéricos.
- Configuración única de las señales y los resultados esperados del C3-3.
- Lectura de secuencias numéricas con corchetes, paréntesis, comas, punto y coma
  o espacios.
- Manejo de texto no numérico o respuestas vacías en los pasos 2, 3 y 4 sin
  interrumpir la aplicación ni alterar el historial con intentos vacíos.
- Entorno local reconstruido y verificable mediante `python -m pip check`.
- Generación del reporte PDF con resultados, gráficas y criterios.
- Pruebas automáticas del cálculo, la evaluación, la interfaz y los archivos
  generados.
- Uso de carpetas temporales para que las pruebas de interfaz no dejen sesiones
  ficticias en `session_outputs`.

## Lo que falta definir

- Permanencia de JSON o migración posterior a SQLite.
- Uso de archivo de audio, micrófono o ambas alternativas.
- Forma en que el docente consultará el reporte.
- Momento exacto en que se generará el PDF.
- Mecanismo de publicación y control de acceso para el piloto con estudiantes.
- Ajustes académicos que soliciten los tutores después de revisar el C3-3.
- Confirmación de la cantidad definitiva de preguntas para extender el banco
  después de validar la carga del piloto C3-3.

Estas decisiones se mantienen separadas del núcleo numérico. Así pueden ajustarse más adelante sin rehacer el cálculo ni las reglas del ejercicio aprobado.
