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
- iniciar una sesión desde una interfaz gráfica con el código estudiantil;
- guardar la sesión desde el inicio y después de cada interacción;
- conservar intentos separados aunque se repita el código estudiantil;
- recuperar la última sesión incompleta o iniciar voluntariamente un nuevo
  intento;
- validar el código estudiantil con reglas técnicas de longitud y caracteres,
  sin asumir un formato institucional;
- visualizar las señales de entrada del C3-3 como secuencias y gráficas discretas;
- desarrollar y verificar el reconocimiento de longitudes desde la interfaz;
- calcular la convolución lineal desde la interfaz y comprobar su gráfica;
- verificar mediante DFT/FFT los casos `N = 3` y `N = 5`;
- comparar visualmente el resultado circular con la convolución lineal;
- calificar automáticamente ocho preguntas sobre dieciocho puntos;
- guardar la sesión en un archivo JSON;
- generar un reporte docente corto y protegido por estudiante, ejercicio e
  intento, con un código de verificación asociado al registro original;
- calcular una nota automática de `0,0` a `5,0`.

La interacción por consola se conserva como apoyo para las pruebas. La interfaz
gráfica ya permite desarrollar los cuatro pasos numéricos, responder la
evaluación de ocho preguntas y revisar la calificación antes del envío
definitivo. Al terminar, muestra el resultado por criterio y permite descargar
el reporte docente protegido. Los avances se guardan después de cada
interacción.

## Estructura del repositorio

```text
software-interactivo-teoria-senales/
├── app.py                  # entrada de la interfaz Streamlit
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

El entorno `.venv` es local y no debe copiarse de otro computador. En el equipo
que se usará para la presentación se crea nuevamente con:

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
python -m pip check
```

El último comando debe responder `No broken requirements found.` antes de abrir
la aplicación.

## Ejecución

Para abrir la interfaz gráfica:

```bash
python -m streamlit run app.py
```

La aplicación se abre en el navegador. Si no se abre automáticamente, se puede
ingresar a `http://localhost:8501`.

Para generar una sesión de demostración con datos ficticios:

```bash
python main.py --demo
```

Para recorrer el ejercicio desde la consola:

```bash
python main.py
```

Los archivos generados durante la ejecución se guardan en `demo_outputs/`. Esta carpeta no se publica porque puede contener información de sesiones de prueba.

Las sesiones iniciadas desde la interfaz se guardan en `session_outputs/`.
Cada intento utiliza un identificador propio para evitar que un archivo anterior
sea reemplazado.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas verifican los resultados numéricos de referencia, la evaluación
automática, el inicio de la sesión desde la interfaz y la generación de los
archivos JSON y PDF. Las pruebas de interfaz usan carpetas temporales y no dejan
sesiones ficticias en `session_outputs/`.

## Documentación

- [Arquitectura inicial del sistema](docs/Arquitectura_Inicial_Sistema.pdf)
- [Diagrama de arquitectura](docs/Diagrama_Arquitectura_Sistema.png)
- [Decisiones y estado del desarrollo](docs/estado_actual.md)
- [Reporte de demostración con datos ficticios](docs/evidencias/reporte_demostracion_C3-3.pdf)

## Límites actuales

El primer avance del generador de señales está integrado como un explorador
visual posterior a la evaluación. Permite ingresar dos secuencias discretas,
elegir la longitud de transformación y comparar la convolución lineal con el
resultado obtenido mediante DFT/FFT, sin modificar la sesión ni la nota.

El repositorio no contiene todavía la
integración de voz ni los otros once ejercicios. También falta definir el
mecanismo definitivo de almacenamiento y el canal institucional para recibir y
consultar los reportes.

El código y la documentación se mantienen en un repositorio privado mientras se definen las condiciones institucionales de uso y distribución.
