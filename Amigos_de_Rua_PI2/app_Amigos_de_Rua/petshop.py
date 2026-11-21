import os
import re
from datetime import datetime, timezone
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from supabase import create_client

load_dotenv()  # lê o arquivo .env (só existe no seu computador)

app = Flask(__name__)

# A URL e a chave do Supabase vêm de variáveis de ambiente:
#   no computador -> arquivo .env  |  no Render -> aba Environment
supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_KEY"],
)


# =====================================================================
# PÁGINAS DO SITE (cada uma só entrega um arquivo HTML)
# =====================================================================

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


# =====================================================================
# FUNÇÕES AUXILIARES: traduzem entre o formato do site e o do banco
# =====================================================================

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
    # "4,8 kg" -> 4800   |   "500 g" -> 500   |   "12" -> 12000
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


def agora_iso():
    return datetime.now(timezone.utc).isoformat()


def texto_ou_none(valor):
    valor = (valor or "").strip()
    return valor or None


def dados_do_pet(d):
    """Campos do formulário -> colunas da tabela cadastros_pet."""
    return {
        "nome_pet": d["nome"].strip(),
        "raca_pet": (d.get("raca") or "").strip(),
        "porte_pet": d["porte"],
        "cor_pet": (d.get("cor") or "").strip(),
        "peso_grama": peso_para_gramas(d.get("peso")),
        "esta_castrado": d.get("castrado") == "Sim",
        "observacoes_pet": texto_ou_none(d.get("alergias")),
        "idade_aprox_meses": idade_para_meses(d.get("idade")),
        "sexo_pet": d.get("sexo") or None,
        "icone_pet": d.get("icone") or "🐶",
    }


def dados_do_tutor(d):
    """Campos do formulário -> colunas da tabela cadastros_tutor."""
    return {
        "nome_tutor": d["tutor"].strip(),
        "telefone_tutor": texto_ou_none(d.get("telefone")),
        "nis_tutor": (d.get("nis") or "").strip(),
        "endereco_tutor": texto_ou_none(d.get("endereco")),
    }


# Colunas que foram acrescentadas depois (rode o arquivo supabase_setup.sql).
# Se ainda não existirem no banco, o site continua funcionando sem elas.
COLUNAS_NOVAS = ("sexo_pet", "icone_pet", "endereco_tutor")


def gravar(operacao, dados):
    try:
        return operacao(dados)
    except Exception as erro:
        if any(coluna in str(erro) for coluna in COLUNAS_NOVAS):
            sem_novas = {k: v for k, v in dados.items() if k not in COLUNAS_NOVAS}
            return operacao(sem_novas)
        raise


def pet_para_site(p):
    """Linha do banco (com o tutor embutido) -> formato que o JavaScript espera."""
    tutor = p.get("cadastros_tutor") or {}
    return {
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
    }


def erro_json(erro, codigo=500):
    return jsonify({"erro": str(erro)}), codigo


# =====================================================================
# API: PETS
# =====================================================================

@app.route("/api/pets")
def api_listar_pets():
    try:
        resposta = (
            supabase.table("cadastros_pet")
            .select("*, cadastros_tutor(*)")  # traz o tutor junto com cada pet
            .order("id_pet")
            .execute()
        )
        return jsonify([pet_para_site(p) for p in resposta.data])
    except Exception as erro:
        return erro_json(erro)


@app.route("/api/pets", methods=["POST"])
def api_criar_pet():
    d = request.get_json(silent=True) or {}
    try:
        cpf = d["cpf"]

        # 1) Tutor: só cria se esse CPF ainda não existir
        existente = (
            supabase.table("cadastros_tutor")
            .select("cpf_tutor").eq("cpf_tutor", cpf).execute()
        )
        if not existente.data:
            dados_tutor = {**dados_do_tutor(d), "cpf_tutor": cpf, "data_criacao": agora_iso()}
            gravar(lambda x: supabase.table("cadastros_tutor").insert(x).execute(), dados_tutor)

        # 2) Pet: ligado ao tutor pelo CPF
        dados_pet = {**dados_do_pet(d), "cpf_tutor": cpf, "data_criacao": agora_iso()}
        novo = gravar(lambda x: supabase.table("cadastros_pet").insert(x).execute(), dados_pet)

        return jsonify({"id": str(novo.data[0]["id_pet"])}), 201

    except KeyError as faltando:
        return erro_json(f"Campo obrigatório ausente: {faltando}", 400)
    except Exception as erro:
        return erro_json(erro)


