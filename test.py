from flask import Flask, redirect, request, url_for, jsonify, make_response, render_template
from flask.ext.assets import Environment, Bundle
from webassets.filter import register_filter
from jinja2 import Environment as Jinja2Environment
from webassets import Environment as AssetsEnvironment
from webassets.ext.jinja2 import AssetsExtension
import requests
import urllib.parse
import os
from pprint import pprint

from jsx_assets import ReactFilter
from reverse_proxied import ReverseProxied

app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
assets = Environment()
assets.init_app(app)
register_filter(ReactFilter)
assets_env = AssetsEnvironment('./static/js', '/media')
jinja2_env = Jinja2Environment(extensions=[AssetsExtension])
jinja2_env.assets_environment = assets_env

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

config = {
    'client_id': client_id,
    'client_secret': client_secret,
    'api_base_uri': 'https://api.sipgate.com',
    'check_ssl': False,
    'access_token': None,
    'listen_host': '0.0.0.0'
}


@app.route("/")
def hello():
    
    token = request.cookies.get("access_token")
    redirect_uri = request.url_root + "callback"

    if (token):
        return redirect(url_for("show_webrtc_client"))
    else:
        location = config.get('api_base_uri') + '/v1/authorization/oauth/authorize' + '?' + urllib.parse.urlencode(
            {'client_id': config.get('client_id'), 'redirect_uri': redirect_uri, 'response_type': 'code', 'scope': 'users:read devices:read'})
        return redirect(location)


@app.route("/callback")
def callback():
    code = request.args.get('code')
    redirect_uri = request.url_root + "callback"

    if code:
        payload = {
            'client_id': config.get('client_id'),
            'client_secret': config.get('client_secret'),
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }

        r = requests.post(config.get('api_base_uri') + '/v1/authorization/oauth/token',
                          data=payload, verify=config.get('check_ssl'))

        if r.status_code == 200:
            #config['access_token'] = response.get('access_token')
            response = redirect(url_for("show_webrtc_client"))
            response.set_cookie('access_token', r.json().get('access_token'))
            return response

        return str(r.status_code)

    return "no code"

def read_device_settings(token):

    r = requests.get(config.get('api_base_uri') + '/v1/devices',
                     headers={'Authorization': 'Bearer ' + token},
                     verify=config.get('check_ssl'))


    if r.status_code == 200:
        return next(filter(lambda e: e.get("type") == "REGISTER", r.json().get('items')))
    else:
        return None


@app.route("/users")
def get_users():
    token = request.cookies.get("access_token")

    if not token:
        return "no token"

    r = requests.get(config.get('api_base_uri') + '/v1/users',
                     headers={'Authorization': 'Bearer ' + token},
                     verify=config.get('check_ssl'))

    if r.status_code == 200:
        return jsonify(r.json())
    else:
        return str(r.status_code)

@app.route("/webrtc")
def show_webrtc_client():

    token = request.cookies.get("access_token")

    if not token:
        return "no token"


    credentials = read_device_settings(token)

    username=credentials.get("credentials").get("username")
    password=credentials.get("credentials").get("password")

    return render_template("webrtc.html", username=username, password=password)



@app.route("/logout")
def delete_authcookie():
    response = make_response("logged out")
    response.set_cookie('access_token', "")
    return response



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
