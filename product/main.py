from fastapi import FastAPI
from . import models
from .database import engine
from .routers import product, seller, login

app = FastAPI(
    title="Products API Docuementation",
    description="This is an API Documentation of Products API",
    contact={
        "Developer Name": "Sanjay Gopal",
        "Website": "https://www.linkedin.com"
    },
    # docs_url="/product/api/documentation"
)
app.include_router(product.router)
app.include_router(seller.router)
app.include_router(login.router)
models.Base.metadata.create_all(engine)