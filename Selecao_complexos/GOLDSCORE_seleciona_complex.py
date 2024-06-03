import os

sdf_file_path = "C:/Users/Portilho/Desktop/Resultados/Result_metabo/2W0H/NAD_comFAD/1b_G1/1bG1_2W0H_NADcomFAD.sdf"
output_file_path = os.path.join(os.path.dirname(sdf_file_path), 'output.txt')

# Abra o arquivo SDF
with open(sdf_file_path, 'r') as arquivo_sdf, open(output_file_path, 'w') as arquivo_saida:
    complexos = {}
    complexo_atual = None

    # Função para processar informações de um complexo
    def processar_complexo(complexo_id, complexo_dados):
        fitness = None
        hbond = None
        vdw = None
        for linha in complexo_dados:
            if linha.startswith("> <Gold.Goldscore.Fitness>"):
                fitness = float(next(complexo_dados))
            elif linha.startswith("> <Gold.Goldscore.External.HBond>"):
                hbond = float(next(complexo_dados))
            elif linha.startswith("> <Gold.Goldscore.External.Vdw>"):
                vdw = float(next(complexo_dados))
            elif linha.startswith("$$$$"):
                return (fitness, hbond, vdw)

    for linha in arquivo_sdf:
        if "|M" in linha:
            # Extrair o número de complexo do identificador
            partes = linha.split("|M")
            if len(partes) >= 2:
                complexo_id = "M" + partes[1].split("|")[0]
                if complexo_id not in complexos:
                    complexos[complexo_id] = {"Fitness": 0.0, "Fitdock": str, "HBond": 0.0, "Hbonddock": str, "Vdw": 0.0, "Vdwdock": str}
                complexo_atual = complexos[complexo_id]
                fitness, hbond, vdw = processar_complexo(complexo_id, arquivo_sdf)
                if fitness is not None and fitness > complexo_atual["Fitness"]:
                    complexo_atual["Fitness"] = fitness
                    complexo_atual["Fitdock"] = partes[1]
                if hbond is not None and hbond > complexo_atual["HBond"]:
                    complexo_atual["HBond"] = hbond
                    complexo_atual["Hbonddock"] = partes[1]
                if vdw is not None and vdw > complexo_atual["Vdw"]:
                    complexo_atual["Vdw"] = vdw
                    complexo_atual["Vdwdock"] = partes[1]

    # Escrever os resultados no arquivo de saída
    for complexo_id, valores in complexos.items():
        arquivo_saida.write(complexo_id + "\n")
        for chave, valor in valores.items():
            arquivo_saida.write(f"{chave}:  ")
            arquivo_saida.write(f"{valor}\n")
        arquivo_saida.write("\n\n")