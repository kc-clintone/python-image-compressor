from PIL import Image
from flask import Flask, request, redirect, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_and_compress():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'image' not in request.files:
            return redirect(request.url)
        image = request.files['image']
        if image.filename == '':
            return redirect(request.url)
        if image:
            # Save the uploaded image to a temporary file
            image_path = 'temp_image.jpg'
            image.save(image_path)

            # Compress the image
            compressed_image_path = 'compressed_image.jpg'
            compress_image(image_path, compressed_image_path, quality=50)

            # Render the template with the compressed image path
            return render_template('result.html', image_path=compressed_image_path)

    return render_template('upload.html')


def compress_image(input_path, output_path, quality):
    """
    Compresses an image using Pillow library.
    :param input_path: Path to the input image file.
    :param output_path: Path to save the compressed image.
    :param quality: Compression quality (0-100).
    """
    try:
        # Open the image file
        with Image.open(input_path) as image:
            # Save the compressed image with the specified quality
            image.save(output_path, optimize=True, quality=quality)
    except IOError:
        print(f"Cannot open or save file: {input_path}")


if __name__ == '__main__':
    app.run()
