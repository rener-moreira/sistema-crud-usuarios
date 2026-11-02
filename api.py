from fastapi import FastAPI, APIRouter, HTTPException
from models import Usuario, UsuarioUpdate
from crud_usuario import criar_usuario as criar_usuario_crud
from crud_usuario import listar_user, listar_por_id
from crud_usuario import atualizar, excluir



app = FastAPI(
    title="Sistema CRUD de Usuários",
    version="1.0.0",
)

router = APIRouter()

#Router Criar 

@router.post("/usuarios")
def criar_usuario(usuario: Usuario):
    criar_usuario_crud(
        usuario.nome,
        usuario.idade,
        usuario.cidade
    )
    return{"msg":"Usuário criado com sucesso"}

#Router Listar
@router.get("/usuarios")
def listar_all():
    return listar_user()

#Router Listar by ID
@router.get("/usuarios/{id}")
def listar_id(id:int):
    usuario = listar_por_id(id)

    if usuario is None:
        raise HTTPException(404, f"Usuario não encontrado.")

    else: 
        return usuario

#Router Atualizar PATCH
@router.patch("/usuarios")
def atualizar_usuario(id:int, usuario:UsuarioUpdate):
    if not usuario.model_dump(exclude_unset=True):
        raise HTTPException(400, "Envie pelo menos um campo para atualilzar")

    usuario_listar = listar_por_id(id)
    if usuario_listar is None:
        raise HTTPException (404, "Esse Usuário não existe")

    atualizar(id, usuario)
    return{"msg":f"Usuário {id} atualizado com sucesso"}

#Router Deletar
@router.delete("/usuarios/deletar") 
def deletar_usuario(id:int):
    usuario = listar_por_id(id)

    if usuario is None :
        raise HTTPException(404, "Este Usuario Não existe")
    
    excluir(id)
    return{"msg":f"Usuario {id} excluido com sucesso!"}    

app.include_router(router)