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
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(kpis.router, prefix="/kpis", tags=["KPIs"])

@app.get("/")
def root():
    return {"message": "Marketing Analytics API funcionando 🚀"}