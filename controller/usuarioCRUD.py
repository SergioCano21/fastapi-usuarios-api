from typing import List
from fastapi import HTTPException, APIRouter
from db.db import collection
from model.usuario import Usuario


router = APIRouter()

@router.post("/", response_description="Crear nuevo usuario", response_model= Usuario)
async def create_usuario(usuario: Usuario):
    exist_user = await collection.find_one({"email": usuario.email})
    if exist_user != None:
        raise HTTPException(status_code=404, detail="Email existente")
    
    result = await collection.insert_one(usuario.dict())
    usuario._id = str(result.inserted_id)
    return usuario

@router.get("/", response_description="Listar usuarios", response_model= List[Usuario])
async def read_usuarios():
    usuarios = await collection.find().to_list(100)
    for usuario in usuarios:
        usuario["_id"] = str(usuario["_id"])
    return usuarios

@router.put("/{email}", response_description="Actualizar usuario", response_model=Usuario)
async def update_usuario(email: str, usuario: Usuario):
    updated_usuario = await collection.find_one_and_update({"email":email}, {"$set": usuario.dict()})
    if updated_usuario:
        return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.get("/{email}", response_description="Encontrar usuario por email", response_model=Usuario)
async def find_by_email_usuario(email:str):
    usuario = await collection.find_one({"email": email})
    if usuario:
        return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.delete("/{email}", response_description="Elimimar usuario", response_model=Usuario)
async def delete_usuario(email:str):
    deleted_usuario = collection.find_one_and_delete({"email": email})
    if deleted_usuario:
        return deleted_usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")