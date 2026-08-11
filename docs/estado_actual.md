# Decisiones y estado actual

Este documento deja por escrito qué se mantiene del planteamiento aprobado, qué partes ya funcionan en el piloto y cuáles decisiones técnicas siguen abiertas.

## Lo que se mantiene

1. El módulo conserva doce ejercicios, organizados en tres grupos de cuatro.
2. La voz se incorpora dentro de los cuatro ejercicios del Componente 3. No crea ejercicios adicionales ni reemplaza el trabajo con señales sintéticas.
3. El piloto corresponde al ejercicio C-3-3 de convolución y conserva `x[n] = {1, 2, 1}`, `h[n] = {1, -1, 2}`, `N = 3` y `N = 5`.
4. El estudiante desarrolla el procedimiento e interpreta los resultados durante
   el recorrido guiado. La herramienta se utiliza para visualizar, verificar y
   comparar. La evaluación y la nota final se obtienen únicamente mediante los
   tres formatos autocalificables aprobados: respuesta numérica, selección
   múltiple y verdadero/falso; no se solicitan respuestas abiertas.
5. Los intentos, las correcciones y las ayudas se registran por cada paso.
6. Al finalizar el ejercicio se genera un reporte PDF. El estudiante no debe preparar otro archivo.
7. La evaluación de C-3-3 utiliza ocho preguntas autocalificables: cuatro
   numéricas, dos de selección múltiple y dos de verdadero/falso.
8. Las ocho preguntas suman dieciocho puntos y producen una nota automática de
   `0,0` a `5,0`.

## Lo que ya funciona

### C-1-1

- Página integrada en la aplicación multipágina.
- Guía breve del estudiante visible dentro del ejercicio.
- Guía completa del estudiante disponible como PDF descargable.
- Guía técnica/docente externa con respuestas y controles, no visible para el estudiante.
- Representación gráfica de impulso, escalón, rampa, exponencial y senoidal.
- Cuatro pasos guiados con intentos, orientaciones, retroalimentación y recuperación.
- Banco de quince preguntas y selección reproducible por sesión de tres de
  selección múltiple y dos de verdadero/falso.
- Nota automática de `0,0` a `5,0`, criterios C1_1_CR1 a C1_1_CR3 y reporte PDF.

### C-1-2

- Página integrada en la misma aplicación multipágina.
- Cuatro pasos guiados sobre paridad, periodicidad, duración, energía y potencia.
- Cálculos de energía y potencia realizados desde funciones matemáticas comunes.
- Banco independiente de quince preguntas con selección reproducible de cinco por sesión.
- Nota automática de `0,0` a `5,0`, criterios C1_2_CR1 a C1_2_CR3 y reporte PDF.
- Guía del estudiante C-1-2 descargable y guía técnica del docente C-1-2 externa.

### C-1-3

- Página integrada en la misma aplicación multipágina.
- Pulso rectangular par definido con `T₀ = 2π`, amplitud 1 y ancho activo π.
- Cálculo por fórmula de `ω₀`, `a₀`, `aₙ`, `bₙ`, amplitudes y fases.
- Cuatro pasos guiados y reconstrucción temporal con cinco armónicos.
- Banco independiente de quince preguntas con selección reproducible de cinco por sesión.
- Nota automática de `0,0` a `5,0`, criterios C1_3_CR1 a C1_3_CR3 y reporte PDF.
- Guía del estudiante C-1-3 descargable y guía técnica del docente C-1-3 externa.

### C-1-4

- Página integrada en la misma aplicación multipágina.
- Continuidad del pulso rectangular de C-1-3 para comparar sumas parciales.
- Reconstrucciones calculadas para `N = 1`, `N = 5` y `N = 15`.
- Error cuadrático medio calculado mediante la relación de Parseval.
- Sobreimpulso límite de Gibbs calculado desde `Si(π)/π − 1/2`.
- Cuatro pasos guiados con intentos, orientaciones y retroalimentación.
- Banco independiente de quince preguntas con selección reproducible de cinco por sesión.
- Nota automática de `0,0` a `5,0`, criterios C1_4_CR1 a C1_4_CR3 y reporte PDF.
- Guía del estudiante C-1-4 descargable y guía técnica del docente C-1-4 externa.

