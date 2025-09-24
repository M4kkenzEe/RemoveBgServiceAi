import ollama


def describe_image_with_gemma3(image_path: str) -> str:
    # Используем chat метод из ollama с моделью gemma3
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that describes the content of images."
        },
        {
            "role": "user",
            "content": "Please describe this image:",
            "images": [image_path]  # путь к изображению на локальном ПК
        }
    ]

    response = ollama.chat(
        model="gemma3",
        messages=messages
    )
    return response.message.content


# Пример использования
image_path = "/Users/chenigovtsev2001mail.ru/Wardrobe/PocketWardrobeBackend/looks/e447e621-3dd3-40a3-bf05-3e8fd915c522.jpg"
description = describe_image_with_gemma3(image_path)
print("Описание изображения:", description)
