import os
from bs4 import BeautifulSoup
from selenium import webdriver


def carrega_html(url):
    '''
    Carrega html gerado dinamicamente a partir da url.
    '''
    driver = webdriver.Chrome()
    driver.get(url)
    return driver.page_source


def pega_dados(html):
    '''
    Extrai dados da string html e devolve em um dicionário.

    Cada chave do dicionário é um curso. Cada valor do dicionário é uma lista
    com todas as entradas daquele curso. Cada entrada é um dicionário com as
    chaves 'andar', 'turma', 'nome' e 'professores'. Todos os valores são
    strings, exceto professores, que é uma lista de strings.
    '''
    soup = BeautifulSoup(html, "html5lib")
    entradas = soup.find_all('div', {'class': 'contentCurso'})
    todos_dados = dict()
    for entrada in entradas:
        titulo = entrada.find('p', {'class': 'titCurso'})
        if not titulo:
            continue
        titulo = titulo.contents[0]
        col_desc = entrada.find_all('div', {'class': 'colDesc'})
        textos = [c.find_all(text=True) for c in col_desc]
        entradas_curso = [extrai_entrada(*textos[i:i + 5])
                          for i in range(0, len(textos), 5)]
        todos_dados[titulo] = entradas_curso
    return todos_dados


def extrai_entrada(andar, turma, nome, professores, sala):
    '''
    Recebe os dados de uma entrada e devolve o dicionário montado.
    '''
    professores = sum([p.strip().split('\n') for p in professores], [])
    professores = [p for p in professores if p]
    return {
        'andar': andar[0],
        'turma': turma[0],
        'nome': nome[0],
        'professores': professores,
    }


if __name__ == '__main__':
    html = carrega_html('https://www.insper.edu.br/agenda/')
    dados = pega_dados(html)
    for titulo in dados:
        print(titulo)
        entradas_curso = dados[titulo]
        for e in entradas_curso:
            for chave in sorted(e):
                print('%s: %s' % (chave, e[chave]))
            print()
        print('-' * 10)
