import questionary

def menu_interativo():
    resposta = questionary.select(
        "Escolha uma opção:",
        choices=["Cadastro", "Login", "LGPD", "Sair"]
    ).ask()

    if resposta:
        print(f"Você escolheu: {resposta}")
    else:
        print("Nenhuma opção selecionada.")

menu_interativo()