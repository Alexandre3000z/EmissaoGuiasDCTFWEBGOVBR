import pandas as pd
from fuzzywuzzy import fuzz

# Carregando a planilha
df = pd.read_excel('dados.xlsx')

def nomeEmpresas():
    empresas_series = df['EMPRESA']
    empresas_array = empresas_series.to_numpy()
    return empresas_array

def nomeMetodo():
    metodo_series = df['Metodo']
    metodo_array = metodo_series.to_numpy()
    return metodo_array

def puxarCnpj():
    metodo_series = df['CNPJ']
    metodo_array = metodo_series.to_numpy()
    return metodo_array


def strings_sao_parecidas(str1, str2, limite_similaridade=70):
    """
    Compara duas strings e retorna True se forem parecidas, False caso contrário.
    A primeira palavra de ambas as strings deve ser igual para serem consideradas parecidas.
    
    :param str1: Primeira string para comparação
    :param str2: Segunda string para comparação
    :param limite_similaridade: Limite percentual de similaridade (padrão: 70)
    :return: True se as strings forem parecidas, False caso contrário
    """
    # Converte as strings para minúsculas
    str1 = str1.lower()
    str2 = str2.lower()
    
    # Verifica se a primeira palavra é igual
    primeira_palavra1 = str1.split()[0] if str1.split() else ""
    primeira_palavra2 = str2.split()[0] if str2.split() else ""
    
    if primeira_palavra1 != primeira_palavra2:
        return False
    
    # Calcula diferentes tipos de similaridade
    ratio = fuzz.ratio(str1, str2)
    partial_ratio = fuzz.partial_ratio(str1, str2)
    token_sort_ratio = fuzz.token_sort_ratio(str1, str2)
    
    # Usa o maior valor entre as diferentes métricas
    max_similarity = max(ratio, partial_ratio, token_sort_ratio)
    
    # Verifica se a string mais curta está contida na mais longa
    if len(str1) > len(str2):
        contains = str2 in str1
    else:
        contains = str1 in str2
    
    # Retorna True se a similaridade for maior ou igual ao limite ou se uma string contém a outra
    return max_similarity >= limite_similaridade or contains
# Obtendo todas as células da coluna 'EMPRESAS' como uma série


# Convertendo para um array numpy, se necessário

print(strings_sao_parecidas("ESPACO VIVER BEM DE MASSOTERAPIA LTDA", "ESPACO VIVER BEM DE MASSO..."))  # Deve retornar True

# print(empresas_array,metodo_array )