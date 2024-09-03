from flask import Flask, render_template, redirect, url_for
import os
import datetime

app = Flask(__name__)

# Inicializa o estado do botao e o historico de atendimentos
button_state = {'Rejane': False, 'Joao': False}
history = []

@app.route('/')
def index():
    global button_state, history
    return render_template('index.html', button_state=button_state, history=history)

@app.route('/toggle/<user>')
def toggle(user):
    global button_state, history

    # Forca o botao do outro usuario a ficar OFF quando um botao e ligado
    if user == 'Rejane':
        button_state['Rejane'] = True
        button_state['Joao'] = False
        register_attendance(user)
    elif user == 'Joao':
        button_state['Joao'] = True
        button_state['Rejane'] = False
        register_attendance(user)

    return redirect(url_for('index'))

@app.route('/clear_history')
def clear_history():
    global button_state, history
    history = []  # Limpa o historico de atendimentos
    # Reseta os botoes para OFF
    button_state['Rejane'] = False
    button_state['Joao'] = False
    return redirect(url_for('index'))

def register_attendance(user):
    # Registra o atendimento no historico
    attendance = f"Atendimento realizado por {user} em {datetime.datetime.now()}"
    history.append(attendance)

if __name__ == "__main__":
    # Pega a porta do ambiente (necessario para o Render)
    port = int(os.environ.get('PORT', 5000))
    # Inicia o servidor Flask no host 0.0.0.0 e na porta especificada
    app.run(host='0.0.0.0', port=port, debug=True)
