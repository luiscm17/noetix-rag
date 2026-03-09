# 1. Diseño de la Infraestructura de Evaluación (Evals)

No podemos medir un tutor socrático con métricas tradicionales de Chatbot. Necesitamos un enfoque de **evaluación pedagógica automatizada**.

## Niveles de Evaluación

1. **Evaluación de Recuperación (RAG Metrics):** Usar el framework **Ragas** para medir:

* *Fidelidad (Faithfulness):* ¿La respuesta del agente se basa solo en el PDF?.
* *Relevancia del Contexto:* ¿El fragmento del PDF extraído es el que realmente resuelve la duda?.

1. **Evaluación de la Guía Socrática (GuideEval):** Evaluar el comportamiento del tutor en tres fases:

* *Percepción:* ¿El agente infirió correctamente que el estudiante no entendió el concepto?
* *Orquestación:* ¿Seleccionó la estrategia correcta (analogía, andamiaje, descomposición)?
* *Elicitación:* ¿La pregunta lanzada realmente estimula la reflexión del alumno?

1. **LLM-as-a-Judge:** Configurar un agente evaluador (usando GPT-4o o Claude 3.5 Sonnet) con una rúbrica que califique de 1 a 5:

* *Prohibición de Respuesta Directa:* ¿El tutor dio la solución? (Puntaje bajo si lo hizo).
* *Tono y Coherencia:* ¿Es empático y mantiene el hilo pedagógico?.

---

## 2. Diseño de Guardrails y Seguridad

Dado que trabajas con el ecosistema de Microsoft, utilizaremos el concepto de **Foundry Control Plane** para implementar "barandillas" a nivel de agente.

### Capas de Protección

* **Prompt Shields (Entrada):** Bloquear intentos de *jailbreak* donde el usuario intente forzar al tutor a escribir código ajeno al libro o a dar respuestas directas.
* **Filtro de Adherencia a la Tarea (Task Adherence):** Detectar si el agente comienza a "alucinar" fuera del dominio del paper científico.
* **La "Barrera del Conocimiento" (Pedagogical Guardrail):** Un script intermedio que verifique si la salida contiene frases como "La respuesta es..." o "Esto significa que...". Si detecta una respuesta directa, el sistema debe regenerar el mensaje forzando una pregunta socrática.
* **Privacidad (PII Detection):** Anonimizar automáticamente cualquier dato personal que el estudiante suba accidentalmente en sus notas.
* **Integridad Académica:** Asegurar que cada afirmación del chat incluya una **cita exacta con coordenadas** en el PDF (página y párrafo) para fomentar la verificación.

---

## 3. Propuesta de Stack para el Frontend

Para un lector tipo NotebookLM, el frontend debe manejar streaming pesado y una interfaz de doble panel sincronizada.

* **Framework:** **Next.js (App Router)** con TypeScript. Es el estándar para aplicaciones de IA por su manejo nativo de streaming y Server Components.
* **Interfaz de Usuario:** **shadcn/ui**. Al ser "Open Code", permite modificar el código fuente de los componentes directamente, algo ideal para integrar lógica de IA en barras laterales o tablas de datos.
* **Visor de PDF:** **`@react-pdf-viewer/react`**. Es altamente modular y permite crear "layers" de anotación y resaltado dinámico cuando el agente menciona una parte del texto.
* **Conectividad IA:** **Vercel AI SDK**. Simplifica la gestión de flujos de chat y el renderizado de interfaces generativas (GenUI) como cuestionarios o mapas conceptuales que aparecen en el sidebar.
* **Visualización de Grafos:** **D3.js** o **Nivo** para generar el mapa de conexiones entre los libros de la biblioteca del usuario.

---
