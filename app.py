from flask import Flask, flash, request, redirect, url_for
from flask_restplus import Resource, Api
from database import db_session
import pipeline
import os
from glob import glob
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = "./upload_folder"
ALLOWED_EXTENSIONS = [".txt"]


application = Flask(__name__)
application.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@application.route("/upload", methods=["POST"])
def upload_file():
    """
    Here is the relevant html
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """
    # check if the post request has the file part
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return redirect(url_for("uploaded_file", filename=filename))


@application.route("/test")
def upload_file_html():
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


api = Api(
    application,
    version="0.1",
    title="Our sample API",
    description="This is our sample API",
)


@api.route("/testnotes")
class test_transform_23_and_me_dataset_to_notes(Resource):
    def get(self):
        with open("./test_data/test_data.txt") as f:
            test_data = f.read()
        notes = pipeline.transform_23_and_me_dataset_to_notes(test_data)
        return {"notes": notes}


@api.route("/notes")
class notes(Resource):
    def get(self):
        glob()


if __name__ == "__main__":
    application.run(debug=True)
