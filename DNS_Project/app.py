from flask import Flask, render_template, Response, flash, request, send_file
from form import DNSForm, RevForm
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
        return render_template('test.html',post={'www.google.com':'8.8.8.8'},lon=77.102,lat=28.704)
    return render_template("dnslookup.html", title="Login", form=form)

@app.route("/Revdnslookup", methods=["GET", "POST"])
def Revdnslookup():
    form = RevForm()
    if form.validate_on_submit():
        return render_template('test.html',post={'www.google.com':'8.8.8.8'},lon=77.102,lat=28.704)
    return render_template("revlookup.html", title="Login", form=form)

@app.route('/test')
def test():
    return render_template('test.html',post={'www.google.com':'8.8.8.8'},lon=77.102,lat=28.704)

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True,debug=True)
