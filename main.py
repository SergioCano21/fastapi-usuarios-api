from fastapi import FastAPI, HTTPException
from db.db import client
from controller.usuarioCRUD import router as usuarios_router


app = FastAPI()
app.include_router(usuarios_router, tags=["usuarios"], prefix="/usuarios")
# MongoDB connection URL
@app.on_event("shutdown")
def shutdown_db_client():
    client.close()



