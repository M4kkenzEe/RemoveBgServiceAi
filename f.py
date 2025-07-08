from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from PIL import Image
from io import BytesIO
import uvicorn

app = FastAPI()


@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    """
    Удаляет фон с изображения и возвращает результат как PNG.
    """
    try:
        # Читаем изображение
        input_image = Image.open(BytesIO(await file.read()))
        # Удаляем фон
        output_image = remove(input_image)
        # Сохраняем результат в буфер
        buffer = BytesIO()
        output_image.save(buffer, format="PNG")
        buffer.seek(0)
        # Возвращаем обработанное изображение
        return StreamingResponse(buffer, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
