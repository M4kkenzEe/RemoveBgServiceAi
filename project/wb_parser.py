import os
from io import BytesIO

import requests
from PIL import Image

a1 = "https://basket-20.wbbasket.ru/vol3409/part340963/340963452/images/c246x328/1.webp"
a2 = "https://basket-11.wbbasket.ru/vol1650/part165009/165009684/images/big/1.webp"
a3 = "https://basket-11.wbbasket.ru/vol3821/part382184/382184520/images/c246x328/1.webp"
a4 = "https://basket-14.wbbasket.ru/vol2172/part217257/217257578/images/big/1.webp"


def wb_parser1(url: str) -> str:
    article = get_article(url)
    if not article:
        return None

    os.makedirs("uploads", exist_ok=True)

    for number in range(1, 100):
        buff_number = ""
        if number < 10:
            buff_number += "0"

        img_url = f"https://basket-{buff_number + str(number)}.wbbasket.ru/vol{article[:4]}/part{article[:6]}/{article}/images/big/1.webp"
        response = requests.get(img_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            png_path = os.path.join("uploads", f"{article}_{number}.png")
            img.save(png_path, "PNG")
            return png_path  # Возвращаем путь к сохранённому PNG
    return None


def get_article(url: str) -> str:
    import re

    pattern = r"/catalog/(\d+)/detail\.aspx"

    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


def wb_parser(url: str) -> bytes:
    article = get_article(url)
    if not article:
        return None

    for number in range(10, 30):
        img_url = f"https://basket-{number}.wbbasket.ru/vol{article[:4]}/part{article[:6]}/{article}/images/big/1.webp"
        response = requests.get(img_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            output_buffer = BytesIO()
            img.save(output_buffer, "PNG")
            return output_buffer.getvalue()  # Возвращаем байты PNG
    return None
