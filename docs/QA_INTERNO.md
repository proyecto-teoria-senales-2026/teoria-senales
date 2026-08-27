# QA interno obligatorio

Cada corte del software se cierra únicamente cuando cumple estas capas:

1. **Núcleo matemático:** resultados de referencia y casos límite.
2. **Nomenclatura:** convención uniforme en interfaz, guías, preguntas,
   retroalimentación y reportes.
3. **Regresión:** los ejercicios aprobados conservan cálculos, evaluación,
   sesiones y generación de PDF.
4. **Interfaz:** apertura efectiva de cada página con Streamlit.
5. **Distribución:** una sola aplicación, cinco guías PDF del estudiante y
   ausencia de guías docentes o editables en `docs/guias`.
6. **Windows:** ZIP extraído completamente, una sola carpeta raíz
   `teoria-senales-app` e inicio mediante `INICIAR_APLICACION.bat`.
7. **Integridad:** reporte original aceptado y copia alterada rechazada.
8. **Regresión visual:** los cinco ejercicios muestran el encabezado
   institucional y las 15 páginas de las guías no contienen artefactos en el
   margen izquierdo.

## Corte integrado C-1-1 a C-1-4 y C-3-3

**Fecha de comprobación:** 11 de agosto de 2026.

- Entorno reconstruido desde `requirements.txt` y dependencias sin conflictos.
- Comando reproducible: `python run_tests.py`.
- **55 de 55 pruebas automatizadas aprobadas; cero omisiones.**
- Cinco pruebas de apertura Streamlit ejecutadas: C-1-1, C-1-2, C-1-3,
  C-1-4 y C-3-3.
- Bancos verificados: 15 preguntas para cada ejercicio C-1 y 8 preguntas para
  C-3-3, con 18 puntos posibles.
- Nomenclatura visible verificada: `C-1-1` a `C-1-4`, `C-3-3`, `L_x`, `L_h`
  y `L_y`.
- Cinco guías del estudiante integradas exclusivamente en PDF, con tres páginas
  por guía y formulación matemática.
- Las 15 páginas de las guías fueron renderizadas y revisadas: encabezados
  completos, sin puntos residuales, rectángulos vacíos, ecuaciones cortadas ni
  tablas desbordadas.
- Autoría de las cinco guías normalizada a Juan Esteban Rengifo Segura y
  Julián Felipe Montaña Aguilar.
- Encabezado institucional incluido en
  `src/teoria_senales/assets/encabezado_institucional.png`.
- Un solo lanzador de la aplicación: `INICIAR_APLICACION.bat`.
- Reporte de demostración actualizado a `C-3-3` y cifrado con AES-256.
- Verificador docente: reporte original `VÁLIDO`; copia modificada
  `ALTERADO O NO VÁLIDO`.
- Flujo de GitHub Actions agregado para repetir el QA en ramas y pull requests.
- Pruebas de regresión agregadas para exigir el encabezado en los cinco
  ejercicios y renderizar las 15 páginas de las guías con Poppler.
- No se encontraron marcas ni referencias relacionadas con IA en los archivos
  de texto distribuidos.

La protección del PDF restringe modificaciones y registra una huella SHA-256.
No se presenta como firma digital institucional, porque esa firma requiere una
clave oficial y una política institucional de custodia.
