from flask import Flask, render_template, request, jsonify
from datetime import datetime
from nltk.chat.util import Chat, reflections
from sympy import sympify, simplify
import locale

app = Flask(__name__, template_folder='C:/Users/ismae/Desktop/chat2.0/templates')
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

pares = [
    ("oi", ["Oi!", "Olá!", "Como posso ajudar?"]),
    ("qual é o seu nome?", ["Eu sou um chatbot.", "Você pode me chamar de Bot."]),
    ("como você está?", ["Estou bem, obrigado por perguntar!",
                         "Eu sou um programa, não tenho sentimentos, mas estou aqui para ajudar."]),
("tudo bem?", ["Estou bem, obrigado por perguntar!",
                         "Eu sou um programa, não tenho sentimentos, mas estou aqui para ajudar."]),
    ("qual é o significado da vida?", ["A resposta para a pergunta fundamental sobre a vida, o universo e tudo mais é 42 (segundo Douglas Adams)."]),
    ("o que você acha do Nicolas?", ["ele é um rapaz muito inteligente!", "Ele peida muito fedorento!", "Caga igual um iceberg! KKKK"]),
    ("o que você acha do Ismael?",["Ele é muito lindo!", "Ele é muito inteligente!"]),
    ("quem te inventou?", ["Foi um programador muito inteligente, chamado Ismael Figueiredo de Oliveira"]),
("quem te criou?", ["Foi um programador muito inteligente, chamado Ismael Figueiredo de Oliveira"]),

]

chatbot = Chat(pares, reflections)

def math_response(question):
    try:
        return f"A resposta para '{question}' é {simplify(sympify(question))}."
    except:
        return "Desculpe, não consigo resolver essa expressão matemática."

def date_response():
    current_date = datetime.now().strftime("%d-%m-%y")
    current_day = datetime.now().strftime("%A").capitalize()
    return f"Hoje é {current_date} e é um(a) {current_day}."

def get_response(user_input):
    if "calcule" in user_input:
        response = math_response(user_input.replace("calcule", "").strip())
    elif any(keyword in user_input for keyword in ["data", "dia da semana"]):
        response = date_response()
    else:
        response = chatbot.respond(user_input)

    # Se a resposta for nula, use uma mensagem padrão
    return response or "Desculpe, eu não entendi. Pode reformular sua pergunta?"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response_route():
    user_input = request.form.get("user_input")
    return jsonify({"response": get_response(user_input)})

if __name__ == "__main__":
    app.run(debug=True)
