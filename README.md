
-----
```markdown
# BACKEND-FAPI-BDI-SMART_HEALTH

# SmartHealth - Sistema de Consulta Clínica Inteligente con RAG

**Desarrolladores**: Ivan Ospino, Gisell Anaya, Jhoan Smith, Jeison Mendez, Jhon Mantilla, Jhoana Inocencio, Sergio Villamizar, Jhoan Valero  
**Versión**: 2.0.0  
**Creado**: 22-Noviembre-2025  
**Última actualización**: 10-Diciembre-2025

-----

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Características Principales](#características-principales)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Requisitos del Sistema](#requisitos-del-sistema)
5. [Instalación Rápida](#instalación-rápida)
6. [Instalación Detallada](#instalación-detallada)
7. [Configuración del Frontend](#configuración-del-frontend)
8. [Uso del Sistema](#uso-del-sistema)
9. [API Endpoints](#api-endpoints)
10. [WebSocket](#websocket)
11. [Seguridad](#seguridad)
12. [Estructura del Proyecto](#estructura-del-proyecto)
13. [Tecnologías Utilizadas](#tecnologías-utilizadas)
14. [Desarrollo](#desarrollo)
15. [Testing](#testing)
16. [Despliegue en Producción](#despliegue-en-producción)
17. [Monitoreo y Logs](#monitoreo-y-logs)
18. [Troubleshooting](#troubleshooting)
19. [Recursos Adicionales](#recursos-adicionales)
20. [Contribución](#contribución)
21. [Licencia](#licencia)
22. [Agradecimientos](#agradecimientos)
23. [Contacto](#contacto)
24. [Changelog](#changelog)

-----

## Descripción General

SmartHealth es un **sistema de consulta clínica inteligente** que utiliza **RAG (Retrieval-Augmented Generation)** para proporcionar respuestas precisas sobre historiales médicos de pacientes. El sistema combina:

  - **Backend FastAPI**: API REST y WebSocket con arquitectura modular
  - **PostgreSQL + pgvector**: Base de datos vectorial para búsqueda semántica
  - **OpenAI GPT-4o-mini**: Modelo de lenguaje para generar respuestas naturales
  - **Frontend Vanilla JS**: Interfaz web moderna y responsive

### ¿Qué hace SmartHealth?

  - ✅ Consulta historiales clínicos completos de pacientes
  - ✅ Búsqueda semántica en citas, diagnósticos, prescripciones y registros médicos
  - ✅ Chat en tiempo real con streaming de respuestas token por token
  - ✅ Autenticación segura con JWT
  - ✅ Auditoría completa de consultas

### Caso de Uso

```

Usuario: "¿Cuándo fue la última cita del paciente Juan Pérez?"

Sistema:

1.  Busca al paciente por documento
2.  Realiza búsqueda vectorial en su historial
3.  Construye contexto clínico relevante
4.  Genera respuesta natural con GPT-4o-mini
5.  Retorna respuesta con fuentes verificables

Respuesta: "Juan Pérez tuvo su última cita el 9 de noviembre de 2024,
un examen médico de chequeo general con la doctora Carolina Gutiérrez,
especialista en medicina física y rehabilitación."

```

-----

## Características Principales

### Backend

  - **API REST + WebSocket**: Máxima flexibilidad de integración
  - **RAG Inteligente**: Combina búsqueda vectorial con LLM
  - **Búsqueda Semántica**: Encuentra información relevante usando embeddings
  - **Autenticación JWT**: Sistema seguro de registro y login
  - **Rate Limiting**: Protección contra abuso (20 msg/min WebSocket, 100 req/min API)
  - **Validación de Inputs**: Protección contra SQL injection y jailbreak
  - **Logging y Auditoría**: Registro completo de operaciones
  - **Streaming**: Respuestas token por token en tiempo real

### Frontend

  - **Interfaz Moderna**: Diseño responsive con animaciones suaves
  - **Chat en Tiempo Real**: Comunicación WebSocket con streaming
  - **Autenticación Integrada**: Login y registro con validación en cliente
  - **Protección de Rutas**: Redirección automática según estado de autenticación
  - **Gestión de Estado**: Almacenamiento local de tokens y datos de usuario
  - **Sin Frameworks**: JavaScript vanilla para máxima portabilidad

### Base de Datos

  - **13 Tablas Relacionadas**: Modelo completo de datos clínicos
  - **Vectores Embeddings**: En 6 tablas para búsqueda semántica
  - **Índices Optimizados**: HNSW para búsqueda vectorial rápida
  - **Esquema Smart Health**: Namespace separado para organización

-----

## Arquitectura del Sistema

### Arquitectura General

```

