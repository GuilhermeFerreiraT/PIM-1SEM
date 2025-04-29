from utils import carregar_questionarios
from rich.console import Console

console = Console()

# Carregar os questionários
questionarios = carregar_questionarios()

# Verificar se os questionários foram carregados corretamente
if questionarios:
    console.print(f"Colunas disponíveis: {list(questionarios[0].keys())}")
else:
    console.print("[red]Nenhum questionário encontrado ou arquivo vazio.[/red]")