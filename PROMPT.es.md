# Prompt de EDA — reseñas WeLoveReviews

Copia todo lo que está debajo de esta línea en tu agente de código (Cursor, Copilot, Claude Code, etc.).

---

Estás ayudando a un ingeniero de IA a explorar un dataset de reseñas de clientes antes de cualquier trabajo de modelado.

Contexto:

- Cliente: reseñas de servicio estilo WeLoveReviews / Harbor House Café
- Boilerplate: 4GeeksAcademy machine-learning-python-template
- Archivo: `data/raw/reviews.csv` (columnas: `review_id`, `rating`, `review_text`)
- Pregunta de negocio (solo como contexto — no resuelvas el proyecto completo): si el sentimiento escrito se alinea con un promedio de ~4.5 / 5 estrellas

Tu trabajo en el notebook del proyecto `src/explore.ipynb`:

1. Explorar el dataset (forma, dtypes, valores faltantes, distribución de ratings, estadísticas de longitud de texto, una pequeña muestra de textos de reseñas).
2. Destacar los insights más importantes que más adelante justifiquen un plan de acción (mantén la lista de insights corta y accionable).
3. Proponer acciones de limpieza solo si hacen falta; si no hacen falta, explica por qué.

Reglas:

- Escribe markdown breve entre celdas de código que explique la transición al siguiente paso (tono tutorial, texto mínimo).
- No ejecutes modelos de sentimiento.
- No escribas ni modifiques `src/app.py`.
- No produzcas un informe markdown para el cliente.
- No afirmes que el proyecto completo está terminado — detente después de la exploración, los insights y la propuesta de limpieza.
- Mantén el trabajo en `src/explore.ipynb`.
