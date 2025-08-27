# Marketing Analytics (FastAPI + React + Postgres)

## 🚀 Levantar entorno

```bash
docker compose up --build
```

### Servicios
- Backend → http://localhost:8000  
- Swagger → http://localhost:8000/docs  
- Frontend → http://localhost:5173  
- DB → localhost:5432 (user=app, pass=app, db=marketing)

### 📌 Flujo
1. Subir Excel/CSV en **Frontend → Upload**.  
2. Procesar datos en DB vía FastAPI.  
3. Consultar KPIs básicos en **Frontend → Dashboard**.  
