import json
from config import (
    console, verificar_senha, sessao, espaço_linhas, FuzzyCompleter, WordCompleter
)
from prompt_toolkit import prompt
from utils import USUARIOS_JSON

def login():
    menu_banner = espaço_linhas("LOGIN", font="small")
    console.print(f"[blue]{menu_banner}[blue]")

    try:
        wordcomp_email = WordCompleter(['@gmail.com', '@outlook.com'], ignore_case=True)
        completer_email = FuzzyCompleter(wordcomp_email)
        
        while True:
            email = prompt('Email: ', completer=completer_email)
            if '@' not in email:
                console.print("[red]E-mail inválido. Certifique-se de incluir '@'.[/red]")
                continue
            break

        senha_log = prompt("Senha: ", is_password=True)

        # Procurar usuário no arquivo JSON
        with open(USUARIOS_JSON, 'r', encoding='utf-8') as arquivo:
            usuarios = json.load(arquivo)
        
        usuario_encontrado = None
        for usuario in usuarios:
            if usuario["email"] == email:
                usuario_encontrado = usuario
                break

        if usuario_encontrado:
            if verificar_senha(senha_log, usuario_encontrado["senha"]):
                sessao['usuario'] = email
                sessao['perfil'] = usuario_encontrado["perfil"]
                sessao['nome'] = usuario_encontrado["nome"]
                sessao['classe'] = usuario_encontrado.get("classe", None)  # Garantir que 'classe' seja obtida corretamente
                sessao['cidade'] = usuario_encontrado["cidade"]
                sessao['idade'] = usuario_encontrado["idade"]
                sessao['id_usuario'] = usuario_encontrado["id_usuario"]
                console.print(f"[green]Login bem-sucedido! Bem-vindo {usuario_encontrado['nome']} ({usuario_encontrado['perfil']}).[/green]")
            else:
                console.print("[red]Usuário ou senha inválidos.[/red]")
        else:
            console.print("[red]Usuário não encontrado.[/red]")
            
    except FileNotFoundError:
        console.print("[red]Arquivo de usuários não encontrado.[/red]")
    except json.JSONDecodeError:
        console.print("[red]Erro ao ler arquivo de usuários.[/red]")
    except Exception as e:
        console.print(f"[red]Erro no login: {e}[/red]")