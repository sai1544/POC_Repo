import logging
import io
from PIL import Image

def main(inputBlob: bytes, outputBlob: io.TextIOWrapper):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Size: {len(inputBlob)} bytes")

    try:
        # Open the input image from bytes
        image = Image.open(io.BytesIO(inputBlob))
        
        # Define thumbnail size
        thumbnail_size = (128, 128)
        
        # Create thumbnail
        image.thumbnail(thumbnail_size)
        
        # Save the thumbnail to the output blob
        # We need to save it to a byte buffer first
        output_buffer = io.BytesIO()
        image.save(output_buffer, format=image.format)
        
        # Write the buffer's content to the output blob
        outputBlob.write(output_buffer.getvalue())
        
        logging.info(f"Thumbnail created and saved to output blob.")
        
    except Exception as e:
        logging.error(f"Error processing image: {str(e)}")