@app.route("/api/pets/<int:id_pet>", methods=["PUT"])
def api_editar_pet(id_pet):
    d = request.get_json(silent=True) or {}
    try:
        cpf_novo = d["cpf"]

        atual = (
            supabase.table("cadastros_pet")
            .select("cpf_tutor").eq("id_pet", id_pet).execute()
        )
        if not atual.data:
            return erro_json("Pet não encontrado", 404)
        cpf_atual = atual.data[0]["cpf_tutor"]

        if cpf_novo == cpf_atual:
            # mesmo tutor: atualiza os dados dele
            gravar(
                lambda x: supabase.table("cadastros_tutor").update(x).eq("cpf_tutor", cpf_atual).execute(),
                dados_do_tutor(d),
            )
        else:
            # CPF trocado: usa o tutor desse CPF (cria se ainda não existir)
            existente = (
                supabase.table("cadastros_tutor")
                .select("cpf_tutor").eq("cpf_tutor", cpf_novo).execute()
            )
            if not existente.data:
                dados_tutor = {**dados_do_tutor(d), "cpf_tutor": cpf_novo, "data_criacao": agora_iso()}
                gravar(lambda x: supabase.table("cadastros_tutor").insert(x).execute(), dados_tutor)

        dados_pet = {**dados_do_pet(d), "cpf_tutor": cpf_novo}
        gravar(
            lambda x: supabase.table("cadastros_pet").update(x).eq("id_pet", id_pet).execute(),
            dados_pet,
        )
        return jsonify({"id": str(id_pet)})

    except KeyError as faltando:
        return erro_json(f"Campo obrigatório ausente: {faltando}", 400)
    except Exception as erro:
        return erro_json(erro)


# =====================================================================
# API: LISTAS (serviços, profissionais e raças)
# =====================================================================

@app.route("/api/servicos")
def api_listar_servicos():
    try:
        resposta = supabase.table("servicos").select("*").order("id_servico").execute()
        return jsonify([
            {"id": s["id_servico"], "nome": s["tipo_servico"], "preco": float(s["preco_servico"])}
            for s in resposta.data
        ])
    except Exception as erro:
        return erro_json(erro)


@app.route("/api/profissionais")
def api_listar_profissionais():
    try:
        resposta = supabase.table("profissionais").select("*").order("id_profissional").execute()
        return jsonify([
            {"id": p["id_profissional"], "nome": p["nome_profissional"]}
            for p in resposta.data
        ])
    except Exception as erro:
        return erro_json(erro)


@app.route("/api/racas")
def api_listar_racas():
    try:
        resposta = supabase.table("racas_existentes").select("raca_geral").order("raca_geral").execute()
        return jsonify([r["raca_geral"] for r in resposta.data])
    except Exception as erro:
        return erro_json(erro)


# =====================================================================
# API: PROCEDIMENTOS
# =====================================================================

@app.route("/api/procedimentos")
def api_listar_procedimentos():
    try:
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
    except Exception as erro:
        return erro_json(erro)


@app.route("/api/procedimentos", methods=["POST"])
def api_criar_procedimento():
    d = request.get_json(silent=True) or {}
    try:
        servicos = d.get("servicos") or []
        if not servicos:
            return erro_json("Escolha pelo menos um serviço", 400)

        # uma linha no banco para cada serviço marcado
        linhas = [
            {
                "id_pet": int(d["idPaciente"]),
                "id_profissional": int(d["profissional"]),
                "id_servico": int(id_servico),
                "data_procedimento": d["data"],
                "estado_anterior": d["descricao"],
                "estado_posterior": (d.get("observacoes") or "").strip() or "Sem observações",
                "is_retorno": False,
            }
            for id_servico in servicos
        ]
        supabase.table("procedimentos").insert(linhas).execute()
        return jsonify({"ok": True}), 201

    except (KeyError, ValueError, TypeError) as erro:
        return erro_json(f"Dados inválidos do formulário: {erro}", 400)
    except Exception as erro:
        return erro_json(erro)


# =====================================================================
# MONITORAMENTO (para manter o site e o banco acordados)
# =====================================================================

@app.route("/saude")
def saude():
    try:
        supabase.table("servicos").select("id_servico").limit(1).execute()
        return jsonify({"status": "ok"})
    except Exception as erro:
        return jsonify({"status": "erro", "detalhe": str(erro)}), 500


if __name__ == "__main__":
    app.run(debug=True)
