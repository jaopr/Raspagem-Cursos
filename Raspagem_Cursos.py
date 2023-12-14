import requests
import pandas as pd

def verifica_links(planilha, resultado_excel):

    df = pd.read_excel(planilha)

    links_funcionando = []
    links_com_conteudo_excluido = []
    links_com_erro = []

    for index, row in df.iterrows():
        link = str(row['Url'])

        try:
            response = requests.get(link)
            if response.status_code == 200:
                if "o conteúdo desta página foi excluído" in response.text.lower():
                    links_com_conteudo_excluido.append(link)
                else:
                    links_funcionando.append(link)
            else:
                links_com_erro.append(link)
        except Exception as e:
            print(f"Erro ao acessar {link}: {e}")
            links_com_erro.append(link)

    max_len = max(len(links_funcionando), len(links_com_conteudo_excluido), len(links_com_erro))

    resultados_df = pd.DataFrame({
        'Links Funcionando': links_funcionando + [''] * (max_len - len(links_funcionando)),
        'Links com Conteúdo Excluído': links_com_conteudo_excluido + [''] * (
                    max_len - len(links_com_conteudo_excluido)),
        'Links com Erro': links_com_erro + [''] * (max_len - len(links_com_erro))
    })

    resultados_df.to_excel(resultado_excel, index=False)

    return links_funcionando, links_com_conteudo_excluido, links_com_erro

links_funcionando, links_com_conteudo_excluido, links_com_erro = verifica_links(
    'C:/Users/joaop/OneDrive/Documentos/CURSOS_em_planilha.xlsx',
    'C:/Users/joaop/OneDrive/Documentos/Resultados.xlsx'
)

print("Links funcionando:")
print(links_funcionando)

print("\nLinks com conteúdo excluído:")
print(links_com_conteudo_excluido)

print("\nLinks com erro:")
print(links_com_erro)
