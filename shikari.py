import os
import rclone
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return """
        <html>
        <head>
            <title>OneDrive File Downloader</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <h1>OneDrive File Downloader</h1>
            <form action="/download" method="post">
                <input type="text" name="file_name" placeholder="File name">
                <input type="submit" value="Download">
            </form>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Upload">
            </form>
            <form action="/add_rclone_conf" method="post">
                <input type="text" name="rclone_conf" placeholder="Rclone config file">
                <input type="submit" value="Add Rclone config">
            </form>
        </body>
        </html>
    """

@app.route("/download")
def download():
    file_name = request.form["file_name"]
    rclone_client = rclone.Rclone()
    rclone_client.config = os.getenv("RCLONE_CONFIG")
    file_path = rclone_client.get("onedrive:/", file_name)
    with open(file_path, "rb") as f:
        data = f.read()
    response = requests.Response()
    response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name)
    response.content = data
    return response

@app.route("/upload")
def upload():
    file = request.files["file"]
    file_name = file.filename
    rclone_client = rclone.Rclone()
    rclone_client.config = os.getenv("RCLONE_CONFIG")
    rclone_client.upload(file, "onedrive:/{}".format(file_name))
    return "File uploaded successfully!"

@app.route("/add_rclone_conf")
def add_rclone_conf():
    rclone_conf = request.form["rclone_conf"]
    with open("rclone.conf", "w") as f:
        f.write(rclone_conf)
    return "Rclone config added successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
