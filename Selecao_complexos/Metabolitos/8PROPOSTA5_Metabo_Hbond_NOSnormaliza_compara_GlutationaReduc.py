import os
import re

def extrair_secao_hbond(conteudo):
    padrao_hbond = r'Hbond\n\n(.*?)(?=\n\n\w+|\Z)'
    correspondencia = re.search(padrao_hbond, conteudo, re.DOTALL)
    if correspondencia:
        return correspondencia.group(1)
    return None

def extrair_numero_de_atomos_N_O_S(arquivo_pdb):
    num_atomos_N = 0
    num_atomos_O = 0
    num_atomos_S = 0
    with open(arquivo_pdb, 'r') as pdb_file:
        for linha in pdb_file:
            if linha.startswith("ATOM"):
                simbolo = linha[77:78]
                if simbolo == "N":
                    num_atomos_N += 1
                elif simbolo == "O":
                    num_atomos_O += 1
                elif simbolo == "S":
                    num_atomos_S += 1
    return num_atomos_N, num_atomos_O, num_atomos_S

def processar_arquivos(diretorio_base):
    resultados = {}
    maiores_somatorios_N_O_S = []
    maior_somatorio_global = 0

    for entrada in os.scandir(diretorio_base):
        if entrada.is_dir() and "output" in [subdir.name for subdir in os.scandir(entrada.path) if subdir.is_dir()]:
            pasta_output = [subdir for subdir in os.scandir(entrada.path) if subdir.is_dir() and subdir.name == "output"][0]
            pasta_root = entrada.path
            pasta_output_root = pasta_output.path
            arquivo_pdb = os.path.join(pasta_output_root, "ligand.pdb")

            for arquivo in os.scandir(pasta_output_root):
                if arquivo.is_file() and arquivo.name == "resultado.txt":
                    caminho_arquivo = arquivo.path
                    with open(caminho_arquivo, 'r') as f:
                        conteudo = f.read()
                    
                    num_atomos_N, num_atomos_O, num_atomos_S = extrair_numero_de_atomos_N_O_S(arquivo_pdb)
                    somatorio_N_O_S = num_atomos_N + num_atomos_O + num_atomos_S

                    if somatorio_N_O_S > maior_somatorio_global:
                        maior_somatorio_global = somatorio_N_O_S

                    resultados[caminho_arquivo] = {
                        'num_atomos_N_O_S': somatorio_N_O_S,
                        'secao_hbond': extrair_secao_hbond(conteudo)
                    }
                    maiores_somatorios_N_O_S.append(somatorio_N_O_S)

    return resultados, maiores_somatorios_N_O_S, maior_somatorio_global

def comparar_com_listas_palavras(secao_hbond, listas_palavras):
    correspondencias = {}
    secao_hbond_lower = secao_hbond.lower()
    for nome_lista, lista_palavras in listas_palavras.items():
        contador = 0
        palavras_encontradas = []
        for palavra in lista_palavras:
            palavra_lower = palavra.lower()
            contador += secao_hbond_lower.count(palavra_lower)
            if palavra_lower in secao_hbond_lower:
                palavras_encontradas.append(palavra)
        correspondencias[nome_lista] = {'correspondencias': contador, 'palavras_encontradas': palavras_encontradas}
    return correspondencias

def calcular_hbond_normalizado(resultados, maiores_somatorios_N_O_S, maior_somatorio_global, listas_palavras):
    hbond_normalizados = {}
    for arquivo, correspondencias in resultados.items():
        secao_hbond = correspondencias['secao_hbond']
        
        # Verifica se a seção Hbond não é None
        if secao_hbond:
            num_interacoes_hbond = secao_hbond.count('\n') - 1
            valor_normalizacao = float(correspondencias['num_atomos_N_O_S']) / float(maior_somatorio_global)
            contatos_normalizados = float(num_interacoes_hbond) / valor_normalizacao
            correspondencias_listas_palavras = comparar_com_listas_palavras(secao_hbond, listas_palavras)
            hbond_normalizados[arquivo] = contatos_normalizados, valor_normalizacao, correspondencias_listas_palavras

    return hbond_normalizados

import os
import re

# ... (todo o código anterior)

if __name__ == "__main__":
    diretorio_base = "C:/Users/Portilho/Desktop/Resultados/Result_metabo/4AGS/sitio_2/1_G1"
    arquivo_saida = os.path.join(diretorio_base, "Hbond_NOS_norma_compara_GlutationaReduc.txt")

    resultados_globais = {}
    maiores_somatorios_N_O_S_globais = []
    maior_somatorio_global = 0

    listas_palavras = {
        "sitioG1": ["Cys14", "Arg39", "Glu40", "Val55", "Pro56", "Glu70", "Ser71", "HOH"],
        "sitioG2": ["Cys240", "His265", "Gln267", "Val280", "Pro281", "Glu293", "Ser294"],
        "sitioH1": ["His114", "Tyr215"],
        "sitioH2": ["Pro241", "Met338", "Ile342", "His439", "Ile440", "Arg443"]
    }

    resultados_globais, maiores_somatorios_N_O_S_globais, maior_somatorio_global = processar_arquivos(diretorio_base)

    hbond_normalizados = calcular_hbond_normalizado(resultados_globais, maiores_somatorios_N_O_S_globais, maior_somatorio_global, listas_palavras)

    with open(arquivo_saida, "w") as arquivo_analise:
    # Criar uma lista de tuplas (arquivo, valor de normalização, Hbond norma)
        resultados_ordenados = []

        for arquivo, (contatos_normalizados, valor_normalizacao, correspondencias_listas_palavras) in hbond_normalizados.items():
            somatorio_correspondencias = sum([correspondencias['correspondencias'] for correspondencias in correspondencias_listas_palavras.values()])
            hbond_norma = somatorio_correspondencias / valor_normalizacao
            resultados_ordenados.append((arquivo, valor_normalizacao, hbond_norma))

        # Classificar a lista com base em Hbond norma (segundo elemento da tupla)
        resultados_ordenados = sorted(resultados_ordenados, key=lambda x: -x[2])

        # Escrever os resultados ordenados no arquivo
        for arquivo, valor_normalizacao, hbond_norma in resultados_ordenados:
            arquivo_analise.write(f"{arquivo}\n")
            arquivo_analise.write(f"Hbond Normalizado: {hbond_norma:.8f}\n")
            arquivo_analise.write(f"Valor de Normalização: {valor_normalizacao:.8f}\n")
            arquivo_analise.write("Seção Hbond:\n")
            arquivo_analise.write(resultados_globais[arquivo]['secao_hbond'])
            arquivo_analise.write("Correspondências com Listas de Palavras:\n")
            for lista_nome, correspondencias in hbond_normalizados[arquivo][2].items():
                arquivo_analise.write(f"{lista_nome}:\n")
                arquivo_analise.write(f"  - Total de Correspondências: {correspondencias['correspondencias']}\n")
                arquivo_analise.write(f"  - Palavras Encontradas: {', '.join(correspondencias['palavras_encontradas'])}\n")
            arquivo_analise.write("=" * 120 + "\n")
