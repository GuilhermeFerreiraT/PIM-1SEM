import json
import os

CURSOS_JSON = "NP1OFC/JSON/cursos.json"
PROGRESSO_JSON = "NP1OFC/JSON/progresso.json"
USUARIOS_JSON = "NP1OFC/JSON/usuarios.json"
QUESTIONARIO_JSON = "NP1OFC/JSON/questionarios.json"


def carregar_questionarios():
    # Carrega os questionários existentes do arquivo JSON.
    if os.path.exists(QUESTIONARIO_JSON):
        with open(QUESTIONARIO_JSON, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return []

def carregar_progresso():
    if os.path.exists(PROGRESSO_JSON):
        with open(PROGRESSO_JSON, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return []

def carregar_cursos():
    if os.path.exists(CURSOS_JSON):
        with open(CURSOS_JSON, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return []

def salvar_cursos(cursos):
    with open(CURSOS_JSON, 'w', encoding='utf-8') as arquivo:
        json.dump(cursos, arquivo, indent=4, ensure_ascii=False)

def carregar_progresso():
    if os.path.exists(PROGRESSO_JSON):
        with open(PROGRESSO_JSON, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return []

def carregar_usuarios():
    if os.path.exists(USUARIOS_JSON):
        with open(USUARIOS_JSON, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return []

def salvar_usuarios(usuarios):
    with open(USUARIOS_JSON, 'w', encoding='utf-8') as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)