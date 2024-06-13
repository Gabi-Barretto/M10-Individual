from PIL import Image
import io
import logging
import base64
from fastapi import UploadFile, HTTPException, APIRouter, File
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)

async def remove_background(file: UploadFile):
    try:
        # Leia o arquivo como bytes
        contents = await file.read()
        logging.info("File read successfully.")
        
        # Abra a imagem usando PIL
        image = Image.open(io.BytesIO(contents))
        logging.info("Image opened successfully.")
        
        # Processamento de imagem (exemplo simples)
        image = image.convert("L")  # Convertendo para grayscale como exemplo
        logging.info("Image converted to grayscale.")
        
        # Salve a imagem processada em um buffer de bytes
        output = io.BytesIO()
        image.save(output, format='PNG')
        output.seek(0)
        logging.info("Image saved to output buffer.")
        
        return output.read()
    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error during image processing: {str(e)}")
