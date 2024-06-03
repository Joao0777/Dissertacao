import os

sdf_file_path = "C:/Users/Portilho/Desktop/Selecao_complex_metabos/spreadsheet.sdf"
output_file_path = os.path.join(os.path.dirname(sdf_file_path), 'output.txt')

# Abra o arquivo SDF
with open(sdf_file_path, 'r') as arquivo_sdf, open(output_file_path, 'w') as arquivo_saida:
    complexos = {}
    complexo_atual = None

    # Função para processar informações de um complexo
    def processar_complexo(complexo_id, complexo_dados):
        fitness = None
        hbond = None
        lipo = None
        deltag = None
        for linha in complexo_dados:
            if linha.startswith("> <Gold.Chemscore.Fitness>"):
                fitness = float(next(complexo_dados))
            elif linha.startswith("> <Gold.Chemscore.Hbond>"):
                hbond = float(next(complexo_dados))
            elif linha.startswith("> <Gold.Chemscore.Lipo>"):
                lipo = float(next(complexo_dados))
            elif linha.startswith("> <Gold.Chemscore.DG>"):
                deltag = float(next(complexo_dados))
            elif linha.startswith("$$$$"):
                return (fitness, hbond, lipo, deltag)

    for linha in arquivo_sdf:
        if "|M" in linha:
            # Extrair o número de complexo do identificador
            partes = linha.split("|M")
            if len(partes) >= 2:
                complexo_id = "M" + partes[1].split("|")[0]
                if complexo_id not in complexos:
                    complexos[complexo_id] = {"Fitness": 0.0, "Fitdock": str, "HBond": 0.0, "Hbonddock": str, "lipo": 0.0, "lipodock": str, "deltag": 0.0, "deltagdock": str}
                complexo_atual = complexos[complexo_id]
                fitness, hbond, lipo, deltag = processar_complexo(complexo_id, arquivo_sdf)
                if fitness is not None and fitness > complexo_atual["Fitness"]:
                    complexo_atual["Fitness"] = fitness
                    complexo_atual["Fitdock"] = partes[1]
                if hbond is not None and hbond > complexo_atual["HBond"]:
                    complexo_atual["HBond"] = hbond
                    complexo_atual["Hbonddock"] = partes[1]
                if lipo is not None and lipo > complexo_atual["lipo"]:
                    complexo_atual["lipo"] = lipo
                    complexo_atual["lipodock"] = partes[1]
                if deltag is not None and deltag < complexo_atual["deltag"]:
                    complexo_atual["deltag"] = deltag
                    complexo_atual["deltagdock"] = partes[1]

    # Escrever os resultados no arquivo de saída
    for complexo_id, valores in complexos.items():
        arquivo_saida.write(complexo_id + "\n")
        for chave, valor in valores.items():
            arquivo_saida.write(f"{chave}:  ")
            arquivo_saida.write(f"{valor}\n")
        arquivo_saida.write("\n\n")