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

def processar_arquivos(diretorio):
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
                        resultados[caminho_arquivo] = {'massa_molecular': massa_molecular, 'secao_hbond': secao_hbond}

    return resultados, maiores_massas_moleculares

if __name__ == "__main__":
    diretorio = "C:/Users/Portilho/Desktop/Resultados/Result_metabo/5EBK/FAD/1b_G1"

    resultados, maiores_massas_moleculares = processar_arquivos(diretorio)

    with open(os.path.join(diretorio, "Hbond_massaNorma.txt"), "w") as arquivo_analise:
        # Criar uma lista de resultados ordenados antes de escrever no arquivo
        resultados_ordenados = []

        for arquivo, dados in resultados.items():
            arquivo_analise.write(f"{arquivo}\n")
            arquivo_analise.write(f"Massa Molecular Normalizada: {calcular_massa_molecular_normalizada(dados['massa_molecular'], maiores_massas_moleculares)}\n")
            
            arquivo_analise.write("Seção Hbond:\n")
            arquivo_analise.write(dados['secao_hbond'])
            
            # Calcula o número total de interações Hbond
            num_interacoes_hbond = dados['secao_hbond'].count('\n') - 2  # Excluindo as duas primeiras linhas
            massa_molecular_normalizada = calcular_massa_molecular_normalizada(dados['massa_molecular'], maiores_massas_moleculares)
            contatos_normalizados = num_interacoes_hbond / massa_molecular_normalizada
            
            arquivo_analise.write(f"Total de Contatos Hbond Normalizados: {contatos_normalizados}\n")
            
            arquivo_analise.write("===" * 40 + "\n")
            
            # Adicione os resultados a serem classificados
            resultados_ordenados.append((arquivo, contatos_normalizados))

        # Classifique os resultados com base no total de contatos normalizados em ordem decrescente
        resultados_ordenados = sorted(resultados_ordenados, key=lambda x: -x[1])

        # Agora, você pode iterar pelos resultados classificados e escrevê-los no arquivo
        arquivo_analise.write("Resultados Ordenados:\n")
        for arquivo, total_contatos_normalizados in resultados_ordenados:
            arquivo_analise.write(f"Resultado: {arquivo}\n")
            arquivo_analise.write(f"Contatos Normalizados Total: {total_contatos_normalizados}\n")
            arquivo_analise.write("===" * 40 + "\n")
