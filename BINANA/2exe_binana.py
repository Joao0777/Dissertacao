import os
import subprocess
import shutil

def execute_binana(receptor_path, ligand_path, output_folder):
    # Substitua "run_binana.py" pelo caminho do executável "run_binana.py" no seu sistema
    binana_executable = "C:/Users/Portilho/binana-2.1/binana-2.1/python/run_binana.py"

    cmd = ["python", binana_executable, "-receptor", receptor_path, "-ligand", ligand_path, "-output_dir", output_folder, "> errors.txt"]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o Binana para os arquivos {receptor_path} e {ligand_path}: {e}")
    else:
        print(f"Binana executado com sucesso para os arquivos {receptor_path} e {ligand_path}. Resultados salvos em {output_folder}")

def main():
    # Substitua "caminho/da/pasta" pelo caminho da pasta que contém os arquivos de entrada
    folder_path = "C:/Users/Portilho/Desktop/Docking_certo/Resultados/Results_Docking/4AGS/sitio_2/Metabolitos"

    if not os.path.isdir(folder_path):
        print("O caminho fornecido não é uma pasta válida.")
        return

    for root, dirs, files in os.walk(folder_path):
        receptor_file = None
        ligand_file = None

        for file in files:
            if file.endswith(".pdb") and "receptor" in file:
                receptor_file = os.path.join(root, file)
            elif file.endswith(".pdb") and "ligand" in file:
                ligand_file = os.path.join(root, file)

        if receptor_file and ligand_file:
            output_folder = os.path.join(root, "output")
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            execute_binana(receptor_file, ligand_file, output_folder)

if __name__ == "__main__":
    main()