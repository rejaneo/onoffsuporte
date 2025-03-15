from flask import Flask, render_template, redirect, url_for
import os
import datetime
import pytz  # Importa a biblioteca pytz

app = Flask(__name__)

# Inicializa o estado do botão e o histórico de atendimentos
button_state = {'Rejane': False, 'Joao': False}
history = []

@app.route('/')
def index():
    global button_state, history
    return render_template('index.html', button_state=button_state, history=history)

@app.route('/toggle/<user>')
def toggle(user):
    global button_state, history

    # Força o botão do outro usuário a ficar OFF quando um botão é ligado
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
    history = []  # Limpa o histórico de atendimentos
    # Reseta os botões para OFF
    button_state['Rejane'] = False
    button_state['Joao'] = False
    return redirect(url_for('index'))

def register_attendance(user):
    # Define o fuso horário de São Paulo
    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
    # Obtém a data e hora atual no fuso horário de São Paulo
    now = datetime.datetime.now(sao_paulo_tz)
    # Formata a data e hora para exibição
    formatted_time = now.strftime('%d-%m-%Y %H:%M:%S')
    # Registra o atendimento no histórico
    attendance = f"Atendimento realizado por {user} em {formatted_time}"
    history.append(attendance)

if __name__ == "__main__":
    # Pega a porta do ambiente (necessário para o Render)
    port = int(os.environ.get('PORT', 5000))
    # Inicia o servidor Flask no host 0.0.0.0 e na porta especificada
    app.run(host='0.0.0.0', port=port, debug=True)
