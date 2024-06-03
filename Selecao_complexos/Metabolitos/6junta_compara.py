def main():
    # Diretório onde estão os arquivos de entrada e onde será salvo o arquivo de saída
    diretorio = 'C:/Users/Portilho/Desktop/Docking_certo/Resultados/Results_Docking/4AGS/sitio_2/Metabolitos/1b_G1/'

    # Ler o arquivo Contatos.txt
    with open(diretorio + 'Contatos.txt', 'r') as contatos_file:
        resultados_contatos = contatos_file.read().strip().split('='*120)
    
    # Ler o arquivo PontesH.txt
    with open(diretorio + 'PontesH.txt', 'r') as pontesh_file:
        resultados_pontesh = pontesh_file.read().strip().split('='*120)

    # Criar o arquivo de saída
    with open(diretorio + 'result.txt', 'w') as saida_file:
        for contatos_result in resultados_contatos:
            lines_contatos = contatos_result.strip().split('\n')
            caminho_contatos = lines_contatos[0].replace("\\output\\resultado.txt", "")

            sessoes_contatos = [lines_contatos[i:i+4] for i in range(2, len(lines_contatos), 5)]

            pontesh_result = None
            for result in resultados_pontesh:
                if caminho_contatos in result:
                    pontesh_result = result
                    break
            
            if pontesh_result:
                lines_pontesh = pontesh_result.strip().split('\n')
                caminho_pontesh = lines_pontesh[0]

                if len(lines_pontesh) >= 2:
                    informacao_geral_pontesh = lines_pontesh[1]
                else:
                    informacao_geral_pontesh = ""

                sessoes_pontesh = [lines_pontesh[i:i+3] for i in range(4, len(lines_pontesh), 4)]

                saida_file.write(caminho_pontesh + '\n')
                saida_file.write(informacao_geral_pontesh + '\n\n')

                for i in range(len(sessoes_contatos)):
                    saida_file.write('\n'.join(sessoes_contatos[i]) + '\n')
                    saida_file.write('\n'.join(sessoes_pontesh[i]) + '\n\n')

                saida_file.write('='*120 + '\n')

if __name__ == "__main__":
    main()
