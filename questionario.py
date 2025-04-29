import json
import os
from utils import carregar_cursos  # Importar de utils.py
from rich.console import Console

# Inicializa o console para exibir mensagens coloridas
console = Console()

# Nome do arquivo JSON que armazenará todos os questionários
QUESTIONARIO_JSON = "SRC/NP1OFC/JSON/questionarios.json"
PROGRESSO_JSON = "SRC/NP1OFC/JSON/progresso.json"

def carregar_progresso():
    # Carrega o progresso dos usuários.
    if os.path.exists(PROGRESSO_JSON):
        with open(PROGRESSO_JSON, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return []

def verificar_progresso(usuario, curso, modulo):
    # Verifica se o usuário já completou o módulo.
    progresso = carregar_progresso()
    for registro in progresso:
        if registro['usuario'] == usuario and registro['curso'] == curso and registro['modulo'] == modulo:
            return True
    return False

def registrar_progresso(usuario, curso, modulo, pontos):
    # Registra o progresso do usuário.
    progresso = carregar_progresso()
    progresso.append({
        "usuario": usuario,
        "curso": curso,
        "modulo": modulo,
        "pontos": pontos
    })
    with open(PROGRESSO_JSON, 'w', encoding='utf-8') as arquivo:
        json.dump(progresso, arquivo, indent=4, ensure_ascii=False)

def carregar_questionarios():
    # Carrega os questionários existentes do arquivo JSON.
    if os.path.exists(QUESTIONARIO_JSON):
        with open(QUESTIONARIO_JSON, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    return []

def salvar_questionarios(questionarios):
    # Salva todos os questionários em um arquivo JSON.
    with open(QUESTIONARIO_JSON, 'w', encoding='utf-8') as arquivo:
        json.dump(questionarios, arquivo, indent=4, ensure_ascii=False)

def criar_questionario():
    # Cadastra um novo questionário e cria um arquivo JSON correspondente se não existir.
    questionarios = carregar_questionarios()

    titulo = console.input("Digite o título do questionário (ou 'x' para sair): ")
    if titulo.lower() == 'x':
        console.print("[yellow]Operação cancelada.[/yellow]")
        return

    pergunta = console.input("Digite a pergunta (ou 'x' para sair): ")
    if pergunta.lower() == 'x':
        console.print("[yellow]Operação cancelada.[/yellow]")
        return
    
    # Coletando a quantidade de opções
    num_opcoes = input_numerico("Quantas opções você deseja (2 a 5)? (ou 'x' para sair): ", 2, 5)

    # Coletando as opções de resposta
    opcoes = []
    for i in range(num_opcoes):
        opcao = console.input(f"Digite a opção {i + 1} (ou 'x' para sair): ")
        if opcao.lower() == 'x':
            console.print("[yellow]Operação cancelada.[/yellow]")
            return
        opcoes.append(opcao)

    resposta_correta = input_numerico(f"Digite o número da opção correta (1 a {num_opcoes}): (ou 'x' para sair): ", 1, num_opcoes) - 1

    vinculo_curso = console.input("Digite o curso vinculado ao questionário (ou 'x' para sair): ")

    vinculo_modulo= console.input("Digite o modulo vinculado ao questionário (ou 'x' para sair): ")


    # Criando um dicionário para o questionário
    questionario = {
        "titulo": titulo,
        "pergunta": pergunta,
        "opcoes": opcoes,
        "resposta_correta": resposta_correta
    }

    # Adicionando o novo questionário à lista existente
    questionarios.append(questionario)

    # Salvando todos os questionários no arquivo JSON
    salvar_questionarios(questionarios)
    console.print(f"[green]Questionário '{titulo}' cadastrado com sucesso![/green]")

def listar_questionarios():
    # Lista todos os questionários disponíveis.
    questionarios = carregar_questionarios()
    if not questionarios:
        console.print("[red]Nenhum questionário encontrado.[/red]")
        return []
    
    console.print("Questionários disponíveis:")
    for i, questionario in enumerate(questionarios):
        console.print(f"{i + 1}. {questionario['titulo']}")
    
    return questionarios

def alterar_questionario():
    # Altera um questionário existente.
    questionarios = listar_questionarios()
    
    if not questionarios:
        return

    escolha = console.input("Escolha o número do questionário que deseja alterar (ou 'x' para sair): ")
    if escolha.lower() == 'x':
        console.print("[yellow]Operação cancelada.[/yellow]")
        return

    try:
        escolha = int(escolha) - 1
    except ValueError:
        console.print("[red]Entrada inválida. Por favor, insira um número.[/red]")
        return

    if escolha < 0 or escolha >= len(questionarios):
        console.print("[red]Índice inválido. Nenhum questionário encontrado.[/red]")
        return

    questionario = questionarios[escolha]

    console.print(f"\nAlterando o questionário: {questionario['titulo']}")
    console.print(f"Pergunta atual: {questionario['pergunta']}")
    console.print("Opções atuais:")
    for j, opcao in enumerate(questionario['opcoes']):
        console.print(f"  {j + 1}. {opcao}")
    console.print(f"Resposta correta atual: {questionario['opcoes'][questionario['resposta_correta']]}")

    # Listando itens que podem ser alterados
    while True:
        console.print("\nO que você deseja alterar?")
        console.print("1. Alterar Todos os Itens")
        console.print("2. Título")
        console.print("3. Pergunta")
        console.print("4. Opções")
        console.print("5. Resposta Correta")
        console.print("6. Não alterar nada")
        
        escolha_alteracao = console.input("Escolha o número do item que deseja alterar (ou 'x' para sair): ")

        if escolha_alteracao.lower() == 'x':
            console.print("[yellow]Operação cancelada.[/yellow]")
            return

        try:
            escolha_alteracao = int(escolha_alteracao)
        except ValueError:
            console.print("[red]Entrada inválida. Por favor, insira um número.[/red]")
            continue

        if escolha_alteracao == 1:
            questionario['titulo'] = console.input("Digite o novo título do questionário (ou 'x' para sair): ")
            if questionario['titulo'].lower() == 'x':
                console.print("[yellow]Operação cancelada.[/yellow]")
                return
            questionario['pergunta'] = console.input("Digite a nova pergunta (ou 'x' para sair): ")
            if questionario['pergunta'].lower() == 'x':
                console.print("[yellow]Operação cancelada.[/yellow]")
                return
            num_opcoes = len(questionario['opcoes'])
            for i in range(num_opcoes):
                opcao = console.input(f"Digite a nova opção {i + 1} (ou 'x' para sair): ")
                if opcao.lower() == 'x':
                    console.print("[yellow]Operação cancelada.[/yellow]")
                    return
                questionario['opcoes'][i] = opcao
            resposta_correta = input_numerico(f"Digite o número da nova opção correta (1 a {num_opcoes}): (ou 'x' para sair): ", 1, num_opcoes) - 1
            questionario['resposta_correta'] = resposta_correta
            console.print(f"[green]Todos os itens do questionário '{questionario['titulo']}' foram alterados com sucesso![/green]")
            break
        elif escolha_alteracao == 2:
            questionario['titulo'] = console.input("Digite o novo título do questionário (ou 'x' para sair): ")
            if questionario['titulo'].lower() == 'x':
                console.print("[yellow]Operação cancelada.[/yellow]")
                return
        elif escolha_alteracao == 3:
            questionario['pergunta'] = console.input("Digite a nova pergunta (ou 'x' para sair): ")
            if questionario['pergunta'].lower() == 'x':
                console.print("[yellow]Operação cancelada.[/yellow]")
                return
        elif escolha_alteracao == 4:
            num_opcoes = len(questionario['opcoes'])
            for i in range(num_opcoes):
                opcao = console.input(f"Digite a nova opção {i + 1} (ou 'x' para sair): ")
                if opcao.lower() == 'x':
                    console.print("[yellow]Operação cancelada.[/yellow]")
                    return
                questionario['opcoes'][i] = opcao
        elif escolha_alteracao == 5:
            num_opcoes = len(questionario['opcoes'])
            resposta_correta = input_numerico(f"Digite o número da nova opção correta (1 a {num_opcoes}): (ou 'x' para sair): ", 1, num_opcoes) - 1
            questionario['resposta_correta'] = resposta_correta
        elif escolha_alteracao == 6:
            console.print("[yellow]Nenhuma alteração foi feita.[/yellow]")
            break
        else:
            console.print("[red]Opção inválida. Tente novamente.[/red]")
            continue

        # Salvando as alterações
        salvar_questionarios(questionarios)
        console.print(f"[green]Questionário '{questionario['titulo']}' alterado com sucesso![/green]")
        break

def deletar_questionario():
    # Deleta um questionário existente.
    questionarios = listar_questionarios()
    
    if not questionarios:
        return

    escolha = console.input("Escolha o número do questionário que deseja deletar (ou 'x' para sair): ")
    if escolha.lower() == 'x':
        console.print("[yellow]Operação cancelada.[/yellow]")
        return

    try:
        escolha = int(escolha) - 1
    except ValueError:
        console.print("[red]Entrada inválida. Por favor, insira um número.[/red]")
        return

    if escolha < 0 or escolha >= len(questionarios):
        console.print("[red]Índice inválido. Nenhum questionário encontrado.[/red]")
        return

    questionarios.pop(escolha)  # Remove o questionário da lista
    salvar_questionarios(questionarios)  # Salva a lista atualizada
    console.print("[green]Questionário deletado com sucesso![/green]")

def menu_quest():
    # Exibe o menu de opções.
    while True:
        console.print("\nMenu:")
        console.print("1. Cadastrar Questionário")
        console.print("2. Alterar Questionário")
        console.print("3. Deletar Questionário")
        console.print("4. Sair")
        
        escolha = console.input("Escolha uma opção: ")

        if escolha == '1':
            criar_questionario()
        elif escolha == '2':
            alterar_questionario()
        elif escolha == '3':
            deletar_questionario()
        elif escolha == '4':
            console.print("[red]Saindo do sistema...[/red]")
            break
        else:
            console.print("[yellow]Opção inválida![/yellow]")

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

if __name__ == "__main__":
    menu_quest()