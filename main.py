from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from flask_bootstrap import Bootstrap
from wtforms.validators import DataRequired, URL
import csv

# Sets up app and relates with Bootstrap to use a quickform
app = Flask(__name__)
app.secret_key = 'torrent_under_format_uniform'
Bootstrap(app)


# Creates Flask form class with fields
class CafeForm(FlaskForm):
    name = StringField('Name of the cafe', validators=[DataRequired()])
    google_maps_url = StringField("Location of cafe on Google maps(URL): ", validators=[DataRequired(), URL()])
    img_url = StringField("Picture of cafe on Google Maps(URL): ", validators=[DataRequired(), URL()])
    suburb = StringField("Suburb Name:", validators=[DataRequired()])
    pricey = SelectField("Price rating", choices=["$", "$$", "$$$"], validators=[DataRequired()])
    phone_number = StringField("Phone number of cafe")
    website = StringField("Website of the cafe(URL): ")
    menu = StringField("Menu of the cafe(URL): " )
    submit = SubmitField('Submit')


# Home page route. Reads the data in csv file and transfers it to html file as an array.
@app.route('/')
def home():
    with open('cafe-data2.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('index.html', cafes=list_of_rows)


# Add route. Transfers form data to html to Display the form on the page.
# When form is submitted by user, function adds entered data in csv file.
@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data2.csv", mode="a") as csv_file:
            csv_file.write(f"\n{form.name.data},"
                           f"{form.google_maps_url.data},"
                           f"{form.img_url.data},"
                           f"{form.suburb.data},"
                           f"{form.pricey.data},"
                           f"{form.phone_number.data},"
                           f"{form.website.data},"
                           f"{form.menu.data}")
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
