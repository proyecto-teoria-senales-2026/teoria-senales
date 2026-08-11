# Acceso a la interfaz

Este documento registra la ruta acordada para presentar el avance y aplicar
posteriormente el piloto con estudiantes.

## Tutoría del 31 de julio de 2026

La aplicación se mostrará de forma local desde el computador usado para la
presentación.

- No se necesita un enlace público.
- El entorno `.venv` se crea y prueba en el mismo computador que se usará en la
  tutoría; no se copia desde otro equipo.
- El repositorio y sus dependencias deben quedar preparados antes de la tutoría.
- `python -m pip check` debe confirmar que no existen dependencias rotas.
- La aplicación se abre con `python -m streamlit run app.py`.
- El recorrido se realiza desde el navegador en `http://localhost:8501`.
- El código estudiantil se valida con reglas técnicas de longitud y caracteres,
  sin asumir todavía un formato institucional.
- Si existe una sesión sin finalizar, la aplicación permite continuarla o
  iniciar un nuevo intento.
- Antes de entregar el avance se hará una prueba completa en el computador de
  presentación.

El equipo de desarrollo entregará la aplicación preparada, las instrucciones
de apertura y un guion breve. Los estudiantes responsables del proyecto
presentarán el avance y recogerán las observaciones de los tutores.

## Piloto de septiembre de 2026

Para el piloto se proyecta un acceso mediante enlace web, de modo que cada
estudiante pueda ingresar desde el navegador.

La publicación se realizará después de validar con los tutores el flujo del
C-3-3. Antes de desplegar se deben definir:

- el servicio de alojamiento;
- si el acceso será público o restringido;
- el tratamiento de los códigos estudiantiles y reportes;
- el mecanismo para almacenar o descargar las sesiones.

Los estudiantes responsables del proyecto aplicarán las pruebas del piloto con
los participantes. El equipo de desarrollo preparará la herramienta, el
protocolo, las instrucciones y los instrumentos para recoger resultados.
