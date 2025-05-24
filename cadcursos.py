import json
import os
from rich.console import Console
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
from questionario import menu_quest
from utils import carregar_cursos, salvar_cursos, CURSOS_JSON
from config import espaço_linhas

# Inicializa o console para exibir mensagens coloridas
console = Console()

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

def criar_curso():
    # Cadastra um novo curso.
    cursos = carregar_cursos()

    titulo = console.input("Digite o título do curso (ou 'x' para sair): ")
    if titulo.lower() == 'x':
        console.print("[yellow]Operação cancelada.[/yellow]")
        return
    
    num_modulos = input_numerico("Quantos módulos o curso terá? (1 a 5): ", 1, 5)

    modulos = []
    for i in range(num_modulos):
        nome_modulo = console.input(f"Digite o nome do módulo {i + 1} (ou 'x' para sair): ")
        if nome_modulo.lower() == 'x':
            console.print("[yellow]Operação cancelada.[/yellow]")
            return
        
        conteudo = console.input(f"Digite o conteúdo do módulo {i + 1} (ou 'x' para sair): ")
        if conteudo.lower() == 'x':
            console.print("[yellow]Operação cancelada.[/yellow]")
            return
        
        modulos.append({
            "nome": nome_modulo,
            "conteudo": conteudo
        })

    # Vincular o curso a uma classe
    cursos_por_classe = {1: [], 2: [], 3: []}
    for curso in cursos:
        cursos_por_classe[curso["classe"]].append(curso["titulo"])

    console.print("[blue]Escolha a classe para vincular ao curso:[/blue]")
    for classe, cursos_vinculados in cursos_por_classe.items():
        if cursos_vinculados:
            console.print(f"{classe}. Classe {classe} ({', '.join(cursos_vinculados)})")
        else:
            console.print(f"{classe}. Classe {classe} (nenhum curso vinculado)")
    classe = input_numerico("Classe (1, 2 ou 3): ", 1, 3)

    curso = {
        "id_curso": len(cursos) + 1,
        "titulo": titulo,
        "modulos": modulos,
        "classe": classe  # Adiciona a classe vinculada ao curso
    }

    cursos.append(curso)
    salvar_cursos(cursos)
    console.print(f"[green]Curso '{titulo}' cadastrado com sucesso e vinculado à Classe {classe}![/green]")

def listar_cursos():
    # Lista todos os cursos disponíveis.
    cursos = carregar_cursos()
    if not cursos:
        console.print("[red]Nenhum curso encontrado.[/red]")
        return []
    
    console.print("Cursos disponíveis:")
    for i, curso in enumerate(cursos):
        console.print(f"- {curso['titulo']}")
    
    return cursos

def alterar_curso():
    # Altera um curso existente.
    cursos = listar_cursos()
    
    if not cursos:
        return

    titulos_cursos = [curso['titulo'] for curso in cursos]
    wordcomp_cursos = WordCompleter(titulos_cursos, ignore_case=True)

    escolha = prompt("Escolha o título do curso que deseja alterar (ou 'x' para sair): ", completer=wordcomp_cursos)
    if escolha.lower() == 'x':
        console.print("[yellow]Operação cancelada.[/yellow]")
        return

    for i, curso in enumerate(cursos):
        if curso['titulo'] == escolha:
            index = i
            break
    else:
        console.print("[red]Curso não encontrado.[/red]")
        return

    curso = cursos[index]
    console.print(f"\nAlterando o curso: {curso['titulo']}")
    
    # Alterar título
    novo_titulo = console.input("Digite o novo título do curso (ou 'x' para não alterar): ")
    if novo_titulo.lower() != 'x':
        curso['titulo'] = novo_titulo

    # Alterar módulos
    for i, modulo in enumerate(curso['modulos']):
        console.print(f"\nMódulo atual: {modulo['nome']}")
        novo_nome_modulo = console.input("Digite o novo nome do módulo (ou 'x' para não alterar): ")
        if novo_nome_modulo.lower() != 'x':
            curso['modulos'][i]['nome'] = novo_nome_modulo
        
        novo_conteudo = console.input("Digite o novo conteúdo do módulo (ou 'x' para não alterar): ")
        if novo_conteudo.lower() != 'x':
            curso['modulos'][i]['conteudo'] = novo_conteudo

    salvar_cursos(cursos)
    console.print(f"[green]Curso '{curso['titulo']}' alterado com sucesso![/green]")

def deletar_curso():
    # Deleta um curso existente.
    cursos = listar_cursos()
    
    if not cursos:
        return

    titulos_cursos = [curso['titulo'] for curso in cursos]
    wordcomp_cursos = WordCompleter(titulos_cursos, ignore_case=True)

    escolha = prompt("Escolha o título do curso que deseja deletar (ou 'x' para sair): ", completer=wordcomp_cursos)
    if escolha.lower() == 'x':
        console.print("[yellow]Operação cancelada.[/yellow]")
        return

    for i, curso in enumerate(cursos):
        if curso['titulo'] == escolha:
            index = i
            break
    else:
        console.print("[red]Curso não encontrado.[/red]")
        return

    cursos.pop(index)  # Remove o curso da lista
    salvar_cursos(cursos)  # Salva a lista atualizada
    console.print("[green]Curso deletado com sucesso![/green]")

def menu_altcursos():
    # Exibe o menu de opções.
    from config import sessao  # Supondo que você tenha uma função para verificar sessão

    if 'perfil' in sessao:
        while True:
            menu_banner = espaço_linhas("CURSOS", font="small")
            console.print(f"[blue]{menu_banner}[blue]")
            console.print("- Cadastrar Curso")
            console.print("- Alterar Curso")
            console.print("- Deletar Curso")
            console.print("- Questionarios")
            console.print("- Sair")
            
            wordcomp_adm = WordCompleter(['Cadastrar Curso', 'Alterar Curso', 'Deletar Curso', 'Questionarios','Sair'], ignore_case=True)
            escolha = prompt("Escolha uma opção: ", completer=wordcomp_adm)

            if escolha.lower() == 'cadastrar curso':
                criar_curso()
            elif escolha.lower() == 'alterar curso':
                alterar_curso()
            elif escolha.lower() == 'deletar curso':
                deletar_curso()
            elif escolha.lower() == 'questionarios':
                menu_quest()
            elif escolha.lower() == 'sair':
                console.print("[red]Voltando ao menu principal...[/red]")
                from menu import menu
                menu()
                break
            else:
                console.print("[yellow]Opção inválida![/yellow]")

    else:
        console.print("[red]Você não está logado. retornando ao menu inicial[/red]")
        from menu import menu
        menu()  



if __name__ == "__main__":
    menu_altcursos()