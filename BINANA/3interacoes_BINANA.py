import json
import os

def extract_hydrogen_bonds(log_data):
    interactions = []
    hydrogen_bonds = log_data.get("hydrogenBonds", [])

    for hbond in hydrogen_bonds:
        ligand_atoms = hbond.get("ligandAtoms", [])
        receptor_atoms = hbond.get("receptorAtoms", [])
        metrics = hbond.get("metrics", {})
        angle = metrics.get("angle", 0)
        distance = metrics.get("distance", 0)

        if len(ligand_atoms) == 2 and len(receptor_atoms) == 1:
            interaction_info = (
                f"{receptor_atoms[0]['resName']}{receptor_atoms[0]['resID']}{receptor_atoms[0]['chain']}"
                f"({angle:.3f}; {distance:.3f})({ligand_atoms[0]['atomName']}{ligand_atoms[1]['atomName']}"
                f"-{receptor_atoms[0]['atomName']})"
            )
        elif len(ligand_atoms) == 1 and len(receptor_atoms) == 2:
            interaction_info = (
                f"{receptor_atoms[0]['resName']}{receptor_atoms[0]['resID']}{receptor_atoms[0]['chain']}"
                f"({angle:.3f}; {distance:.3f})({ligand_atoms[0]['atomName']}-"
                f"{receptor_atoms[0]['atomName']}{receptor_atoms[1]['atomName']})"
            )
        else:
            # Default: If neither of the above cases matches, use the previous format
            interaction_info = (
                f"{receptor_atoms[0]['resName']}{receptor_atoms[0]['resID']}{receptor_atoms[0]['chain']}"
                f"({angle:.3f}; {distance:.3f})({ligand_atoms[0]['atomName']}-{receptor_atoms[0]['atomName']})"
            )

        # Verificar se o "resName" do "ligand" é "HOH" e adicionar o sufixo "(HOH)" se for o caso
        if ligand_atoms[0].get("resName") == "HOH":
            interaction_info += "(HOH)"

        interactions.append(interaction_info)

    return interactions

def extract_hydrophobic_contacts(log_data):
    contacts_dict = {}  # Dicionário para armazenar os contatos hidrofóbicos únicos
    hydrophobic_contacts = log_data.get("hydrophobicContacts", [])

    for contact in hydrophobic_contacts:
        receptor_atom = contact.get("receptorAtoms", [{}])[0]
        distance = contact.get("metrics", {}).get("distance", 0)

        # Montar a chave para identificar o contato hidrofóbico (chain, resID, resName do receptor)
        key = (receptor_atom['chain'], receptor_atom['resID'], receptor_atom['resName'])

        # Verificar se a chave já existe no dicionário
        if key in contacts_dict:
            # Se já existe, comparamos as distâncias e mantemos apenas o contato com a menor distância
            if distance < contacts_dict[key]['distance']:
                contacts_dict[key] = {'contact': contact, 'distance': distance}
        else:
            # Se ainda não existe, adicionamos o novo contato no dicionário
            contacts_dict[key] = {'contact': contact, 'distance': distance}

    contacts = []
    for key, value in contacts_dict.items():
        contact = value['contact']
        receptor_atom = contact.get("receptorAtoms", [{}])[0]
        distance = value['distance']

        interaction_info = (
            f"{receptor_atom['resName']}{receptor_atom['resID']}{receptor_atom['chain']}"
            f"({distance:.3f})"
        )

        contacts.append(interaction_info)

    # Ordenar os contatos hidrofóbicos usando a função de ordenação personalizada
    contacts_sorted = sorted(contacts, key=custom_sort_key)

    return contacts_sorted

def extract_salt_bridges(log_data):
    salt_bridges = log_data.get("saltBridges", [])

    bridges = []
    for bridge in salt_bridges:
        receptor_atom = bridge.get("receptorAtoms", [{}])[0]
        distance = bridge.get("metrics", {}).get("distance", 0)

        interaction_info = (
            f"{receptor_atom['resName']}{receptor_atom['resID']}{receptor_atom['chain']}"
            f"({distance:.3f})"
        )

        bridges.append(interaction_info)

    # Ordenar as interações do tipo salt_bridge usando a função de ordenação personalizada
    bridges_sorted = sorted(bridges, key=custom_sort_key)

    return bridges_sorted

