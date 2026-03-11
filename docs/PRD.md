# Documento de Requerimientos del Producto (PRD)

## Proyecto: Ecosistema de Lectura Agéntica y Biblioteca Inteligente

**Estado:** Planificación / Finalizado para Desarrollo

**Framework de Backend:** Microsoft Agent Framework (Python)

**Framework de Frontend:** Next.js / shadcn/ui

---

## 1. Resumen Ejecutivo

El propósito de este sistema es transformar el acto pasivo de leer documentos PDF técnicos y científicos en un proceso de **aprendizaje activo y asistido**. A diferencia de los lectores convencionales, este software integra una arquitectura multi-agente que actúa como un tutor socrático personal, fomentando la metacognición y asegurando que el estudiante no solo consuma información, sino que construya conocimiento profundo y duradero.

## 2. Definición del Problema

Los estudiantes de educación superior enfrentan tres barreras críticas que este producto busca resolver:

* **La "Ilusión de Competencia":** Leer sin procesar realmente los conceptos, fallando al aplicarlos .
* **Saturación de la Memoria de Trabajo:** La densidad de la jerga técnica agota los recursos cognitivos, llevando al abandono del texto .
* **Fragmentación Digital:** La desconexión entre múltiples fuentes y las constantes distracciones del entorno web.

## 3. Objetivos Estratégicos

1. **Andamiaje Cognitivo:** Proveer soporte justo a tiempo (definiciones, analogías) para reducir la carga cognitiva extraña .
2. **Tutoría Socrática:** Guiar al usuario mediante preguntas reflexivas en lugar de entregar respuestas directas para evitar el "de-skilling" .
3. **Memoria Adaptativa:** Mantener un perfil persistente del dominio del usuario para personalizar la dificultad y el tono de la enseñanza .
4. **Rigor Académico:** Garantizar que cada interacción de la IA esté anclada (grounded) en fuentes verificables con citas exactas.

## 4. Requerimientos Funcionales

### 4.1. Gestión de Biblioteca e Ingesta Inteligente

* **Procesamiento Estructural (Docling):** El sistema debe desglosar los PDFs en Markdown estructurado, identificando tablas, fórmulas, jerarquías de títulos y metadatos (autores, año).

* **Indexación Multimodal:** Los datos deben almacenarse en un Vector Store (ChromaDB / Azure AI Search) permitiendo búsquedas semánticas y recuperación por contexto.

* **Biblioteca Persistente:** Los usuarios deben poder organizar sus documentos en colecciones con sincronización de estado.

### 4.2. Arquitectura de Agentes (Microsoft Agent Framework)

El backend operará bajo un flujo de trabajo agéntico (Agentic Workflow) compuesto por:

* **Agente Tutor Socrático:** Encargado de la interacción dialógica. Utiliza técnicas de *Chain-of-Thought* para diseñar preguntas que desafíen el modelo mental del estudiante.

* **Agente Investigador (GraphRAG):** Conecta el documento actual con el resto de la biblioteca del usuario, identificando contradicciones o refuerzos entre autores.

* **Agente de Estado (Context Provider):** Mantiene la memoria de largo plazo, inyectando el perfil del estudiante en cada sesión .

### 4.3. Interfaz de Usuario (Frontend)

* **Visor PDF Sincronizado:** Implementación de `@react-pdf-viewer` con una capa de anotaciones que resalte el texto referido por el agente tutor en tiempo real.

* **Sidebar de Diálogo Proactivo:** Un chat interactivo que no espera la pregunta del usuario, sino que interviene tras detectar hitos de lectura o secciones de alta densidad .
* **Dashboard de Maestría:** Visualización de "conceptos dominados" vs "brechas de conocimiento" basada en el JSON de estado del estudiante.

## 5. Memoria Estudiante y Persistencia (Student State)

El sistema implementará un **Modelo de Doble Memoria** para garantizar la continuidad pedagógica:

1. **Estado de Sesión (Short-term):** Almacena el hilo de la conversación actual para mantener la coherencia inmediata.
2. **Perfil de Conocimiento (Long-term):** Un objeto JSON persistente en base de datos que rastrea:

* **Conceptos en Gaps:** Temas donde el usuario ha pedido aclaraciones repetidas.
* **Logros Metacognitivos:** Preguntas socráticas respondidas con éxito.
* **Historial de Interés:** Áreas de enfoque para que el tutor use analogías personalizadas .

## 6. Infraestructura de Evaluación (Evals)

Se establecen tres métricas críticas para la mejora continua del sistema:

* **Fidelidad de Recuperación (Faithfulness):** Uso de **Ragas** para asegurar que el agente no invente datos ajenos al PDF.

* **Índice Socrático (GuideEval):** Medición de tres fases: *Percepción* (detección de duda), *Orquestación* (elección de estrategia) y *Elicitación* (efectividad de la pregunta guía) .
* **LLM-as-a-Judge:** Un agente supervisor calificará aleatoriamente las conversaciones para detectar si el tutor entregó una respuesta directa (penalización alta) .

## 7. Guardrails y Seguridad

Basado en las políticas de **Microsoft Foundry Control Plane**:

* **Pedagogical Guardrail:** Interceptor de salida que bloquea frases que entreguen soluciones directas, forzando una reformulación socrática .
* **Task Adherence:** Monitoreo para evitar que el agente discuta temas fuera del dominio académico del documento cargado .
* **Groundedness Validation:** Obligación técnica de incluir citas con coordenadas de página y párrafo para cada afirmación técnica.

## 8. Requerimientos No Funcionales

* **Escalabilidad:** La arquitectura multi-agente debe soportar la orquestación asíncrona para evitar cuellos de botella en el procesamiento de PDFs extensos .
* **Latencia:** Las respuestas del chat deben iniciar el streaming en menos de 2 segundos para mantener el flujo de lectura profunda .
* **Privacidad:** Cumplimiento con estándares educativos (tipo FERPA/GDPR), asegurando que los datos del perfil de estudiante sean privados y cifrados .

---
