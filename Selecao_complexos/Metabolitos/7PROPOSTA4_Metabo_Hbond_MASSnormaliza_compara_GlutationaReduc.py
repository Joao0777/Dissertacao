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

def extrair_secao_hbond(conteudo):
    # Padrão para identificar a seção Hbond
    padrao_hbond = r'Hbond\n\n(.*?)(?=\n\n\w+|\Z)'
    # Encontre a primeira correspondência
    correspondencia = re.search(padrao_hbond, conteudo, re.DOTALL)
    if correspondencia:
        return correspondencia.group(1)
    return None

def contar_palavras_em_secao_hbond(secao_hbond, lista_palavras):
    contador = 0
    palavras_encontradas = []
    secao_hbond_lower = secao_hbond.lower()
    for palavra in lista_palavras:
        palavra_lower = palavra.lower()
        contador += secao_hbond_lower.count(palavra_lower)
        if palavra_lower in secao_hbond_lower:
            palavras_encontradas.append(palavra)
    return contador, palavras_encontradas

def encontrar_palavras_em_secao_hbond(secao_hbond, listas_palavras):
    correspondencias = {}
    for nome_lista, lista_palavras in listas_palavras.items():
        contador, palavras_encontradas = contar_palavras_em_secao_hbond(secao_hbond, lista_palavras)
        correspondencias[nome_lista] = {'correspondencias': contador, 'palavras_encontradas': palavras_encontradas}
    return correspondencias

def processar_arquivos(diretorio, listas_palavras):
    resultados = {}
    maiores_massas_moleculares = []

    for pasta_raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            if arquivo.endswith('.txt'):
                caminho_arquivo = os.path.join(pasta_raiz, arquivo)
                with open(caminho_arquivo, 'r') as f:
                    conteudo = f.read()

                # Verifique se o arquivo contém a seção Hbond
                if "Hbond" in conteudo:
                    massa_molecular = extrair_massa_molecular(conteudo)
                    secao_hbond = extrair_secao_hbond(conteudo)
                    if massa_molecular is not None and secao_hbond:
                        maiores_massas_moleculares.append(massa_molecular)

                        # Verificar correspondências com listas de palavras
                        correspondencias = encontrar_palavras_em_secao_hbond(secao_hbond, listas_palavras)

                        resultados[caminho_arquivo] = {
                            'massa_molecular': massa_molecular,
                            'secao_hbond': secao_hbond,
                            'correspondencias': correspondencias
                        }

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

    with open(os.path.join(diretorio, "Hbond_massaNorma_compara_Tripanotiona.txt"), "w") as arquivo_analise:
        resultados_ordenados = []

        for arquivo, dados in resultados.items():
            contatos_total = sum(correspondencias['correspondencias'] for correspondencias in dados['correspondencias'].values())
            contatos_total /= calcular_massa_molecular_normalizada(dados['massa_molecular'], maiores_massas_moleculares)
            resultados_ordenados.append((arquivo, contatos_total, dados))

        resultados_ordenados = sorted(resultados_ordenados, key=lambda x: -x[1])

        for arquivo, contatos_total, dados in resultados_ordenados:
            arquivo_analise.write(f"{arquivo}\n")
            arquivo_analise.write(f"Massa Molecular Normalizada: {calcular_massa_molecular_normalizada(dados['massa_molecular'], maiores_massas_moleculares)}\n")
            
            arquivo_analise.write("Seção Hbond:\n")
            arquivo_analise.write(dados['secao_hbond'])
            
            arquivo_analise.write(f"Contatos Normalizados Total: {contatos_total}\n")
            
            arquivo_analise.write("Correspondências encontradas:\n")
            for lista_nome, palavras_encontradas in dados['correspondencias'].items():
                arquivo_analise.write(f"{lista_nome}:\n{dados['correspondencias'][lista_nome]['correspondencias']} interações\n")
                arquivo_analise.write(f"Número de resíduos importantes: {', '.join(palavras_encontradas['palavras_encontradas'])}\n\n")
            arquivo_analise.write("===" * 40 + "\n")
