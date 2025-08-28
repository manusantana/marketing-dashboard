from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import upload, kpis

app = FastAPI(
    title="Marketing Analytics API",
    description="API para ingesta de datos y cálculo de KPIs de marketing",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod restringe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⬇️ sin prefix aquí (ya está en cada router)
app.include_router(upload.router)
app.include_router(kpis.router)

@app.get("/")
def root():
    return {"message": "Marketing Analytics API funcionando 🚀"}
