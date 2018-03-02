# -*- coding: UTF-8 -*-
#!/usr/bin/python

"""
Universidade de Lisboa
Faculdade de Ciencias
Departamento de Informatica
Licenciatura em Tecnologias da Informacao 2016/2017

Programacao II

Projeto de Programacao II - Erasmus

Este modulo contem funcoes que ultimamente transformam os dados retirados de ficheiros CSV 
em quatro graficos. O primeiro grafico e referente aos estudantes erasmus por pais, o segundo 
grafico aos estudantes erasmus na proporcao da populacao por pais, o terceiro grafico linguagem 
utilizada nos intercambios e por fim o ultimo grafico sobre numero medio de ects realizados pelos estudantes em erasmus.

"""

__author__ = "Ana Pinheiro, 50029 ; Nuno Soares, 43558"
__copyright__ = "Programacao II, LTI, DI/FC/UL, 2017"
__version__ = "0.1"
__maintainer__ = "Ana Pinheiro, Nuno Soares"
__email__ = "fc50029@alunos.fc.ul.pt, fc43558@alunos.fc.ul.pt"

import csv
import math
import numpy
import pylab
from copy import deepcopy

def acumula (lista_dicionarios, chave_pesquisa):
    """
    Requires: A chave_pesquisa ocorre em todos os
    dicionários constantes na lista_dicionarios.
    Ensures: Devolve um dicionario onde a) as várias chaves
    são os valores associados à chave_pesquisa na
    lista_dicionarios e b) os valores do resultado são o
    número de vezes que as chaves do resultado ocorrem na
    lista_dicionarios.
    >>> l = []
    >>>acumula(l,'x') == {} #lista vazia, elemento nao vazio , ocorrencias = 0
    >>>True
    
    >>> l = [{'x': 'a', 'y': 23}, {'x': 'b', 'y': 78},{'x': 'a', 'y': 99}]
    >>> acumula (l, 'x') == {'a': 2, 'b': 1}   #Lista não vazia, elemento não vazio, ocorrencias > 1
    >>>True
    
    >>>acumula(l,'') == {}  # elemento vazio
    >>>True
    
    >>>acumula(l,'j') == {}  #lista nao vazia, elemento nao vazio, ocorrencias = 0
    >>>True
    
    >>> k = [{}]   
    >>> acumula(k,'x') == {} #lista vazia, elemento nao vazio
    >>>True
    
    >>> acumula(k,'')=={} #lista vazia, elemento vazio
    >>>True
    """
    lista = []
    d = {}
    if chave_pesquisa != '':
        for i in lista_dicionarios:
            if chave_pesquisa in i.keys():
                value = i[chave_pesquisa]
                lista.append(value)
                if value in d:
                    d[value] = 1 + d[value]
                else:
                    d[value] = 1
            else:
                return d

    return d


def correct_country_name(dicionario):
    """
    Funcao que recebe um dicionario e limita os caracteres das keys que excedem os 2 carateres (de maneira a corrigir 
    casos como o da Bélgica, que tem mais de 2 caracteres).
    Requires: dicionario e um dicionario.
    Ensures: Devolve um dicionario cujas todas as keys tem 2 carateres.
    """
    for key in dicionario.keys():
        if len(key) > 2:
            new_key = key[:2]
            if new_key in dicionario:
                dicionario[new_key] = dicionario[new_key] + dicionario[key]
            else:
                dicionario[new_key] = dicionario[key]
            del dicionario[key]
    return dicionario


