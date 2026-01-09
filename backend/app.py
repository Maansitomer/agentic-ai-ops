from fastapi import FastAPI
from backend.api.ops_chat_routes import router as ops_router
from backend.api.debug_routes import router as debug_router

app = FastAPI(
    title="Agentic AI Operations Intelligence",
    version="1.0.0"
)

app.include_router(ops_router, prefix="/api")
app.include_router(debug_router)

@app.get("/")
def health_check():
    return {"status": "Backend is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000)