### C-3-3

- Cálculo de la convolución lineal.
- Verificación mediante DFT/FFT para `N = 3` y `N = 5`.
- Validación de cuatro pasos numéricos.
- Registro de la sesión en formato JSON.
- Seguimiento de intentos, correcciones y ayudas.
- Evaluación automática de ocho preguntas sobre dieciocho puntos.
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
- Explorador visual posterior a la evaluación para probar otras secuencias,
  elegir `N` y comparar la convolución lineal con el resultado DFT/FFT.
- Primer paso guiado para identificar `Lx`, `Lh` y `Ly`, con verificación,
  retroalimentación y registro de ayudas e intentos.
- Segundo paso guiado para calcular y comprobar la convolución lineal.
- Tercer paso guiado para verificar mediante DFT/FFT el caso `N = 3` y
  reconocer el solapamiento circular.
- Cuarto paso guiado para verificar mediante DFT/FFT el caso `N = 5` y
  comparar su resultado con la convolución lineal.
- Quinto paso integrado con las ocho preguntas autocalificables, puntaje sobre
  dieciocho y nota automática de `0,0` a `5,0`.
- Cierre de la sesión al enviar la evaluación, con una sola evidencia por
  pregunta y resultado por criterio.
- Presentación de un solo paso activo, con los pasos terminados organizados en
  resúmenes plegables.
- Ocultamiento de resultados y explicaciones del recorrido guiado mientras la
  evaluación está activa.
- Revisión de las ocho respuestas antes de confirmar la calificación.
- Registro de una sola consulta por orientación, aunque el control se active
  nuevamente.
- Recuperación en pantalla de las respuestas, intentos y ayudas de los cuatro
  pasos numéricos.
- Configuración única de las señales y los resultados esperados de C-3-3.
- Lectura de secuencias numéricas con corchetes, paréntesis, comas, punto y coma
  o espacios.
- Manejo de texto no numérico o respuestas vacías en los pasos 2, 3 y 4 sin
  interrumpir la aplicación ni alterar el historial con intentos vacíos.
- Entorno local reconstruido y verificable mediante `python -m pip check`.
- Generación del reporte docente corto y protegido con código estudiantil,
  código de sesión, código de verificación, RAE, puntaje, nota y resultado por
  criterio.
- Descarga del reporte docente al finalizar la evaluación.
- Guía del estudiante C-3-3 descargable y guía técnica del docente C-3-3 externa.
- Preguntas `C3-3-P01` a `C3-3-P08` y criterios `C3_3_CR1` a `C3_3_CR6`.
- Metadatos de integridad y huella SHA-256 incorporados al reporte.
- Verificador docente local que compara metadatos y contenido contra el JSON original.
- Evidencia reproducible con un reporte válido y una copia alterada detectada.
- Pruebas automáticas del cálculo, la evaluación, la interfaz y los archivos
  generados.
- Uso de carpetas temporales para que las pruebas de interfaz no dejen sesiones
  ficticias en `session_outputs`.

## Lo que falta definir

- Firma digital institucional con clave privada oficial y política de custodia.
- Uso de archivo de audio, micrófono o ambas alternativas.
- Elección institucional entre la entrega del PDF en Moodle y la consulta del
  registro original por código de sesión.
- Mecanismo de publicación y control de acceso para el piloto con estudiantes.
- Ajustes académicos que soliciten los tutores después de revisar C-3-3.

Estas decisiones se mantienen separadas del núcleo numérico. Así pueden ajustarse más adelante sin rehacer el cálculo ni las reglas del ejercicio aprobado.