def soma (lista_dicionarios, chave_pesquisa, chave_soma):
    """
    Requires: A chave_pesquisa e a chave_soma ocorrem em
    todos os dicionários constantes na lista_dicionarios. O
    valor associado à chave_soma é um número.
    Ensures: Devolve um dicionario onde a) as várias chaves
    são os valores associados à chave_pesquisa na
    lista_dicionarios e b) os valores do resultado são
    obtidos pela soma dos valores associados à
    chave_pesquisa na lista_dicionarios.
    
    >>> h = [{}] 
    >>> soma(h,'x','y') == {} #listavazia
    True
    
    >>> l = [{'x': 'a', 'y': 23}, {'x': 'b', 'y': 78},{'x': 'a', 'y': 99}]
    >>> soma (l, 'x', 'y') == {'a': 122, 'b': 78}
    True

    >>>soma(l,'','') == {} #lista nao vazia, elemento1 vazio, elemento 2 vazio
    >>>True
    
    >>>soma(l,'x','') == {} #lista nao vazia, elemento1 nao vazio, elemento 2 vazio
    >>>True
    
    >>>soma(l,'','y')=={} #lista nao vazia, elemento1 vazio, elemento 2 nao vazio
    >>>True
    
    >>>soma(l,'n','') == {} #lista nao vazia, elemento nao vazio, ocorrencia  = 0
    >>>True
    
    >>>soma(l,'n','y')== {}  #lista nao vazia, elemento nao vazio
    >>>True
    
    """
    dict_soma = {}
    if chave_pesquisa != '' or chave_soma != '':
        for i in lista_dicionarios:
            if chave_pesquisa in i.keys() and chave_soma in i.keys():
                if i[chave_pesquisa] in dict_soma:
                    dict_soma[i[chave_pesquisa]] = i[chave_soma] + dict_soma[i[chave_pesquisa]]

                else:
                    dict_soma[i[chave_pesquisa]] = i[chave_soma]
    return dict_soma


def readcsv(nome_ficheiro_csv, tag_name):
    """
    Funcao que recebe como parametros o nome_ficheiro_csv e a tag_name e devolve um dicionario em que a tag_name sera a key para
    os varios valores.
    Require: nome_ficheiro_csv e um ficheiro csv e tag_name e uma string.
    Ensures: Devolve um dicionario em que as keys são as tag names.
    """
    dados=[]
    with open(nome_ficheiro_csv, 'rU') as ficheiro_csv:
        leitor = csv.DictReader(ficheiro_csv, delimiter = ';')
        for linha in leitor:
            dados.append({tag_name:linha[tag_name]})
        return dados


def readcsv_ects(nome_ficheiro_csv, tag_name):
    """
    Funcao que recebe como parametros o nome_ficheiro_csv e a tag_name e devolve um dicionario em que a tag_name sera a key para
    os varios valores.
    Require: nome_ficheiro_csv e um ficheiro csv e tag_name e uma string.
    Ensures: Devolve um dicionario em que as keys são as tag names.
    """
    dados = []
    with open(nome_ficheiro_csv, 'rU') as ficheiro_csv:
        leitor = csv.DictReader(ficheiro_csv, delimiter=';')
        for linha in leitor:
            if linha[tag_name] != '':
                dados.append({"HOME_INSTITUTION_CTRY_CDE": linha["HOME_INSTITUTION_CTRY_CDE"], tag_name: float(linha[tag_name])})
        return dados


def readcsv_country(nome_ficheiro_csv):
    """
    Funcao que recebe como parametros o nome_ficheiro_csv e a tag_name e devolve um dicionario em que a tag_name sera a key para
    os varios valores.
    Require: nome_ficheiro_csv e um ficheiro csv e tag_name e uma string.
    Ensures: Devolve um dicionario em que as keys são as tag names.
    """
    dados = []
    with open(nome_ficheiro_csv, 'rU') as ficheiro_csv:
        leitor = csv.DictReader(ficheiro_csv, delimiter=';')
        for linha in leitor:
            dados.append({"Country code": linha["Country code"], "Population": int(linha["Population"])})
        return dados


def seleccionar_numero_paises(dicionario, numero_max):
    """
    Funcao que ira filtrar os 15 paises cujos dados serao usados posteriormente nos graficos.
    Require: dicionario e um dicionario, numero_max e um int.
    Ensures: Devolve um dicionario que tem no maximo numero_max de keys.
    """
    dic = deepcopy(dicionario)
    novo_dic = {}
    for i in range(numero_max):
        key_max = max(dic, key=dic.get)
        novo_dic[key_max] = dic[key_max]
        del dic[key_max]

    return novo_dic


def convert_upper(dicionario):
    """
    Funcao que recebe um dicionario e transforma os carateres das keys em letras maiusculas.
    Require: dicionario e um dicionario.
    Ensures: Devolve um dicionario.
    """
    dic = deepcopy(dicionario)
    dic_keys = dic.keys()
    novo_dic = {}
    for i in dic_keys:
        new_key = i.upper()
        if new_key in novo_dic:
            novo_dic[new_key] = novo_dic[new_key] + dic[i]
        else:
            novo_dic[new_key] = dic[i]

    return novo_dic


