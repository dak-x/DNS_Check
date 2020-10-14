from flask import Flask, render_template,flash
from flaskwebgui import FlaskUI
from form import DNSForm, RevForm
from dns_rq import get_records, get_reversename, get_recordsRecursive
import flask_excel as xl
import copy
import urllib3
import json
import pyexcel_io.writers
import pyexcel_io.writers.csv_in_memory

app = Flask(__name__)
app.config['SECRET_KEY'] = '21a00ee024ebe902cf1848208f5c1a29'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
_records = []


@app.route('/')
def index():
    return render_template('home.html')


@app.route("/dnslookup", methods=["GET", "POST"])
def dnslookup():
    global _records
    form = DNSForm()
    if form.validate_on_submit():
        domain_name = form.domain_name.data
        type = form.type.data
        dns_server = form.default_dns.data
        rd = form.recursion_desired.data
        if(rd == False):
            temp = (get_recordsRecursive(domain_name, type, dns_server))

        else:
            temp = get_records(domain_name, type, dns_server)

        # *This section creates a global records var which can be used for download
        _records = [["Domain Name", domain_name], [
            "Request Type", type], ["Request To", dns_server]]

        for row in temp:
            _records.append([])
            for r in temp[row]:
                _records.append(r)
        # *====================================* #

        flag = False
        lon = 77.102
        lat = 28.704
        if(type == "A" or type == "ANY"):
            try:
                x = temp["A"]
                if(len(x) > 1):
                    ip_addr = x[1][2]
                    http = urllib3.PoolManager()
                    r = http.request(
                        'GET', "http://ip-api.com/json/" + ip_addr)
                    response = json.loads(r.data.decode('utf-8'))
                    lat, lon = response['lat'], response['lon']
                flag = True
            except:
                if(rd == False):
                    flash('The root does not have the record !! Choose another server or allow recursion ', 'danger')
                    return render_template("dnslookup.html", title="Login", form=form)
                else:
                    flash('The server does-not allow recursion','danger')
                    return render_template("dnslookup.html", title="Login", form=form)
        return render_template('test.html', post=temp, lon=lon, lat=lat, flag=flag)
    return render_template("dnslookup.html", title="Login", form=form)


@app.route("/Revdnslookup", methods=["GET", "POST"])
def Revdnslookup():
    form = RevForm()
    if form.validate_on_submit():
        domain_ip = form.domain_name.data
        temp = get_reversename(domain_ip)
        if(temp != -1):
            flash('The name of the dns server with ip ' +
                  domain_ip + ' is '+temp, "success")
        else:
            flash('No DNS found with ip '+domain_ip, 'danger')
    return render_template("revlookup.html", title="Login", form=form)


@app.route('/test')
def test():
    return render_template('test.html', post={'www.google.com': '8.8.8.8'}, lon=77.102, lat=28.704)


@app.route('/download')
def get_csv():
    global _records
    xl.init_excel(app)
    return xl.make_response_from_array(_records, file_type="csv", file_name="records")


if __name__ == '__main__':
    ui = FlaskUI(app,fullscreen=True,maximized=True,browser_path = "/snap/bin/firefox")
    ui.run()
    #app.run(host='0.0.0.0', threaded=True, debug=True)

