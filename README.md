# LARC 2021 - Red Dragons UFSCar
## _Very Small Size Soccer (VSSS)_

Neste repositório encontra-se o código fonte utilizado na LARC 2021, na categoria Very Small Size Soccer (VSSS) em ambiente simulado online.

# Reconhecimento e créditos

A utilização do código em Python foi possível graças a interface feita pela equipe Yapira, disponível [neste repositório](https://github.com/YapiraUFPR/FIRAClient). 

# Instalação

Primeiramente, para a instalação correta do nosso repositório, é necessário realizar a instalação do [FIRASim](https://github.com/IEEEVSS/FIRASim) e do [VSSReferee](https://github.com/IEEEVSS/VSSReferee), se atentando a todos os seus requisitos.

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

Para executar nosso código, no terminal, você deverá executar o código main.py, passando os parâmetros de time escolhido (*blue* ou *yellow*). Por exemplo:

```sh
python3 main.py blue
```

```sh
python3 main.py yellow
```
