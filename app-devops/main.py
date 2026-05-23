import os

from flask import Flask, abort, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

from bussiness_logic import allowed_file, check_password, create_folder, get_files_in_folder


app = Flask(__name__)
app.config.from_object("settings")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    create_folder(app.config["UPLOAD_FOLDER"])

    if request.method == "POST":
        for uploaded_file in request.files.values():
            if uploaded_file and allowed_file(uploaded_file.filename):
                safe_name = secure_filename(uploaded_file.filename)
                uploaded_file.save(os.path.join(app.config["UPLOAD_FOLDER"], safe_name))

        return {"files": get_files_in_folder(app.config["UPLOAD_FOLDER"])}

    return render_template("upload.html", files=get_files_in_folder(app.config["UPLOAD_FOLDER"]))


@app.route("/download/<name>", methods=["GET"])
def download(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route("/files", methods=["GET"])
def files():
    create_folder(app.config["UPLOAD_FOLDER"])
    return render_template("files.html", files=get_files_in_folder(app.config["UPLOAD_FOLDER"]))


@app.route("/to_files")
def to_files():
    return redirect(url_for("files"))


@app.route("/success/<name>")
def success(name):
    return "welcome %s" % name


@app.route("/increment/<int:a>")
def increment_int(a):
    return redirect(url_for("increment_int", a=a + 1))


@app.route("/check_even/<int:a>")
def check_even(a):
    if a % 2 == 0:
        return redirect(url_for("even", a=a))

    return redirect(url_for("odd", a=a))


@app.route("/even/<int:a>")
def even(a):
    return redirect(url_for("check_even", a=a // 2))


@app.route("/odd/<int:a>")
def odd(a):
    return "{} is odd".format(a)


@app.route("/login", methods=["POST"])
def login():
    user = request.form.get("name", "")
    password = request.form.get("password", "")

    if check_password(user, password):
        return redirect(url_for("success", name=user))

    abort(401)


if __name__ == "__main__":
    create_folder(app.config["UPLOAD_FOLDER"])
    app.run(host="0.0.0.0", port=5000, debug=False)
