import json
import os  # Importa o módulo para manipulação de diretórios
import re  # Importa o módulo para validação de padrões
from config import console, gerar_hash, sessao, espaço_linhas, FuzzyCompleter, WordCompleter
from prompt_toolkit import prompt
from utils import carregar_usuarios, salvar_usuarios, carregar_cursos # Importa as funções do utils.py

USUARIOS_JSON = "JSON/usuarios.json"
cursos= carregar_cursos()  


def input_numerico(mensagem, minimo=None, maximo=None):
    while True:
        try:
            valor = prompt(mensagem)
            if valor.lower() == 'x':
                return None
            valor = int(valor)
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
        # Carrega os usuários utilizando a função centralizada
        usuarios = carregar_usuarios()

        wordcomp_email = WordCompleter(['@gmail.com', '@outlook.com'], ignore_case=True)
        completer_email = FuzzyCompleter(wordcomp_email)

        while True:
            nome = prompt('Nome (ou digite "x" para cancelar): ')
            if nome.lower() == 'x':
                console.print("[yellow]Cadastro cancelado pelo usuário.[/yellow]")
                return
            if nome.strip():
                break
            console.print("[red]O nome não pode estar vazio. Tente novamente.[/red]")

        while True:
            email = prompt('Email (ou digite "x" para cancelar): ', completer=completer_email)
            if email.lower() == 'x':
                console.print("[yellow]Cadastro cancelado pelo usuário.[/yellow]")
                return
            if '@' not in email:
                console.print("[red]E-mail inválido. Certifique-se de incluir '@'.[/red]")
                continue
            if any(usuario['email'] == email for usuario in usuarios):
                console.print("[red]E-mail já cadastrado. Tente outro.[/red]")
                continue
            break

        idade = input_numerico('Idade (ou digite "x" para cancelar): ', 1)
        if idade is None:
            console.print("[yellow]Cadastro cancelado pelo usuário.[/yellow]")
            return

        cidade = prompt('Cidade (ou digite "x" para cancelar): ')
        if cidade.lower() == 'x':
            console.print("[yellow]Cadastro cancelado pelo usuário.[/yellow]")
            return

        cursos_por_classe = {1: [], 2: [], 3: []}
        for curso in cursos:
            cursos_por_classe[curso["classe"]].append(curso["titulo"])

        console.print("[blue]Escolha a classe para vincular ao curso:[/blue]")
        for classe, cursos_vinculados in cursos_por_classe.items():
            if cursos_vinculados:
                console.print(f"{classe}. Classe {classe} ({', '.join(cursos_vinculados)})")
            else:
                console.print(f"{classe}. Classe {classe} (nenhum curso vinculado)")
        classe = input_numerico('Classe (1, 2 ou 3) (ou digite "x" para cancelar): ', 1, 3)
        if classe is None:
            console.print("[yellow]Cadastro cancelado pelo usuário.[/yellow]")
            return

        num_usuarios = len(usuarios)
        perfil = "admin" if num_usuarios == 0 else "aluno"

        console.print("[blue]A senha deve atender aos seguintes requisitos:[/blue]")
        console.print("- Pelo menos 8 caracteres.")
        console.print("- Pelo menos uma letra maiúscula.")
        console.print("- Pelo menos um número.")

        while True:
            senha = prompt('Senha (ou digite "x" para cancelar): ', is_password=True)
            if senha.lower() == 'x':
                console.print("[yellow]Cadastro cancelado pelo usuário.[/yellow]")
                return
            if validar_senha(senha):
                senha_confirmacao = prompt('Confirme a senha (ou digite "x" para cancelar): ', is_password=True)
                if senha_confirmacao.lower() == 'x':
                    console.print("[yellow]Cadastro cancelado pelo usuário.[/yellow]")
                    return
                if senha == senha_confirmacao:
                    break
                console.print("[red]As senhas não coincidem. Tente novamente.[/red]")
            else:
                console.print("[red]Senha inválida. Tente novamente.[/red]")

        senha_hash = gerar_hash(senha)
        idade_hash = gerar_hash(str(idade))
        cidade_hash = gerar_hash(cidade)

        novo_usuario = {
            "id_usuario": num_usuarios + 1,
            "nome": nome,
            "email": email,
            "senha": senha_hash,
            "perfil": perfil,
            "idade": idade_hash,
            "cidade": cidade_hash,
            "classe": classe
        }

        usuarios.append(novo_usuario)

        # Salva os usuários utilizando a função centralizada
        salvar_usuarios(usuarios)

        console.print(f"[green]Usuário {nome} cadastrado com sucesso como {perfil}![/green]")

        sessao['usuario'] = email
        sessao['perfil'] = perfil
        sessao['nome'] = nome
        sessao['classe'] = classe
        sessao['idade'] = idade
        sessao['cidade'] = cidade
        sessao['id_usuario'] = num_usuarios + 1

    except Exception as e:
        console.print(f"[red]Erro no cadastro: {e}[/red]")

    if 'perfil' in sessao:
        from menu import menu
        menu()            