import importlib
from fouls_foulder import fouls_wallDeffenseDefault, fouls_blockingWallDeffense, fouls_default5v5 # Importa os módulos de cada estratégia

# Função que retorna o módulo de fouls da estratégia selecionada
def FoulsHandler(selectedStrategy): 
    if selectedStrategy == "wallDeffenseDefault": 
        try:
            currentFouls = importlib.import_module('fouls_foulder.fouls_wallDeffenseDefault')
            return currentFouls
        except:
            print("Erro ao importar o módulo de fouls")
    elif selectedStrategy == "blockingWallDeffense":
        try:
            currentFouls = importlib.import_module('fouls_foulder.fouls_blockingWallDeffense')
            return currentFouls
        except:
            print("Erro ao importar o módulo de fouls")
    elif selectedStrategy == "default5v5":
        try:
            currentFouls = importlib.import_module('fouls_foulder.fouls_default5v5')
            return currentFouls
        except:
            print("Erro ao importar o módulo de fouls")
    elif selectedStrategy == "tripleAttack":
        try:
            currentFouls = importlib.import_module('fouls_foulder.fouls_wallDeffenseDefault')
            return currentFouls
        except:
            print("Erro ao importar o módulo de fouls")