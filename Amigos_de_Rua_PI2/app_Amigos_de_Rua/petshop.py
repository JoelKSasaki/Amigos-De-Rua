import os
import re
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
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


# ---------- Funções que traduzem entre o site e o banco ----------

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


def peso_para_gramas(texto):
    # "4,8 kg" -> 4800   |   "500 g" -> 500
    texto = (texto or "").lower().replace(",", ".")
    numero = re.search(r"\d+(\.\d+)?", texto)
    if not numero:
        return 0
    valor = float(numero.group())
    if "kg" in texto or "g" not in texto:
        valor *= 1000
    return int(round(valor))


def idade_para_meses(texto):
    # "3 anos e 2 meses" -> 38
    texto = (texto or "").lower()
    anos = re.search(r"(\d+)\s*an", texto)
    meses = re.search(r"(\d+)\s*m", texto)
    total = 0
    if anos:
        total += int(anos.group(1)) * 12
    if meses:
        total += int(meses.group(1))
    return total


# ---------- API: pets ----------

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


@app.route("/api/pets", methods=["POST"])
def api_criar_pet():
    d = request.get_json()
    agora = datetime.now(timezone.utc).isoformat()

    try:
        # 1) Tutor: só cria se esse CPF ainda não existir
        existente = (
            supabase.table("cadastros_tutor")
            .select("cpf_tutor")
            .eq("cpf_tutor", d["cpf"])
            .execute()
        )
        if not existente.data:
            supabase.table("cadastros_tutor").insert({
                "cpf_tutor": d["cpf"],
                "nome_tutor": d["tutor"],
                "telefone_tutor": d.get("telefone") or None,
                "nis_tutor": d["nis"],
                "data_criacao": agora,
            }).execute()

        # 2) Pet: ligado ao tutor pelo CPF
        novo = supabase.table("cadastros_pet").insert({
            "nome_pet": d["nome"],
            "raca_pet": d.get("raca") or "",
            "porte_pet": d["porte"],
            "cor_pet": d.get("cor") or "",
            "peso_grama": peso_para_gramas(d.get("peso")),
            "esta_castrado": d.get("castrado") == "Sim",
            "observacoes_pet": d.get("alergias") or None,
            "idade_aprox_meses": idade_para_meses(d.get("idade")),
            "cpf_tutor": d["cpf"],
            "data_criacao": agora,
        }).execute()

        return jsonify({"id": str(novo.data[0]["id_pet"])}), 201

    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500


# ---------- API: listas de serviços e profissionais ----------

@app.route("/api/servicos")
def api_listar_servicos():
    resposta = supabase.table("servicos").select("*").order("id_servico").execute()
    return jsonify([
        {"id": s["id_servico"], "nome": s["tipo_servico"], "preco": float(s["preco_servico"])}
        for s in resposta.data
    ])


@app.route("/api/profissionais")
def api_listar_profissionais():
    resposta = supabase.table("profissionais").select("*").order("id_profissional").execute()
    return jsonify([
        {"id": p["id_profissional"], "nome": p["nome_profissional"]}
        for p in resposta.data
    ])


# ---------- API: procedimentos ----------

@app.route("/api/procedimentos")
def api_listar_procedimentos():
    resposta = (
        supabase.table("procedimentos")
        .select("*, servicos(tipo_servico), profissionais(nome_profissional)")
        .order("data_procedimento", desc=True)
        .execute()
    )

    # Um atendimento com vários serviços vira várias linhas no banco.
    # Aqui juntamos de volta num só (mesmo pet, data, profissional e textos).
    grupos = {}
    for linha in resposta.data:
        chave = (
            linha["id_pet"], linha["data_procedimento"], linha["id_profissional"],
            linha["estado_anterior"], linha["estado_posterior"],
        )
        if chave not in grupos:
            grupos[chave] = {
                "id": f"proc-{linha['id_procedimento']}",
                "idPaciente": str(linha["id_pet"]),
                "data": linha["data_procedimento"],
                "tipos": [],
                "profissional": (linha.get("profissionais") or {}).get("nome_profissional", ""),
                "descricao": linha["estado_anterior"],
                "observacoes": linha["estado_posterior"],
                "fotoAntes": "",
                "fotoDepois": "",
            }
        nome_servico = (linha.get("servicos") or {}).get("tipo_servico")
        if nome_servico:
            grupos[chave]["tipos"].append(nome_servico)

    return jsonify(list(grupos.values()))


@app.route("/api/procedimentos", methods=["POST"])
def api_criar_procedimento():
    d = request.get_json()
    try:
        # uma linha no banco para cada serviço marcado
        linhas = [
            {
                "id_pet": int(d["idPaciente"]),
                "id_profissional": int(d["profissional"]),
                "id_servico": int(id_servico),
                "data_procedimento": d["data"],
                "estado_anterior": d["descricao"],
                "estado_posterior": d.get("observacoes") or "Sem observações",
                "is_retorno": False,
            }
            for id_servico in d.get("servicos", [])
        ]
        if not linhas:
            return jsonify({"erro": "Escolha pelo menos um serviço"}), 400

        supabase.table("procedimentos").insert(linhas).execute()
        return jsonify({"ok": True}), 201

    except Exception as erro:
        return jsonify({"erro": str(erro)}), 500


if __name__ == "__main__":
    app.run(debug=True)