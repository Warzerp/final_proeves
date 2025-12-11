# BACKEND-FAPI-BDI-SMART_HEALTH
# SmartHealth - Sistema de Consulta Clínica Inteligente con RAG

**Desarrolladores**: Ivan Ospino, Gisell Anaya, Jhoan Smith, Jeison Mendez, Jhon Mantilla  
**Versión**: 2.0.0 Final  
**Creado**: 22-Noviembre-2025  
**Última actualización**: 11-Diciembre-2025

---

## 📋 Tabla de Contenidos

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
12. [Despliegue en Producción](#despliegue-en-producción)
13. [Troubleshooting](#troubleshooting)
14. [Contribución](#contribución)
15. [Licencia](#licencia)

---

## 🎯 Descripción General

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
1. Busca al paciente por documento
2. Realiza búsqueda vectorial en su historial
3. Construye contexto clínico relevante
4. Genera respuesta natural con GPT-4o-mini
5. Retorna respuesta con fuentes verificables

Respuesta: "Juan Pérez tuvo su última cita el 9 de noviembre de 2024,
un examen médico de chequeo general con la doctora Carolina Gutiérrez,
especialista en medicina física y rehabilitación."
```

---

## ✨ Características Principales

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

---

## 🏗️ Arquitectura del Sistema

### Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTE WEB                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Login     │  │   Register   │  │     Chat     │      │
│  │  (HTML/CSS)  │  │  (HTML/CSS)  │  │  (HTML/CSS)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
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
│  │  Schema: smart_health                                │   │
│  │                                                       │   │
│  │  • patients (embeddings)                             │   │
│  │  • doctors (embeddings)                              │   │
│  │  • appointments (embeddings)                         │   │
│  │  • medical_records (embeddings)                      │   │
│  │  • diagnoses (embeddings)                            │   │
│  │  • prescriptions                                     │   │
│  │  • medications (embeddings)                          │   │
│  │  • users (auth)                                      │   │
│  │  • audit_logs (history)                              │   │
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
1. Usuario envía pregunta + documento de paciente
   ↓
2. Backend busca paciente en PostgreSQL
   ↓
3. Búsqueda vectorial: similar_chunks (k=15, min_score=0.3)
   • appointments.reason_embedding
   • medical_records.summary_embedding
   • diagnoses.description_embedding
   • prescriptions.medication_embedding
   ↓
4. Construcción de contexto:
   • Información básica del paciente
   • Citas médicas recientes
   • Diagnósticos registrados
   • Medicamentos prescritos
   • Chunks relevantes de búsqueda vectorial
   ↓
5. LLM genera respuesta:
   system_prompt + context + question → GPT-4o-mini
   ↓
6. Construcción de sources (trazabilidad)
   ↓
7. Respuesta JSON estructurada + metadata
   ↓
8. Guardado en audit_logs para historial
```

---

## 📦 Requisitos del Sistema

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
  - Obtener en: https://platform.openai.com/api-keys
  - Modelos necesarios: GPT-4o-mini + text-embedding-3-small

---

## 🚀 Instalación Rápida

### Opción 1: Script Automatizado (Recomendado)

```bash
# 1. Clonar repositorio
git clone https://github.com/Ospino89/-backend-fapi-bdi-smart_health.git
cd -backend-fapi-bdi-smart_health

# 2. Ejecutar instalador automático
./install.sh  # Linux/Mac
# o
install.bat   # Windows

# 3. El script realizará:
#    - Instalación de dependencias Python
#    - Configuración de PostgreSQL + pgvector
#    - Creación de base de datos
#    - Inserción de datos de ejemplo
#    - Configuración del archivo .env
```

### Opción 2: Docker (Próximamente)

```bash
# Construcción y ejecución con Docker Compose
docker-compose up --build

# Acceder a:
# - Frontend: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - PostgreSQL: localhost:5432
```

---

## 📚 Instalación Detallada

### Paso 1: Preparar el Entorno

```bash
# 1. Clonar el repositorio
git clone https://github.com/Ospino89/-backend-fapi-bdi-smart_health.git
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

Ver guía completa en: [`backend/database_setup.md`](backend/database_setup.md)

```bash
# 1. Instalar PostgreSQL 16
# Windows: https://www.postgresql.org/download/windows/
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
# Obtener en: https://platform.openai.com/api-keys
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

```bash
# Este paso consume créditos de OpenAI
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

---

## 🎨 Configuración del Frontend

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

1. **Sin Dependencias Externas**: JavaScript vanilla, no requiere npm/webpack
2. **Auto-configuración**: Detecta automáticamente la URL del backend
3. **Responsive Design**: Se adapta a móviles, tablets y escritorio
4. **Protección de Rutas**: Redirección automática según autenticación
5. **WebSocket Integrado**: Chat en tiempo real con reconexión automática

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

---

## 🎮 Uso del Sistema

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
INFO:     Uvicorn running on http://127.0.0.1:8000
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

1. **Registro de Usuario**
   - Ir a http://localhost:8000/register
   - Completar formulario
   - Click en "Registrarse"

2. **Login**
   - Ir a http://localhost:8000/login
   - Ingresar credenciales
   - El sistema redirige a /chat

3. **Realizar Consulta**
   - Seleccionar tipo de documento
   - Ingresar número de documento
   - Escribir pregunta
   - Click en "Enviar" o Enter
   - Ver respuesta en tiempo real (streaming)

4. **Ver Historial**
   - Click en botón "Historial"
   - Ver consultas anteriores
   - Click en una consulta para ver detalles

---

## 🔌 API Endpoints

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

---

## 🔌 WebSocket

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

---

## 🔒 Seguridad

### Autenticación JWT

**Configuración:**
- Algoritmo: HS256
- Expiración: 30 minutos
- Payload: `{"sub": user_id, "exp": timestamp}`
- Secret Key: Mínimo 32 caracteres (configurado en `.env`)

**Flujo:**
1. Usuario hace login → Backend genera JWT
2. Cliente almacena JWT en `localStorage`
3. Cliente incluye JWT en header `Authorization: Bearer <token>`
4. Backend valida JWT en cada request

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
def sanitize_document_number(
