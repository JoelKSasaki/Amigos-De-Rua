from flask import Flask, render_template
from supabase import create_client

app = Flask(__name__)

#Credenciais do Supabase
supabase = create_client(
    "https://brnwhhxzekizjkxuobri.supabase.co",
    "sb_publishable_Nxf5kNQo1ts9dUhT3bakNg_Upr14QON"
)

'''@app.route("/")
def main():
    resposta = supabase.table("cadastros_tutor").select("*").execute()

    #armazena os registros da tabela de cadastros do tutor
    usuarios = resposta.data 
    print(usuarios)
    return render_template('users.html', users=usuarios)'''

@app.route("/")
def welcome():
    return render_template('bemvindo.html')

@app.route("/inicio")
def pag_inicial():
    return render_template('inicio.html')

@app.route("/cadastrar-pet")
def novos_pets():
    return render_template('cadastro.html')

@app.route("/novo-procedimento")
def novos_procedimentos():
    return render_template('procedimento.html')

@app.route("/ficha-pet")
def ficha_pet():
    return render_template('ficha.html')

@app.route("/pets-cadastrados")
def pets_cadastrados():
    return render_template('todos-cadastros.html')

@app.route("/todos-procedimentos")
def procedimentos_totais():
    return render_template('todos-procedimentos.html')

if __name__ == "__main__":
    app.run(debug=True)