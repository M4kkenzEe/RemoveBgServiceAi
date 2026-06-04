import asyncio
from concurrent.futures import ProcessPoolExecutor
from io import BytesIO

from fastapi import FastAPI, Query, HTTPException
from fastapi import UploadFile, File
from fastapi.responses import StreamingResponse

from project.remove_background import remove_background_sync
from project.wb_parser import wb_parser

app = FastAPI()

process_pool = ProcessPoolExecutor(max_workers=4)


@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    file_bytes = await file.read()

    # loop = asyncio.get_running_loop()
    # output_bytes = await loop.run_in_executor(process_pool, remove_background_sync, file_bytes)
    output_bytes = remove_background_sync(file_bytes)

    return StreamingResponse(BytesIO(output_bytes), media_type="image/png")


@app.get("/get_wb_image/")
async def get_wb_image(url: str = Query(..., description="URL товара Wildberries")):
    png_bytes = wb_parser(url)
    if not png_bytes:
        raise HTTPException(status_code=404, detail="Изображение не найдено или URL некорректен")

    processed_bytes = remove_background_sync(png_bytes)
    return StreamingResponse(BytesIO(processed_bytes), media_type="image/png")


@app.get("/")
async def hello():
    return {"hello": "world"}

@app.get("/hello")
async def hello1():
    return {"hello": "world1"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
