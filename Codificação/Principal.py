#Tentar importar biblioteca de cores. Se não funcionar, não haverá problema para o código.
try:
    from colorama import Fore, Style, init
    init(autoreset=True) # Destrava as cores e limpa o pincel sozinha
    origem = "C/ Cor"
except ImportError:
    class FakeColor:
        def __getattr__(self, name):
            return ""
    Fore = FakeColor()
    Style = FakeColor()
    origem = "S/ Cor"
#Guia de cores e formatação usadas no código
titulo = Fore.MAGENTA + Style.BRIGHT #Roxo em negrito
titulo2 = Fore.YELLOW #Amarelo
titulo3 = Fore.BLUE #Azul
texto = Style.BRIGHT  #Negrito
resetcor = Style.RESET_ALL  #Resetar estilo para o padrão
largura = 40


#Mostrar que está na tela de cadastro de cliente
print(f'{titulo}{"="*30}SISTEMA AMIGOS DE RUA{"="*30}')
print(f'{titulo2}{"Escolher ações".center(largura, "-")}\n')
'''print(f'Status do sistema: {Fore.CYAN}{origem}\n")''' #somente ative se vc quiser ver se o progarama está puxando cores ou não.




import json


Açoes = {
    "1":"Visualizar procedimentos",
    "2":"Visualizar cadastros",
    "3":"Adicionar novo procedimento",
    "4":"Adicionar novo cadastro"
}
visualizacao = {
    1:"5 ultimos",
    2:"10 ultimos",
    3:"Todos",
    4:"Buscar por chave"
}


def ver_cadastros():
    for chave,valor in dicionario.items():
        print(f'{titulo2}{chave}{resetcor}')
        if isinstance(valor, dict):
            for subchave, subvalor in valor.items():
                print(f"    {titulo3}{subchave}{resetcor}: {subvalor}")
        else:
            print(f"    {valor}")
    print(f'\n')
def pesquisa_livre():
          escolha2 = input("Digite o dado que queira pesquisar(o nome, cpf...): ")
          encontrou = False
               #vê se o input existe nos cadastros.
          for cadastro in cadastros:
              texto_cadastro = str(cadastro).lower()
              if escolha2 in texto_cadastro:
                  encontrou = True


                  print("REGISTRO ENCONTRADO\n")
                  #printa o todos os dicionarios que tem esses valores.
                  for chave, valor in cadastro.items():
                      print(f"{titulo2}{chave}{resetcor}:")
                      if isinstance(valor, dict):
                          for subchave, subvalor in valor.items():
                              print(f"    {titulo3}{subchave}{resetcor}: {subvalor}")
                      print()

          if not encontrou:
              print("Nenhum cadastro encontrado.")

for chave,valor in Açoes.items():
    print(f'{titulo3}{chave}{resetcor} : {valor}')

pergunta = ""
escolha = ""
while pergunta not in [1,2,3,4]:
    pergunta = int(input("O que voçê deseja fazer? Digite o número ao lado: "))
    if pergunta not in [1,2,3,4]:
        print("Digite um número entre 1 e 4.")
print()



if pergunta == 1:
    with open("procedimentos.json", 'r', encoding='utf-8') as arquivo:
        cadastros = json.load(arquivo)
        while escolha not in [1,2,3,4]:
            for chave,valor in visualizacao.items():
                print(f'{titulo3}{chave}{resetcor} : {valor}')
            escolha = int(input("Quantos procedimentos quer ver? "))
        if escolha == 1:
            for dicionario in cadastros[-5:]:
                ver_cadastros()
        if escolha == 2:
            for dicionario in cadastros[-10:]:
                ver_cadastros()
        if escolha == 3:
            for dicionario in cadastros:
                ver_cadastros()
        if escolha == 4:
            pesquisa_livre()


if pergunta == 2:
    with open("dados_mensais.json", 'r', encoding='utf-8') as arquivo:
        cadastros = json.load(arquivo)
        while escolha not in [1,2,3,4]:
            for chave,valor in visualizacao.items():
                print(f'{titulo3}{chave}{resetcor} : {valor}')
            escolha = int(input("Quantos cadastros quer ver? "))
        if escolha == 1:
            for dicionario in cadastros[-5:]:
                ver_cadastros()
        if escolha == 2:
            for dicionario in cadastros[-10:]:
                ver_cadastros()
        if escolha == 3:
            for dicionario in cadastros:
                ver_cadastros()
        if escolha == 4:
            pesquisa_livre()
        
if pergunta == 3:
  import Sistema_procedimento

if pergunta == 4:
  import Sistema_cadastro