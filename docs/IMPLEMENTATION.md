# Project Blueprint - Starter Kit

**Nombre del proyecto:**
**Cliente:** Sector Educativo / Estudiantes Universitarios e Investigadores
**Versión:** 1.0
**Creado por:** Asistente de Investigación IA

---

## 1. Contexto

### 1.1 Propósito del sistema

El sistema busca resolver la crisis de comprensión lectora en la educación superior, donde los estudiantes enfrentan textos científicos de alta densidad léxica y sufren de "lectura superficial" debido a las distracciones digitales. El software actuará como un ecosistema web que integra una biblioteca inteligente y un lector de PDF con un tutor basado en IA que utiliza el diálogo socrático para guiar al usuario hacia el descubrimiento del conocimiento, en lugar de darle respuestas directas .

### 1.2 Actores involucrados

1. **Estudiante / Lector:** Usuario principal que busca comprender textos complejos y gestionar su biblioteca personal.
2. **Agente Tutor Socrático (Backend):** Sistema inteligente que interactúa proactivamente para monitorear la comprensión y plantear desafíos cognitivos .
3. **Agente Investigador / Bibliotecario:** Sistema encargado de conectar conceptos a través de múltiples documentos (RAG multidocumento).

4. **Administrador de Contenido:** (Opcional) Docente que carga materiales específicos y configura las metas de aprendizaje para un grupo.

### 1.3 Objetivos del Proyecto

* **Fomentar la Metacognición:** Obligar al estudiante a "pensar sobre su pensamiento" mediante preguntas reflexivas durante la lectura .
* **Reducir la Carga Cognitiva:** Proveer soporte léxico y conceptual instantáneo para evitar que el estudiante abandone el texto por frustración.

* **Sintetizar Conocimiento Transversal:** Permitir que el usuario encuentre conexiones entre diferentes "papers" o libros de su biblioteca automáticamente.

* **Garantizar la Integridad Académica:** Asegurar que todas las respuestas de la IA estén ancladas (grounded) en citas textuales verificables del PDF.

---

## 2. Casos de Uso

### 2.1 Acciones clave por actor

**Actor: Estudiante / Lector**

1. **Subir y organizar** documentos PDF en una biblioteca personal persistente.

2. **Activar el "Modo Lectura Profunda"** para bloquear distracciones y recibir alertas de fatiga.

3. **Interactuar con el Tutor** mediante lenguaje natural para aclarar dudas o debatir tesis del autor .
4. **Generar mapas conceptuales y flashcards** automáticas basadas en las secciones críticas del texto.

**Actor: Agente Tutor Socrático (Sistema)**

1. **Analizar la estructura semántica** del documento al ser cargado (tesis, metodología, conclusiones).

2. **Plantear preguntas de verificación** cuando el usuario termina una sección densa .
3. **Ajustar el nivel de andamiaje** (scaffolding) basándose en el historial y desempeño previo del estudiante.

---

## 3. Diagrama de Flujo

### 3.1 Identifica el Flujo Principal

**Actor: Estudiante**

1. Carga el PDF -> 2. Inicia lectura -> 3. Recibe intervención del Tutor -> 4. Responde pregunta socrática -> 5. Consolida aprendizaje con quiz/flashcard.

**Actor: Agente Tutor (Backend)**

1. Indexa el PDF (RAG) -> 2. Monitorea progreso de lectura -> 3. Detecta conceptos clave -> 4. Evalúa la respuesta del estudiante -> 5. Actualiza el perfil de conocimiento del usuario.

---

## 4. Requerimientos Funcionales

### 4.1 Requerimientos Principales

* El sistema debe permitir la carga masiva de archivos PDF y su indexación semántica en una base de datos vectorial.

* El sistema debe ofrecer un chat de tutoría que no entregue definiciones directas, sino pistas y preguntas guía (Método Socrático) .
* El sistema debe mostrar citas dinámicas y enlaces directos a la página y párrafo exacto de donde extrae la información .

### 4.2 Requerimientos Secundarios

* El sistema debe detectar patrones de "lectura superficial" (scroll rápido sin pausas) y sugerir un cambio de ritmo o resumen de audio .
* El sistema debe generar visualizaciones (grafos de conocimiento) que conecten el libro actual con otros libros en la biblioteca del usuario.

---

## 5. Story Mapping

| Épica                      | Historia de Usuario                                                                                                                                                                  | Criterios de Aceptación                                                                                                                         |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **Comprensión Activa**     | **Como** estudiante, **quiero** que el tutor me pregunte qué entendí de un párrafo complejo, **para** evitar la "ilusión de competencia" y asegurar que realmente estoy aprendiendo. | • El tutor interviene tras secciones marcadas como "densas". <br>• La IA evalúa la respuesta del usuario y ofrece feedback constructivo.        |
| **Biblioteca Inteligente** | **Como** investigador, **quiero** preguntar "¿cómo se relaciona este paper con el que leí la semana pasada?", **para** construir un marco teórico sólido.                            | • El sistema busca en todos los documentos de la colección. <br>• Genera una respuesta comparativa con citas de ambos documentos.               |
| **Soporte Léxico**         | **Como** alumno de primer año, **quiero** hacer clic en un término técnico y ver una explicación sencilla, **para** no perder el hilo de la lectura buscando en Google.              | • El panel lateral muestra definiciones contextuales sin salir de la pestaña. <br>• Las definiciones se adaptan al nivel previo del estudiante. |

---

**Nota final:** Este blueprint prioriza el uso de **Sistemas Multi-Agente** para separar la lógica de tutoría (pedagogía) de la lógica de recuperación de datos (precisión técnica), atacando directamente la fragmentación de la atención y la carga cognitiva en estudiantes modernos.
