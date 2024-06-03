from pathlib import Path
import shutil

def read_syb_file(file_path):
    with open(file_path, 'r') as syb_file:
        lines = syb_file.readlines()
    # Ignorar a primeira e as últimas 4 linhas
    data_lines = lines[1:-4]
    # Ler as informações de coordenadas e cargas do arquivo .syb
    coordinates = [line.split()[:3] for line in data_lines]
    charges = [line.split()[3] for line in data_lines]
    return coordinates, charges

def replace_mol2_content(mol2_path, coordinates, charges):
    with open(mol2_path, 'r') as mol2_file:
        mol2_lines = mol2_file.readlines()

    # Encontrar a linha onde inicia o bloco de coordenadas no arquivo .mol2
    start_line = mol2_lines.index('@<TRIPOS>ATOM\n') + 1

    # Substituir as coordenadas e as cargas no arquivo .mol2
    for i, line in enumerate(mol2_lines[start_line:start_line + len(coordinates)]):
        atom_info = line.split()[1:3]  # Manter o tipo de átomo (segundo e terceiro elemento da linha)
        atom_infor = line.split()[5:7]  # Manter o tipo de átomo (segundo e terceiro elemento da linha)
        #mol2_lines[start_line + i] = f"{line.split()[0]:<7}  {atom_info[0]:<5}    {coordinates[i][0]:>10}    {coordinates[i][1]:>10}    {coordinates[i][2]:>10}  {atom_infor[0]:<5}     1   UNK0   {charges[i]:>10}\n"
        coordinates[i][0] = float(coordinates[i][0])
        coordinates[i][1] = float(coordinates[i][1]) 
        coordinates[i][2] = float(coordinates[i][2])
        mol2_lines[start_line + i] = f"{atom_info[0]:<3}     {coordinates[i][0]:>10.4f}      1  {coordinates[i][1]:>10.4f}      1  {coordinates[i][2]:>10.4f}      1\n"

    # Escrever as alterações no arquivo .mol2
    with open(mol2_path, 'w') as mol2_file:
        mol2_file.writelines(mol2_lines)

def main():
    folder1 = Path('C:/Users/Portilho/Desktop/Docking_certo/Metabolitos/Metabo_Arq_Prep/1a_G1/mol2')
    folder2 = Path('C:/Users/Portilho/Desktop/Docking_certo/Metabolitos/Metabo_Arq_Prep/1a_G1/MOPAC_2cargas')
    folder3 = Path('C:/Users/Portilho/Desktop/Docking_certo/Metabolitos/Metabo_Arq_Prep/1a_G1/MOPAC_1geometria')

    # Verificar se as pastas existem
    if not folder1.exists():
        print(f"A pasta1 '{folder1}' não existe.")
        return
    if not folder2.exists():
        print(f"A pasta2 '{folder2}' não existe.")
        return
    if not folder3.exists():
        print(f"A pasta3 '{folder3}' não existe.")
        return

    # Copiar arquivos da pasta1 para a pasta2
    for mol2_file_path in folder1.glob('*.mol2'):
        shutil.copy(mol2_file_path, folder2)

    # Processar os arquivos na pasta2
    for mol2_file_path in folder2.glob('*.mol2'):
        filename = mol2_file_path.name
        syb_file_path = folder3 / (filename.replace('.mol2', '.syb'))

        if not syb_file_path.exists():
            print(f"Arquivo .syb correspondente não encontrado para '{filename}'.")
            continue

        coordinates, charges = read_syb_file(syb_file_path)
        replace_mol2_content(mol2_file_path, coordinates, charges)

    print("Conversão concluída.")

if __name__ == "__main__":
    main()
