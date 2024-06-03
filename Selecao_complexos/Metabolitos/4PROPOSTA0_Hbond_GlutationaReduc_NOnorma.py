import os
import re

# Listas de palavras em maiúsculas
sitioG1 = ["Cys14", "Arg39", "Glu40", "Val55", "Pro56", "Glu70", "Ser71"]
sitioG2 = ["Cys240", "His265", "Gln267", "Val280", "Pro281", "Glu293", "Ser294"]
sitioH1 = ["His114", "Tyr215"]
sitioH2 = ["Pro241", "Met338", "Ile342", "His439", "Ile440", "Arg443"]

# Função para extrair resíduo e segundo número de uma linha da sessão Hbond
def extrair_residuo_segundo_numero(linha):
    match = re.search(r'([A-Z]+\d+[A-Z]?)\(\d+\.\d+;\s(\d+\.\d+)\)', linha)
    if match:
        return f"{match.group(1)}({match.group(2)})"
    return None

# Diretório mãe
pasta_mae = 'C:/Users/Portilho/Desktop/Resultados/Result_metabo/4AGS/sitio_2/1a_G1'

# Criação do arquivo de saída
output_file_path = os.path.join(pasta_mae, 'PontesH_NONorma.txt')

# Lista para armazenar os resultados
resultados = []

# Percorre subdiretórios e analisa arquivos
for subdir, _, arquivos in os.walk(pasta_mae):
    for arquivo in arquivos:
        if arquivo.lower() == 'resultado.txt':
            arquivo_path = os.path.join(subdir, arquivo)
            with open(arquivo_path, 'r') as arquivo:
                conteudo = arquivo.read()

            inicio_Hbond = conteudo.lower().find('hbond')
            if inicio_Hbond != -1:
                final_Hbond = conteudo.lower().find('contatos hidrofóbicos', inicio_Hbond)
                if final_Hbond == -1:
                    final_Hbond = len(conteudo)
                linhas_Hbond = conteudo[inicio_Hbond:final_Hbond].split('\n')

                # Após encontrar 'hbond', pule a linha de título
                linhas_Hbond = linhas_Hbond[1:]

                correspondencias_sitioG1 = []
                correspondencias_sitioG2 = []
                correspondencias_sitioH1 = []
                correspondencias_sitioH2 = []

                # Remove a última linha em branco da sessão Hbond
                linhas_Hbond = [linha for linha in linhas_Hbond if linha.strip()]

                # Remove o título "Hbond" da contagem
                num_elementos_Hbond = len(linhas_Hbond)

                for linha in linhas_Hbond:
                    correspondencia = extrair_residuo_segundo_numero(linha)
                    if correspondencia:
                        for palavra in sitioG1:
                            if palavra.lower() in correspondencia.lower():
                                correspondencias_sitioG1.append(correspondencia)
                        for palavra in sitioG2:
                            if palavra.lower() in correspondencia.lower():
                                correspondencias_sitioG2.append(correspondencia)
                        for palavra in sitioH1:
                            if palavra.lower() in correspondencia.lower():
                                correspondencias_sitioH1.append(correspondencia)
                        for palavra in sitioH2:
                            if palavra.lower() in correspondencia.lower():
                                correspondencias_sitioH2.append(correspondencia)

                num_correspondencias_sitioG1 = len(correspondencias_sitioG1)
                num_correspondencias_sitioG2 = len(correspondencias_sitioG2)
                num_correspondencias_sitioH1 = len(correspondencias_sitioH1)
                num_correspondencias_sitioH2 = len(correspondencias_sitioH2)

                # Calcular o somatório das correspondências de todas as listas
                total_correspondencias = num_correspondencias_sitioG1 + num_correspondencias_sitioG2 + num_correspondencias_sitioH1 + num_correspondencias_sitioH2

                # Armazene os resultados na lista
                resultados.append({
                    'subdir': subdir,
                    'num_elementos_Hbond': num_elementos_Hbond,
                    'correspondencias_sitioG1': correspondencias_sitioG1,
                    'correspondencias_sitioG2': correspondencias_sitioG2,
                    'correspondencias_sitioH1': correspondencias_sitioH1,
                    'correspondencias_sitioH2': correspondencias_sitioH2,
                    'total_correspondencias': total_correspondencias
                })

# Ordene os resultados com base no somatório total
resultados = sorted(resultados, key=lambda x: x['total_correspondencias'], reverse=True)

# Escreva os resultados no arquivo de saída
with open(output_file_path, 'w') as analise_arquivo:
    for resultado in resultados:
        analise_arquivo.write(f"{resultado['subdir']}\n")
        analise_arquivo.write(f"Número de Interação por ponte de Hidrogênio detectadas: {resultado['num_elementos_Hbond']}\n\n")
        analise_arquivo.write(f"Somatório de Correspondências de Todas as Listas: {resultado['total_correspondencias']}\n")
        
        analise_arquivo.write(f"sitioG1:\nInteração por ponte de Hidrogênio detectada: {len(resultado['correspondencias_sitioG1'])}\n")
        analise_arquivo.write("Correspondências sitioG1:")
        for correspondencia in resultado['correspondencias_sitioG1']:
            analise_arquivo.write(f"{correspondencia},  ")
        analise_arquivo.write(f"\n\n")

        analise_arquivo.write(f"sitioG2:\nInteração por ponte de Hidrogênio detectada: {len(resultado['correspondencias_sitioG2'])}\n")
        analise_arquivo.write("Correspondências sitioG2:")
        for correspondencia in resultado['correspondencias_sitioG2']:
            analise_arquivo.write(f"{correspondencia},  ")
        analise_arquivo.write(f"\n\n")

        analise_arquivo.write(f"sitioH1:\nInteração por ponte de Hidrogênio detectada: {len(resultado['correspondencias_sitioH1'])}\n")
        analise_arquivo.write("Correspondências sitioH1: ")
        for correspondencia in resultado['correspondencias_sitioH1']:
            analise_arquivo.write(f"{correspondencia},  ")
        analise_arquivo.write(f"\n\n")

        analise_arquivo.write(f"sitioH2:\nInteração por ponte de Hidrogênio detectada: {len(resultado['correspondencias_sitioH2'])}\n")
        analise_arquivo.write("Correspondências sitioH2:")
        for correspondencia in resultado['correspondencias_sitioH2']:
            analise_arquivo.write(f"{correspondencia},  ")
        analise_arquivo.write(f"\n\n")
        analise_arquivo.write("===" * 40 + "\n")
