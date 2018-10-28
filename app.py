from flask import Flask, request, render_template, redirect
import pipeline
import os
from os import path
from werkzeug.utils import secure_filename


# config
application = Flask(__name__)
application.config["UPLOAD_FOLDER"] = "."

@application.route("/")
def index():
    return render_template("index.html")


@application.route("/upload", methods=["GET", "POST"])
def upload_file():
    """
    upload 23 and me data, convert to notes and redirect the user to a page
    that consumes those notes
    """
    if request.method == "POST":
        file = request.files["file"]
        fp = path.join(
            application.config["UPLOAD_FOLDER"], secure_filename(file.filename)
        )
        file.save(fp)
        res = pipeline.transform_23_and_me_dataset_to_notes(fp)
        notes, depression, caffeine, schizophrenia = res
        os.remove(fp)
        return render_template(
            "music.html",
            notes=str(notes),
            caffeine=caffeine,
            schizophrenia=schizophrenia,
        )
    elif request.method == "GET":
        return render_template("upload.html")


@application.route("/resources/soundfonts/choir_aahs-mp3.js")
def root():
    return redirect(
        "https://raw.githubusercontent.com/gleitz/midi-js-soundfonts/gh-pages/FluidR3_GM/choir_aahs-mp3.js"
    )


if __name__ == "__main__":
    application.run(debug=True)
