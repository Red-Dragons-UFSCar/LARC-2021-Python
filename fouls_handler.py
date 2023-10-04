import importlib
from fouls_foulder import fouls_default # Importa os módulos de cada estratégia

# Função que retorna o módulo de fouls da estratégia selecionada
def FoulsHandler(selectedStrategy): 
    if selectedStrategy == "default": 
        try:
            currentFouls = importlib.import_module('fouls_foulder.fouls_default')
            return currentFouls
        except:
            print("Erro ao importar o módulo de fouls")