from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter
import os

from app.api.auth import router as auth_router
from app.database import engine, Base
import app.models  # ensure models are registered on import

@strawberry.type
class Query:
    @strawberry.field
    def ping(self) -> str:
        return "pong"

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI(title="Heroes Chess API")

origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")
app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok"}
