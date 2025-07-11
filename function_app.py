import logging
import azure.functions as func
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = "/tmp/uploads"  # Use Azure storage or a temp folder

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="upload", methods=["POST"])
def upload_handler(req: func.HttpRequest) -> func.HttpResponse:
    try:
        name = req.form.get('name')
        email = req.form.get('email')
        phone = req.form.get('phone')
        price = req.form.get('price')
        photo = req.files.get('photo')

        if not all([name, email, phone, price, photo]):
            return func.HttpResponse("Missing fields", status_code=400)

        # Save photo securely
        filename = secure_filename(photo.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(photo.read())

        logging.info(f"Bike uploaded by {name} ({email}, {phone}) for £{price}")
        return func.HttpResponse(f"Thanks {name}, your beast has been sent to the workshop!", status_code=200)

    except Exception as e:
        logging.error(f"Upload failed: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)