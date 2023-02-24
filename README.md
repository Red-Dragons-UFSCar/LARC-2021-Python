# LARC 2021 - Red Dragons UFSCar
## _Very Small Size Soccer (VSSS)_

Neste repositório encontra-se o código fonte utilizado na LARC 2021, na categoria Very Small Size Soccer (VSSS) em ambiente simulado online.

# Reconhecimento e créditos

A utilização do código em Python foi possível graças a API desenvolvida pela Equipe Yapira, disponível [neste repositório](https://github.com/YapiraUFPR/FIRAClient). 

# Instalação

Primeiramente, para a instalação correta do nosso repositório, é necessário realizar a instalação do [FIRASim](https://github.com/VSSSLeague/FIRASim) e do [VSSReferee](https://github.com/VSSSLeague/VSSReferee), se atentando a todos os seus requisitos.

Você pode conferir o passo-a-passo da instalação [aqui](SETUP.md)

Por seguinte, ao clonar esse repositório, instale nossas dependências do python utilizando:

```sh
pip3 install -r requirements.txt
```

Para gerar os arquivos de comunicação entre o código em Python e o simulador em C++, execute no repositório local os seguintes comandos:

```sh
mkdir build
cd build
qmake ..
make
```

*LEMBRETE:* Todas as vezes que realizar o clone ou gerar uma branch nova a partir da main, realizar esse procedimento de build do repositório.

# Execução

Para executar nosso código no terminal, você deverá executar o código main.py passando a ele alguns parâmetros, os quais são:
- ```-t``` ou ```--team```: Seleciona a cor que será jogada (blue ou yellow);
- ```-s``` ou ```--strategy```: Seleciona a estratégia padrão de jogo (twoAttackers ou default);
- ```-op``` ou ```--offensivePenalty```: Seleciona a cobrança de penalti desejada (spin, direct ou switch);
- ```-dp``` ou ```--defensivePenalty```: Seleciona a defesa de penalti desejada (spin, spin-v ou direct);
- ```-aop``` ou ```--adaptativeOffensivePenalty```: Acionamento das cobranças de penaltis adatativas (on ou off);
- ```-adp``` ou ```--adaptativeDefensivePenalty```: Acionamento das defesas de penaltis adatativas (on ou off);

Segue abaixo um exemplo de execução:

```sh
python3 main.py -t blue -s twoAttackers -op direct -aop on -dp spin -adp off
```

# Executando todos os arquivos

[//]: # (*Precisa ser atualizado para os novos parametros*)

É possível executar todos os arquivos (FIRASim, Referee e códigos) ao mesmo tempo. Para isso é necessário criar um arquivo .py ao lado das pastas instaladas anteriormente com o seguinte código:

```python
import os

def fira():
	cmd_fira = 'gnome-terminal -x sh -c "./FIRASim/bin/FIRASim; bash"'
	print("Abrindo o FIRASim...")
	os.system(cmd_fira)

def referee():
	cmd_ref = 'gnome-terminal -x sh -c "./VSSReferee/bin/VSSReferee --3v3; bash"'
	print("Abrindo o Referee...")
	os.system(cmd_ref)

def codigo(time, estrategia):
	cmd_ref = 'gnome-terminal -x sh -c "cd LARC-2021-Python; python3 main.py'+ ' ' + time + ' ' + estrategia + '; bash"'
	print("Abrindo o CÃ³digo...")
	os.system(cmd_ref)



if __name__ == "__main__":
	codigo('blue','twoAttackers')	
	codigo('yellow','twoAttackers')	
	referee()
	fira()
```
