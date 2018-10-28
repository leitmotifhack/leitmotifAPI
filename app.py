from flask import Flask, redirect, url_for, request
from flask_restplus import Resource, Api
from database import db_session
import pipeline
import os
from werkzeug.utils import secure_filename
from uuid import uuid4


# config
UPLOAD_FOLDER = "./upload_folder"
ALLOWED_EXTENSIONS = [".txt"]
application = Flask(__name__)
application.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
api = Api(
    application,
    version="0.1",
    title="Leitmotif API",
    description="API to serve the Leitmotif app",
)

quote_unquote_database = {}


@application.route("/uploadsnps", methods=["POST"])
def upload_file():
    """
    upload 23 and me data, convert to notes and redirect the user to a page
    that consumes those notes
    """
    file = request.files["file"]
    fp = os.path.join(
        application.config["UPLOAD_FOLDER"], secure_filename(file.filename)
    )
    file.save(fp)
    notes = pipeline.transform_23_and_me_dataset_to_notes(test_data)
    notes_id = uuid4()
    quote_unquote_database[notes_id] = notes
    return redirect("frontend/music?notes_id={}".format(notes_id))


@api.route("/notes/<notes_id>")
class notes(Resource):
    def get(self, notes_id):
        return quote_unquote_database[notes_id]


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    application.run(debug=True)
