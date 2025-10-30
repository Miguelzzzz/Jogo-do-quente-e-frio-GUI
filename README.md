# 🧩 Exercício — Jogo do Quente ou Frio, Fase 2 (Python).

Versão ampliada do jogo **“Quente ou Frio”**, agora com **interface gráfica** e **análise visual das jogadas** em Python.

## 🎯 Objetivo

Desenvolver uma versão gráfica interativa do jogo “Quente ou Frio”, com janelas de interação, controle de fluxo e um **gráfico de desempenho** exibindo as jogadas realizadas.

## 🧠 Requisitos e Funcionalidades

1. **Tela de abertura**  
   - Exibe o nome do jogo e um botão **“Iniciar”**.  
   - Pode conter o nome do jogador e uma mensagem de boas-vindas.

2. **Escolha da dificuldade**  
   - O jogador escolhe **quantos dígitos** terá o número misterioso (1, 2, 3, 4...).  
   - O programa gera o número aleatoriamente conforme a escolha:  
     - 1 dígito → `0 a 9`  
     - 2 dígitos → `10 a 99`  
     - 3 dígitos → `100 a 999`  
     - 4 dígitos → `1000 a 9999`  
     - ... e assim por diante.

3. **Tela de jogo – Adivinhações**  
   - Permite que o jogador digite seus palpites e envie o valor por meio de um botão.  
   - Após cada tentativa, o programa exibe uma mensagem indicando se o palpite é **maior** ou **menor** que o número misterioso.  
   - O jogo continua até o jogador acertar.

4. **Registro das jogadas**  
   - Cada jogada é registrada em uma lista com duas informações:  
     - **Número da tentativa**  
     - **Valor chutado pelo jogador**

5. **Tela de resultado – Parabéns, você acertou!**  
   - Ao acertar, o jogo exibe:  
     - O **número misterioso**  
     - O **total de tentativas realizadas**  
     - Uma **mensagem de parabéns** com o nome do jogador  

6. **Gráfico de desempenho**  
   - Exibe um gráfico mostrando as jogadas realizadas:  
     - **Eixo X:** número da jogada  
     - **Eixo Y:** valor chutado  
   - Cada ponto representa uma tentativa (`x = jogada`, `y = valor chutado`).  
   - O gráfico deve ser gerado com a biblioteca **Seaborn** (ou **matplotlib**).  

7. **Tela final – Jogar novamente**  
   - Após o gráfico, o jogo pergunta:  
     > Quer jogar de novo?  
   - Se o jogador escolher **“Sim”**, o jogo reinicia desde a tela de abertura.  
   - Se escolher **“Não”**, o programa exibe uma mensagem de despedida e encerra.

## ⚙️ Especificações Técnicas

**Arquivo principal:** `hot_cold_gui.py`

**Descrição:**  
Versão gráfica do jogo “Quente ou Frio” com:
- Telas: inicial, escolha de dígitos, jogo e resultado  
- Registro de jogadas (`[número_tentativa, valor_chutado]`)  
- Gráfico de desempenho usando **Seaborn/Matplotlib** integrado ao **Tkinter**  
- Opção de jogar novamente  

**Dependências:**
- Python **3.8+**  
- `tkinter` *(nativo do Python)*  
- `matplotlib`  
- `seaborn`  

**Instalação (exemplo):**
   > pip install matplotlib seaborn

## 🖼️ Fluxo da Interface

1. Tela inicial → título e botão **Iniciar**  
2. Tela de escolha → número de dígitos  
3. Tela de jogo → campo para palpites e mensagens de dica  
4. Tela de resultado → acerto, tentativas e gráfico  
5. Tela final → opção para **jogar novamente** ou **sair**