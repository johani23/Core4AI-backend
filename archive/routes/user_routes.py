from fastapi import APIRouter

routes = APIRouter()

@routes.get("/")
def root():
    return {"message": "Hello from user_routes"}
