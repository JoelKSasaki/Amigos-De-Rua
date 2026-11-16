from flask import Flask, render_template
from supabase import create_client

app = Flask(__name__)

#Credenciais do Supabase
supabase = create_client(
    "https://brnwhhxzekizjkxuobri.supabase.co",
    "sb_publishable_Nxf5kNQo1ts9dUhT3bakNg_Upr14QON"
)

@app.route("/")
def main():
    resposta = supabase.table("cadastros_tutor").select("*").execute()

    #armazena os registros da tabela de cadastros do tutor
    usuarios = resposta.data 
    print(usuarios)
    return render_template('users.html', users=usuarios)

@app.route("/pets")
def pets():
    return render_template('pets.html')

if __name__ == "__main__":
    app.run(debug=True)