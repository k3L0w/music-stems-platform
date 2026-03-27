from fastapi import FastAPI

app = FastAPI(
    title="Music Stems Platform API",
    description="Scaffolding inicial da API do projeto.",
    version="0.1.0",
)


@app.get("/health", tags=["infra"])
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
