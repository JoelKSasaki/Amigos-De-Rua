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
print(f'{titulo}{"="*30}CADASTRO DE CLIENTE{"="*30}')
print()
print(f'{titulo2}{"Dados do Tutor".center(largura, "-")}\n')
'''print(f'Status do sistema: {Fore.CYAN}{origem}\n")''' #somente ative se vc quiser ver se o progarama está puxando cores ou não.


#A codificação para o nome, o id_pet e os dados do responsável


from datetime import date
from random import randint
import json


dados_dono = {
"Nome dono": "",
"NIS": "",
"CPF": "",
"Numero telefone": ""}


#pergunta o nome do dono.
def perg_nome_dono():
 nome_dono = str(input('Qual é o nome do dono do pet? ').title())
 nome_dono = nome_dono.title()
 dados_dono["Nome dono"] = nome_dono
 print(f'{nome_dono}\n')
perg_nome_dono()


def perg_nis():
 nis = ""
 while len(nis) < 11:
    try:
        nis = str(input('Informe o NIS: ').replace(" ",""))
        while len(nis) != 11:
            print('Valor inválido. O NIS possui 11 dígitos, digite novamente.')
            nis = str(int(input('Informe o NIS: ').replace(" ","")))
    except ValueError:
        print("Digite um número valido.")
 dados_dono["NIS"] = f"{nis[:3]}.{nis[3:8]}.{nis[8:10]}-{nis[10:]}"
 print (dados_dono["NIS"])
perg_nis()


def perg_cpf():
  #VALIDAR CPF
  cpf = ""
  multiplicador = 10
  multiplicador2 = 11
  soma = 0
  soma2 = 0
  dig_verificador1 = 10
  dig_verificador2 = 10
  resto = 0
  resto2 = 0


  while len(cpf) < 11:
      cpf = list(map(int, ''.join(c for c in input("Informe seu CPF: ") if c.isdigit())))
      cpf2 = cpf.copy()
      cpf3 = cpf.copy()
      while len(cpf) != 11:
          print("Valor inválido. O CPF possui 11 dígitos, digite novamente. ")
          cpf = list(map(int, ''.join(c for c in input("Informe seu CPF: ") if c.isdigit())))
          cpf2 = cpf.copy()
          cpf3 = cpf.copy()
  while cpf[9] != dig_verificador1 or cpf[10] != dig_verificador2:
      try:
          multiplicador = 10
          multiplicador2 = 11
          soma = 0
          soma2 = 0
          for i in range(0, 9):
              cpf3[i] = cpf[i] * multiplicador
              soma += cpf3[i]
              multiplicador -= 1
          resto = (soma*10) % 11
          if resto == 10:
              dig_verificador1 = 0
          else:
              dig_verificador1 = resto
          for j in range(0, 10):
              cpf2[j] = cpf[j] * multiplicador2
              soma2 += cpf2[j]
              multiplicador2 -= 1
          resto2 = (soma2*10) % 11
          if resto2 == 10:
              dig_verificador2 = 0
          else:
              dig_verificador2 = resto2
          if cpf[9] != dig_verificador1 or cpf[10] != dig_verificador2:
              print(cpf)
              print("CPF inválido. Digite um CPF válido")
              cpf = list(map(int, ''.join(c for c in input("Informe seu CPF: ") if c.isdigit())))
              while len(cpf) != 11:
                  print("Valor inválido. O CPF possui 11 dígitos, digite novamente. ")
                  cpf = list(map(int, ''.join(c for c in input("Informe seu CPF: ") if c.isdigit())))
              cpf2 = cpf.copy()
              cpf3 = cpf.copy()
          resto = 0
          resto2 = 0
      except ValueError:
          print("Número invalido.")


  if cpf[9] == dig_verificador1 and cpf[10] == dig_verificador2:
      cpf = ''.join(map(str, cpf))
      cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
      dados_dono["CPF"] = cpf
      print (f'{dados_dono["CPF"]}\n')
perg_cpf()


#Para a validação do telefone, é necessário o DDD e 9 digitos.
numero_tel = "00000000000"
tel_pergunta = (input(f"O cliente tem nº de telefone?{texto} (S/N){resetcor} ").strip().capitalize())


dado_para_alterar = ""
#pergunta e valida o telefone inserido
def perg_tel():
  if tel_pergunta == "S" or  dado_para_alterar in ["telefone", "4"]:
      numero_tel = input('Qual o seu número de telefone?')
      numero_tel = numero_tel.replace(" ", "")
      while len(numero_tel) != 11 and numero_tel != "sair" :
          print("Telefone inválido. Precisa de um DDD e de 11 caracteres")
          numero_tel = input("Digite o telefone corretamente(ou digite 'sair'): ")
          numero_tel = numero_tel.replace(" ", "")
      if numero_tel != "sair":
          numero_tel = f"({numero_tel[:2]}) {numero_tel[2:7]}-{numero_tel[7:]}"
          print(numero_tel)
      else:
          numero_tel = "Não fornecido"
  else:
      numero_tel = "Não fornecido"
  dados_dono["Numero telefone"] = numero_tel
