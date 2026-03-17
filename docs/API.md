# Neotix RAG - Backend API Documentation

**Versión:** 1.0.0  
**Última actualización:** 2026-03-17

---

## Base URL

```yml
Production: https://api.neotix.example.com
Development: http://localhost:8000
```

---

## Autenticación

La API utiliza **JWT (JSON Web Tokens)** para autenticación.

### Encabezados Requeridos

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

### Flujo de Autenticación

1. **Registro**: El usuario se registra con email, username y password
2. **Login**: El usuario obtiene un `access_token` JWT
3. **Requests**: Incluir el token en el header `Authorization`
4. **Logout**: El usuario puede cerrar sesión invalidando el token

---

## Endpoints

### Tabla de Contenido

| Método | Endpoint                | Descripción                   | Auth |
| ------ | ----------------------- | ----------------------------- | ---- |
| POST   | `/api/auth/register`    | Registrar nuevo usuario       | No   |
| POST   | `/api/auth/login`       | Iniciar sesión                | No   |
| POST   | `/api/auth/logout`      | Cerrar sesión                 | ✅    |
| GET    | `/api/documents/`       | Listar documentos del usuario | ✅    |
| GET    | `/api/documents/{id}`   | Obtener documento por ID      | ✅    |
| POST   | `/api/documents/upload` | Subir nuevo documento         | ✅    |
| POST   | `/api/chat`             | Enviar mensaje al chat        | ✅    |
| GET    | `/api/health`           | Verificar estado del servicio | No   |

---

## Autenticación

### POST /api/auth/register

Registrar un nuevo usuario en el sistema.

**URL:** `POST /api/auth/register`  
**Autenticación:** No requerida  
**Rate Limit:** 5 solicitudes por minuto

#### Request Body

```json
{
  "email": "usuario@ejemplo.com",
  "username": "mi_usuario",
  "password": "contraseña123"
}
```

#### Campos

| Campo      | Tipo              | Requerido | Descripción                   |
| ---------- | ----------------- | --------- | ----------------------------- |
| `email`    | string (EmailStr) | Sí        | Correo electrónico válido     |
| `username` | string            | Sí        | Username (3-50 caracteres)    |
| `password` | string            | Sí        | Contraseña (8-128 caracteres) |

#### Response (201 Created)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "user_id": 1,
    "email": "usuario@ejemplo.com",
    "username": "mi_usuario",
    "role": "user"
  }
}
```

#### Códigos de Error

| Código | Descripción                           |
| ------ | ------------------------------------- |
| 400    | Email ya registrado o datos inválidos |
| 422    | Error de validación de datos          |

---

### POST /api/auth/login

Iniciar sesión y obtener token de acceso.

**URL:** `POST /api/auth/login`  
**Autenticación:** No requerida  
**Rate Limit:** 5 solicitudes por minuto

#### Request Body

```json
{
  "email": "usuario@ejemplo.com",
  "password": "contraseña123"
}
```

#### Response (200 OK)

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "user_id": 1,
    "email": "usuario@ejemplo.com",
    "username": "mi_usuario",
    "role": "user"
  }
}
```

#### Códigos de Error

| Código | Descripción            |
| ------ | ---------------------- |
| 401    | Credenciales inválidas |
| 422    | Error de validación    |

---

### POST /api/auth/logout

Cerrar sesión invalidando el token actual.

**URL:** `POST /api/auth/logout`  
**Autenticación:** ✅ Requiere token JWT

#### Headers

```http
Authorization: Bearer <access_token>
```

#### Response (200 OK)

```json
{
  "message": "Successfully logged out"
}
```

#### Notas

- El token es añadido a una blacklist en Redis
- El token bleibt válido hasta su fecha de expiración
- No es posible usar el token después del logout

---

## Documentos

### GET /api/documents/

Listar todos los documentos del usuario autenticado.

**URL:** `GET /api/documents/`  
**Autenticación:** ✅ Requiere token JWT

#### Headers

```http
Authorization: Bearer <access_token>
```

#### Response (200 OK)

```json
{
  "documents": [
    {
      "document_id": 1,
      "user_id": 1,
      "title": "mi_documento.pdf",
      "file_path": "1_1234567890_mi_documento.pdf",
      "page_count": 0,
      "created_at": "2026-03-17T10:00:00",
      "updated_at": "2026-03-17T10:00:00",
      "tags": null,
      "status": "pending"
    }
  ]
}
```

#### Modelo Document

| Campo         | Tipo     | Descripción                                 |
| ------------- | -------- | ------------------------------------------- |
| `document_id` | int      | ID único del documento                      |
| `user_id`     | int      | ID del propietario                          |
| `title`       | string   | Título del documento                        |
| `file_path`   | string   | Ruta en Azure Blob Storage                  |
| `page_count`  | int      | Número de páginas                           |
| `created_at`  | datetime | Fecha de creación                           |
| `updated_at`  | datetime | Fecha de actualización                      |
| `tags`        | array    | Etiquetas asociadas                         |
| `status`      | string   | Estado (pending/processing/processed/error) |

---

### GET /api/documents/{document_id}

Obtener un documento específico por su ID.

**URL:** `GET /api/documents/{document_id}`  
**Autenticación:** ✅ Requiere token JWT

#### Path Parameters

| Parámetro     | Tipo | Descripción      |
| ------------- | ---- | ---------------- |
| `document_id` | int  | ID del documento |

#### Headers

```http
Authorization: Bearer <access_token>
```