┌─────────────────────────────────────────────────────────────┐
│                        CLIENTE WEB                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │    Login     │  │   Register   │  │     Chat     │       │
│  │  (HTML/CSS)  │  │  (HTML/CSS)  │  │  (HTML/CSS)  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘             │
│                            │                                │
│                  JavaScript (Vanilla)                       │
│         API Client + WebSocket + Auth Utils                 │
└─────────────────────────────────────────────────────────────┘
│
▼ HTTP/HTTPS + WebSocket
┌─────────────────────────────────────────────────────────────┐
│                    BACKEND FASTAPI                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Middlewares                             │   │
│  │  • CORS • Security Headers • Request Logging         │   │
│  │  • Rate Limiting • Exception Handlers                │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  Routers                             │   │
│  │  • Auth (register/login)                             │   │
│  │  • Users (CRUD)                                      │   │
│  │  • Query (RAG endpoint)                              │   │
│  │  • WebSocket Chat (streaming)                        │   │
│  │  • History (audit logs)                              │   │
│  │  • Catalog (document types)                          │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   Services                           │   │
│  │  • Auth Service (JWT)                                │   │
│  │  • Clinical Service (fetch data)                     │   │
│  │  • Vector Search (semantic search)                   │   │
│  │  • LLM Service (OpenAI GPT)                          │   │
│  │  • RAG Context Builder                               │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
│
▼ SQLAlchemy
┌─────────────────────────────────────────────────────────────┐
│              PostgreSQL 16 + pgvector                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Schema: smart\_health                                │   │
│  │                                                      │   │
│  │  • patients (embeddings)                             │   │
│  │  • doctors (embeddings)                              │   │
│  │  • appointments (embeddings)                         │   │
│  │  • medical\_records (embeddings)                      │   │
│  │  • diagnoses (embeddings)                            │   │
│  │  • prescriptions                                     │   │
│  │  • medications (embeddings)                          │   │
│  │  • users (auth)                                      │   │
│  │  • audit\_logs (history)                              │   │
│  │  • + 4 tablas auxiliares                             │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│                      OpenAI API                             │
│  • GPT-4o-mini (generación de respuestas)                   │
│  • text-embedding-3-small (embeddings)                      │
└─────────────────────────────────────────────────────────────┘

```

### Flujo RAG (Retrieval-Augmented Generation)

```

1.  Usuario envía pregunta + documento de paciente
    ↓
2.  Backend busca paciente en PostgreSQL
    ↓
3.  Búsqueda vectorial: similar\_chunks (k=15, min\_score=0.3)
    • appointments.reason\_embedding
    • medical\_records.summary\_embedding
    • diagnoses.description\_embedding
    • prescriptions.medication\_embedding
    ↓
4.  Construcción de contexto:
    • Información básica del paciente
    • Citas médicas recientes
    • Diagnósticos registrados
    • Medicamentos prescritos
    • Chunks relevantes de búsqueda vectorial
    ↓
5.  LLM genera respuesta:
    system\_prompt + context + question → GPT-4o-mini
    ↓
6.  Construcción de sources (trazabilidad)
    ↓
7.  Respuesta JSON estructurada + metadata
    ↓
8.  Guardado en audit\_logs para historial

<!-- end list -->

````

-----

## Requisitos del Sistema

### Software Requerido

| Software | Versión Mínima | Propósito |
|----------|----------------|-----------|
| Python | 3.9+ | Runtime del backend |
| PostgreSQL | 16+ | Base de datos |
| pgvector | 0.5.1+ | Extensión para vectores |
| pip | Latest | Gestor de paquetes |
| Git | Latest | Control de versiones |

### Navegadores Soportados (Frontend)

  - Chrome 90+
  - Firefox 88+
  - Safari 14+
  - Edge 90+

### Recursos de Hardware

**Desarrollo:**

  - CPU: 2 cores
  - RAM: 4 GB
  - Disco: 10 GB libre

**Producción:**

  - CPU: 4+ cores
  - RAM: 8+ GB
  - Disco: 50+ GB

### Cuentas Externas

  - **OpenAI Account**: API key con créditos disponibles
      - Obtener en: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
      - Modelos necesarios: GPT-4o-mini + text-embedding-3-small

-----

## Instalación Rápida

### Opción 1: Clonar

