# Alcance del avance para la tutoría del 17 de julio de 2026

Este documento resume las decisiones que delimitan la primera implementación. Su función es mantener la trazabilidad entre la matriz de ejercicios, la guía del estudiante, la arquitectura y el código disponible en el repositorio.

## Decisiones vigentes

1. El módulo conserva doce ejercicios, distribuidos en la estructura 4 + 4 + 4.
2. La incorporación de voz se plantea dentro de los cuatro ejercicios del Componente 3; no crea ejercicios adicionales ni reemplaza el trabajo con señales sintéticas.
3. El piloto corresponde al ejercicio C3-3 de convolución y conserva `x[n] = {1, 2, 1}`, `h[n] = {1, -1, 2}`, `N = 3` y `N = 5`.
4. El estudiante desarrolla el procedimiento y realiza la interpretación. La herramienta apoya la visualización, la verificación y la comparación de resultados.
5. El sistema registra intentos, correcciones y ayudas por paso.
6. Al finalizar, el sistema genera un reporte PDF por estudiante y ejercicio; el estudiante no prepara un archivo adicional.
7. Las comprobaciones numéricas pueden automatizarse. Las respuestas conceptuales y la conclusión permanecen disponibles para revisión docente.

## Implementado en el piloto

- Cálculo de la convolución lineal.
- Verificación mediante DFT/FFT para `N = 3` y `N = 5`.
- Validación de cuatro pasos numéricos.
- Registro estructurado de la sesión en JSON.
- Seguimiento de intentos, correcciones y ayudas.
- Generación de un reporte PDF con resultados, gráficas y criterios.
- Pruebas automatizadas del núcleo numérico y del flujo de evidencia.

## Pendiente de validación con los tutores

- Tecnología de la interfaz gráfica.
- Uso de JSON únicamente en el piloto o migración posterior a SQLite.
- Captura de voz mediante archivo, micrófono o ambas alternativas.
- Forma de acceso del docente al reporte generado.
- Momento exacto de generación del PDF.
- Nivel de automatización aceptable para los criterios interpretativos.

Estas decisiones pendientes no se presentan como funciones terminadas. La arquitectura las mantiene separadas para que puedan definirse sin modificar el núcleo numérico ya comprobado.
