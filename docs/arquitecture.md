# Arquitectura del repositorio `marketing-dashboard`

> **Stack**: FastAPI (Python) + React/Vite (JS) + Postgres + Docker Compose.

## 0) TL;DR (arranque rápido)
```bash
docker compose up --build
```
Servicios por defecto:
- **Backend**: http://localhost:8000
- **Swagger**: http://localhost:8000/docs
- **Frontend**: http://localhost:5173
- **DB**: localhost:5432 (user=app, pass=app, db=marketing)

Variables en `.env` (ejemplo mínimo):
```
POSTGRES_USER=app
POSTGRES_PASSWORD=app
POSTGRES_DB=marketing
DATABASE_URL=postgresql+psycopg2://app:app@db:5432/marketing
BACKEND_CORS_ORIGINS=["http://localhost:5173"]
ENV=dev
```

---

## 1) Estructura de carpetas (propuesta consolidada)

```
marketing-dashboard/
├─ backend/
│  └─ app/
│     ├─ main.py                     # Punto de entrada FastAPI
│     ├─ api/                        # Routers (v1, endpoints)
│     │  ├─ v1/
│     │  │  ├─ __init__.py
│     │  │  ├─ upload.py             # Endpoints de subida de ficheros
│     │  │  ├─ kpis.py               # Endpoints KPIs/consultas
│     │  │  └─ health.py             # Liveness/readiness
│     │  └─ __init__.py
│     ├─ core/                       # Configuración y seguridad
│     │  ├─ config.py                # BaseSettings (Pydantic)
│     │  └─ logging.py               # Logging estructurado
│     ├─ db/
│     │  ├─ base.py                  # Base declarativa (SQLAlchemy)
│     │  ├─ models/                  # Modelos ORM
│     │  │  ├─ __init__.py
│     │  │  └─ kpi.py                # Ejemplo de tabla KPI
│     │  ├─ session.py               # SessionLocal, engine
│     │  └─ migrations/              # Alembic (autogenerate)
│     ├─ schemas/                    # Pydantic (request/response)
│     │  ├─ __init__.py
│     │  ├─ upload.py                # Esquemas de subida
│     │  └─ kpi.py                   # Esquemas de salida KPIs
│     ├─ services/                   # Lógica de negocio
│     │  ├─ __init__.py
│     │  ├─ ingest.py                # Limpieza/parse de CSV/XLSX
│     │  └─ kpi.py                   # Cálculos/consultas KPI
│     ├─ utils/                      # Helpers reutilizables
│     │  ├─ files.py                 # Validación, tamaños, extensiones
│     │  └─ pandas.py                # Utilidades de df -> ORM/JSON
│     └─ __init__.py
│
├─ frontend/
│  └─ src/
│     ├─ api/                        # Clientes HTTP (axios/fetch)
│     │  ├─ client.ts
│     │  └─ kpis.ts                  # Llamadas a backend
│     ├─ components/                 # UI atómica (inputs, tablas, charts)
│     │  ├─ Chart.tsx
│     │  ├─ FileUploader.tsx
│     │  └─ KPICard.tsx
│     ├─ pages/ (o routes/)          # Vistas
│     │  ├─ Upload.tsx
│     │  └─ Dashboard.tsx
│     ├─ hooks/
│     │  └─ useUpload.ts
│     ├─ lib/                        # Utils front (formatters)
│     ├─ styles/                     # CSS/ Tailwind / variables
│     ├─ types/                      # Tipos TS (alineados a schemas)
│     └─ main.tsx
│
├─ docker-compose.yml
├─ .env.example
├─ Makefile                          # Atajos (lint, test, run)
├─ README.md
└─ docs/                             # Documentación del proyecto
   ├─ arquitectura.md                # (este documento)
   └─ api.md                        # Especificación endpoints
```

**Notas clave**
- `schemas/` ≠ `models/`: Pydantic (E/S) separado de ORM (SQLAlchemy).
- Versiona API en `/api/v1` para cambios compatibles en el futuro.
- `services/` sin dependencias de FastAPI (facilita tests unitarios).

---

## 2) Backend: patrones y convenciones

### 2.1 Configuración (Pydantic BaseSettings)
```python
# backend/app/core/config.py
from pydantic import BaseSettings, AnyHttpUrl
from typing import List

class Settings(BaseSettings):
    ENV: str = "dev"
    DATABASE_URL: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        env_file = ".env"

settings = Settings()
```
- Centraliza variables. No importes `.env` manualmente.

