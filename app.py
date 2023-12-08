from flask import Flask, redirect, url_for, session, request, jsonify, render_template
from authlib.integrations.flask_client import OAuth
import config

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
oauth = OAuth(app)

oauth.register(
    name='suap',
    client_id= config.client_id,
    client_secret=config.client_secret,
    api_base_url='https://suap.ifrn.edu.br/api/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://suap.ifrn.edu.br/o/token/',
    authorize_url='https://suap.ifrn.edu.br/o/authorize/',
    fetch_token=lambda: session.get('suap_token')
)


@app.route('/')
def index():
    if 'suap_token' in session:
        meus_dados = oauth.suap.get('v2/minhas-informacoes/meus-dados')
        return render_template('user.html', user_data=meus_dados.json())
    else:
        return render_template('home.html')

# @app.route('/boletim/',methods = ['get', 'post'])
# def boletim():
#     if request.method == 'POST':
#         ano = request.form['ano']
#     boletim = oauth.suap.get(f'v2/minhas-informacoes/boletim/{ano}/1')
#     return render_template('boletim.html', boletim=boletim.json())

@app.route('/boletim', methods = ['get', 'post'], defaults={'ano': '2023'})
@app.route('/boletim/<ano>', methods = ['get', 'post'])
def boletim(ano):
    if request.method == 'POST':
        ano = request.form['ano']
    print(ano)
    boletim_data = oauth.suap.get(f'v2/minhas-informacoes/boletim/{ano}/1/').json()
    return render_template('boletim.html', boletim=boletim_data)

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    print(redirect_uri)
    return oauth.suap.authorize_redirect(redirect_uri)


@app.route('/logout')
def logout():
    session.pop('suap_token', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def auth():
    token = oauth.suap.authorize_access_token()
    session['suap_token'] = token
    return redirect(url_for('index'))