perg_tel()




#A codificação para a adição de informações do cachorro
nome = ""
raca = ""
porte = ""
cor = ""
peso = ""
genero = ""
castrado = ""
select = 0
perg_obser = ""
cont = 1


caracteristicas_pet = {
"ID pet": "",
"Nome pet": "",
"Raca": "",
"Porte": "",
"Cor": "",
"Genero": "",
"Idade": "",
"Peso": "",
"Castrado": "",
"Observacoes": ""
}


Portes = {
1 : "Micro",
2 : "Pequeno",
3 : "Médio",
4 : "Grande",
5 : "Gigante"
}


dado_para_alterar = 0
alterar_dados = (input(f"\nVocê quer alterar os dados do tutor? [S/N] ").strip().capitalize())
while alterar_dados  == "S":
  for i, (chave,valor) in enumerate(dados_dono.items()) :
      print(f'{titulo3}{i:<2} {resetcor}{chave:<16}:   {texto}{valor}')
  dado_para_alterar = (input("O que gostaria de atualizar? Digite o tipo de dado ou o número ao lado.").strip().capitalize())
  if dado_para_alterar in ["Nome", "1"]:
      perg_nome_dono()
  if dado_para_alterar in ["Nis", "2"]:
      perg_nis()
  if dado_para_alterar in ["Cpf", "3"]:
      perg_cpf()
  if dado_para_alterar in ["Telefone", "4"]:
      perg_tel()
  alterar_dados = (input(f"\nVocê quer alterar os dados do tutor? [S/N] ").strip().capitalize())
#Mostrar as características digitadas numa lista
iterador =  iter(caracteristicas_pet.items())
next(iterador)
for i, (chave,valor) in enumerate(iterador, 2) :
  print(f'{titulo3}{i:<2} {resetcor}{chave:<12}:   {texto}{valor}')




#cria um id baseado na data atual e 4 numeros aleatórios
def criar_id():
  data = date.today()
  data_id_pet = data.strftime('%d%m%y')
  id_pet_velho = randint(0, 9999)
  id_pet = f"{data_id_pet}{id_pet_velho:04}"
  caracteristicas_pet["ID pet"] = id_pet
criar_id()


print(f'\n{titulo2}{"Dados do Pet".center (largura, "-")}\n')


#adiciona as informações iniciais do pet para o cadastro
while cont != 0 and cont <= 8:
  if cont == 1:
      def perg_nome_pet():
          nome = input("Digite o nome do cachorro: ")
          print(f'{nome}\n')
          caracteristicas_pet["Nome pet"] = nome
      perg_nome_pet()
  elif cont == 2:
      def perg_raca():
          raca = input("Digite a raça do cachorro: ")
          print(f'{raca}\n')
          caracteristicas_pet["Raca"] = raca
      perg_raca()
  elif cont == 3:
      def perg_idade():
          Verdade = False
          while Verdade == False:
              try:
                  idade_anos = int(input("Digite a idade do cachorro em ANOS: "))
                  print(f'{idade_anos} Anos\n')
                  idade_meses = int(input("Digite a idade do cachorro em MESES: "))
                  print(f'{idade_meses} Meses\n')
                  caracteristicas_pet["Idade"] = f"{idade_anos} Anos e {idade_meses} Meses"
                  if idade_anos > 0 or idade_meses > 0:
                      Verdade = True
                  else:
                      print("Digite um número positivo.")
              except ValueError:
                  print("Digite um número valido.")
      perg_idade()
  elif cont == 4:
      Portes = {
       1 : "Micro",
       2 : "Pequeno",
       3 : "Médio",
       4 : "Grande",
       5 : "Gigante"
       }
      def perg_porte():
          for chave,valor in Portes.items():
              print(f'{chave} : {valor}')
          perg_porte = 0
          while perg_porte == 0 or perg_porte == None :
              try:
                  perg_porte = int(input("Escolha o número do porte do cachorro."))
                  perg_porte = Portes.get(perg_porte)
                  if perg_porte == None:
                      print("Esse número não esta na lista.")
                  else:
                      caracteristicas_pet["Porte"] = perg_porte
                      print (f'{perg_porte}\n')
              except ValueError:
                  print("Digite um número valido.")
      perg_porte()
  elif cont == 5:
      def perg_cor():
          cor = input("Digite a cor do cachorro: ")
          print(f'{cor}\n')
          caracteristicas_pet["Cor"] = cor
      perg_cor()
  elif cont == 6:
      def perg_peso():
          Verdade = False
          while Verdade == False:
              try:
                  peso = int(input("Digite o peso do cachorro (em gramas)"))
                  if peso >= 0:
                      peso /= 1000
                      peso =f"{peso}Kg"
                      caracteristicas_pet["Peso"] = peso
                      print(f'{caracteristicas_pet["Peso"]}\n')
                      Verdade = True
                  else:
                      print("Digite um número positivo.")
              except ValueError:
                  print("Digite um número valido.")
      perg_peso()
  elif cont == 7:
      def perg_genero():
          select_update = 0
          while select_update not in [1, 2]:
              try:
                  select_update = int(input("Selecione o gênero. Macho(1) e Fêmea(2): "))
              except ValueError:
                  print("Digite um número. ")
              if select_update == 1:
                  caracteristicas_pet["Genero"] = "Macho"
                  print(f'{caracteristicas_pet["Genero"]}\n')
              elif select_update == 2:
                  caracteristicas_pet["Genero"] = "Fêmea"
                  print(f'{caracteristicas_pet["Genero"]}\n')
              else:
                  print("Número errado, escreva 1 ou 2.")
      perg_genero()
  elif cont == 8:
      def perg_castrado():
          castrado = ""
          while str(castrado).capitalize().strip() not in ["S", "N"]:
              castrado = input("O pet é castrado? (S/N)").capitalize()
              if str(castrado).capitalize() == "S":
                  caracteristicas_pet["Castrado"] = "Sim"
              elif str(castrado).capitalize() == "N":
                  caracteristicas_pet["Castrado"] = "Não"
              else:
                  print("Digite sim ou não.")
      perg_castrado()
  cont += 1








