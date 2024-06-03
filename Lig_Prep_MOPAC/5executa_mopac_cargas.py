import os
import subprocess

# Caminho para o diretório contendo os arquivos .mop
diretorio = "C:/Users/Portilho/Desktop/Docking_certo/Metabolitos/Metabo_Arq_Prep/1a_G1/MOPAC_2cargas"

# Lista de arquivos .mop no diretório
arquivos_mop = [arquivo for arquivo in os.listdir(diretorio) if arquivo.endswith(".mop")]

# Loop para executar os arquivos .mop em fila
for arquivo in arquivos_mop:
    caminho_arquivo = os.path.join(diretorio, arquivo)
    comando_mopac = "C:/tripos/sybylx1.1/advcomp/source/qcpe/bin/mopac.exe"  # Substitua pelo caminho correto para o executável do MOPAC
    # Argumentos para o comando MOPAC
    args = [comando_mopac, caminho_arquivo]

    # Executar o comando MOPAC
    try:
        subprocess.run(args, check=True)  # A função run espera que o processo seja concluído
        print(f"Arquivo {arquivo} executado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o arquivo {arquivo}: {e}")

print("Todos os arquivos .mop foram executados.")