# LARC 2021 - Red Dragons UFSCar
## _Very Small Size Soccer (VSSS)_

Neste repositório encontram-se os códigos-fonte utilizados no ano de 2023, na categoria Very Small Size Soccer (VSSS) em ambiente simulado e físico.

Esta branch possui o código utilizado na LARC 2023, na modalidade física.

# Instalação

Ao clonar esse repositório, instale nossas dependências do python utilizando:

```sh
pip3 install -r requirements.txt
```

A outra parte das dependências é a instalação da biblioteca [vsss_communication](https://github.com/Red-Dragons-UFSCar/vsss_communication). Entre no repositório e siga as instruções de instalação.

Para gerar os arquivos de comunicação entre o código em Python e a ponte em C++, execute no repositório local os seguintes comandos:

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
- ```-c``` ou ```--side```: Define o lado que será jogado (left ou right);
- ```-s``` ou ```--strategy```: Seleciona a estratégia padrão de jogo (twoAttackers ou default);
- ```-op``` ou ```--offensivePenalty```: Seleciona a cobrança de penalti desejada (spin, direct ou switch);
- ```-dp``` ou ```--defensivePenalty```: Seleciona a defesa de penalti desejada (spin, spin-v ou direct);
- ```-aop``` ou ```--adaptativeOffensivePenalty```: Acionamento das cobranças de penaltis adatativas (on ou off);
- ```-adp``` ou ```--adaptativeDefensivePenalty```: Acionamento das defesas de penaltis adatativas (on ou off);

Segue abaixo um exemplo de execução:

```sh
python3 main.py -t blue -c left
```

Vale ressaltar que para essa branch, apenas os dois primeiros parâmetros (team e side) possuem influência no código total, os outros não foram implementados até o momento.

Lembre-se de:
- Verificar o par (IP, PORT) de todos módulos utilizados, Visão e Referee;
- Ter um dispositivo conectado na USB e seu endereço serial inserido adequadamente no código. Ou caso seja apenas um teste, não inicialize a serial.
