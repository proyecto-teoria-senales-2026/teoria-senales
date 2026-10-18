# Estado de entrega SCORM al 18 de octubre de 2026

Los doce ejercicios están aprobados, cargados en Moodle y con QA completado, según la confirmación del equipo del proyecto. Esta rama consolida doce ZIP recuperados, con fuentes extraídas sin cambios, guías incluidas y huellas SHA-256.

- [Inventario y registro de consolidación](scorm/docs/CONSOLIDACION_2026-10-18.md).
- [Inventario verificable en JSON](scorm/docs/INVENTARIO_2026-10-18.json).
- [Paquetes de distribución](scorm/dist/).

C-2-3 V2 quedó incorporado con el ZIP aprobado adjuntado por el equipo el 18 de octubre. Los doce ejercicios cuentan con respaldo de paquetes y fuentes en esta rama.

Las carpetas `scorm/c1-1/` a `scorm/c3-4/` contienen las fuentes; el `imsmanifest.xml` de cada paquete identifica el HTML de lanzamiento vigente. El contenido siguiente describe el prototipo histórico Python/Streamlit y no sustituye el inventario SCORM de cierre.

---

# Software interactivo para Teoría de Señales

Este repositorio reúne el desarrollo del proyecto de grado orientado a construir un software interactivo para la generación, el análisis espectral y la práctica guiada de señales discretas en la asignatura Teoría de Señales.

**Autores**

- Juan Esteban Rengifo Segura
- Julián Felipe Montaña Aguilar

**Programa:** Ingeniería Electrónica  
**Institución:** Universidad de Ibagué  
**Estado del proyecto:** C-3-3 aprobado como patrón funcional; C-1-1, C-1-2, C-1-3 y C-1-4 integrados.

## Estado actual

La versión disponible conserva el ejercicio aprobado **C-3-3: Convolución lineal de señales discretas y verificación mediante DFT/FFT** e incorpora **C-1-1: Representación de señales fundamentales de tiempo discreto**, **C-1-2: Características de las señales discretas**, **C-1-3: Coeficientes y espectro de la serie de Fourier** y **C-1-4: Reconstrucción de Fourier y fenómeno de Gibbs**.

El desarrollo permite:

- acceder a C-1-1, C-1-2, C-1-3, C-1-4 y C-3-3 desde la misma aplicación multipágina;
- desarrollar C-1-1 mediante cuatro pasos guiados y una evaluación final;
- visualizar impulso, escalón, rampa, exponencial y senoidal;
- consultar dentro de C-1-1 la guía breve del estudiante y descargar su PDF;
- seleccionar para C-1-1 cinco preguntas reproducibles por sesión desde un
  banco de quince;
- desarrollar C-1-2 mediante cuatro pasos guiados sobre paridad,
  periodicidad, duración, energía y potencia;
- seleccionar para C-1-2 cinco preguntas reproducibles por sesión desde un
  banco independiente de quince;
- desarrollar C-1-3 mediante cuatro pasos guiados sobre periodo, frecuencia
  fundamental, coeficientes trigonométricos y espectros de amplitud y fase;
- calcular los resultados de C-1-3 desde funciones matemáticas comunes y
  reconstruir el pulso rectangular con cinco armónicos;
- seleccionar para C-1-3 cinco preguntas reproducibles por sesión desde un
  banco independiente de quince;
- desarrollar C-1-4 mediante cuatro pasos guiados sobre discontinuidades,
  sumas parciales, error cuadrático medio y fenómeno de Gibbs;
- comparar reconstrucciones para `N = 1`, `N = 5` y `N = 15`;
- calcular el error mediante Parseval y el sobreimpulso límite desde la
  integral seno;
- seleccionar para C-1-4 cinco preguntas reproducibles por sesión desde un
  banco independiente de quince;

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
- visualizar las señales de entrada de C-3-3 como secuencias y gráficas discretas;
- desarrollar y verificar el reconocimiento de longitudes desde la interfaz;
- calcular la convolución lineal desde la interfaz y comprobar su gráfica;
- verificar mediante DFT/FFT los casos `N = 3` y `N = 5`;
- comparar visualmente el resultado circular con la convolución lineal;
- calificar automáticamente ocho preguntas sobre dieciocho puntos;
- guardar la sesión en un archivo JSON;
- generar un reporte docente corto y protegido por estudiante, ejercicio e
  intento, con un código de verificación asociado al registro original;
