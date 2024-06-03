import os
import re

# Listas de palavras em maiúsculas
FAD = ["SER14", "ASP35", "ALA47", "THR51", "LYS61", "GLY127", "ARG290", "ASP327", "LEU334", "NDP"]
NADPH = ["TYR198", "ILE199", "GLU202", "TYR221", "ARG222", "ARG228", "MET333", "ALA365", "FAD"]
Tripanotiona = ["CYS52", "CYS57", "TYR110", "LYS240", "HIS461", "THR463", "SER464", "GLU466", "GLU467"]

# Função para extrair resíduo e segundo número de uma linha da sessão Hbond
def extrair_residuo_segundo_numero(linha):
    match = re.search(r'([A-Z]+\d+[A-Z]?)\(\d+\.\d+;\s(\d+\.\d+)\)', linha)
    if match:
        return f"{match.group(1)}({match.group(2)})"
    return None

# Diretório mãe
pasta_mae = 'C:/Users/Portilho/Desktop/Docking_certo/Resultados/Results_Docking/5EBK/FAD/Metabolitos/1b_G1'

# Criação do arquivo de saída
output_file_path = os.path.join(pasta_mae, 'PontesH.txt')
with open(output_file_path, 'w') as analise_arquivo:
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

                    correspondencias_FAD = []
                    correspondencias_NADPH = []
                    correspondencias_Tripanotiona = []

                    # Remove a última linha em branco da sessão Hbond
                    linhas_Hbond = [linha for linha in linhas_Hbond if linha.strip()]

                    # Remove o título "Hbond" da contagem
                    num_elementos_Hbond = len(linhas_Hbond) - 1

                    for linha in linhas_Hbond:
                        correspondencia = extrair_residuo_segundo_numero(linha)
                        if correspondencia:
                            if any(palavra in correspondencia for palavra in FAD):
                                correspondencias_FAD.append(correspondencia)
                            if any(palavra in correspondencia for palavra in NADPH):
                                correspondencias_NADPH.append(correspondencia)
                            if any(palavra in correspondencia for palavra in Tripanotiona):
                                correspondencias_Tripanotiona.append(correspondencia)

                    num_correspondencias_FAD = len(correspondencias_FAD)
                    num_correspondencias_NADPH = len(correspondencias_NADPH)
                    num_correspondencias_Tripanotiona = len(correspondencias_Tripanotiona)

                    analise_arquivo.write(f"{subdir}\n")
                    analise_arquivo.write(f"Número de Interação por ponte de Hidrogênio detectadas: {num_elementos_Hbond}\n\n")
                    analise_arquivo.write(f"FAD:\nInteração por ponte de Hidrogênio detectada: {num_correspondencias_FAD}\n")
                    analise_arquivo.write("Correspondências FAD:")
                    for correspondencia in correspondencias_FAD:
                        analise_arquivo.write(f"{correspondencia},  ")
                    analise_arquivo.write(f"\n\n")
                    analise_arquivo.write(f"NADPH:\nInteração por ponte de Hidrogênio detectada: {num_correspondencias_NADPH}\n")
                    analise_arquivo.write("Correspondências NADPH:")
                    for correspondencia in correspondencias_NADPH:
                        analise_arquivo.write(f"{correspondencia},  ")
                    analise_arquivo.write(f"\n\n")
                    analise_arquivo.write(f"Tripanotiona:\nInteração por ponte de Hidrogênio detectada: {num_correspondencias_Tripanotiona}\n")
                    analise_arquivo.write("Correspondências Tripanotiona: ")
                    for correspondencia in correspondencias_Tripanotiona:
                        analise_arquivo.write(f"{correspondencia},  ")
                    analise_arquivo.write(f"\n\n")

                    analise_arquivo.write("===" * 40 + "\n")
