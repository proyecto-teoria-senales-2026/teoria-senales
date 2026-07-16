# Decisiones y estado actual

Este documento deja por escrito qué se mantiene del planteamiento aprobado, qué partes ya funcionan en el piloto y cuáles decisiones técnicas siguen abiertas.

## Lo que se mantiene

1. El módulo conserva doce ejercicios, organizados en tres grupos de cuatro.
2. La voz se incorpora dentro de los cuatro ejercicios del Componente 3. No crea ejercicios adicionales ni reemplaza el trabajo con señales sintéticas.
3. El piloto corresponde al ejercicio C3-3 de convolución y conserva `x[n] = {1, 2, 1}`, `h[n] = {1, -1, 2}`, `N = 3` y `N = 5`.
4. El estudiante desarrolla el procedimiento y explica los resultados. La herramienta se utiliza para visualizar, verificar y comparar.
5. Los intentos, las correcciones y las ayudas se registran por cada paso.
6. Al finalizar el ejercicio se genera un reporte PDF. El estudiante no debe preparar otro archivo.
7. Los resultados numéricos se comprueban automáticamente. Las respuestas conceptuales y la conclusión quedan para revisión del docente.

## Lo que ya funciona

- Cálculo de la convolución lineal.
- Verificación mediante DFT/FFT para `N = 3` y `N = 5`.
- Validación de cuatro pasos numéricos.
- Registro de la sesión en formato JSON.
- Seguimiento de intentos, correcciones y ayudas.
- Generación del reporte PDF con resultados, gráficas y criterios.
- Pruebas automáticas del cálculo y de los archivos generados.

## Lo que falta definir

- Tecnología de la interfaz gráfica.
- Permanencia de JSON o migración posterior a SQLite.
- Uso de archivo de audio, micrófono o ambas alternativas.
- Forma en que el docente consultará el reporte.
- Momento exacto en que se generará el PDF.
- Criterios interpretativos que podrían automatizarse sin reemplazar la revisión docente.

Estas decisiones se mantienen separadas del núcleo numérico. Así pueden ajustarse más adelante sin rehacer el cálculo ni las reglas del ejercicio aprobado.
