import asyncio
from concurrent.futures import ProcessPoolExecutor
from io import BytesIO

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from PIL import Image
from rembg import remove

app = FastAPI()

# Создаём пул процессов для CPU-интенсивных задач
process_pool = ProcessPoolExecutor(max_workers=4)  # число воркеров подберите под CPU сервера

def remove_background_sync(input_image_bytes: bytes) -> bytes:
    """
    Синхронная функция удаления фона.
    Принимает байты изображения, возвращает байты PNG после обработки.
    """
    input_image = Image.open(BytesIO(input_image_bytes))
    # Ваша функция удаления фона (замените на реальную)
    output_image = remove(input_image)  # remove - ваша CPU-интенсивная функция
    buffer = BytesIO()
    output_image.save(buffer, format="PNG")
    return buffer.getvalue()

@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    file_bytes = await file.read()

    loop = asyncio.get_running_loop()
    # Запускаем синхронную CPU-задачу в пуле процессов, не блокируя event loop
    output_bytes = await loop.run_in_executor(process_pool, remove_background_sync, file_bytes)

    return StreamingResponse(BytesIO(output_bytes), media_type="image/png")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
