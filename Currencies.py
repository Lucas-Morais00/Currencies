#Author: Lucas Morais Zaroni
#Date: 16/03/2021
#Version: 2.0
#GitHub: https://github.com/Lucas-Morais00

import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

#Importando as URLs para os codigos de dinheiro real e valor das criptomoedas
url_cash = "https://www.iban.com/currency-codes"
url_cripto  = "https://www.infomoney.com.br/ferramentas/criptomoedas/"

#Trabalhando com possiveis erros nas URLs
try:
    r_iban = requests.get(url_cash)
    r_infomoney = requests.get(url_cripto)
except:
    print(f"Encontramos um problema no sistema, tente novamente mais tarde :(")

#Usando o BeautifulSoup para pegar o que eu preciso nos sites (trabalhando com HTML)
html_iban = r_iban.text
html_infomoney = r_infomoney.text

soup_iban = BeautifulSoup(html_iban, 'html.parser')
soup_infomoney = BeautifulSoup(html_infomoney, 'html.parser')

#Trabalhando com os codigos do Iban --------------------------------------------------------------------
find_tables = soup_iban.find('table')
tr_list = find_tables.find_all('tr')

del tr_list[0]

countrie_list = []
code_list = []
code_list_format = []
final_code = []
index = 0

for item in tr_list:
    countrie_list.append(item.find('td').string)

for item in tr_list:
    code_list.append(item.find_all('td'))

for i in range(0, len(code_list)):
    for j in range(0, 1):
        code_list_format.append(code_list[i][2])

for item in code_list_format:
    code = str(item)
    format_code = code.replace('<td>', '').replace('</td>', '')
    final_code.append(format_code)

#USANDO COUNTRIE_LIST PARA OS PAISES E FINAL_CODE PARA OS CODIGOS

countrie_list.remove("ANTARCTICA")
del final_code[8]
countrie_list.remove("PALESTINE, STATE OF")
del final_code[181]
del countrie_list[219]
del final_code[219]

#Fim dos codigos Iban, coloquei todos em uma lista ja formatados ------------------------------------------------------
#Inicio dos codigos Infomoney

find_cripto = soup_infomoney.find('table')
tr_list_infomoney = find_cripto.find_all('tr')

#Fim dos codigos Infomoney, coloquei todos em uma lista ja formatados ------------------------------------------------------

print("Bem-vindo ao Negociador de Moedas")
print("")

for countrie in countrie_list:
    print(f"#{index} {countrie.lower().capitalize()}")
    index = index + 1

print("")

countries_choice = []
valor_final = []

def get_countrie_1():
    print("Digite o número do país de origem da moeda para converter:")
    try:
        countrie_1 = int(input())
        if countrie_1 < 0 or countrie_1 > (len(final_code) - 1):
            print("Numero indisponivel")
            del countrie_1
        countries_choice.append(countrie_1)

    except:
        print("Opcao invalida")
        get_countrie_1()

def get_countrie_2():
    print("Digite o número do país de destino da moeda para converter:")
    try:
        countrie_2 = int(input())
        if countrie_2 < 0 or countrie_2 > (len(final_code) - 1):
            print("Numero indisponivel")
            del countrie_2
        countries_choice.append(countrie_2)

    except:
        print("Opcao invalida")
        get_countrie_2()

get_countrie_1()
first = countries_choice[0]
print(f"País selecionado: {countrie_list[first].capitalize()}")

get_countrie_2()
second = countries_choice[1]
print(f"País selecionado: {countrie_list[second].capitalize()}")

def get_valor():
    try:
        valor = int(input(f"Quantos {final_code[first]} você quer converter para {final_code[second]}?\n"))
        valor_final.append(valor)
    
    except:
        print("Opção invalida")
        get_valor()

get_valor()
quant = valor_final[0]

#USANDO FIRST, SECOND E QUANT

source = str(final_code[first])
destiny = str(final_code[second])

def get_change():

    url_transfer = "https://transferwise.com/gb/currency-converter/"

    req = requests.get(f"{url_transfer}{source}-to-{destiny}-rate?amount={int(quant)}")

    html_transfer = req.text

    transfer_soup = BeautifulSoup(html_transfer, 'html.parser')

    transfer = transfer_soup.find('span', class_='text-success').string

    return transfer

print(f"Transformando {quant} {source} para {destiny}...")

final = int(quant) * float(get_change())

rounded = round(final, 2)

base = format_currency(quant, source)
total = format_currency(rounded, destiny)

print(f"Conversão pronta: {base} é igual {total}")
print("Obrigado por usar o Conversor de Moedas 2.0!")