def first_graph(nome_ficheiro_csv, n_max):
    """
    Funcao que ira produzir um dos graficos pretendidos e que sera posteriormente chamado na funçao "Erasmus".
    Requires: nome_ficheiro_csv e o nome do ficheiro csv e n_max é um int.
    Ensures: devolve um grafico.
    """
    ler = readcsv(nome_ficheiro_csv, "HOME_INSTITUTION_CTRY_CDE")
    dados = acumula(ler, "HOME_INSTITUTION_CTRY_CDE")
    dados2 = correct_country_name(dados)
    dados3 = seleccionar_numero_paises(dados2, 15)

    tuple_list = dados3.items()
    tuple_list = sorted(tuple_list, key=lambda x: x[1], reverse=True)
    #print tuple_list

    keys_list = []
    values_list = []

    for i in range(len(tuple_list)):
        keys_list.append(tuple_list[i][0])
        values_list.append(tuple_list[i][1])

    pylab.bar(range(len(dados3)), values_list, align="center")
    pylab.xticks(range(len(dados3)), keys_list)

    pylab.title(u'Distribuição dos estudantes Erasmus em intercâmbio')
    pylab.xlabel(u'Países')
    pylab.ylabel(u'Número de intercâmbios')

    #pylab.show()


def fourth_graph(nome_ficheiro_csv, n_max):
    """
    Funcao que ira produzir um dos graficos pretendidos e que sera posteriormente chamado na funçao "Erasmus".
    Requires: nome_ficheiro_csv e o nome do ficheiro csv e n_max é um int.
    Ensures: devolve um grafico.
    """
    ler = readcsv_ects(nome_ficheiro_csv, "TOTAL_ECTS_CREDITS_AMT")
    dados = soma(ler, "HOME_INSTITUTION_CTRY_CDE", "TOTAL_ECTS_CREDITS_AMT")
    dados2 = correct_country_name(dados)

    lista_paises = dados2.keys()

    paises = acumula(ler, "HOME_INSTITUTION_CTRY_CDE")
    paises_corrigido = correct_country_name(paises)

    for i in lista_paises:
        valor_inteiro = dados2[i]
        dados2[i] = valor_inteiro/paises_corrigido[i]

    dados3 = seleccionar_numero_paises(dados2, 15)

    tuple_list = dados3.items()
    tuple_list = sorted(tuple_list, key=lambda x: x[1], reverse=True)
    #print tuple_list

    keys_list = []
    values_list = []

    for i in range(len(tuple_list)):
        keys_list.append(tuple_list[i][0])
        values_list.append(tuple_list[i][1])

    pylab.bar(range(len(dados3)), values_list, align="center")
    pylab.xticks(range(len(dados3)), keys_list)

    pylab.title(u'Número médio de ECTS obtidos')
    pylab.xlabel(u'Países')
    pylab.ylabel(u'Número médio de ECTS')

    #pylab.show()


def third_graph(nome_ficheiro_csv, n_max):
    """
    Funcao que ira produzir um dos graficos pretendidos e que sera posteriormente chamado na funçao "Erasmus".
    Requires: nome_ficheiro_csv e o nome do ficheiro csv e n_max é um int.
    Ensures: devolve um grafico.
    """
    ler = readcsv(nome_ficheiro_csv, "LANGUAGE_TAUGHT_CDE")
    dados = acumula(ler, "LANGUAGE_TAUGHT_CDE")
    dados2 = correct_country_name(dados)
    dados3 = convert_upper(dados2)
    dados4 = seleccionar_numero_paises(dados3, 15)

    tuple_list = dados4.items()
    tuple_list = sorted(tuple_list, key=lambda x: x[1], reverse=True)
    #print tuple_list

    keys_list = []
    values_list = []

    for i in range(len(tuple_list)):
        keys_list.append(tuple_list[i][0])
        values_list.append(tuple_list[i][1])

    pylab.bar(range(len(dados4)), values_list, align="center")
    pylab.xticks(range(len(dados4)), keys_list)

    pylab.title(u'Línguas utilizadas nos intercâmbios')
    pylab.xlabel(u'Língua')
    pylab.ylabel(u'Número de intercâmbios')

    #pylab.show()


