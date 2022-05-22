from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, StringField
import base64, cv2, io
from PIL import Image
from identifier import get_colors
import numpy as np


class UploadImageForm(FlaskForm):
    image = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Continue without cropping')


app = Flask(__name__)
app.config["SECRET_KEY"] = '0c9e4aaa-d36c-11ec-a68b-64c753dd4d94'

@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    form = UploadImageForm()
    if form.validate_on_submit():
        # print(request.form["image_data"])
        image_file = io.BytesIO()
        form.image.data.save(image_file)
        image_file.seek(0)
        image = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        color_data = get_colors(image)

        return render_template('images.html', img_list=color_data['images'], hex_list=color_data['hex'], rgb_list=color_data["rgb"])

    return render_template("home.html", form=form)

@app.route("/process_data", methods=["POST"])
def process_data():
    if request.method == "POST":
        image = request.form['image'].split(',')[-1]
        image = base64.b64decode(image)
        image = np.frombuffer(image, dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        color_data = get_colors(image)

        return color_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)