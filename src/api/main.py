from dotenv import load_dotenv
from fastapi import FastAPI
from routes.auth_routes import auth_router
from routes.process_routes import process_router


app = FastAPI()

app.include_router(auth_router, prefix= '/api')
app.include_router(process_router,  prefix= '/api')
load_dotenv()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)