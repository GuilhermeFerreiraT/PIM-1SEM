import json
import os  # Import necessário para localizar a pasta de Downloads
from config import console, sessao
from utils import carregar_progresso, carregar_cursos, carregar_usuarios
from collections import defaultdict
from openpyxl import Workbook

USUARIOS_JSON = "SRC/NP1OFC/JSON/usuarios.json"

def salvar_usuarios(usuarios):
    # Salva os usuários no arquivo JSON.
    with open(USUARIOS_JSON, 'w', encoding='utf-8') as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

def atualizar_classe_usuario(usuario_email):
    # Atualiza a classe do usuário com base no progresso.
    progresso = carregar_progresso()
    cursos = carregar_cursos()
    usuarios = carregar_usuarios()

    usuario = next((u for u in usuarios if u['email'] == usuario_email), None)
    if not usuario or usuario['perfil'] != 'aluno':
        return

    # Verificar se o usuário completou todos os cursos da classe atual
    cursos_classe_atual = [curso for curso in cursos if curso['classe'] == usuario['classe']]
    cursos_concluidos = {registro['curso'] for registro in progresso if registro['usuario'] == usuario_email}

    if all(curso['titulo'] in cursos_concluidos for curso in cursos_classe_atual):
        usuario['classe'] += 1  # Avança para a próxima classe
        salvar_usuarios(usuarios)
        console.print(f"[green]Usuário {usuario['nome']} avançou para a classe {usuario['classe']}![/green]")

def gerar_relatorio_excel():
    # Gera um relatório Excel com as notas.
    progresso = carregar_progresso()
    usuarios = carregar_usuarios()
    cursos = carregar_cursos()

    if not progresso:
        console.print("[yellow]Nenhum progresso registrado até o momento.[/yellow]")
        return

    # Criar um novo workbook
    wb = Workbook()

    # Adicionar planilha para notas por módulo
    ws_modulos = wb.active
    ws_modulos.title = "Notas por Módulo"
    ws_modulos.append(["Curso", "Módulo", "Usuário", "Pontos"])

    for registro in progresso:
        ws_modulos.append([registro['curso'], registro['modulo'], registro['usuario'], registro['pontos']])

    # Adicionar planilha para notas por curso
    ws_cursos = wb.create_sheet(title="Notas por Curso")
    ws_cursos.append(["Curso", "Soma das Notas"])

    cursos_dict = defaultdict(list)
    for registro in progresso:
        cursos_dict[registro['curso']].append(registro['pontos'])

    for curso, notas in cursos_dict.items():
        soma = sum(notas)
        ws_cursos.append([curso, soma])

    # Adicionar planilha para notas por aluno
    ws_alunos = wb.create_sheet(title="Notas por Aluno")
    ws_alunos.append(["Usuário", "Curso", "Módulo", "Pontos"])

    for registro in progresso:
        ws_alunos.append([registro['usuario'], registro['curso'], registro['modulo'], registro['pontos']])

    # Localizar a pasta de Downloads do usuário
    caminho_downloads = os.path.join(os.path.expanduser("~"), "Downloads")

    # Garantir que a pasta de Downloads existe
    if not os.path.exists(caminho_downloads):
        console.print("[red]Erro: A pasta de Downloads não foi encontrada.[/red]")
        return

    # Salvar o arquivo Excel na pasta de Downloads
    caminho_arquivo = os.path.join(caminho_downloads, "relatorio_notas.xlsx")
    wb.save(caminho_arquivo)
    console.print(f"[green]Relatório Excel gerado com sucesso: {caminho_arquivo}[/green]")

def input_numerico(mensagem, minimo=None, maximo=None):
    while True:
        try:
            valor = int(console.input(mensagem))
            if (minimo is not None and valor < minimo) or (maximo is not None and valor > maximo):
                console.print(f"[red]Por favor, insira um número entre {minimo} e {maximo}.[/red]")
                continue
            return valor
        except ValueError:
            console.print("[red]Entrada inválida. Por favor, insira um número válido.[/red]")
