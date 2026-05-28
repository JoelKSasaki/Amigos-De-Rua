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


print(f'{titulo}{"="*30}DOCUMENTAÇÃO DE PROCEDIMENTO{"="*30}')
print(f'{titulo2}{"Dados do procedimento".center(largura, "-")}\n')


from datetime import date
import json


data_procedimento = date.today()
data_br = data_procedimento.strftime('%d/%m/%Y')


Profissonais = {
  1:"Davi",
  2:"Otavio",
  3:"Iohanna",
  4:"Ingrid",
}
Tipos_Procedimentos = {
  1:"Tosa",
  2:"Banho",
  3:"Vermifugacao",
  4:"Exame Apenas",
}


dados_procedimento = {
   "Data do Procedimento" : f'{data_br}',
   "Id pet": "",
   "Nome pet": "",
   "Procedimento" :"",
   "Funcionário" :"",
   "Estado anterior" :"",
   "Estado posterior" :""
}
def escolher_cachorro():
   with open("dados_mensais.json", 'r', encoding='utf-8') as arquivo:
      cadastros = json.load(arquivo)
      escolha2 = ""
      while len(escolha2) != 10:
         try:
            escolha2 = (input("Digite o id do cachorro que fez esse procedimento: "))
            if len(escolha2) != 10:
               print("Digite um número de 10 digitos. ")
         except ValueError:
            print("Digite um número. ")
      encontrou = False
            #vê se o input existe nos cadastros.

      for cadastro in cadastros:
            texto_cadastro = str(cadastro).lower()
            if escolha2 in texto_cadastro:
               encontrou = True


               dados_procedimento["Nome pet"] = cadastro["Dados_Pet"]["Nome pet"]
               dados_procedimento["Id pet"] = cadastro["Dados_Pet"]["ID pet"]


               #print(f"Nome: {dados_procedimento["Nome pet"]}")
               #print(f"ID: {dados_procedimento["Id pet"]}")


               print("\nCADASTRO ENCONTRADO\n")
               #printa o todos os dicionarios que tem esses valores.
               for chave, valor in cadastro.items():
                  print(f"{titulo2}{chave}{resetcor}:")
                  if isinstance(valor, dict):
                        for subchave, subvalor in valor.items():
                           print(f"    {titulo3}{subchave}{resetcor}: {subvalor}")
                  print()
      if not encontrou:
            print("Nenhum cadastro encontrado.")
escolher_cachorro()


def escolher_procedimento():
   procedimento = ""
   while procedimento not in [1,2,3,4]:
      for chave,valor in Tipos_Procedimentos.items():
         print(f'{titulo3}{chave}{resetcor} : {valor}')
      procedimento = int(input("Qual foi o procedimento feito? "))
   if procedimento == 1:
      dados_procedimento["Procedimento"] = "Tosa"
   if procedimento == 2:
      dados_procedimento["Procedimento"] = "Banho"
   if procedimento == 3:
      dados_procedimento["Procedimento"] = "Vermifugacao"
   if procedimento == 4:
      dados_procedimento["Procedimento"] = "Exame Apenas"
escolher_procedimento()
print()


def escolher_profissional():
   profissional = ""
   while profissional not in [1,2,3,4]:
      for chave,valor in Profissonais.items():
         print(f'{titulo3}{chave}{resetcor} : {valor}')
      profissional =  int(input("Escolha um profissional "))
   if profissional == 1:
      dados_procedimento["Funcionário"] = "Davi"
   if profissional == 2:
      dados_procedimento["Funcionário"] = "Otavio"
   if profissional == 3:
      dados_procedimento["Funcionário"] = "Iohanna"
   if profissional == 4:
      dados_procedimento["Funcionário"] = "Ingrid"
escolher_profissional()
print()


dados_procedimento["Estado anterior"] = input("Descreva o estado do animal na chegada ao pet shop: ")
print()
dados_procedimento["Estado posterior"] = input("Descreva o estado do animal depois do procedimento: ")




print(f'{dados_procedimento["Procedimento"].upper()} para o cachorro {dados_procedimento["Nome pet"].upper()}, foi feito no dia {dados_procedimento["Data do Procedimento"]} pelo(a) profissional {dados_procedimento["Funcionário"].upper()}')
print(f'Estado do pet ao entrar na pet shop: {dados_procedimento["Estado anterior"]}')
print(f'Estado do pet ao término do procedimento: {dados_procedimento["Estado posterior"]}')
#with open("procedimentos.txt", "a", encoding="utf-8") as procedimentos:
  #procedimentos.write(f'{dados_procedimento["Id pet"]}|{nome}|{raca}|{porte}|{cor}|{peso}|{procedimentos}|{dados_procedimento["Estado anterior"]}|{dados_procedimento["Estado anterior"]}')


try:
  with open ("procedimentos.json", "r", encoding="utf-8") as procedimentos:
          dados = json.load(procedimentos)
          if not isinstance(dados, list):
              dados = []
except (FileNotFoundError, json.JSONDecodeError):
  dados=[]
dados.append(dados_procedimento)
with open ("procedimentos.json", "w", encoding="utf-8") as procedimentos:
  json.dump(dados, procedimentos, indent=4, ensure_ascii=False)