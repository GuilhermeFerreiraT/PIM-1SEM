from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt
from rich.console import Console
from config import console, espaço_linhas, sessao, completer, estilo
from cadastro import cadastro
from login import login
from lgpd import lgpd
from cadcursos import menu_altcursos
from notas import gerar_relatorio_excel
from cursos import exibir_menu_cursos, navegar_cursos

# Estilo e autocompletar
estilo = Style.from_dict({'': 'black'})
word_completer = WordCompleter(['CADASTRO', 'LOGIN', 'LGPD', 'SAIR', 'MENU'], ignore_case=True)
completer = FuzzyCompleter(word_completer)

# Banner do menu
menu_banner = espaço_linhas("MENU", font="small")


# Função de menu
def menu():
    if 'perfil' in sessao:  
        banner_nome = espaço_linhas(f"DE {sessao['nome']}", font="small")   
        console.print(f"[blue]{menu_banner}{banner_nome}[/blue]")   
        if sessao['perfil'] == 'admin':
            console.print("[bold]-NOTAS[/bold]")
            console.print("[bold]-EDIÇÃO DE CURSOS E QUESTIONARIOS[/bold]")
            console.print("[bold]-ENTRAR COMO OUTRO USUARIO[/bold]")
            console.print("[bold]-LGPD[/bold]")
            console.print("[bold]-SAIR[/bold]" + '\n')

            wordcomp_adm = WordCompleter(['NOTAS', 'EDIÇÃO DE CURSOS E QUESTIONARIOS', 'ENTRAR COMO OUTRO USUARIO', 'LGPD', 'SAIR'], ignore_case=True)
            completer_adm = FuzzyCompleter(wordcomp_adm)
            escolha = prompt(
                [('class:prompt', 'Escolha a página: ')],
                style=estilo,
                completer=completer_adm,
                complete_while_typing=True
            )

            if escolha.lower() == "notas":
                submenu_notas()
            elif escolha.lower() == "edição de cursos e questionarios":
                menu_altcursos()
            elif escolha.lower() == "entrar como outro usuario":
                sessao.clear()
                login()
            elif escolha.lower() == "lgpd":
                lgpd()
            elif escolha.lower() == "sair":
                console.print("[red]Encerrando sessão..[/red]")
                sessao.clear()
            else:
                console.print("[yellow]Opção inválida![/yellow]")

        elif sessao['perfil'] == 'aluno':
            console.print("[bold]-MINHAS NOTAS[/bold]")
            console.print("[bold]-CURSOS[/bold]")
            console.print("[bold]-ENTRAR COMO OUTRO USUARIO[/bold]")
            console.print("[bold]-LGPD[/bold]")
            console.print("[bold]-SAIR[/bold]" + '\n')

            wordcomp_alu = WordCompleter(['MINHAS NOTAS', 'CURSOS', 'ENTRAR COMO OUTRO USUARIO', 'LGPD', 'SAIR'], ignore_case=True)
            completer_alu = FuzzyCompleter(wordcomp_alu)
            escolha = prompt(
                [('class:prompt', 'Escolha a página: ')],
                style=estilo,
                completer=completer_alu,
                complete_while_typing=True
            )

            if escolha.lower() == "minhas notas":
                console.print("[yellow]A funcionalidade de exibir notas ainda não está implementada.[/yellow]")
            elif escolha.lower() == "cursos":
                navegar_cursos()  # Chama a função para exibir o menu de cursos
            elif escolha.lower() == "entrar como outro usuario":
                sessao.clear()
                login()
            elif escolha.lower() == "lgpd":
                lgpd()
            elif escolha.lower() == "sair":
                console.print("[red]Encerrando sessão...[/red]")
                sessao.clear()
            else:
                console.print("[yellow]Opção inválida![/yellow]")

    else:
        console.print(f"[blue]{menu_banner}[/blue]")
        console.print("[bold]-CADASTRO[/bold]")
        console.print("[bold]-LOGIN[/bold]")
        console.print("[bold]-LGPD[/bold]")
        console.print("[bold]-SAIR[/bold]" + '\n')        
        escolha = prompt(
            [('class:prompt', 'Escolha a página: ')],
            style=estilo,
            completer=completer,
            complete_while_typing=True
        )

        if escolha.lower() == "cadastro":
            cadastro()
        elif escolha.lower() == "login":
            login()
        elif escolha.lower() == "lgpd":
            lgpd()
        elif escolha.lower() == "sair":
            console.print("[red]Saindo do programa...[/red]")
        else:
            console.print("[yellow]Opção inválida![/yellow]")

    return escolha.upper()


def submenu_notas():
    # Submenu para exibir notas dos alunos.
    while True:
        console.print("\n[blue]Submenu - Notas dos Alunos[/blue]")
        console.print("[bold]- GERAR RELATÓRIO EXCEL[/bold]")
        console.print("[bold]- VOLTAR[/bold]")

        wordcomp_notas = WordCompleter(
            ['GERAR RELATÓRIO EXCEL', 'VOLTAR'],
            ignore_case=True
        )
        escolha = prompt("Escolha uma opção: ", completer=wordcomp_notas)

        if escolha.lower() == 'gerar relatório excel':
            gerar_relatorio_excel()  # Chama a função para gerar o relatório Excel
        elif escolha.lower() == 'voltar':
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


# Função principal
def main():
    while True:
        escolha = menu()
        if escolha.lower() == "sair":
            break


if __name__ == "__main__":
    main()