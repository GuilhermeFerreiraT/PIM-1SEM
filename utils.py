import json
import os

CURSOS_JSON = "NP1OFC/JSON/cursos.json"
PROGRESSO_JSON = "NP1OFC/JSON/progresso.json"
USUARIOS_JSON = "NP1OFC/JSON/usuarios.json"
QUESTIONARIO_JSON = "NP1OFC/JSON/questionarios.json"


def carregar_questionarios():
    # Carrega os questionários existentes do arquivo JSON.
    try:
        if os.path.exists(QUESTIONARIO_JSON):
            with open(QUESTIONARIO_JSON, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
    except (json.JSONDecodeError, FileNotFoundError):
        print("[red]Erro ao carregar questionários. Verifique o arquivo JSON.[/red]")
    return []

def carregar_progresso():
    try:
        if os.path.exists(PROGRESSO_JSON):
            with open(PROGRESSO_JSON, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
    except (json.JSONDecodeError, FileNotFoundError):
        print("[red]Erro ao carregar progresso. Verifique o arquivo JSON.[/red]")
    return []

def carregar_cursos():
    try:
        if os.path.exists(CURSOS_JSON):
            with open(CURSOS_JSON, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
    except (json.JSONDecodeError, FileNotFoundError):
        print("[red]Erro ao carregar cursos. Verifique o arquivo JSON.[/red]")
    return []

def salvar_cursos(cursos):
    try:
        with open(CURSOS_JSON, 'w', encoding='utf-8') as arquivo:
            json.dump(cursos, arquivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[red]Erro ao salvar cursos: {e}[/red]")

def carregar_usuarios():
    try:
        # Garante que o diretório e o arquivo JSON existem
        os.makedirs(os.path.dirname(USUARIOS_JSON), exist_ok=True)
        if not os.path.exists(USUARIOS_JSON):
            with open(USUARIOS_JSON, 'w', encoding='utf-8') as arquivo:
                json.dump([], arquivo)  # Cria um arquivo JSON vazio com uma lista inicial

        if os.path.exists(USUARIOS_JSON):
            with open(USUARIOS_JSON, 'r', encoding='utf-8') as arquivo:
                return json.load(arquivo)
    except (json.JSONDecodeError, FileNotFoundError):
        print("[red]Erro ao carregar usuários. Verifique o arquivo JSON.[/red]")
    return []

def salvar_usuarios(usuarios):
    try:
        with open(USUARIOS_JSON, 'w', encoding='utf-8') as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[red]Erro ao salvar usuários: {e}[/red]")
