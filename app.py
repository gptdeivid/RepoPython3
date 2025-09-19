from flask import Flask, render_template, request, redirect, url_for, session, flash
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'

# Usuarios simples en memoria (sin base de datos)
USERS = {
    'admin@test.com': {
        'password': 'admin123',
        'name': 'Administrador'
    },
    'user@test.com': {
        'password': 'user123',
        'name': 'Usuario'
    },
    'demo@demo.com': {
        'password': 'demo',
        'name': 'Demo User'
    }
}

# Cache busting
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    email = request.form['email']
    password = request.form['password']

    # Validar credenciales con datos en memoria
    if email in USERS and USERS[email]['password'] == password:
        session['username'] = USERS[email]['name']
        session['email'] = email
        flash(f"¡Bienvenido {USERS[email]['name']}!")
        return redirect(url_for('welcome'))
    else:
        flash("Credenciales incorrectas. Prueba con: admin@test.com/admin123 o user@test.com/user123")
        return redirect(url_for('login'))

@app.route('/welcome')
def welcome():
    if 'username' in session:
        return render_template('welcome.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    username = session.get('username', 'Usuario')
    session.clear()
    flash(f"¡Hasta luego {username}!")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


