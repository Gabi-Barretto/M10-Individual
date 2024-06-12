from PIL import Image
import io
from fastapi import UploadFile 

async def remove_background(file: UploadFile):
    # Leia o arquivo como bytes
    contents = await file.read()
    # Abra a imagem usando PIL
    image = Image.open(io.BytesIO(contents))
    # Processamento de imagem (exemplo simples)
    image = image.convert("L")  # Convertendo para grayscale como exemplo
    # Salve a imagem processada em um buffer de bytes
    output = io.BytesIO()
    image.save(output, format='PNG')
    output.seek(0)
    return output.read()