```bash
# 1. Clonar repositorio
git clone [https://github.com/Ospino89/-backend-fapi-bdi-smart_health.git](https://github.com/Ospino89/-backend-fapi-bdi-smart_health.git)
cd -backend-fapi-bdi-smart_health
````

### Opción 2: Docker

> **Nota**: Docker: Archivos de configuración en desarrollo. Por ahora, usar instalación manual.

-----

## Instalación Detallada

### Paso 1: Preparar el Entorno

```bash
# 1. Clonar el repositorio
git clone [https://github.com/Ospino89/-backend-fapi-bdi-smart_health.git](https://github.com/Ospino89/-backend-fapi-bdi-smart_health.git)
cd -backend-fapi-bdi-smart_health

# 2. Crear entorno virtual Python
cd backend
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt
```

### Paso 2: Instalar y Configurar PostgreSQL

Ver guía completa en: [`backend/database_setup.md`](https://www.google.com/search?q=backend/database_setup.md)

```bash
# 1. Instalar PostgreSQL 16
# Windows: [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
# Linux: sudo apt install postgresql-16
# Mac: brew install postgresql@16

# 2. Instalar pgvector
# Ver instrucciones específicas por OS en database_setup.md

# 3. Verificar instalación
psql --version
# Debe mostrar: psql (PostgreSQL) 16.x
```

### Paso 3: Crear Base de Datos

```bash
# 1. Navegar a pipelines
cd ../pipelines/01-create-database

# 2. Crear entorno virtual para scripts
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate en Windows

# 3. Instalar dependencias de scripts
pip install psycopg2-binary tqdm python-dotenv

# 4. Configurar contraseñas en scripts
# Editar script-01.py, script-02.py con tu contraseña de PostgreSQL

# 5. Ejecutar scripts de creación
python script-01.py  # Crea base de datos y usuario
python script-02.py  # Instala pgvector

# 6. Otorgar permisos de superusuario
psql -U postgres -d smarthdb
ALTER USER sm_admin WITH SUPERUSER;
\q
```

### Paso 4: Crear Esquema y Tablas

```bash
# 1. Navegar a directorio de inserción
cd ../02-insert-data

# 2. Crear tablas
python create-tables.py

# 3. Insertar datos de ejemplo
python script-02.py
# Este proceso puede tardar 5-10 minutos
```

### Paso 5: Configurar Variables de Entorno

```bash
# 1. Crear archivo .env en la RAÍZ del proyecto
cd ../..
touch .env  # o copy nul .env en Windows

# 2. Editar .env con tu editor favorito
nano .env
```

**Contenido del archivo `.env`:**

```env
# ===================================================================
# BASE DE DATOS
# ===================================================================
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smarthdb
DB_USER=sm_admin
DB_PASSWORD=TU_CONTRASEÑA_AQUI

# ===================================================================
# SEGURIDAD - CRÍTICO
# ===================================================================
# Generar con: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=GENERA_UNA_CLAVE_SEGURA_DE_64_CARACTERES_AQUI

# Entorno: development, staging, production
APP_ENV=development

# ===================================================================
# OPENAI API
# ===================================================================
# Obtener en: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
OPENAI_API_KEY=sk-TU_API_KEY_AQUI

# ===================================================================
# CONFIGURACIÓN LLM
# ===================================================================
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=2000
LLM_TIMEOUT=30

# ===================================================================
# WEBSOCKET (Opcional)
# ===================================================================
WEBSOCKET_TIMEOUT=300
WEBSOCKET_RATE_LIMIT=20
WEBSOCKET_MAX_MESSAGE_SIZE=10485760

# ===================================================================
# JWT (Opcional)
# ===================================================================
JWT_EXPIRATION_MINUTES=30
JWT_ALGORITHM=HS256

# ===================================================================
# CORS (Producción)
# ===================================================================
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# ===================================================================
# RATE LIMITING (Producción)
# ===================================================================
GLOBAL_RATE_LIMIT=100
```

### Paso 6: Generar Embeddings (Opcional)

**⚠️ ADVERTENCIA: Este proceso consume créditos de OpenAI. Aproximadamente $0.02-$0.05 USD por 1000 registros.**

```bash
# Solo ejecutar si tienes créditos disponibles

cd backend/src
python -m app.services.generate_embeddings

# Generará embeddings para:
# - medical_records
# - patients
# - doctors
# - appointments
# - diagnoses
# - medications
```

-----

## Configuración del Frontend

### Estructura del Frontend

```
frontend/
├── public/                 # Archivos HTML
│   ├── index.html         # Aplicación principal (chat)
│   ├── login.html         # Página de login
│   ├── register.html      # Página de registro
│   ├── test.html          # Test de WebSocket
│   └── unauthorized.html  # Acceso no autorizado
├── static/                # Recursos estáticos
│   ├── css/              # Estilos
│   │   ├── base.css      # Estilos base
│   │   ├── chat.css      # Estilos del chat
│   │   ├── animations.css # Animaciones
│   │   └── test.css      # Estilos de test
│   ├── js/               # JavaScript
│   │   ├── utils.js      # Utilidades (API, Auth, Storage)
│   │   ├── auth.js       # Lógica de autenticación
│   │   ├── chat.js       # Lógica del chat
│   │   ├── route-protection.js # Protección de rutas
│   │   └── test.js       # Scripts de test
│   └── img/              # Imágenes
│       └── Logo, Png.png
└── docs/                  # Documentación
    └── websocket.md       # Protocolo WebSocket
```

### Características del Frontend

1.  **Sin Dependencias Externas**: JavaScript vanilla, no requiere npm/webpack
2.  **Auto-configuración**: Detecta automáticamente la URL del backend
3.  **Responsive Design**: Se adapta a móviles, tablets y escritorio
4.  **Protección de Rutas**: Redirección automática según autenticación
5.  **WebSocket Integrado**: Chat en tiempo real con reconexión automática

### Conexión Frontend-Backend

El frontend **NO requiere variables de entorno**. Se conecta automáticamente al backend usando:

```javascript
// El frontend detecta la URL del servidor automáticamente
const API_BASE = window.location.origin;  // http://localhost:8000

// WebSocket también se configura automáticamente
const WS_URL = `ws://${window.location.host}/ws/chat`;
```

Esto significa que:

  - ✅ En desarrollo: Se conecta a `http://localhost:8000`
  - ✅ En producción: Se conecta al dominio donde está desplegado
  - ✅ No necesita configuración adicional

### Almacenamiento Local

El frontend usa `localStorage` para:

```javascript
// Token JWT
localStorage.setItem('jwt_token', token);
localStorage.getItem('jwt_token');

// Datos de usuario
localStorage.setItem('user_data', JSON.stringify(user));
localStorage.getItem('user_data');

// Limpiar al logout
localStorage.removeItem('jwt_token');
localStorage.removeItem('user_data');
```

> **⚠️ NOTA**: La API `window.storage` está documentada pero AÚN NO implementada en el frontend actual. Próximamente se agregará esta funcionalidad.

-----

## Uso del Sistema

### Iniciar el Servidor

```bash
# Opción 1: Script de inicio (Recomendado)
cd backend
python start_server.py

# Opción 2: Uvicorn directo
uvicorn src.app.main:app --reload --port 8000

# Opción 3: Gunicorn (Producción)
gunicorn src.app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

**Salida esperada:**

```
INFO:     Uvicorn running on [http://127.0.0.1:8000](http://127.0.0.1:8000)
INFO:     Application startup complete.
```

### Acceder al Sistema

**Frontend (Interfaz Web):**

  - Login: http://localhost:8000/login
  - Registro: http://localhost:8000/register
  - Chat: http://localhost:8000/chat (requiere autenticación)

**API (Desarrollo):**

  - Swagger UI: http://localhost:8000/docs
  - ReDoc: http://localhost:8000/redoc
  - OpenAPI JSON: http://localhost:8000/openapi.json

**Health Check:**

  - http://localhost:8000/health

### Flujo de Uso Típico

1.  **Registro de Usuario**

      - Ir a http://localhost:8000/register
      - Completar formulario
      - Click en "Registrarse"

2.  **Login**

      - Ir a http://localhost:8000/login
      - Ingresar credenciales
      - El sistema redirige a /chat

3.  **Realizar Consulta**

      - Seleccionar tipo de documento
      - Ingresar número de documento
      - Escribir pregunta
      - Click en "Enviar" o Enter
      - Ver respuesta en tiempo real (streaming)

4.  **Ver Historial**

      - Click en botón "Historial"
      - Ver consultas anteriores
      - Click en una consulta para ver detalles

-----

## API Endpoints

### Autenticación

#### POST `/auth/register`

Registra un nuevo usuario.

**Request:**

```json
{
  "email": "usuario@ejemplo.com",
  "password": "SecurePass123!",
  "first_name": "Juan",
  "middle_name": "Carlos",
  "first_surname": "Pérez",
  "second_surname": "González"
}
```

**Response (201):**

```json
{
  "user_id": 1,
  "email": "usuario@ejemplo.com",
  "first_name": "Juan",
  "first_surname": "Pérez",
  "is_active": true,
  "created_at": "2025-12-11T10:30:00Z"
}
```

#### POST `/auth/login`

Inicia sesión y obtiene token JWT.

**Request:**

```json
{
  "email": "usuario@ejemplo.com",
  "password": "SecurePass123!"
}
```

**Response (200):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Usuarios

#### GET `/users/me`

Obtiene perfil del usuario actual.

**Headers:**

```
Authorization: Bearer <token>
```

**Response (200):**

```json
{
  "user_id": 1,
  "email": "usuario@ejemplo.com",
  "first_name": "Juan",
  "first_surname": "Pérez",
  "is_active": true,
  "created_at": "2025-12-11T10:30:00Z"
}
```

### Consultas RAG

#### POST `/query/`

Realiza consulta clínica con RAG.

**Request:**

```json
{
  "user_id": "1",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "document_type_id": 1,
  "document_number": "123456789",
  "question": "¿Cuándo fue la última cita del paciente?"
}
```

**Response (200):**

```json
{
  "status": "success",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "sequence_chat_id": 1,
  "timestamp": "2025-12-11T10:35:00Z",
  "patient_info": {
    "patient_id": 42,
    "full_name": "Juan Carlos Pérez González",
    "document_type": "CC",
    "document_number": "123456789"
  },
  "answer": {
    "text": "Juan Pérez tuvo su última cita el 9 de noviembre de 2024...",
    "confidence": 0.94,
    "model_used": "gpt-4o-mini"
  },
  "sources": [
    {
      "source_id": 1,
      "type": "appointment",
      "appointment_id": 123,
      "date": "2024-11-09",
      "relevance_score": 0.98,
      "doctor": {
        "name": "Carolina Gutiérrez",
        "specialty": "Medicina Física y Rehabilitación"
      }
    }
  ],
  "metadata": {
    "total_records_analyzed": 15,
    "query_time_ms": 1234,
    "sources_used": 5,
    "context_tokens": 1456
  }
}
```

### Historial

#### GET `/history/`

Obtiene historial de consultas del usuario.

**Headers:**

```
Authorization: Bearer <token>
```

**Query Parameters:**

  - `limit`: Número de registros (default: 50)

**Response (200):**

```json
[
  {
    "audit_log_id": 1,
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "sequence_chat_id": 1,
    "question": "¿Cuándo fue la última cita?",
    "created_at": "2025-12-11T10:35:00Z",
    "document_type_id": 1,
    "document_number": "123456789"
  }
]
```

### Catálogo

#### GET `/catalog/document-types`

Obtiene tipos de documento disponibles.

**Response (200):**

```json
[
  {
    "document_type_id": 1,
    "type_name": "Cédula de Ciudadanía",
    "type_code": "CC",
    "description": "Documento de identidad colombiano"
  },
  {
    "document_type_id": 2,
    "type_name": "Cédula de Extranjería",
    "type_code": "CE",
    "description": null
  }
]
```

-----

## WebSocket

### Conexión

**URL:** `ws://localhost:8000/ws/chat?token=<JWT_TOKEN>`

### Protocolo

El WebSocket usa mensajes JSON bidireccionales:

#### Cliente → Servidor

**Ping (Keep-alive):**

```json
{
  "type": "ping"
}
```

**Query (Consulta):**

```json
{
  "type": "query",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "document_type_id": 1,
  "document_number": "123456789",
  "question": "¿Cuándo fue la última cita?"
}
```

#### Servidor → Cliente

**Connected (Bienvenida):**

```json
{
  "type": "connected",
  "message": "Conexión establecida exitosamente",
  "user_id": 1,
  "timestamp": "2025-12-11T10:30:00Z"
}
```

**Pong:**

```json
{
  "type": "pong",
  "timestamp": "2025-12-11T10:30:05Z"
}
```

**Status (Progreso):**

```json
{
  "type": "status",
  "message": "Buscando información del paciente"
}
```

**Stream Start:**

```json
{
  "type": "stream_start"
}
```

**Token (Streaming):**

```json
{
  "type": "token",
  "token": "Juan "
}
```

**Stream End:**

```json
{
  "type": "stream_end"
}
```

**Complete (Respuesta completa):**

```json
{
  "type": "complete",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2025-12-11T10:35:00Z",
  "patient_info": { ... },
  "answer": { ... },
  "sources": [ ... ],
  "metadata": { ... }
}
```

**Error:**

```json
{
  "type": "error",
  "error": {
    "code": "PATIENT_NOT_FOUND",
    "message": "Paciente no encontrado"
  }
}
```

### Rate Limiting

  - **Límite**: 20 mensajes por minuto por usuario
  - **Respuesta al exceder**: Error con código `RATE_LIMIT_EXCEEDED`
  - **Timeout**: 5 minutos de inactividad

-----

## Seguridad

### Autenticación JWT

**Configuración:**

  - Algoritmo: HS256
  - Expiración: 30 minutos
  - Payload: `{"sub": user_id, "exp": timestamp}`
  - Secret Key: Mínimo 32 caracteres (configurado en `.env`)

**Flujo:**

1.  Usuario hace login → Backend genera JWT
2.  Cliente almacena JWT en `localStorage`
3.  Cliente incluye JWT en header `Authorization: Bearer <token>`
4.  Backend valida JWT en cada request

### Hashing de Contraseñas

  - **Algoritmo**: bcrypt
  - **Factor de costo**: 12
  - **Nunca** se almacenan contraseñas en texto plano
  - **Requisitos de contraseña**:
      - Mínimo 8 caracteres
      - Al menos 1 mayúscula
      - Al menos 1 minúscula
      - Al menos 1 número
      - Al menos 1 carácter especial

### Protección contra Inyección SQL

```python
# ✅ CORRECTO: Usando parámetros
query = text("SELECT * FROM users WHERE email = :email")
result = db.execute(query, {"email": user_email})

# ❌ INCORRECTO: Concatenación de strings
query = f"SELECT * FROM users WHERE email = '{user_email}'"
```

### Validación de Inputs

**Sanitización de número de documento:**

```python
def sanitize_document_number(doc_number: str) -> str:
    """
    Sanitiza el número de documento eliminando caracteres peligrosos.
    Solo permite: letras (A-Z, a-z), números (0-9), guiones (-)
    """
    # Eliminar espacios
    doc_number = doc_number.strip()
    
    # Solo permitir caracteres seguros
    sanitized = re.sub(r'[^A-Za-z0-9\-]', '', doc_number)
    
    # Limitar longitud máxima
    if len(sanitized) > 50:
        sanitized = sanitized[:50]
    
    return sanitized
```

**Validación de queries:**

```python
def validate_query_input(input_data: QueryInput) -> tuple[bool, Optional[str]]:
    """
    Valida los datos de entrada para prevenir inyecciones.
    
    Returns:
        (is_valid, error_message)
    """
    # Validar document_type_id
    valid_doc_types = [1, 2, 3, 4, 5, 6, 7, 8]
    if input_data.document_type_id not in valid_doc_types:
        return False, f"Tipo de documento inválido: {input_data.document_type_id}"
    
    # Validar pregunta
    if len(input_data.question) > 1000:
        return False, "La pregunta no puede exceder 1000 caracteres"
    
    # Detectar intentos de inyección SQL
    dangerous_patterns = [
        r"(\bOR\b.*=.*)",
        r"(DROP\s+TABLE)",
        r"(DELETE\s+FROM)",
        r"(--\s*$)",
    ]
    
    combined_input = f"{input_data.document_number} {input_data.question}"
    for pattern in dangerous_patterns:
        if re.search(pattern, combined_input, re.IGNORECASE):
            return False, "Query contiene patrones potencialmente peligrosos"
    
    return True, None
```

### Protección CORS

**Desarrollo:**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Producción:**

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "[https://smarthealth.com](https://smarthealth.com)",
        "[https://app.smarthealth.com](https://app.smarthealth.com)"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

-----

## Estructura del Proyecto

```
BACKEND-FAPI-BDI-SMART_HEALTH/
│
├── backend/                          # Backend FastAPI
│   ├── src/
│   │   └── app/
│   │       ├── __init__.py
│   │       ├── main.py              # Punto de entrada FastAPI
│   │       │
│   │       ├── core/                # Configuración central
│   │       │   ├── __init__.py
│   │       │   ├── security.py      # JWT, bcrypt, dependencies
│   │       │
│   │       ├── database/            # Base de datos
│   │       │   ├── __init__.py
│   │       │   ├── database.py      # Engine SQLAlchemy
│   │       │   └── db_config.py     # Settings Pydantic
│   │       │
│   │       ├── models/              # Modelos SQLAlchemy
│   │       │   ├── __init__.py
│   │       │   ├── user.py
│   │       │   ├── patient.py
│   │       │   ├── appointment.py
│   │       │   ├── medical_record.py
│   │       │   ├── diagnosis.py
│   │       │   ├── prescription.py
│   │       │   ├── record_diagnosis.py
│   │       │   └── audit_logs.py
│   │       │
│   │       ├── schemas/             # Schemas Pydantic
│   │       │   ├── __init__.py
│   │       │   ├── user.py
│   │       │   ├── clinical.py      # DTOs clínicos
│   │       │   ├── rag.py           # SimilarChunk
│   │       │   ├── llm_schemas.py
│   │       │   ├── catalog.py
│   │       │   └── audit_logs.py
│   │       │
│   │       ├── routers/             # Endpoints API
│   │       │   ├── __init__.py
│   │       │   ├── auth.py          # /auth/register, /auth/login
│   │       │   ├── user.py          # /users/me, CRUD users
│   │       │   ├── query.py         # /query/ (RAG endpoint)
│   │       │   ├── websocket_chat.py # /ws/chat
│   │       │   ├── history.py       # /history/
│   │       │   └── catalog.py       # /catalog/document-types
│   │       │
│   │       └── services/            # Lógica de negocio
│   │           ├── __init__.py
│   │           ├── auth_service.py  # Registro, login
│   │           ├── auth_utils.py    # Verify token (WebSocket)
│   │           ├── user.py          # CRUD usuarios
│   │           ├── clinical_service.py # P2: Fetch datos clínicos
│   │           ├── vector_search.py    # P3: Búsqueda vectorial
│   │           ├── llm_client.py       # Cliente OpenAI
│   │           ├── llm_service.py      # LLM Service
│   │           ├── rag_context.py      # P4: Build context, sources
│   │           └── generate_embeddings.py # Script de embeddings
│   │
│   ├── requirements.txt              # Dependencias Python
│   ├── start_server.py              # Script de inicio
│   ├── test_db_connection.py        # Test de conexión
│   ├── test_llm_real.py             # Test LLM
│   ├── test_security.py             # Suite de seguridad
│   ├── remove_emojis.py             # Script de limpieza
│   │
│   ├── database_setup.md            # Guía de instalación DB
│   ├── security.md                  # Guía de seguridad
│   └── README.md                    # Este archivo
│
├── frontend/                         # Frontend Vanilla JS
│   ├── public/                      # Archivos HTML
│   │   ├── index.html              # Chat (requiere auth)
│   │   ├── login.html              # Login
│   │   ├── register.html           # Registro
│   │   ├── test.html               # Tests
│   │   └── unauthorized.html       # No autorizado
│   │
│   ├── static/                      # Assets estáticos
│   │   ├── css/
│   │   │   ├── base.css           # Estilos base
│   │   │   ├── animations.css     # Animaciones
│   │   │   ├── chat.css           # Chat UI
│   │   │   └── test.css           # Tests
│   │   │
│   │   ├── js/
│   │   │   ├── utils.js           # Storage, API, Auth, Utils
│   │   │   ├── auth.js            # Login/Register
│   │   │   ├── chat.js            # Lógica del chat
│   │   │   ├── route-protection.js # Protección de rutas
│   │   │   └── test.js            # Suite de tests
│   │   │
│   │   └── img/
│   │       └── Logo, Png.png      # Logo SmartHealth
│   │
│   ├── docs/
│   │   └── websocket.md            # Protocolo WebSocket
│   │
│   ├── scripts/
│   │   ├── setup_websocket.bat    # Setup Windows
│   │   └── test_websocket.py      # Test WebSocket
│   │
│   └── server.py                   # Servidor HTTP simple (dev)
│
├── pipelines/                       # Scripts de base de datos
│   ├── 01-create-database/
│   │   ├── script-01.py           # Crear DB y usuario
│   │   └── script-02.py           # Instalar pgvector
│   │
│   └── 02-insert-data/
│       ├── create-tables.py       # Crear esquema y tablas
│       └── script-02.py           # Insertar datos de ejemplo
│
├── docs/                            # Documentación adicional
│   ├── AUTENTICACION.md            # Sistema de autenticación
│   ├── interface.md                # Interfaces P4
│   └── p4_interface.md             # Funciones P4
│
├── .env                             # Variables de entorno (NO COMMITEAR)
├── .gitignore
└── README.md                        # Este archivo
```

-----

## Tecnologías Utilizadas

### Backend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.9+ | Lenguaje principal |
| **FastAPI** | 0.111.0 | Framework web |
| **Uvicorn** | 0.30.1 | Servidor ASGI |
| **SQLAlchemy** | 2.0.29 | ORM para PostgreSQL |
| **Pydantic** | 2.8.0 | Validación de datos |
| **psycopg2-binary** | 2.9.9 | Driver PostgreSQL |
| **pgvector** | 0.4.1 | Extensión para vectores |
| **OpenAI** | 1.12.0+ | API para GPT y embeddings |
| **python-jose** | 3.3.0 | JWT tokens |
| **passlib[bcrypt]** | 1.7.4 | Hashing de contraseñas |
| **websockets** | 12.0+ | WebSocket support |
| **python-dotenv** | 1.0.1 | Variables de entorno |

### Frontend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Vanilla JavaScript** | ES6+ | Lógica del frontend |
| **HTML5** | - | Estructura |
| **CSS3** | - | Estilos (custom) |
| **WebSocket API** | - | Chat en tiempo real |
| **Fetch API** | - | Llamadas HTTP |
| **LocalStorage API** | - | Almacenamiento local |

### Base de Datos

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **PostgreSQL** | 16+ | Base de datos principal |
| **pgvector** | 0.5.1+ | Búsqueda vectorial |

### Servicios Externos

| Servicio | Modelo | Propósito |
|----------|--------|-----------|
| **OpenAI GPT** | gpt-4o-mini | Generación de respuestas |
| **OpenAI Embeddings** | text-embedding-3-small | Embeddings vectoriales |

-----

## Desarrollo

### Entorno de Desarrollo

**Backend:**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

**Frontend:**

```bash
# No requiere instalación
# Solo abrir en navegador o usar servidor HTTP simple
cd frontend
python server.py
```

### Variables de Entorno de Desarrollo

Crear archivo `.env` en la raíz:

```env
# Desarrollo
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smarthdb
DB_USER=sm_admin
DB_PASSWORD=sm2025

# Generar con: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=dev_secret_key_change_in_production_32chars_min

APP_ENV=development

# OpenAI (obtener en [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys))
OPENAI_API_KEY=sk-your-api-key-here

# Configuración LLM
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=2000
LLM_TIMEOUT=30
```

### Ejecutar en Desarrollo

**Backend:**

```bash
cd backend
python start_server.py
# o
uvicorn src.app.main:app --reload --port 8000
```

**Acceder:**

  - Frontend: http://localhost:8000/chat
  - API Docs: http://localhost:8000/docs
  - Health: http://localhost:8000/health

### Hot Reload

  - **Backend**: Uvicorn con `--reload` detecta cambios automáticamente
  - **Frontend**: Solo refrescar el navegador (Ctrl+R)

### Debugging

**VSCode (Backend):**

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "src.app.main:app",
                "--reload",
                "--port",
                "8000"
            ],
            "cwd": "${workspaceFolder}/backend",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/backend/src"
            }
        }
    ]
}
```

**Browser DevTools (Frontend):**

  - Chrome: F12 → Console/Network
  - Firefox: F12 → Console/Network
  - Safari: Cmd+Opt+I → Console/Network

-----

## Testing

### Tests de Backend

**Test de Conexión a Base de Datos:**

```bash
cd backend
python test_db_connection.py
```

**Test de Seguridad:**

```bash
python test_security.py
```

**Test de LLM:**

```bash
python test_llm_real.py
```

### Tests de Frontend

Abrir en navegador:

```
http://localhost:8000/public/test.html
```

### Tests Manuales

**Flujo Completo:**

1.  Registro: http://localhost:8000/register
2.  Login: http://localhost:8000/login
3.  Chat: http://localhost:8000/chat
4.  Realizar consulta
5.  Verificar respuesta

**Verificar WebSocket:**

```bash
cd frontend/scripts
python test_websocket.py
```

-----

## Despliegue en Producción

### Checklist Pre-Deploy

#### Configuración

  - [ ] `SECRET_KEY` única y segura (64+ caracteres)
  - [ ] `APP_ENV=production`
  - [ ] HTTPS/TLS configurado
  - [ ] CORS restrictivo (solo dominios permitidos)
  - [ ] Rate limiting habilitado
  - [ ] Variables de entorno seguras
  - [ ] API Docs deshabilitada (`/docs`, `/redoc`)
  - [ ] Logs configurados

#### Base de Datos

  - [ ] Contraseña fuerte de PostgreSQL
  - [ ] Firewall configurado (solo IPs específicas)
  - [ ] Backups automáticos configurados
  - [ ] Encriptación habilitada
  - [ ] pgvector instalado

#### Seguridad

  - [ ] Certificado SSL/TLS válido
  - [ ] Headers de seguridad habilitados
  - [ ] JWT con SECRET\_KEY única
  - [ ] Contraseñas hasheadas (bcrypt)
  - [ ] Rate limiting configurado
  - [ ] SQL injection protegido
  - [ ] XSS protegido

### Despliegue con Gunicorn

**Instalar Gunicorn:**

```bash
pip install gunicorn
```

**Ejecutar:**

```bash
gunicorn src.app.main:app \
  -w 4 \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile access.log \
  --error-logfile error.log \
  --log-level info
