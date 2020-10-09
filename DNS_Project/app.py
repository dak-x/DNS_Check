from flask import Flask, render_template, Response, flash, request, send_file
from form import DNSForm, RevForm
from dns_rq import get_records, get_reversename

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
        domain_name = form.domain_name.data
        type = form.type.data
        dns_server = form.default_dns.data
        temp = (get_records(domain_name,type,dns_server))
        flag = False
        if(type == "A" or type == "ANY"):
            flag = True
        return render_template('test.html', post=temp, lon=77.102, lat=28.704, flag=flag)
    return render_template("dnslookup.html", title="Login", form=form)


@app.route("/Revdnslookup", methods=["GET", "POST"])
def Revdnslookup():
    form = RevForm()
    if form.validate_on_submit():
        domain_ip = form.domain_name.data
        temp = get_reversename(domain_ip)
        if(temp!=-1):
            flash('The name of the dns server with ip ' + domain_ip + ' is '+temp,"success")
        else:
            flash('No DNS found with ip '+domain_ip, 'danger')
    return render_template("revlookup.html", title="Login", form=form)


@app.route('/test')
def test():
    return render_template('test.html', post={'www.google.com': '8.8.8.8'}, lon=77.102, lat=28.704)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=True)

