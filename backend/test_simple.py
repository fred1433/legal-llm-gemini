from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Test Simple")

@app.get("/")
async def root():
    return {"message": "Test simple réussi !"}

@app.get("/health")
async def health():
    return {"status": "OK"}

if __name__ == "__main__":
    print("🧪 Test serveur simple...")
    uvicorn.run(app, host="127.0.0.1", port=8001) 