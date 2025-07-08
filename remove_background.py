from PIL import Image
from rembg import remove


def remove_background(input_path, output_path):
    # Загружаем изображение
    input_image = Image.open(input_path)

    # Удаляем фон
    output_image = remove(input_image)

    # Сохраняем результат
    output_image.save(output_path, "PNG")
    print(f"Изображение сохранено по пути: {output_path}")