```

### Despliegue con Docker

**Dockerfile:**

```dockerfile
FROM python:3.9-slim

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Crear usuario no privilegiado
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY src/ ./src/

# Cambiar a usuario no privilegiado
USER appuser

# Puerto
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "src.app.main:app", \
     "-w", "4", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: smarthdb
      POSTGRES_USER: sm_admin
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "127.0.0.1:5432:5432"
    restart: unless-stopped

  api:
    build: ./backend
    env_file:
      - .env
    ports:
      - "127.0.0.1:8000:8000"
    depends_on:
      - db
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true

volumes:
  postgres_data:
```

### Nginx como Reverse Proxy

**nginx.conf:**

```nginx
server {
    listen 80;
    server_name smarthealth.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name smarthealth.com;

    ssl_certificate /etc/letsencrypt/live/[smarthealth.com/fullchain.pem](https://smarthealth.com/fullchain.pem);
    ssl_certificate_key /etc/letsencrypt/live/[smarthealth.com/privkey.pem](https://smarthealth.com/privkey.pem);

    # Headers de seguridad
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass [http://127.0.0.1:8000](http://127.0.0.1:8000);
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws/ {
        proxy_pass [http://127.0.0.1:8000](http://127.0.0.1:8000);
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Systemd Service

**smarthealth.service:**

```ini
[Unit]
Description=SmartHealth API
After=network.target postgresql.service

[Service]
Type=notify
User=appuser
Group=appuser
WorkingDirectory=/opt/smarthealth/backend
Environment="PATH=/opt/smarthealth/venv/bin"
ExecStart=/opt/smarthealth/venv/bin/gunicorn src.app.main:app \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Activar:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable smarthealth
sudo systemctl start smarthealth
sudo systemctl status smarthealth
```

-----

## Monitoreo y Logs

### Logs de Aplicación

**Ubicación:**

  - Backend: `backend/logs/app.log`
  - Gunicorn: `access.log`, `error.log`

**Formato:**

```
2025-12-11 10:30:45 - app.services.auth_service - INFO - Login exitoso: user@example.com
```

### Monitoreo de Base de Datos

**Verificar conexiones:**

```sql
SELECT count(*) FROM pg_stat_activity WHERE datname = 'smarthdb';
```

**Verificar tamaño:**

```sql
SELECT pg_size_pretty(pg_database_size('smarthdb'));
```

**Verificar tablas más grandes:**

```sql
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'smart_health'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### Health Check

```bash
curl http://localhost:8000/health
```

**Respuesta esperada:**

```json
{
    "status": "healthy",
    "timestamp": 1733918400.0,
    "environment": "production",
    "services": {
        "database": "connected",
        "llm": "ready",
        "vector_search": "ready",
        "websocket": "enabled"
    }
}
```

-----

## Troubleshooting

### Problemas Comunes

#### Error: "No se puede conectar a PostgreSQL"

**Síntomas:**

```
psycopg2.OperationalError: could not connect to server
```

**Solución:**

1.  Verificar que PostgreSQL esté corriendo:
    ```bash
    sudo systemctl status postgresql
    ```
2.  Verificar puerto y host en `.env`
3.  Verificar firewall:
    ```bash
    sudo ufw allow 5432/tcp
    ```

#### Error: "Token JWT inválido"

**Síntomas:**

```
401 Unauthorized: No se pudieron validar las credenciales
```

**Solución:**

1.  Verificar que `SECRET_KEY` sea la misma en todos los entornos
2.  Verificar que el token no haya expirado (30 min)
3.  Limpiar localStorage del navegador:
    ```javascript
    localStorage.clear()
    ```

#### Error: "SECRET\_KEY debe tener al menos 32 caracteres"

**Solución:**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

#### Error: "OpenAI API rate limit"

**Síntomas:**

```
openai.error.RateLimitError: You exceeded your current quota
```

**Solución:**

1.  Verificar créditos en [https://platform.openai.com/account/usage](https://platform.openai.com/account/usage)
2.  Reducir `LLM_MAX_TOKENS` en `.env`
3.  Implementar caché de respuestas

#### Error: "pgvector extension not found"

**Síntomas:**

```
psycopg2.errors.UndefinedObject: type "vector" does not exist
```

**Solución:**

1.  Instalar pgvector:
    ```bash
    cd pipelines/01-create-database
    python script-02.py
    ```
2.  Verificar instalación:
    ```sql
    \dx
    ```

#### Error: "CORS policy blocked"

**Síntomas:**

```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solución:**

1.  Verificar configuración de CORS en `main.py`
2.  Agregar origen permitido en `CORS_ORIGINS` del `.env`
3.  En desarrollo, usar `allow_origins=["*"]`

### Logs de Debugging

**Habilitar logs detallados:**

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Ver logs en tiempo real:**

```bash
tail -f backend/logs/app.log
```

-----

## Recursos Adicionales

### Documentación Oficial

  - **FastAPI**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
  - **SQLAlchemy**: [https://docs.sqlalchemy.org/](https://docs.sqlalchemy.org/)
  - **Pydantic**: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)
  - **PostgreSQL**: [https://www.postgresql.org/docs/](https://www.postgresql.org/docs/)
  - **pgvector**: [https://github.com/pgvector/pgvector](https://github.com/pgvector/pgvector)
  - **OpenAI API**: [https://platform.openai.com/docs/](https://platform.openai.com/docs/)

### Tutoriales y Guías

  - [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
  - [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
  - [pgvector Guide](https://github.com/pgvector/pgvector#installation)
  - [JWT Authentication](https://fastapi.tiangolo.com/tutorial/security/)

### Herramientas Útiles

  - **Postman**: Testing de API REST
  - **WebSocket King**: Testing de WebSocket
  - **pgAdmin**: Administración de PostgreSQL
  - **Docker Desktop**: Contenedores

-----

## Contribución

### Guía de Contribución

1.  **Fork** el repositorio
2.  Crear una **branch** para tu feature:
    ```bash
    git checkout -b feature/nueva-funcionalidad
    ```
3.  **Commit** tus cambios:
    ```bash
    git commit -m "feat: agregar nueva funcionalidad"
    ```
4.  **Push** a tu branch:
    ```bash
    git push origin feature/nueva-funcionalidad
    ```
5.  Abrir un **Pull Request**

### Convenciones de Código

**Python:**

  - Seguir PEP 8
  - Docstrings en todas las funciones
  - Type hints siempre que sea posible
  - Nombres descriptivos

**JavaScript:**

  - Camel case para variables y funciones
  - Pascal case para clases
  - Comentarios JSDoc

**Git Commits:**

  - `feat:` nueva funcionalidad
  - `fix:` corrección de bug
  - `docs:` documentación
  - `refactor:` refactorización
  - `test:` tests
  - `chore:` tareas de mantenimiento

-----

## Licencia

Este proyecto está bajo la licencia **MIT**.

```
MIT License

Copyright (c) 2025 SmartHealth Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

-----

## Agradecimientos

  - **OpenAI** por la API de GPT y embeddings
  - **FastAPI** por el excelente framework
  - **pgvector** por la extensión de vectores para PostgreSQL
  - **Comunidad Open Source** por las librerías utilizadas

-----

## Contacto

**Equipo de Desarrollo:**

  - Ivan Ospino
  - Gisell Anaya
  - Jhoan Smith
  - Jeison Mendez
  - Jhon Mantilla

**Repositorio:**
[https://github.com/Ospino89/-backend-fapi-bdi-smart\_health](https://github.com/Ospino89/-backend-fapi-bdi-smart_health)

-----

## Changelog

### v2.0.0 (2025-12-11)

  - ✨ Sistema RAG completo implementado
  - ✨ WebSocket para streaming en tiempo real
  - ✨ Autenticación JWT
  - ✨ Frontend Vanilla JS responsive
  - ✨ Búsqueda vectorial con pgvector
  - ✨ Integración con OpenAI GPT-4o-mini
  - 🐛 Correcciones de seguridad
  - 📝 Documentación completa

### v1.0.0 (2025-11-22)

  - 🎉 Release inicial
  - ⚡ API REST básica
  - 💾 Base de datos PostgreSQL
  - 🔐 Sistema

<!-- end list -->

```
```



