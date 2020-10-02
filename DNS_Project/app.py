from flask import Flask, render_template, Response, flash, request, send_file
from form import DNSForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '21a00ee024ebe902cf1848208f5c1a29'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1


@app.route('/')
def index():
    return render_template('home.html')


@app.route("/dnslookup", methods=["GET", "POST"])
def dnslookup():
    form = DNSForm()
    if form.validate_on_submit():
        return "dns return statements"
    return render_template("dnslookup.html", title="Login", form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)
