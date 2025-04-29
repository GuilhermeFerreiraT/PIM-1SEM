import json
import re  # Importa o módulo para validação de padrões
from config import (
    console, gerar_hash, sessao, espaço_linhas,
    USUARIOS_JSON, FuzzyCompleter, WordCompleter
)
from prompt_toolkit import prompt

def input_numerico(mensagem, minimo=None, maximo=None):
    while True:
        try:
            valor = int(prompt(mensagem))
            if (minimo is not None and valor < minimo) or (maximo is not None and valor > maximo):
                console.print(f"[red]Por favor, insira um número entre {minimo} e {maximo}.[/red]")
                continue
            return valor
        except ValueError:
            console.print("[red]Entrada inválida. Por favor, insira um número válido.[/red]")

def validar_senha(senha):
    # Verifica se a senha atende aos requisitos
    if len(senha) < 8:
        console.print("[red]A senha deve ter pelo menos 8 caracteres.[/red]")
        return False
    if not any(char.isupper() for char in senha):
        console.print("[red]A senha deve conter pelo menos uma letra maiúscula.[/red]")
        return False
    if not any(char.isdigit() for char in senha):
        console.print("[red]A senha deve conter pelo menos um número.[/red]")
        return False
    return True

def cadastro():
    menu_banner = espaço_linhas("CADASTRO", font="small")
    console.print(f"[blue]{menu_banner}[blue]")
    try:
        wordcomp_email = WordCompleter(['@gmail.com', '@outlook.com'], ignore_case=True)
        completer_email = FuzzyCompleter(wordcomp_email)

        nome = prompt('Nome: ')
        email = prompt('Email: ', completer=completer_email)
        idade = input_numerico('Idade: ', 1)
        cidade = prompt('Cidade: ')
        
        console.print("[blue]Escolha a classe do usuário:[/blue]")
        console.print("1. Classe 1 (Python, Banco de Dados, Lógica)")
        console.print("2. Classe 2 (Engenharia de Software, Cibersegurança)")
        console.print("3. Classe 3 (Avançado)")
        classe = input_numerico('Classe (1, 2 ou 3): ', 1, 3)

        # Verificar se o arquivo existe
        try:
            with open(USUARIOS_JSON, 'r', encoding='utf-8') as arquivo:
                usuarios = json.load(arquivo)
        except FileNotFoundError:
            # Criar arquivo se ele não existir
            with open(USUARIOS_JSON, 'w', encoding='utf-8') as arquivo:
                json.dump([], arquivo)
            usuarios = []
        except json.JSONDecodeError:
            console.print("[red]Erro ao ler arquivo de usuários. Inicializando novo arquivo...[/red]")
            with open(USUARIOS_JSON, 'w', encoding='utf-8') as arquivo:
                json.dump([], arquivo)
            usuarios = []

        num_usuarios = len(usuarios)
        perfil = "admin" if num_usuarios == 0 else "aluno"

        console.print("[blue]A senha deve atender aos seguintes requisitos:[/blue]")
        console.print("- Pelo menos 8 caracteres.")
        console.print("- Pelo menos uma letra maiúscula.")
        console.print("- Pelo menos um número.")
        
        while True:
            senha = prompt('Senha: ', is_password=True)
            if not validar_senha(senha):
                continue
            senha_confirmacao = prompt('Confirme a senha: ', is_password=True)
            if senha != senha_confirmacao:
                console.print("[red]As senhas não coincidem. Tente novamente.[/red]")
            else:
                break

        senha_hash = gerar_hash(senha)

        novo_usuario = {
            "id_usuario": num_usuarios + 1,
            "nome": nome,
            "email": email,
            "senha": senha_hash,
            "perfil": perfil,
            "idade": idade,
            "cidade": cidade,
            "classe": classe
        }

        usuarios.append(novo_usuario)
        
        with open(USUARIOS_JSON, 'w', encoding='utf-8') as arquivo:
            json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

        console.print(f"[green]Usuário {nome} cadastrado com sucesso como {perfil}![/green]")

        sessao['usuario'] = email
        sessao['perfil'] = perfil
        sessao['nome'] = nome
        sessao['classe'] = classe 
        sessao['idade'] = idade
        sessao['cidade'] = cidade
        sessao['id_usuario'] = num_usuarios + 1

        console.print(f"[green]Bem-vindo! usuario {sessao['id_usuario']}.[/green]")  


    except Exception as e:
        console.print(f"[red]Erro no cadastro: {e}[/red]")