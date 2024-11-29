# Simulador de Sobrevivência com Q-Learning

Este repositório contém o código para um simulador de sobrevivência que utiliza técnicas de **aprendizado por reforço** para treinar um agente a se alimentar enquanto evita morrer de fome. Foi implementado o algoritmo **Q-Learning**, e os experimentos demonstraram que o agente pode sobreviver por mais de meia hora sem falhar.

## Estrutura do Repositório

- **`jogoInicial.py`**  
  Um jogo single-player no qual o jogador controla a partícula manualmente usando as setas do teclado. A partícula deve se mover pela tela, coletando comida para evitar morrer de fome.  
  - **Regras do jogo:**
    - A partícula começa com 100 pontos de fome, que diminuem ao longo do tempo.
    - Cada partícula de comida coletada aumenta o nível de fome em 20 pontos (até um máximo de 100).
    - A comida aparece em posições aleatórias a cada 2 segundos.
    - Ao sair das bordas da tela, a partícula reaparece no lado oposto.

- **`jogoAutonomo.py`**  
  Introduz o **algoritmo de Q-Learning** com um tabuleiro contínuo. Nesta versão, o agente aprende a se mover autonomamente para buscar comida. No entanto, a partícula se perde.

- **`jogoAutonomoComTabuleiroDiscreto.py`**  
  Também utiliza o **algoritmo de Q-Learning**, mas em um tabuleiro discreto. Aqui, o agente apresenta um comportamento mais satisfatório.

## Requisitos

- Python
- Pygame  
  Instale com:
  ```bash
  pip install pygame
  ```
## Como Executar

1. Para jogar manualmente:

```bash
python jogoInicial.py
```

2. Para testar o algoritmo de Q-Learning:

- Com tabuleiro contínuo:
```bash
python jogoAutonomo.py
```

- Com tabuleiro discreto:
```bash
python jogoAutonomoComTabuleiroDiscreto.py
```

Durante a execução:
- O código realiza primeiro a etapa de treinamento, onde o agente aprende o comportamento ideal.
- Após o treinamento, uma janela é aberta, exibindo o agente se movendo autonomamente durante a fase de teste.

## Vídeos de Demonstração

Aqui estão os vídeos com os resultados:

Teste com jogoAutonomo.py: ?

Teste com jogoAutonomoComTabuleiroDiscreto.py: ?