def extract_pi_pi_stacking(log_data):
    interactions = []
    pi_pi_stacking = log_data.get("piPiStackingInteractions", [])

    for pi_stacking in pi_pi_stacking:
        ligand_atoms = pi_stacking.get("ligandAtoms", [])
        receptor_atoms = pi_stacking.get("receptorAtoms", [])
        metrics = pi_stacking.get("metrics", {})
        angle = metrics.get("angle", 0)
        distance = metrics.get("distance", 0)

        interaction_info = (
            f"{receptor_atoms[0]['resName']}{receptor_atoms[0]['resID']}{receptor_atoms[0]['chain']}"
            f"({angle:.3f}; {distance:.3f})"
        )

        interactions.append(interaction_info)

    return interactions

def extract_halogen_bonds(log_data):
    interactions = []
    halogen_bonds = log_data.get("halogenBonds", [])

    if not halogen_bonds:
        interactions.append("Nenhuma interação de halogênio encontrada")
    else:
        for hbond in halogen_bonds:
            ligand_atoms = hbond.get("ligandAtoms", [])
            receptor_atoms = hbond.get("receptorAtoms", [])
            distance = hbond.get("metrics", {}).get("distance", 0)

            interaction_info = (
                f"{receptor_atoms[0]['resName']}{receptor_atoms[0]['resID']}{receptor_atoms[0]['chain']}"
                f"({distance:.3f})"
            )

            interactions.append(interaction_info)

    return interactions

def extract_metal_coordinations(log_data):
    interactions = []
    metal_coordinations = log_data.get("metalCoordinations", [])

    if not metal_coordinations:
        interactions.append("Nenhuma interação de coordenação com metais encontrada")
    else:
        for coordination in metal_coordinations:
            metal_atom = coordination.get("metalAtom", {})
            ligand_atoms = coordination.get("ligandAtoms", [])
            distance = coordination.get("metrics", {}).get("distance", 0)

            interaction_info = (
                f"{metal_atom['resName']}{metal_atom['resID']}{metal_atom['chain']}"
                f"({distance:.3f})"
            )

            interactions.append(interaction_info)

    return interactions

def extract_t_shaped(log_data):
    interactions = []
    t_shaped = log_data.get("tStackingInteractions", [])

    if not t_shaped:
        interactions.append("Nenhuma interação de T-Stacking encontrada")
    else:
        for t_shape in t_shaped:
            ligand_atoms = t_shape.get("ligandAtoms", [])
            receptor_atoms = t_shape.get("receptorAtoms", [])
            metrics = t_shape.get("metrics", {})
            angle = metrics.get("angle", 0)
            distance = metrics.get("distance", 0)

            interaction_info = (
                f"{receptor_atoms[0]['resName']}{receptor_atoms[0]['resID']}{receptor_atoms[0]['chain']}"
                f"({angle:.3f}; {distance:.3f})"
            )

            interactions.append(interaction_info)

    return interactions

def extract_cation_pi(log_data):
    interactions = []
    cation_pi = log_data.get("cationPiInteractions", [])

    if not cation_pi:
        interactions.append("Nenhuma interação de cátion-pi encontrada")
    else:
        for cation_pi_interaction in cation_pi:
            ligand_atoms = cation_pi_interaction.get("ligandAtoms", [])
            receptor_atoms = cation_pi_interaction.get("receptorAtoms", [])
            metrics = cation_pi_interaction.get("metrics", {})
            distance = metrics.get("distance", 0)

            interaction_info = (
                f"{receptor_atoms[0]['resName']}{receptor_atoms[0]['resID']}{receptor_atoms[0]['chain']}"
                f"({distance:.3f})"
            )

            interactions.append(interaction_info)

    return interactions

def custom_sort_key(interaction):
    parts = interaction.split("(")[0]
    chain = parts[-1]

    # Verificar se o ID do resíduo é um número ou uma string
    resID_str = parts[:-1][3:]
    if resID_str.isdigit():
        resID = int(resID_str)
    else:
        resID = resID_str

    return chain, resID


