# Protocolo de QA para paquetes SCORM

Un paquete no se considera aprobado por abrir localmente. Debe superar una
prueba local y una prueba de aceptación dentro de Moodle.

## Prueba local

- El ZIP contiene `imsmanifest.xml` en su raíz.
- El manifiesto declara una actividad SCORM 1.2 y todos los archivos internos.
- La actividad abre sin Internet ni recursos CDN externos.
- Las fórmulas, gráficas y ayudas coinciden con el ejercicio aprobado.
- La aleatoriedad respeta el banco y el número de preguntas definido.
- Las respuestas numéricas, de selección múltiple y verdadero/falso se
  califican correctamente.
- El avance se guarda, se recupera y no salta etapas al reanudar.
- La actividad no muestra referencias ni marcas de IA.

### C-1-1 — resultado de la revisión local

- Paquete generado: `scorm/dist/C1-1_SCORM_1.2.zip`.
- `imsmanifest.xml` está en la raíz del ZIP, declara un único SCO y lista todos
  sus archivos.
- No hay recursos externos ni dependencias de CDN.
- Se comprobó el runtime con una API SCORM simulada: inicialización, lectura
  de estudiante, guardado, reanudación, avance, interacción, resultados por
  criterio, calificación y cierre.
- El estado del intento conserva fecha/hora de inicio y de finalización. Moodle
  registra adicionalmente la marca de tiempo oficial del intento para la
  consulta docente.
- Se validó el banco aprobado: quince preguntas disponibles y, por intento,
  tres de selección múltiple y dos de verdadero/falso.
- Pendiente institucional: la prueba de aceptación dentro de Moodle, que
  realizará el equipo estudiantil con el tutor.

## Prueba en Moodle

El equipo que realice la carga debe registrar evidencia desde un perfil de
estudiante y uno docente:

1. Actividad cargada dentro del componente correcto.
2. Inicio de intento con nombre del estudiante de Moodle.
3. Guardado del avance al cerrar y reanudación posterior.
4. Calificación final y estado de finalización.
5. Fecha y tiempo de realización.
6. Reporte de intentos desde el perfil docente.
7. Reporte de interacciones con respuesta, resultado y criterio cuando Moodle
   lo soporte.
8. Segundo intento, si la configuración institucional lo permite.

## Criterio de aceptación

La evidencia debe permitir comprobar que la nota que visualiza el estudiante
coincide con la que Moodle registra. Cualquier divergencia bloquea la entrega
del paquete hasta su corrección.

## Distribución

El ZIP listo para cargar se conserva en `scorm/dist/`; las fuentes permanecen en `scorm/c1-1/` para trazabilidad y mantenimiento.
