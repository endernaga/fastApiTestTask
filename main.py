from fastapi import FastAPI

from routers.workflow import workflow_urls

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})
app.include_router(workflow_urls.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