def write_to_result_file(
    hydrogen_bonds,
    hydrophobic_contacts,
    salt_bridges,
    pi_stacking,
    halogen_bonds,
    metal_coordinations,
    t_shaped,
    cation_pi,
    output_dir
):
    output_file_path = os.path.join(output_dir, "resultado.txt")

    with open(output_file_path, "w") as result_file:
        # Escrever o título "Hbond" no arquivo
        result_file.write("Hbond\n\n")
        if hydrogen_bonds:
            for interaction in hydrogen_bonds:
                result_file.write(interaction + "\n")
        else:
            result_file.write("Nenhuma interação de hidrogênio encontrada\n")

        # Adicionar título "Contatos Hidrofóbicos" e escrever os contatos hidrofóbicos no arquivo
        result_file.write("\n\n\nContatos Hidrofóbicos\n\n")
        if hydrophobic_contacts:
            for contact in hydrophobic_contacts:
                result_file.write(contact + "\n")
        else:
            result_file.write("Nenhum contato hidrofóbico encontrado\n")

        # Adicionar título "Salt Bridge" e escrever as interações do tipo salt_bridge no arquivo
        result_file.write("\n\n\nSalt Bridge\n\n")
        if salt_bridges:
            for bridge in salt_bridges:
                result_file.write(bridge + "\n")
        else:
            result_file.write("Nenhuma interação de salt bridge encontrada\n")

        # Adicionar título "Pi-Pi Stacking" e escrever as interações do tipo pi-pi_stacking no arquivo
        result_file.write("\n\n\nPi-Pi Stacking\n\n")
        if pi_stacking:
            for pi_stack in pi_stacking:
                result_file.write(pi_stack + "\n")
        else:
            result_file.write("Nenhuma interação de pi-pi stacking encontrada\n")

        # Adicionar título "Halogen Bonds" e escrever as interações do tipo halogen_bonds no arquivo
        result_file.write("\n\n\nHalogen Bonds\n\n")
        if halogen_bonds:
            for halogen_bond in halogen_bonds:
                result_file.write(halogen_bond + "\n")
        else:
            result_file.write("Nenhuma interação de halogênio encontrada\n")

        # Adicionar título "Metal Coordinations" e escrever as interações do tipo metal_coordinations no arquivo
        result_file.write("\n\n\nMetal Coordinations\n\n")
        if metal_coordinations:
            for metal_coordination in metal_coordinations:
                result_file.write(metal_coordination + "\n")
        else:
            result_file.write("Nenhuma interação de coordenação com metais encontrada\n")

        # Adicionar título "T-Shaped" e escrever as interações do tipo t_shaped no arquivo
        result_file.write("\n\n\nT-Shaped\n\n")
        if t_shaped:
            for t_shaped_interaction in t_shaped:
                result_file.write(t_shaped_interaction + "\n")
        else:
            result_file.write("Nenhuma interação de T-Stacking encontrada\n")

        # Adicionar título "Cation-Pi" e escrever as interações do tipo cation_pi no arquivo
        result_file.write("\n\n\nCation-Pi\n\n")
        if cation_pi:
            for cation_pi_interaction in cation_pi:
                result_file.write(cation_pi_interaction + "\n")
        else:
            result_file.write("Nenhuma interação de cátion-pi encontrada\n")


def process_output_file(file_path):
    try:
        with open(file_path, 'r') as file:
            log_data = json.load(file)
            interactions = extract_hydrogen_bonds(log_data)
            hydrophobic_contacts = extract_hydrophobic_contacts(log_data)
            salt_bridges = extract_salt_bridges(log_data)
            pi_stacking = extract_pi_pi_stacking(log_data)
            halogen_bonds = extract_halogen_bonds(log_data)
            metal_coordinations = extract_metal_coordinations(log_data)
            t_shaped = extract_t_shaped(log_data)
            cation_pi = extract_cation_pi(log_data)

            # Obter o diretório do arquivo de entrada
            output_dir = os.path.dirname(file_path)

            write_to_result_file(
                interactions,
                hydrophobic_contacts,
                salt_bridges,
                pi_stacking,
                halogen_bonds,
                metal_coordinations,
                t_shaped,
                cation_pi,
                output_dir
            )
            print("Arquivo 'resultado.txt' gerado com sucesso.")

    except FileNotFoundError:
        print(f"O arquivo {file_path} não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")

def process_files_in_directory(directory_path):
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file == "output.json":
                file_path = os.path.join(root, file)
                process_output_file(file_path)

# Inserir o caminho da pasta mãe contendo os arquivos "output.json" aqui
directory_path = r"C:/Users/Portilho/Desktop/Docking_certo/Resultados/Results_Docking/4AGS/sitio_2/Metabolitos"
process_files_in_directory(directory_path)