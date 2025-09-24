from io import BytesIO
from PIL import Image
from rembg import remove


def remove_background_sync(input_image_bytes: bytes) -> bytes:
    input_image = Image.open(BytesIO(input_image_bytes))
    output_image = remove(input_image)
    buffer = BytesIO()
    output_image.save(buffer, format="PNG")
    return buffer.getvalue()
