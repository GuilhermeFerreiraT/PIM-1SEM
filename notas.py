import json
import os  # Import necessário para localizar a pasta de Downloads
from config import console, sessao
from utils import carregar_progresso, carregar_cursos, carregar_usuarios
from collections import defaultdict
import pandas as pd
import numpy as np  # Substituir statistics por numpy
from openpyxl import Workbook

USUARIOS_JSON = "NP1OFC/JSON/usuarios.json"

def salvar_usuarios(usuarios):
    # Salva os usuários no arquivo JSON.
    with open(USUARIOS_JSON, 'w', encoding='utf-8') as arquivo:
        json.dump(usuarios, arquivo, indent=4, ensure_ascii=False)

def atualizar_classe_usuario(usuario_email):
    # Atualiza a classe do usuário com base no progresso.
    progresso = carregar_progresso()
    cursos = carregar_cursos()
    usuarios = carregar_usuarios()

    usuario = next((u for u in usuarios if u['email'] == usuario_email), None)
    if not usuario or usuario['perfil'] != 'aluno':
        return

    # Verificar se o usuário completou todos os cursos da classe atual
    cursos_classe_atual = [curso for curso in cursos if curso['classe'] == usuario['classe']]
    cursos_concluidos = {registro['curso'] for registro in progresso if registro['usuario'] == usuario_email}

    if all(curso['titulo'] in cursos_concluidos for curso in cursos_classe_atual):
        usuario['classe'] += 1  # Avança para a próxima classe
        salvar_usuarios(usuarios)
        console.print(f"[green]Usuário {usuario['nome']} avançou para a classe {usuario['classe']}![/green]")

def adicionar_nota_maxima_cursos(df_cursos, df_questionarios):
    """
    Adiciona a nota máxima aos cursos com base na quantidade de questionários vinculados.
    """
    # Calcula a quantidade de questionários por curso
    questionarios_por_curso = df_questionarios.groupby('curso')['id'].count().reset_index()
    questionarios_por_curso.columns = ['titulo', 'nota_maxima']

    # Adiciona a nota máxima ao DataFrame de cursos
    df_cursos = df_cursos.merge(questionarios_por_curso, on='titulo', how='left')
    df_cursos['nota_maxima'] = df_cursos['nota_maxima'].fillna(0).astype(int)

    return df_cursos

def gerar_relatorio_excel():

    from utils import carregar_questionarios
    # Gera um relatório Excel com as notas.
    progresso = carregar_progresso()
    usuarios = carregar_usuarios()
    cursos = carregar_cursos()

    if not progresso:
        console.print("[yellow]Nenhum progresso registrado até o momento.[/yellow]")
        return

    # Preparar dados
    df_progresso = pd.DataFrame(progresso)
    df_usuarios = pd.DataFrame(usuarios)
    df_cursos = pd.DataFrame(cursos)

    # Carregar questionários (supondo que exista uma função para isso)
    df_questionarios = pd.DataFrame(carregar_questionarios())

    # Adicionar a nota máxima aos cursos
    df_cursos = adicionar_nota_maxima_cursos(df_cursos, df_questionarios)

    # Aba 1: Notas por Curso
    notas_curso = (
        df_progresso.groupby(['usuario', 'curso'])['pontos']
        .sum()
        .reset_index()
        .merge(df_usuarios[['email', 'nome']], left_on='usuario', right_on='email')
        .merge(df_cursos[['titulo', 'nota_maxima']], left_on='curso', right_on='titulo')
    )
    notas_curso['situacao'] = notas_curso.apply(
        lambda x: 'Aprovado' if x['pontos'] >= 0.6 * x['nota_maxima'] else 'Reprovado', axis=1
    )
    notas_curso = notas_curso[['nome', 'curso', 'pontos', 'situacao']]
    notas_curso.columns = ['Nome do Aluno', 'Curso', 'Nota', 'Situação']

    # Aba 2: Notas por Módulo
    notas_modulo = (
        df_progresso.merge(df_usuarios[['email', 'nome']], left_on='usuario', right_on='email')
        .merge(df_cursos[['titulo']], left_on='curso', right_on='titulo')
    )
    notas_modulo = notas_modulo[['nome', 'curso', 'modulo', 'pontos']]
    notas_modulo.columns = ['Nome do Aluno', 'Curso', 'Módulo', 'Nota do Módulo']

    # Aba 3: Progresso por Módulo
    progresso_modulo = (
        df_progresso.groupby(['usuario', 'curso'])['modulo']
        .nunique()
        .reset_index()
        .merge(df_usuarios[['email', 'nome']], left_on='usuario', right_on='email')
        .merge(df_cursos[['titulo', 'total_modulos']], left_on='curso', right_on='titulo')
    )
    progresso_modulo['situacao'] = progresso_modulo.apply(
        lambda x: 'Completo' if x['modulo'] == x['total_modulos'] else
                  'Em andamento' if x['modulo'] > 0 else 'Incompleto', axis=1
    )
    progresso_modulo = progresso_modulo[['nome', 'curso', 'total_modulos', 'modulo', 'situacao']]
    progresso_modulo.columns = ['Nome do Aluno', 'Curso', 'Número total de Módulos', 'Número de Módulos Completos', 'Situação']

    # Aba 4: Estatísticas por Módulo
    estatisticas_modulo = (
        df_progresso.groupby(['curso', 'modulo'])['pontos']
        .agg([np.mean, lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan, np.median])
        .reset_index()
    )
    estatisticas_modulo.columns = ['Curso', 'Módulo', 'Média das Notas', 'Moda das Notas', 'Mediana das Notas']

    # Aba 5: Estatísticas por Curso
    estatisticas_curso = (
        df_progresso.groupby('curso')['pontos']
        .agg([np.mean, lambda x: x.mode().iloc[0] if not x.mode().empty else np.nan, np.median])
        .reset_index()
    )
    estatisticas_curso.columns = ['Curso', 'Média das Notas', 'Moda das Notas', 'Mediana das Notas']

    # Criar arquivo Excel
    caminho_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    if not os.path.exists(caminho_downloads):
        console.print("[red]Erro: A pasta de Downloads não foi encontrada.[/red]")
        return

    caminho_arquivo = os.path.join(caminho_downloads, "relatorio_notas.xlsx")
    with pd.ExcelWriter(caminho_arquivo, engine='openpyxl') as writer:
        notas_curso.to_excel(writer, index=False, sheet_name="Notas por Curso")
        notas_modulo.to_excel(writer, index=False, sheet_name="Notas por Módulo")
        progresso_modulo.to_excel(writer, index=False, sheet_name="Progresso por Módulo")
        estatisticas_modulo.to_excel(writer, index=False, sheet_name="Estatísticas por Módulo")
        estatisticas_curso.to_excel(writer, index=False, sheet_name="Estatísticas por Curso")

    console.print(f"[green]Relatório Excel gerado com sucesso: {caminho_arquivo}[/green]")

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
