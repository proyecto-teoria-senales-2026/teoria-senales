# Software interactivo para Teoría de Señales

Recursos educativos interactivos para la asignatura Teoría de Señales del programa de Ingeniería Electrónica de la Universidad de Ibagué.

**Autores del trabajo de grado**

- Juan Esteban Rengifo Segura
- Julián Felipe Montaña Aguilar

## Ejercicios y uso en Moodle

La entrega reúne doce ejercicios, organizados en tres componentes de cuatro actividades. Los paquetes SCORM 1.2 están aprobados e incorporados al curso en Moodle, con sus respectivas guías del estudiante.

Cada carpeta de ejercicio contiene el código de la actividad, los recursos de interfaz, la guía y el manifiesto que identifica su archivo de inicio.

| Componente | Ejercicios | Código y guías |
|---|---|---|
| 1 | C-1-1, C-1-2, C-1-3 y C-1-4 | [C-1-1](scorm/c1-1/) · [C-1-2](scorm/c1-2/) · [C-1-3](scorm/c1-3/) · [C-1-4](scorm/c1-4/) |
| 2 | C-2-1, C-2-2, C-2-3 y C-2-4 | [C-2-1](scorm/c2-1/) · [C-2-2](scorm/c2-2/) · [C-2-3](scorm/c2-3/) · [C-2-4](scorm/c2-4/) |
| 3 | C-3-1, C-3-2, C-3-3 y C-3-4 | [C-3-1](scorm/c3-1/) · [C-3-2](scorm/c3-2/) · [C-3-3](scorm/c3-3/) · [C-3-4](scorm/c3-4/) |

## Descarga de paquetes

Los archivos de instalación se encuentran en [scorm/dist](scorm/dist/). Para cargar una actividad en Moodle se utiliza el ZIP correspondiente, sin descomprimirlo.

Los archivos `C1-1_SCORM_1.2.zip` a `C3-4_SCORM_1.2.zip` corresponden a las versiones aprobadas de los doce ejercicios. La carpeta conserva también paquetes identificados por su versión.

## Guías del estudiante

Las guías que acompañan la entrega se encuentran dentro de las carpetas de cada ejercicio:

| Componente 1 | Componente 2 | Componente 3 |
|---|---|---|
| [C-1-1](scorm/c1-1/guia_estudiante_C-1-1.pdf) | [C-2-1](scorm/c2-1/guia_estudiante_C-2-1.pdf) | [C-3-1](scorm/c3-1/guia_estudiante_C-3-1_V12.pdf) |
| [C-1-2](scorm/c1-2/guia_estudiante_C-1-2.pdf) | [C-2-2](scorm/c2-2/guia_estudiante_C-2-2.pdf) | [C-3-2](scorm/c3-2/guia_estudiante_C-3-2_V5.pdf) |
| [C-1-3](scorm/c1-3/guia_estudiante_C-1-3.pdf) | [C-2-3](scorm/c2-3/guia_estudiante_C-2-3.pdf) | [C-3-3](scorm/c3-3/guia_estudiante_C-3-3_V16.pdf) |
| [C-1-4](scorm/c1-4/guia_estudiante_C-1-4_V6.pdf) | [C-2-4](scorm/c2-4/guia_estudiante_C-2-4_V7.pdf) | [C-3-4](scorm/c3-4/guia_estudiante_C-3-4_V4.pdf) |

## Organización del desarrollo

- `scorm/c1-1/` a `scorm/c3-4/`: código y recursos de los doce ejercicios.
- `scorm/dist/`: paquetes ZIP para Moodle.
- `scorm/docs/`: inventario y registro técnico de versiones.
- `docs/`: documentación del proyecto y de etapas anteriores.
- `src/`, `pages/` y archivos Python de la raíz: prototipo previo desarrollado en Python y Streamlit.
- `tests/`: pruebas automatizadas del desarrollo.

Las guías y las instrucciones del prototipo previo se conservan como documentación de esa etapa. Para consultar las actividades entregadas en Moodle deben utilizarse las carpetas y las guías SCORM enlazadas arriba.

El historial del repositorio conserva la evolución del proyecto.
