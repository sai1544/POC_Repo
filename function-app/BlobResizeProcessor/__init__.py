import logging
import azure.functions as func
from PIL import Image
import io


def main(myblob: func.InputStream) -> None:
    logging.info(f"Blob trigger function processed blob Name: {myblob.name}, Size: {myblob.length} bytes")
    # Placeholder: real resize code would open the image, resize and write to output binding or storage
    try:
        content = myblob.read()
        image = Image.open(io.BytesIO(content))
        logging.info(f"Image size: {image.size}, format: {image.format}")
    except Exception as e:
        logging.exception(f"Failed to process image: {e}")