def perg_obs():
  perg_obser = input("\n Você tem alguma observação sobre este animal?(S/N) ").capitalize()
  if perg_obser == "S":
      caracteristicas_pet["Observacoes"] = input("\nDigite suas Observações: ")
perg_obs()


print()


#Pergunta se deseja alterar alguma informação do pet
dado_para_alterar = 0
alterar_dados = (input(f"\nVocê quer alterar as características do pet? [S/N] ").strip().capitalize())


while alterar_dados  == "S":
  dado_para_alterar = (input("O que gostaria de atualizar? Digite o tipo de dado ou o número ao lado.").strip().capitalize())
  if dado_para_alterar in ["Nome", "2"]:
      perg_nome_pet()
  if dado_para_alterar in ["Raça", "3"]:
      perg_raca()
  if dado_para_alterar in ["Porte", "4"]:
      perg_porte()
  if dado_para_alterar in ["Cor", "5"]:
      perg_cor()
  if dado_para_alterar in ["Gênero", "6"]:
      perg_genero()
  if dado_para_alterar in ["Idade","7"]:
      perg_idade()
  if dado_para_alterar in ["Peso", "8"]:
      perg_peso()
  if dado_para_alterar in ["Castrado", "9"]:
      perg_castrado()
  if dado_para_alterar in ["Obs","10","Observacoes","Observaçoes", "Observacões", "Observações"]:
      perg_obs()
  iterador =  iter(caracteristicas_pet.items())
  next(iterador)
  for i, (chave,valor) in enumerate(iterador, 2) :
      print(f'{titulo3}{i:<2} {resetcor}{chave:<16}:   {texto}{valor}')
  alterar_dados = (input(f"\nVocê quer alterar uma informação? [S/N] ").strip().capitalize())


#formata as informações e mostra todas elas em uma lista
for chave, valor in dados_dono.items():
  dados_dono[chave] = str(valor).title()


for chave, valor in caracteristicas_pet.items():
  caracteristicas_pet[chave] = str(valor).title()


for chave,valor in (dados_dono|caracteristicas_pet).items():
  print(f'{titulo3}{chave:<16}{resetcor}:   {texto}{valor}')


id_DOC ={"Dados_Dono":dados_dono,"Dados_Pet":caracteristicas_pet}
try:
  with open ("dados_mensais.json", "r", encoding="utf-8") as pet_shop:
      dados = json.load(pet_shop)
      if not isinstance(dados, list):
          dados = []
except (FileNotFoundError, json.JSONDecodeError):
  dados=[]
for pessoa in dados:
  pet_arquivo = pessoa["Dados_Pet"].copy()
  pet_novo = caracteristicas_pet.copy()




  del pet_arquivo["ID pet"]
  del pet_novo["ID pet"]
  if pet_arquivo == pet_novo:
      print(f"\nAVISO!!! Esse cadastro é identico a um cadastro ja existente no arquivo. É recomendado que termine esse programa e escreva um cadastro com dados diferentes.")
      if input(f"\nDeseja terminar o programa? Digite 'nao' ou 'não' caso deseje continuar.\n ").lower() == "sim":
          print("Programa terminado.")
          exit()
        
Verdade = 0
while Verdade == 0:
  for pet in dados:
      if str(pet["Dados_Pet"]["ID pet"]) == str(caracteristicas_pet["ID pet"]):
          id_velho = caracteristicas_pet["ID pet"]
          criar_id()
          print(f"AVISO!!! O id do animal já existe no arquivo. O id {id_velho} agora sera {caracteristicas_pet['ID pet']} ")
      else:
          Verdade = 1
        




dados.append(id_DOC)
with open ("dados_mensais.json", "w", encoding="utf-8") as pet_shop:
  json.dump(dados, pet_shop, indent=4, ensure_ascii=False)




print("Programa terminado com sucesso.")













