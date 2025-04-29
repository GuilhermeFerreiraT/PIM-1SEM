import json
import bcrypt
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from prompt_toolkit.styles import Style
from rich.console import Console

# Configurações do sistema
USUARIOS_JSON = "NP1OFC/JSON/usuarios.json"
sessao = {}

def gerar_hash(senha):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(senha.encode('utf-8'), salt).decode('utf-8')

def verificar_senha(senha_log, senha_hash):
    return bcrypt.checkpw(senha_log.encode('utf-8'), senha_hash.encode('utf-8'))

console = Console()

# Estilo e autocompletar
estilo = Style.from_dict({'': 'black'})
word_completer = WordCompleter(['CADASTRO', 'LOGIN', 'LGPD', 'SAIR', 'MENU'], ignore_case=True)
completer = FuzzyCompleter(word_completer)

def espaço_linhas(text, font="standard"):
    import pyfiglet
    banner = pyfiglet.figlet_format(text, font=font)
    lines = [line.rstrip() for line in banner.split('\n') if line.strip()]
    return '\n'.join(lines) + '\n'

def encerrar_sessao():
    sessao.clear()
    console.print("[red]Saindo da conta...[/red]")