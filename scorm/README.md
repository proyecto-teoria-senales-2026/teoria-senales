# Migración SCORM para Moodle

Esta carpeta contiene la futura versión web de los ejercicios de Teoría de
Señales. La aplicación actual en Python y Streamlit se conserva sin cambios
como referencia funcional, de pruebas y de generación/verificación de reportes.

## Estructura propuesta

Cada ejercicio se distribuye como una actividad SCORM 1.2 independiente y se
ubica en el componente correspondiente dentro del curso oficial de Teoría de
Señales en Moodle:

```text
Componente 1
├── C-1-1 — paquete SCORM
├── C-1-2 — paquete SCORM
├── C-1-3 — paquete SCORM
└── C-1-4 — paquete SCORM

Componente 3
└── C-3-3 — paquete SCORM
```

La separación permite que Moodle conserve por ejercicio los intentos, el
avance, la finalización, la nota y las interacciones reportadas.

## Alcance en preparación

1. Motor común de comunicación SCORM 1.2.
2. Guardado y reanudación de un intento por actividad.
3. Registro de puntaje, estado, fecha de inicio y tiempo de sesión.
4. Registro de interacciones para preguntas de selección múltiple, verdadero/
   falso y valores numéricos.
5. Paquetes autocontenidos: sin dependencias de CDNs externas.
6. Migración de C-1-1 a C-1-4 y C-3-3 desde las reglas aprobadas en `src/`.

## Avance de la migración

1. **Completado:** C-3-3 fue homologado con el modelo de evaluación: conserva
   sus cuatro verificaciones numéricas guiadas, cuenta con un banco conceptual
   de quince preguntas y selecciona aleatoriamente tres de selección múltiple y
   dos de verdadero/falso por sesión. La selección se conserva al recuperar un
   intento mediante el identificador de sesión.
2. **Completado:** se creó el runtime común SCORM 1.2 en
   `shared/scorm12-runtime.js`. Este registra avance, guardado/reanudación,
   puntaje, estado, tiempo de sesión e interacciones objetivas, sin CDNs.
3. **Completado:** C-1-1 cuenta con su paquete independiente en
   `dist/C1-1_SCORM_1.2.zip`. Conserva cuatro pasos guiados, una orientación
   por paso, el banco de quince preguntas y la selección reproducible de tres
   preguntas de selección múltiple y dos de verdadero/falso. El paquete ya
   superó la validación local de manifiesto, estado, interacciones y nota.
4. **En curso:** migrar C-1-2 a C-1-4 y C-3-3 a paquetes independientes usando
   el mismo runtime.
5. Iniciar el Componente 2 únicamente después de asegurar esas entregas.

## Modelo de C-3-3

El ejercicio conserva:

- cuatro verificaciones numéricas guiadas;
- un banco conceptual de quince preguntas;
- por intento, tres preguntas de selección múltiple y dos de verdadero/falso;
- nota normalizada de `0,0` a `5,0` a partir de veinte puntos.

La implementación usa la semilla de la sesión para que una recuperación no
cambie las preguntas ya asignadas.

## Secuencia base

1. Mantener C-3-3 con el modelo de evaluación aprobado para los ejercicios:
   conservar sus cuatro pasos numéricos guiados, ampliar el banco conceptual a
   quince preguntas y seleccionar aleatoriamente tres de selección múltiple y
   dos de verdadero/falso por intento.
2. Mantener la escala y los criterios de C-3-3 parametrizables hasta la
   definición institucional de calificación.
3. Construir el motor común SCORM usando ese modelo de guardado, interacción y
   evaluación.
4. Migrar C-1-1 a C-1-4 y, sobre la misma base, empaquetar C-3-3.
5. Iniciar el Componente 2 únicamente después de asegurar esas entregas.

## Repositorio y distribución

GitHub conserva las fuentes de Streamlit, las fuentes SCORM, los bancos de
preguntas, manifiestos, scripts de empaquetado, documentación y pruebas. Los
ZIP listos para Moodle se generan desde dichas fuentes y se distribuyen como
versiones de entrega; no sustituyen al código fuente ni al historial de Git.

El repositorio permanece privado. Ninguna credencial de Moodle se almacena en
GitHub ni se comparte con el desarrollo.

## Decisiones pendientes de tutoría

- Escala final de la actividad: 0–5 o 0–100.
- Nota mínima aprobatoria.
- Rol definitivo del reporte PDF cifrado y del verificador local frente a los
  reportes de Moodle.

Hasta contar con esa decisión, estas variables se mantendrán parametrizables;
no se eliminará el flujo actual de PDF, JSON ni `VERIFICAR_REPORTE.bat`.

## Carga y validación institucional

El equipo estudiantil coordina con el tutor la carga de los ZIP en Moodle. El
desarrollo entrega los paquetes y el protocolo de pruebas; no requiere ni debe
recibir credenciales institucionales.