- calcular una nota automática de `0,0` a `5,0`;
- grabar hasta cinco segundos de voz como laboratorio piloto opcional;
- convolucionar la voz con `h[n] = [1, -1, 2]` y comparar las señales original
  y procesada de forma visual y auditiva;
- registrar únicamente metadatos técnicos del laboratorio, sin almacenar el
  archivo de voz ni modificar la nota.

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
├── pages/                  # ejercicios adicionales de la aplicación
├── main.py
├── requirements.txt
├── src/teoria_senales/
│   ├── app/                 # flujo provisional por consola
│   ├── domain/              # modelos de la sesión
│   ├── exercises/           # reglas de los ejercicios integrados
│   ├── feedback/            # retroalimentación progresiva
│   ├── reports/             # generación del reporte PDF
│   ├── signal_processing/   # convolución y DFT/FFT
│   ├── storage/             # persistencia JSON del piloto
│   └── tracking/            # intentos, ayudas y criterios
├── tests/                   # pruebas automatizadas
└── docs/                    # arquitectura, alcance y evidencias
```

## Instalación

Se requiere Python 3.12 o 3.13.

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
python run_tests.py
```

Las pruebas verifican los resultados numéricos de referencia, la evaluación
automática, el inicio de la sesión desde la interfaz y la generación de los
archivos JSON y PDF. Las pruebas de interfaz usan carpetas temporales y no dejan
sesiones ficticias en `session_outputs/`. El ejecutor agrega automáticamente la
carpeta `src` a la ruta de Python, por lo que el mismo comando funciona en
Windows, Linux y macOS.

## Verificador docente

El reporte incorpora metadatos de integridad y una huella SHA-256 de su
contenido visible. Para verificar un archivo recibido contra el JSON original:

```bash
python verificar_reporte.py reporte.pdf --sessions session_outputs
```

En Windows también se puede arrastrar el PDF sobre `VERIFICAR_REPORTE.bat`.
`DEMOSTRAR_VERIFICADOR.bat` ejecuta la evidencia incluida: el reporte original
debe aparecer como `VÁLIDO` y la copia modificada como `ALTERADO O NO VÁLIDO`.

## Documentación

- [Arquitectura inicial del sistema](docs/Arquitectura_Inicial_Sistema.pdf)
- [Diagrama de arquitectura](docs/Diagrama_Arquitectura_Sistema.png)
- [Decisiones y estado del desarrollo](docs/estado_actual.md)
- [Piloto de voz C-3-3 y decisión para tutores](docs/PILOTO_VOZ_C-3-3.md)
- [Reporte de demostración con datos ficticios](docs/evidencias/reporte_demostracion_C3-3.pdf)
- [Guía del estudiante C-1-1](docs/guias/Guia_del_estudiante_C-1-1.pdf)
- [Guía del estudiante C-1-2](docs/guias/Guia_del_estudiante_C-1-2.pdf)
- [Guía del estudiante C-1-3](docs/guias/Guia_del_estudiante_C-1-3.pdf)
- [Guía del estudiante C-1-4](docs/guias/Guia_del_estudiante_C-1-4.pdf)
- [Guía del estudiante C-3-3](docs/guias/Guia_del_estudiante_C-3-3.pdf)

Las guías técnicas del docente se distribuyen por separado porque contienen
procedimientos resueltos y respuestas que no deben quedar visibles en la
aplicación estudiantil.
- [Reporte original para comprobar](docs/evidencias/verificacion/reporte_original_valido_C-3-3.pdf)
- [Copia alterada para comprobar](docs/evidencias/verificacion/reporte_copia_alterada_C-3-3.pdf)
- [Resultado de la demostración del verificador](docs/evidencias/verificacion/resultado_verificacion.txt)

## Límites actuales

El primer avance del generador de señales está integrado como un explorador
visual posterior a la evaluación. Permite ingresar dos secuencias discretas,
elegir la longitud de transformación y comparar la convolución lineal con el
resultado obtenido mediante DFT/FFT, sin modificar la sesión ni la nota.

El repositorio incorpora el primer laboratorio piloto de voz en C-3-3, pero no contiene todavía los otros siete
ejercicios. El verificador local de integridad ya funciona sin base de datos.
Una firma digital institucional continúa pendiente porque requiere una clave
privada oficial y una política institucional de custodia; el sistema no presenta
la huella SHA-256 como si fuera una firma certificada.

El código y la documentación se mantienen en un repositorio privado mientras se definen las condiciones institucionales de uso y distribución.