def second_graph(nome_ficheiro_csv, n_max, nome_countries_csv):
    """
    Funcao que ira produzir um dos graficos pretendidos e que sera posteriormente chamado na funçao "Erasmus".
    Requires: nome_ficheiro_csv e o nome do ficheiro csv e n_max é um int.
    Ensures: devolve um grafico.
    """
    ler = readcsv(nome_ficheiro_csv, "HOME_INSTITUTION_CTRY_CDE")
    dados = acumula(ler, "HOME_INSTITUTION_CTRY_CDE")
    dados2 = correct_country_name(dados)

    lista_paises = dados2.keys()

    info_paises = readcsv_country(nome_countries_csv)
    info_paises2 = soma(info_paises, "Country code", "Population")

    new_dic = {}
    for i in lista_paises:
        if i == "UK":
            old_key = "GB"
            formula = (float(dados2[i]) / float(info_paises2[old_key]))*1000000
            new_dic[i] = formula
        else:
            formula = (float(dados2[i])/float(info_paises2[i]))*1000000
            new_dic[i] = formula

    dados3 = seleccionar_numero_paises(new_dic, 15)

    tuple_list = dados3.items()
    tuple_list = sorted(tuple_list, key=lambda x: x[1], reverse=True)
    #print tuple_list

    keys_list = []
    values_list = []

    for i in range(len(tuple_list)):
        keys_list.append(tuple_list[i][0])
        values_list.append(tuple_list[i][1])

    pylab.bar(range(len(dados3)), values_list, align="center")
    pylab.xticks(range(len(dados3)), keys_list)

    pylab.title(u'Estudantes Erasmus por milhão de habitantes')
    pylab.xlabel(u'Países')
    pylab.ylabel(u'Intercâmbios / milhão habitantes')

    #pylab.show()


def get_school_year(nome_ficheiro_csv):
    """
    Funçao que retira o ano da primeira data na coluna 'STUDY_START_DATE' cujo mês seja setembro
    Requires: nome_ficheiro_csv que se trata de um nome de ficheiro CSV
    Ensures: um numero inteiro que ira corresponder ao ano letivo que sera depois utilizado 
    no titulo da figura que incluira os quatro graficos de barras
    """

    dados = []
    with open(nome_ficheiro_csv, 'rU') as ficheiro_csv:
        leitor = csv.reader(ficheiro_csv, delimiter=';')
        for linha in leitor:
            dados.append(linha[20])

    dados2 = []
    sept = 0
    for i in range(len(dados)):
        dat1 = dados[i]
        dat2 = dat1[:3]
        if sept == 0 and dat2 == "Sep":
            dados2.append(dat1)
            sept = 1

    data_inicio = dados2[0]
    ano = int(data_inicio[4:])
    return ano


def erasmus(erasmus_csv, paises_csv, max_paises_por_grafico):
    """
    Funcao principal do modulo e que vai chamar a maioria das funçoes previamente criadas, de maneira a poder criar quatro
    graficos de barras a partir dos dados obtidos a partir dos ficheiros CSV fornecidos a esta funçao. O utilizador fornece
    ainda um numero maximo de paises cujos dados serao apresentados em cada um dos graficos de barras.
    Requires: erasmus_csv e paises_csv sao nomes de ficheiros csv e max_paises_por_grafico e um int
    Ensures: Devolve quatro graficos com diversas informacoes retiradas do erasmus_csv e de paises_csv sobre max_paises_por graficos.
    """

    ano = get_school_year(erasmus_csv)
    ano2 = ano+1
    year1 = str(ano)
    year2 = str(ano2)

    fig = pylab.figure()
    pylab.rcParams.update({'font.size': 8})
    fig.suptitle(u'Algumas estatísticas sobre o programa Erasmus para o ano de 20'+ year1 + u'-' + year2, fontsize="large")


    fig.add_subplot(221)
    first_graph(erasmus_csv,max_paises_por_grafico)


    fig.add_subplot(222)
    second_graph(erasmus_csv,max_paises_por_grafico,paises_csv)


    fig.add_subplot(223)
    third_graph(erasmus_csv,max_paises_por_grafico)


    fig.add_subplot(224)
    fourth_graph(erasmus_csv,max_paises_por_grafico)

    pylab.show()


#erasmus("kendrick.csv","countries.csv",15)

#if __name__ == "__main__":
    #erasmus ('kendrick.csv', 'countries.csv', 15)

