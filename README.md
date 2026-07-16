# Software interactivo para Teoría de Señales

Este repositorio reúne el desarrollo del proyecto de grado orientado a construir un software interactivo para la generación, el análisis espectral y la práctica guiada de señales discretas en la asignatura Teoría de Señales.

**Autores**

- Juan Esteban Rengifo Segura
- Julián Felipe Montaña Aguilar

**Programa:** Ingeniería Electrónica  
**Institución:** Universidad de Ibagué  
**Estado del proyecto:** arquitectura inicial y piloto funcional del ejercicio de convolución.

## Estado actual

La versión disponible implementa el núcleo del ejercicio **C3-3: Convolución lineal de señales discretas y verificación mediante DFT/FFT**. El ejercicio conserva las secuencias y longitudes de transformación aprobadas para el piloto.

El desarrollo permite:

- calcular la convolución lineal;
- verificar el resultado mediante DFT/FFT con `N = 3` y `N = 5`;
- validar cuatro pasos numéricos sin anticipar la respuesta completa;
- registrar intentos, correcciones y ayudas consultadas;
- guardar la sesión en un archivo JSON;
- generar un reporte PDF por estudiante y ejercicio;
- dejar las respuestas interpretativas para revisión del docente.

La interacción por consola es provisional. Su propósito es comprobar que el procesamiento, la validación, el seguimiento y la generación del reporte funcionan de forma independiente antes de definir la interfaz gráfica definitiva.

## Estructura del repositorio

```text
software-interactivo-teoria-senales/
├── main.py
├── requirements.txt
├── src/teoria_senales/
│   ├── app/                 # flujo provisional por consola
│   ├── domain/              # modelos de la sesión
│   ├── exercises/           # reglas del ejercicio C3-3
│   ├── feedback/            # retroalimentación progresiva
│   ├── reports/             # generación del reporte PDF
│   ├── signal_processing/   # convolución y DFT/FFT
│   ├── storage/             # persistencia JSON del piloto
│   └── tracking/            # intentos, ayudas y criterios
├── tests/                   # pruebas automatizadas
└── docs/                    # arquitectura, alcance y evidencias
```

## Instalación

Se requiere Python 3.11 o una versión posterior.

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
```

En Linux o macOS:

```bash
source .venv/bin/activate
```

Después se instalan las dependencias:

```bash
python -m pip install -r requirements.txt
```

## Ejecución

Para generar una sesión de demostración con datos ficticios:

```bash
python main.py --demo
```

Para recorrer el ejercicio desde la consola:

```bash
python main.py
```

Los archivos generados durante la ejecución se guardan en `demo_outputs/`. Esta carpeta no se publica porque puede contener información de sesiones de prueba.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas verifican los resultados numéricos de referencia, la validación de longitudes y la generación de los archivos JSON y PDF.

## Documentación

- [Arquitectura inicial del sistema](docs/Arquitectura_Inicial_Sistema.pdf)
- [Diagrama de arquitectura](docs/Diagrama_Arquitectura_Sistema.png)
- [Decisiones y estado del desarrollo](docs/estado_actual.md)
- [Reporte de demostración con datos ficticios](docs/evidencias/reporte_demostracion_C3-3.pdf)

## Límites actuales

Este repositorio no contiene todavía la interfaz gráfica final, la integración de voz ni los otros once ejercicios. También falta definir el mecanismo definitivo de almacenamiento, la forma de consulta del reporte y el nivel de automatización de los criterios interpretativos.

El código y la documentación se mantienen en un repositorio privado mientras se definen las condiciones institucionales de uso y distribución.