### 2.2 DB y sesiones
- `session.py`: crea `engine` y `SessionLocal`.
- Dependencia FastAPI:
```python
from contextlib import contextmanager
from .session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 2.3 Schemas de respuesta
- Define `Response` y `Create/Update` separados.
- Activa `model_config = {"from_attributes": True}` (Pydantic v2) para `ORM`.

### 2.4 Routers (v1)
```python
from fastapi import APIRouter
router = APIRouter(prefix="/api/v1")
```
- `upload.py`: recibe `UploadFile`, valida tipo/tamaño, llama a `services.ingest`.
- `kpis.py`: expone endpoints de métricas agregadas y series temporales.

### 2.5 Servicios (business logic)
- `ingest.py`:
  - Lee CSV/XLSX con `pandas`.
  - Normaliza columnas (nombres, tipos, fechas, NaN).
  - Inserta en BD vía ORM/bulk.
- `kpi.py`:
  - Cálculos (groupby, ratios) siempre aquí; el router solo orquesta.

### 2.6 Errores y validación
- Lanza `HTTPException` con códigos claros (`400`, `413`, `422`, `500`).
- Límite de tamaño de fichero (p.ej. 10–50MB) y whitelist de extensiones.

### 2.7 Logging
- Formato JSON en `logging.py` (para Docker). Añade `request_id` middleware.

### 2.8 Alembic (migraciones)
- Inicializa en `db/migrations`. Usa `autogenerate` + revisiones con nombre semántico.

---

## 3) Frontend: patrones y convenciones

- **Estado**: local + hooks específicos; evita global si no es necesario.
- **HTTP**: `api/client.ts` (axios con `baseURL`), manejo de errores centralizado.
- **Tipos**: genera tipos TS desde OpenAPI (opcional) o mantenlos alineados a `schemas`.
- **UI**: componentes puros (sin llamadas a API). Páginas orquestan.
- **Gráficos**: componente `Chart` con wrapper de librería (Recharts/ApexCharts) y props tipadas.

```ts
// frontend/src/api/client.ts
import axios from "axios";
export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000" });
```

---

## 4) Flujo de datos (E2E)
1) **Upload** (Front) → `POST /api/v1/upload` (multipart).
2) **Ingesta** (Back) → parsea y persiste en Postgres.
3) **KPIs** (Back) → endpoints agregados/series.
4) **Dashboard** (Front) → consulta KPIs y renderiza charts/cards.

Representación recomendada de endpoints:
```
GET  /api/v1/health
POST /api/v1/upload (file)
GET  /api/v1/kpis/overview          # totales/ratios
GET  /api/v1/kpis/timeseries        # series por fecha
GET  /api/v1/kpis/top?by=channel    # rankings
```

---

## 5) Calidad: lint, tests, CI
- **Python**: `ruff` (lint), `black` (format), `pytest` (tests), `mypy` (tipado opcional).
- **JS/TS**: `eslint`, `prettier`, `vitest`/`jest`.
- **Makefile** (sugerido):
```
make up        # docker compose up --build
make down      # docker compose down -v
make fmt       # black . && prettier --write .
make lint      # ruff . && eslint .
make test      # pytest -q && vitest run
```
- **CI**: GitHub Actions con jobs para lint+test de backend y frontend.

---

## 6) Seguridad y robustez
- **CORS** restringido a orígenes conocidos.
- **Rate limit** (si se expone públicamente) vía proxy o middleware.
- **Validación de ficheros** (MIME, extensión, tamaño) y sanitización de nombres.
- **Manejo de PII**: evita persistir datos sensibles sin necesidad.

---

## 7) Versionado y convenciones
- Ramas: `feat/*`, `fix/*`, `chore/*`.
- Commits: Conventional Commits.
- API: versionar en ruta (`/api/v1`) y documentar breaking changes.

---

## 8) Roadmap técnico sugerido
- [ ] Añadir **Alembic** con `env.py` y `script.py.mako` en `db/migrations`.
- [ ] Endpoints `kpis` paginados y con filtros (`date_from`, `date_to`, `channel`).
- [ ] Generar **OpenAPI client** para el Front (orval/openapi-typescript).
- [ ] Añadir **task de seed** (datos demo) y **fixtures** para tests.
- [ ] Docker multi-stage (slim) y healthchecks para backend.
- [ ] Observabilidad: logs JSON + métricas (Prometheus) + tracing (OTel).

---

## 9) Ejemplos de código breves

### 9.1 Schema Pydantic (respuesta KPI)
```python
# backend/app/schemas/kpi.py
from pydantic import BaseModel

class KPIOverview(BaseModel):
    total_leads: int
    conversion_rate: float
    revenue: float
    avg_ticket: float

    model_config = {"from_attributes": True}
```

### 9.2 Router KPIs
```python
# backend/app/api/v1/kpis.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.kpi import KPIOverview
from app.services.kpi import compute_overview

router = APIRouter(prefix="/api/v1/kpis", tags=["kpis"])

@router.get("/overview", response_model=KPIOverview)
def get_overview(db: Session = Depends(get_db)):
    return compute_overview(db)
```

### 9.3 Frontend: cliente + uso
```ts
// frontend/src/api/kpis.ts
import { api } from "./client";
export const getOverview = async () => (await api.get("/api/v1/kpis/overview")).data;
```
```tsx
// frontend/src/pages/Dashboard.tsx
import { useEffect, useState } from "react";
import { getOverview } from "@/api/kpis";

export default function Dashboard() {
  const [data, setData] = useState(null);
  useEffect(() => { getOverview().then(setData); }, []);
  // Render de tarjetas con data
  return <div>{JSON.stringify(data)}</div>;
}
```

---

## 10) FAQ del repo
- **¿Dónde van los modelos de BD?** `backend/app/db/models/`.
- **¿Dónde van los schemas?** `backend/app/schemas/`.
- **¿Qué hace `services/`?** Toda la lógica de negocio (sin FastAPI).
- **¿Cómo añado un KPI?** Modelo/consulta en `services/kpi.py`, schema de respuesta en `schemas/kpi.py`, endpoint en `api/v1/kpis.py`.
- **¿Puedo cambiar a otra librería de charts?** Sí; mantén `components/Chart.tsx` como wrapper para no tocar páginas.

---

> Mantén este documento en `docs/arquitectura.md` y actualízalo con cada cambio estructural.

