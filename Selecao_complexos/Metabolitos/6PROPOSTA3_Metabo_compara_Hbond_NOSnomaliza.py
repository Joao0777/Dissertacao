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

def processar_arquivos(diretorio):
    resultados = {}
    maiores_somatorios_N_O_S = []
    maior_somatorio_global = 0

    for pasta_raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            if arquivo.endswith('.txt'):
                caminho_arquivo = os.path.join(pasta_raiz, arquivo)
                arquivo_pdb = os.path.join(pasta_raiz, "ligand.pdb")
                with open(caminho_arquivo, 'r') as f:
                    conteudo = f.read()

                if "Hbond" in conteudo:
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

def calcular_hbond_normalizado(resultados, maiores_somatorios_N_O_S, maior_somatorio_global):
    hbond_normalizados = {}
    for arquivo, correspondencias in resultados.items():
        num_interacoes_hbond = correspondencias['secao_hbond'].count('\n') - 1
        valor_normalizacao = float(correspondencias['num_atomos_N_O_S']) / float(maior_somatorio_global)
        contatos_normalizados = float(num_interacoes_hbond) / valor_normalizacao
        hbond_normalizados[arquivo] = contatos_normalizados, valor_normalizacao
    return hbond_normalizados

if __name__ == "__main__":
    diretorio_base = "C:/Users/Portilho/Desktop/Resultados/Result_metabo/4AGS/sitio_2/1a_G1"
    arquivo_saida = os.path.join(diretorio_base, "Hbond_NOS_norma.txt")

    resultados_globais = {}
    maiores_somatorios_N_O_S_globais = []
    maior_somatorio_global = 0

    for entrada in os.scandir(diretorio_base):
        if entrada.is_dir() and "output" in [subdir.name for subdir in os.scandir(entrada.path) if subdir.is_dir()]:
            pasta_output = [subdir for subdir in os.scandir(entrada.path) if subdir.is_dir() and subdir.name == "output"][0]
            resultados_locais, maiores_somatorios_N_O_S_locais, somatorio_global_local = processar_arquivos(pasta_output.path)
            
            resultados_globais.update(resultados_locais)
            maiores_somatorios_N_O_S_globais.extend(maiores_somatorios_N_O_S_locais)
            if somatorio_global_local > maior_somatorio_global:
                maior_somatorio_global = somatorio_global_local

    hbond_normalizados = calcular_hbond_normalizado(resultados_globais, maiores_somatorios_N_O_S_globais, maior_somatorio_global)

    with open(arquivo_saida, "w") as arquivo_analise:
        resultados_ordenados = sorted(hbond_normalizados.items(), key=lambda x: -x[1][0])
        for arquivo, (hbond_normalizado, valor_normalizacao) in resultados_ordenados:
            arquivo_analise.write(f"{arquivo}\n")
            arquivo_analise.write(f"Hbond Normalizado: {hbond_normalizado:.4f}\n")
            arquivo_analise.write(f"Valor de Normalização: {valor_normalizacao:.4f}\n")
            arquivo_analise.write("Seção Hbond:\n")
            arquivo_analise.write(resultados_globais[arquivo]['secao_hbond'])
            arquivo_analise.write("===" * 40 + "\n")
