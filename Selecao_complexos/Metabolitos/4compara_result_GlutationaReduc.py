import os

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
        for nome_lista, lista_palavras in listas_palavras.items():
            contador, palavras_encontradas = contar_palavras_em_arquivo(arquivo, lista_palavras)
            correspondencias[nome_lista] = {'correspondencias': contador, 'palavras_encontradas': palavras_encontradas}
    return correspondencias

def processar_arquivos(diretorio, listas_palavras):
    resultados = {}

    for pasta_raiz, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            if arquivo.endswith('.txt'):
                caminho_arquivo = os.path.join(pasta_raiz, arquivo)
                correspondencias = contar_correspondencias_para_listas(caminho_arquivo, listas_palavras)
                resultados[caminho_arquivo] = correspondencias

    return resultados

if __name__ == "__main__":
    diretorio = "C:/Users/Portilho/Desktop/Docking_certo/Resultados/Results_Docking/4AGS/sitio_2/Metabolitos/1b_G1"
    
    # Defina suas listas de palavras aqui
    sitioG1 = ["Cys14", "Arg39", "Glu40", "Val55", "Pro56", "Glu70", "Ser71"]
    sitioG2 = ["Cys240", "His265", "Gln267", "Val280", "Pro281", "Glu293", "Ser294"]
    sitioH1 = ["His114", "Tyr215"]
    sitioH2 = ["Pro241", "Met338", "Ile342", "His439", "Ile440", "Arg443"]
    # ... Defina as outras listas de palavras
    
    listas_palavras = {
        "sitioG1": sitioG1,
        "sitioG2": sitioG2,
        "sitioH1": sitioH1,
        "sitioH2": sitioH2,
        # ... Adicione as outras listas de palavras aqui
    }

    resultados = processar_arquivos(diretorio, listas_palavras)

    with open(os.path.join(diretorio, "Contatos.txt"), "w") as arquivo_analise:
        resultados_ordenados = sorted(resultados.items(), key=lambda x: (sum([len(v['palavras_encontradas']) for v in x[1].values()]), sum([v['correspondencias'] for v in x[1].values()])), reverse=True)
        for arquivo, correspondencias in resultados_ordenados:
            if os.path.basename(arquivo) == "resultado.txt":  # Verificar o nome do arquivo
                arquivo_analise.write(f"{arquivo}\n\n")
                for lista_nome, dados in correspondencias.items():
                    contador = dados['correspondencias']
                    palavras_encontradas = ', '.join(dados['palavras_encontradas'])
                    arquivo_analise.write(f"{lista_nome}:\n{contador} interações\n")
                    arquivo_analise.write(f"Número de resíduos importantes: {len(dados['palavras_encontradas'])}\n")
                    arquivo_analise.write(f"Resíduos importantes: {palavras_encontradas}\n\n")
                    
                arquivo_analise.write("===" * 40 + "\n")