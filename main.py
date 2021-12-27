from fastapi import FastAPI, File, UploadFile, status
from fastapi.responses import HTMLResponse
import aiofiles
from starlette.responses import JSONResponse

app = FastAPI()


@app.post("/files")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/uploadFile")
async def create_upload_file(file: UploadFile = File(...)):
    try:
        async with aiofiles.open(file.filename, "wb") as out_file:
            content = await file.read()
            await out_file.write(content)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)}
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"result": "success"}
        )


@app.get("/")
async def main():
    content = """
                <body>
                <form action="/files/" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit">
                </form>
                <form action="/uploadFile/" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit">
                </form>
                </body>
              """
    return HTMLResponse(content=content)