#### Response (200 OK)

```json
{
  "document": {
    "document_id": 1,
    "user_id": 1,
    "title": "mi_documento.pdf",
    "file_path": "1_1234567890_mi_documento.pdf",
    "page_count": 0,
    "created_at": "2026-03-17T10:00:00",
    "updated_at": "2026-03-17T10:00:00",
    "tags": null,
    "status": "pending"
  }
}
```

#### Códigos de Error

| Código | Descripción                                     |
| ------ | ----------------------------------------------- |
| 404    | Documento no encontrado                         |
| 403    | No tienes permiso para acceder a este documento |

---

### POST /api/documents/upload

Subir un nuevo documento (PDF).

**URL:** `POST /api/documents/upload`  
**Autenticación:** ✅ Requiere token JWT  
**Content-Type:** `multipart/form-data`

#### Headers

```http
Authorization: Bearer <access_token>
```

#### Request Body (Form Data)

| Campo  | Tipo   | Descripción         |
| ------ | ------ | ------------------- |
| `file` | binary | Archivo PDF a subir |

#### Response (201 Created)

```json
{
  "message": "Document uploaded successfully",
  "document_id": 1234567890
}
```

#### Códigos de Error

| Código | Descripción                  |
| ------ | ---------------------------- |
| 400    | Error al procesar el archivo |
| 422    | Archivo no proporcionado     |

---

## Chat

### POST /api/chat

Enviar un mensaje al agente conversacional.

**URL:** `POST /api/chat`  
**Autenticación:** ✅ Requiere token JWT

#### Headers

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

#### Request Body

```json
{
  "message": "¿Qué contiene mi documento sobre matemáticas?",
  "session_id": "sesion-123-abc"  // opcional
}
```

#### Campos

| Campo        | Tipo   | Requerido | Descripción                         |
| ------------ | ------ | --------- | ----------------------------------- |
| `message`    | string | Sí        | Mensaje del usuario                 |
| `session_id` | string | No        | ID de sesión para mantener contexto |

#### Response (200 OK)

```json
{
  "response": "El documento contiene información sobre álgebra lineal...",
  "session_id": "sesion-123-abc"
}
```

#### Notas

- El `session_id` es opcional
- Si no se proporciona, se creará una nueva sesión
- El historial de la sesión se guarda en Redis
- El agente puede acceder a los documentos subidos del usuario

---

## Health Check

### GET /api/health

Verificar el estado del servicio.

**URL:** `GET /api/health`  
**Autenticación:** No requerida

#### Response (200 OK)

```json
{
  "status": "healthy",
  "service": "pdf-reader-api"
}
```

---

## Códigos de Estado HTTP

| Código | Descripción                                |
| ------ | ------------------------------------------ |
| 200    | OK - Request exitosa                       |
| 201    | Created - Recurso creado                   |
| 400    | Bad Request - Datos inválidos              |
| 401    | Unauthorized - Token inválido o faltante   |
| 403    | Forbidden - Sin permisos                   |
| 404    | Not Found - Recurso no encontrado          |
| 422    | Unprocessable Entity - Validación fallida  |
| 429    | Too Many Requests - Rate limit excedido    |
| 500    | Internal Server Error - Error del servidor |

---

## Errores Comunes

### 401 - Unauthorized

```json
{
  "detail": "Authentication required"
}
```

Causas posibles:

- Token no incluido en el header
- Token expirado
- Token inválido
- Token ha sido revocado (logout)

### 403 - Forbidden

```json
{
  "detail": "User account is inactive"
}
```

### 429 - Too Many Requests

```json
{
  "detail": "Too many requests. Please try again later."
}
```

---

## Ejemplo de Implementación (JavaScript)

```javascript
class NeotixAPI {
  constructor(baseUrl, token = null) {
    this.baseUrl = baseUrl;
    this.token = token;
  }

  setToken(token) {
    this.token = token;
  }

  async request(endpoint, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Request failed');
    }

    return response.json();
  }

  // Auth
  async register(email, username, password) {
    return this.request('/api/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, username, password }),
    });
  }

  async login(email, password) {
    const response = await this.request('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    this.setToken(response.access_token);
    return response;
  }

  async logout() {
    return this.request('/api/auth/logout', {
      method: 'POST',
    });
  }

  // Documents
  async listDocuments() {
    return this.request('/api/documents/');
  }

  async getDocument(documentId) {
    return this.request(`/api/documents/${documentId}`);
  }

  async uploadDocument(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${this.baseUrl}/api/documents/upload`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
      },
      body: formData,
    });
    
    return response.json();
  }

  // Chat
  async sendMessage(message, sessionId = null) {
    return this.request('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message, session_id: sessionId }),
    });
  }
}

// Uso
const api = new NeotixAPI('http://localhost:8000');

// Login
const { access_token, user } = await api.login('user@test.com', 'password123');

// Listar documentos
const { documents } = await api.listDocuments();

// Enviar mensaje al chat
const { response, session_id } = await api.sendMessage(
  '¿Qué contiene mi documento?',
  sessionId
);
```

---

## Notas Importantes para Frontend

1. **Siempre guardar el token** - Usar localStorage o secure storage
2. **Manejar 401** - Redireccionar a login si el token expira
3. **Manejar logout** - Limpiar token y redireccionar a login
4. **Session ID** - Guardar para mantener contexto de conversación
5. **Documentos por usuario** - Solo se muestran los documentos del usuario autenticado
