import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from supabase import create_client

load_dotenv()  # lê o arquivo .env

app = Flask(__name__)

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_KEY"],
)


# ---------- Páginas do site ----------

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


# ---------- Funções que traduzem o banco para o formato do site ----------

def formatar_peso(gramas):
    # 4800 -> "4,8 kg"
    if gramas is None:
        return ""
    kg = gramas / 1000
    return f"{kg:g}".replace(".", ",") + " kg"


def formatar_idade(meses):
    # 38 -> "3 anos e 2 meses"
    if meses is None:
        return ""
    anos, resto = divmod(int(meses), 12)
    partes = []
    if anos:
        partes.append(f"{anos} ano" + ("s" if anos > 1 else ""))
    if resto:
        partes.append(f"{resto} " + ("mês" if resto == 1 else "meses"))
    return " e ".join(partes) if partes else "0 meses"


# ---------- Rota que devolve a lista de pets em JSON ----------

@app.route("/api/pets")
def api_listar_pets():
    # busca cada pet junto com os dados do tutor dele
    resposta = (
        supabase.table("cadastros_pet")
        .select("*, cadastros_tutor(*)")
        .order("id_pet")
        .execute()
    )

    pets = []
    for p in resposta.data:
        tutor = p.get("cadastros_tutor") or {}
        pets.append({
            "id": str(p["id_pet"]),
            "codigo": f"#{p['id_pet']}",
            "nome": p["nome_pet"],
            "raca": p["raca_pet"],
            "porte": p["porte_pet"],
            "cor": p["cor_pet"],
            "peso": formatar_peso(p["peso_grama"]),
            "idade": formatar_idade(p["idade_aprox_meses"]),
            "castrado": "Sim" if p["esta_castrado"] else "Não",
            "alergias": p.get("observacoes_pet") or "",
            "tutor": tutor.get("nome_tutor", ""),
            "cpf": tutor.get("cpf_tutor", ""),
            "telefone": tutor.get("telefone_tutor") or "",
            "nis": tutor.get("nis_tutor") or "",
            "sexo": p.get("sexo_pet") or "",
            "endereco": tutor.get("endereco_tutor") or "",
            "icone": p.get("icone_pet") or "🐶",
            "criadoEm": p["data_criacao"],
        })
    return jsonify(pets)


if __name__ == "__main__":
    app.run(debug=True)