import base64
from some_image_processing_library import remove_background

def remove_background_from_base64(base64_image: str) -> str:
    image_data = base64.b64decode(base64_image)
    processed_image_data = remove_background(image_data)
    return base64.b64encode(processed_image_data).decode('utf-8')
