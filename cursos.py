import json
import os
from utils import (carregar_progresso, carregar_cursos, PROGRESSO_JSON, CURSOS_JSON, USUARIOS_JSON,
carregar_questionarios, QUESTIONARIO_JSON)
from rich.console import Console
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
from config import sessao  # Importa a sessão do usuáriom questionario

# Inicializa o console para exibir mensagens coloridas
console = Console()

# Nome dos arquivos JSON com o caminho especificado


# Verificar se o módulo statistics está disponível
try:
    from statistics import mean, median, mode
except ImportError:
    # Implementar funções alternativas para mean, median e mode
    def mean(data):
        return sum(data) / len(data) if data else 0

    def median(data):
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        return sorted_data[mid]

    def mode(data):
        from collections import Counter
        count = Counter(data)
        max_count = max(count.values())
        modes = [k for k, v in count.items() if v == max_count]
        if len(modes) == 1:
            return modes[0]
        raise ValueError("No unique mode found")


def salvar_progresso(progresso):
    # Salva o progresso dos usuários.
    with open(PROGRESSO_JSON, 'w', encoding='utf-8') as arquivo:
        json.dump(progresso, arquivo, indent=4, ensure_ascii=False)

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
    salvar_progresso(progresso)


def exibir_menu_cursos():
    # Exibe o menu de cursos disponíveis.
    cursos = carregar_cursos()
    if not cursos:
        console.print("[red]Nenhum curso encontrado.[/red]")
        return None

    if sessao.get('perfil') == 'admin':
        console.print("[blue]Administrador visualizando todos os cursos sem restrição de classe.[/blue]")
    else:
        # Filtrar cursos pela classe do usuário
        classe_usuario = sessao.get('classe')
        cursos = [curso for curso in cursos if curso.get('classe') == classe_usuario]

    if not cursos:
        console.print("[yellow]Nenhum curso disponível para sua classe.[/yellow]")
        from menu import menu
        return menu()

    console.print("Cursos disponíveis:")
    for i, curso in enumerate(cursos):
        console.print(f"{i + 1}. {curso['titulo']}")

    return cursos

def navegar_cursos():
    cursos = exibir_menu_cursos()
    if cursos is None:
        return

    while True:
        wordcomp_cursos = WordCompleter([curso['titulo'] for curso in cursos], ignore_case=True)
        escolha = prompt("Digite o nome do curso (ou 'x' para sair): ", completer=wordcomp_cursos)
        if escolha.lower() == 'x':
            console.print("[yellow]Operação cancelada.[/yellow]")
            return
        curso = next((curso for curso in cursos if curso['titulo'].lower() == escolha.lower()), None)
        if curso:
            break
        else:
            console.print("[red]Curso não encontrado. Tente novamente.[/red]")

    # Navegar pelos módulos do curso
    for i, modulo in enumerate(curso['modulos']):
        console.print(f"\nMódulo: {modulo['nome']}")
        console.print(f"Conteúdo: {modulo['conteudo']}")

        # Indicativo de avanço
        console.print("[blue]Pressione 'Enter' para prosseguir para o questionário ou digite 'x' para retornar ao menu principal.[/blue]")
        
        # Opções para avançar ou retornar
        acao = prompt("Ação: ")
        if acao.lower() == 'x':
            console.print("[yellow]Retornando ao menu principal...[/yellow]")
            return

        if acao == '':
            questionario = carregar_questionarios()
            questionario_modulo = [q for q in questionario if q.get('curso') == curso.get('titulo') and q.get('modulo') == modulo['nome']]
            if questionario_modulo:
                realizar_questionario(questionario_modulo)
            else:
                console.print(f"[red]Nenhum questionário encontrado para o módulo '{modulo['nome']}' do curso '{curso['titulo']}'.[/red]")
            continue  # Avança para o próximo módulo

    console.print("[green]Você completou todos os módulos deste curso![/green]")

def realizar_questionario(questionario_modulo):
    # Realiza o questionário para o módulo selecionado.
    usuario = sessao.get('usuario')  # Obtém o usuário da sessão
    if not usuario:
        console.print("[red]Nenhum usuário logado. Faça login para continuar.[/red]")
        return

    curso = questionario_modulo[0]['curso']
    modulo = questionario_modulo[0]['modulo']

    if verificar_progresso(usuario, curso, modulo):
        console.print("[yellow]Você já completou este questionário. Progresso salvo.[/yellow]")
        return

    pontos = 0
    total_perguntas = len(questionario_modulo)

    for questionario in questionario_modulo:
        console.print(f"\nPergunta: {questionario['pergunta']}")
        for i, opcao in enumerate(questionario['opcoes'], start=1):  # Ajustar para começar do 1
            console.print(f"{i}. {opcao}")

        resposta = prompt("Digite o número da sua resposta: ")
        try:
            resposta_usuario = int(resposta)  # O índice da resposta do usuário já está 1-based
            if resposta_usuario == questionario['resposta_correta']:  # Comparar diretamente com o índice 1-based
                console.print("[green]Resposta correta![/green]")
                pontos += 1
            else:
                console.print(f"[red]Resposta incorreta! A resposta correta é: {questionario['opcoes'][questionario['resposta_correta'] - 1]}[/red]")
        except (ValueError, IndexError):
            console.print("[red]Resposta inválida. Tente novamente.[/red]")

    console.print(f"\nVocê acumulou {pontos} ponto(s) em {total_perguntas} pergunta(s).")
    registrar_progresso(usuario, curso, modulo, pontos)

def calcular_nota_total_curso(usuario, curso_titulo):
    # Calcula a nota total de um curso para um usuário.
    progresso = carregar_progresso()
    total_pontos = sum(
        registro['pontos'] for registro in progresso
        if registro['usuario'] == usuario and registro['curso'] == curso_titulo
    )
    return total_pontos

def exibir_notas_alunos():
    # Exibe as notas de todos os alunos (apenas para administradores).
    if sessao.get('perfil') != 'admin':
        console.print("[red]Acesso negado. Apenas administradores podem acessar esta área.[/red]")
        return

    progresso = carregar_progresso()
    if not progresso:
        console.print("[yellow]Nenhum progresso registrado até o momento.[/yellow]")
        return

    console.print("[blue]Notas dos Alunos:[/blue]")
    alunos = {}
    cursos = {}

    for registro in progresso:
        usuario = registro['usuario']
        curso = registro['curso']
        pontos = registro['pontos']

        # Agrupar notas por aluno
        if usuario not in alunos:
            alunos[usuario] = []
        alunos[usuario].append(pontos)

        # Agrupar notas por curso
        if curso not in cursos:
            cursos[curso] = []
        cursos[curso].append(pontos)

    # Exibir estatísticas por aluno
    console.print("\n[green]Estatísticas por Aluno:[/green]")
    for aluno, notas in alunos.items():
        console.print(f"Aluno: {aluno}")
        console.print(f"  Média: {mean(notas):.2f}")
        console.print(f"  Mediana: {median(notas):.2f}")
        try:
            console.print(f"  Moda: {mode(notas):.2f}")
        except:
            console.print("  Moda: Não aplicável (sem valores únicos)")

    # Exibir estatísticas por curso
    console.print("\n[green]Estatísticas por Curso:[/green]")
    for curso, notas in cursos.items():
        console.print(f"Curso: {curso}")
        console.print(f"  Média: {mean(notas):.2f}")
        console.print(f"  Mediana: {median(notas):.2f}")
        try:
            console.print(f"  Moda: {mode(notas):.2f}")
        except:
            console.print("  Moda: Não aplicável (sem valores únicos)")

