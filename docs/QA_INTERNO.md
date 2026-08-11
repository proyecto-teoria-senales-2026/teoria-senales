# QA interno obligatorio

Cada iteración del software se cierra únicamente cuando cumple estas capas:

1. **Núcleo matemático:** resultados de referencia y casos límite.
2. **Nomenclatura:** los textos visibles usan la misma convención en enunciados,
   ayudas, preguntas, retroalimentación y reportes.
3. **Regresión:** C-3-3 conserva los cálculos, la evaluación, las sesiones y el PDF
   previamente aprobados.
4. **Interfaz:** recorrido completo del ejercicio, errores de entrada y recuperación
   de sesión.
5. **Windows:** ZIP extraído completamente, una sola carpeta raíz
   `teoria-senales-app` e inicio mediante `INICIAR_APLICACION.bat`.
6. **Evidencia:** cantidad de pruebas ejecutadas, resultado y hallazgos pendientes.

## Corte de la iteración C-1-1

- 83 pruebas automáticas aprobadas, incluidas las pruebas de interfaz.
- Flujo C1-1 probado de extremo a extremo en el dominio: cuatro pasos,
  evaluación aleatoria, criterios, persistencia y PDF protegido.
- Regresión C-3-3 aprobada.
- Exponencial causal unificada como `x[n] = (1/2)^n u[n]` en la fuente
  matemática, la gráfica, la interfaz, el banco y ambas guías.
- Valores esperados de los cuatro pasos calculados desde las funciones de
  señales, sin duplicar manualmente los resultados numéricos en la validación.
- Banco completo verificado: `C1-1-P01` a `C1-1-P15`, con tres preguntas de
  selección múltiple y dos de verdadero/falso por sesión.
- Criterios verificados: `C1_1_CR1`, `C1_1_CR2` y `C1_1_CR3`.
- Guía del estudiante C-1-1 renderizada y revisada visualmente en dos páginas.
- Guía técnica del docente C-1-1 con la estructura completa de 19 apartados,
  renderizada y revisada visualmente en seis páginas.
- Encabezado gráfico institucional y estructura documental verificados por dos
  pruebas automáticas nuevas.
- Fórmulas, títulos de los pasos y nomenclatura cruzados entre código y guías.
- La aplicación conserva C-1-1 y C-3-3 integrados; no se libera un instalador en
  este corte.

No se considera válida una prueba ejecutada desde la vista interna del archivo ZIP.

## Corte de la iteración C-1-2

- 71 pruebas automáticas aprobadas en este entorno y 23 pruebas de interfaz
  omitidas porque Streamlit no está instalado; no se cuentan como aprobadas.
- Núcleo matemático verificado para paridad, energía y potencia periódica.
- Cuatro pasos guiados y sesión C1-2 integrados a la aplicación existente.
- Banco verificado: `C1-2-P01` a `C1-2-P15`.
- Criterios verificados: `C1_2_CR1`, `C1_2_CR2` y `C1_2_CR3`.
- Guía del estudiante C-1-2 renderizada y revisada visualmente en dos páginas.
- Guía técnica del docente C-1-2, con 19 apartados y banco completo, renderizada
  y revisada visualmente en siete páginas.
- Reporte PDF protegido probado de extremo a extremo.
- C-1-1 y C-3-3 conservan sus pruebas de regresión aprobadas.

## Corte de la iteración C-1-3

- 82 pruebas automáticas aprobadas y 23 pruebas de interfaz omitidas porque
  Streamlit no está instalado en este entorno.
- Núcleo matemático verificado para `T₀`, `ω₀`, `a₀`, `aₙ`, `bₙ`, amplitud,
  fase y reconstrucción temporal.
- La convención quedó declarada de forma uniforme como
  `x(t) = a₀/2 + Σ[aₙ cos(nω₀t) + bₙ sen(nω₀t)]`.
- Cuatro pasos guiados y sesión C1-3 integrados a la aplicación existente.
- Banco verificado: `C1-3-P01` a `C1-3-P15`.
- Criterios verificados: `C1_3_CR1`, `C1_3_CR2` y `C1_3_CR3`.
- Guía del estudiante C-1-3 renderizada y revisada visualmente en dos páginas.
- Guía técnica del docente C-1-3, con 19 apartados y banco completo,
  renderizada y revisada visualmente en siete páginas.
- Reporte PDF protegido probado de extremo a extremo.
- C-1-1, C-1-2 y C-3-3 conservan sus pruebas de regresión aprobadas en las
  capas ejecutables del entorno.
- Las 23 pruebas de interfaz deben ejecutarse en el entorno completo antes de
  afirmar que el corte pasó sin omisiones.

## Corte integrado C-1-1 a C-1-4 y C-3-3

- 120 pruebas ejecutadas y aprobadas en el entorno completo; cero omisiones.
- Las 23 pruebas de interacción Streamlit se ejecutaron de forma efectiva.
- C-1-4 integrado con reconstrucción para `N = 1, 5, 15`, ECM por Parseval,
  fenómeno de Gibbs, banco de 15 preguntas, criterios y PDF.
- Nomenclatura visible unificada: `C-1-1` a `C-1-4` y `C-3-3`.
- Nomenclatura de C-3-3 unificada: preguntas `C3-3-P01` a `C3-3-P08` y
  criterios `C3_3_CR1` a `C3_3_CR6`.
- Guías del estudiante y técnicas del docente de C-3-3 renderizadas y revisadas
  visualmente en dos y cinco páginas.
- Reporte PDF con metadatos de integridad y huella SHA-256.
- Verificador docente probado contra el JSON original: reporte original
  `VÁLIDO`; copia modificada `ALTERADO O NO VÁLIDO`.
- La verificación implementada no se presenta como firma digital institucional;
  esa firma requiere una clave oficial y una política de custodia.
