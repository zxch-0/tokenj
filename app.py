from flask import Flask, request, render_template, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_bot_link', methods=['POST'])
def create_bot_link():
    bot_name = request.form['bot_name']
    bot_description = request.form['bot_description']
    redirect_uri = request.form['redirect_uri']

    # Créez un lien OAuth2 pour le bot
    oauth_url = f"https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&scope=bot&permissions=YOUR_PERMISSIONS&redirect_uri={redirect_uri}&response_type=code"

    return redirect(oauth_url)

@app.route('/oauth2/callback')
def oauth2_callback():
    code = request.args.get('code')
    redirect_uri = request.args.get('redirect_uri')

    # Échangez le code d'autorisation contre un token d'accès
    data = {
        'client_id': 'YOUR_CLIENT_ID',
        'client_secret': 'YOUR_CLIENT_SECRET',
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }
    response = requests.post('https://discord.com/api/oauth2/token', data=data)
    token_data = response.json()

    # Stockez le token dans la session
    session['access_token'] = token_data['access_token']

    return 'Token récupéré avec succès !'

if __name__ == '__main__':
    app.run(debug=True)
