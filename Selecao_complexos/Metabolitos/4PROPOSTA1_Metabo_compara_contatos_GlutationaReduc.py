import os
import re

def extrair_massa_molecular(conteudo):
    padrao_massa = r"Massa Molecular:\s+(\d+\.\d+)\s+u"
    resultado = re.search(padrao_massa, conteudo)
    if resultado:
        return float(resultado.group(1))
    return None

def calcular_massa_molecular_normalizada(massa_molecular, maiores_massas_moleculares):
    if not maiores_massas_moleculares:
        return 1.0
    maior_massa_molecular = max(maiores_massas_moleculares)
    return massa_molecular / maior_massa_molecular

def contar_palavras_em_arquivo(arquivo, lista_palavras):
    contador = 0
    palavras_encontradas = []
    with open(arquivo, 'r') as f:
        conteudo = f.read()
        for palavra in lista_palavras:
            palavra_lower = palavra.lower()
            contador += conteudo.lower().count(palavra_lower)
            if palavra_lower in conteudo.lower():
                palavras_encontradas.append(palavra)
    return contador, palavras_encontradas

def contar_correspondencias_para_listas(arquivo, listas_palavras):
    correspondencias = {}
    with open(arquivo, 'r') as f:
        conteudo = f.read()
        massa_molecular = extrair_massa_molecular(conteudo)
        if massa_molecular is not None:
            for nome_lista, lista_palavras in listas_palavras.items():
                contador, palavras_encontradas = contar_palavras_em_arquivo(arquivo, lista_palavras)
                correspondencias[nome_lista] = {'correspondencias': contador, 'palavras_encontradas': palavras_encontradas}
            return correspondencias, massa_molecular
        return {}, None

def processar_arquivos(diretorio, listas_palavras):
    resultados = {}
    maiores_massas_moleculares = []

    for pasta_raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            if arquivo.endswith('.txt'):
                caminho_arquivo = os.path.join(pasta_raiz, arquivo)
                correspondencias, massa_molecular = contar_correspondencias_para_listas(caminho_arquivo, listas_palavras)
                if correspondencias:
                    maiores_massas_moleculares.append(massa_molecular)
                    resultados[caminho_arquivo] = correspondencias

    return resultados, maiores_massas_moleculares

if __name__ == "__main__":
    diretorio = "C:/Users/Portilho/Desktop/Resultados/Result_metabo/4AGS/sitio_1/1a_G1"
    
    # Defina suas listas de palavras aqui
    sitioG1 = ["Cys14", "Arg39", "Glu40", "Val55", "Pro56", "Glu70", "Ser71", "HOH"]
    sitioG2 = ["Cys240", "His265", "Gln267", "Val280", "Pro281", "Glu293", "Ser294"]
    sitioH1 = ["His114", "Tyr215"]
    sitioH2 = ["Pro241", "Met338", "Ile342", "His439", "Ile440", "Arg443"]
    # ... Defina as outras listas de palavras
    
    listas_palavras = {
        "sitioG1": sitioG1,
        "sitioG2": sitioG2,
        "sitioH1": sitioH1,
        "sitioH2": sitioH2,
    }

    resultados, maiores_massas_moleculares = processar_arquivos(diretorio, listas_palavras)

    with open(os.path.join(diretorio, "Contatos_GlutaReduc.txt"), "w") as arquivo_analise:
        # Criar uma lista de resultados ordenados antes de escrever no arquivo
        resultados_ordenados = []

        for arquivo, correspondencias in resultados.items():
            if os.path.basename(arquivo) == "resultado.txt":  # Verificar o nome do arquivo
                with open(arquivo, 'r') as f:
                    conteudo = f.read()
                    massa_molecular = extrair_massa_molecular(conteudo)
                if massa_molecular is not None:
                    arquivo_analise.write(f"{arquivo}\n")
                    massa_molecular_normalizada = calcular_massa_molecular_normalizada(massa_molecular, maiores_massas_moleculares)
                    arquivo_analise.write(f"Massa Molecular Normalizada: {massa_molecular_normalizada}\n")
                    
                    # Calcular o valor do total de contatos normalizados
                    total_contatos_normalizados = 0
                    for lista_nome, dados in correspondencias.items():
                        contador = dados['correspondencias']
                        contatos_normalizados = contador / massa_molecular_normalizada  # Calculo de contatos normalizados
                        total_contatos_normalizados += contatos_normalizados
                    
                    arquivo_analise.write(f"Contatos Normalizados Total: {total_contatos_normalizados}\n\n")
                    
                    # Agora, para cada lista de palavras
                    for lista_nome, dados in correspondencias.items():
                        contador = dados['correspondencias']
                        arquivo_analise.write(f"{lista_nome}:\n{contador} interações\n")
                        arquivo_analise.write(f"Número de resíduos importantes: {len(dados['palavras_encontradas'])}\n")
                        arquivo_analise.write(f"Resíduos importantes: {', '.join(dados['palavras_encontradas'])}\n\n")
                    
                    arquivo_analise.write("===" * 40 + "\n")

                    # Adicione os resultados a serem classificados
                    resultados_ordenados.append((arquivo, total_contatos_normalizados))

        # Classifique os resultados com base no total de contatos normalizados em ordem decrescente
        resultados_ordenados = sorted(resultados_ordenados, key=lambda x: -x[1])

        # Agora, você pode iterar pelos resultados classificados e escrevê-los no arquivo
        for arquivo, total_contatos_normalizados in resultados_ordenados:
            arquivo_analise.write(f"Resultado: {arquivo}\n")
            arquivo_analise.write(f"Contatos Normalizados Total: {total_contatos_normalizados}\n")
            arquivo_analise.write("===" * 40 + "\n")
