from fastapi import FastAPI


app = FastAPI()

#rotas fixas devem vim primeiro para evitar que sejam confundidos por outra com parametros em uma requisição.
@app.get("/")
async def root():
    return {"message": "Hello Word! This API is working."}

@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
