import random

class Game:
    """Classe responsavel pela logica do jogo."""

    def __init__(self, playerName="Jogador", digits=1):
        self.playerName = playerName
        self.digits = digits
        self.minimum = 10 ** (digits - 1) if digits > 1 else 0
        self.maximum = (10 ** digits) - 1
        self.mysteriousNumber = random.randint(self.minimum, self.maximum)
        self.attempts = [] 
        self.counter = 0

    def guess(self, value: int):
        """Recebe um chute e retorna o resultado."""
        self.counter += 1
        self.attempts.append([self.counter, value])

        if value == self.mysteriousNumber:
            return "acertou"
        elif value < self.mysteriousNumber:
            return "menor"
        else:
            return "maior"

    def reset(self, digits: int = None):
        """Reinicia o jogo com nova quantidade de digitos."""
        if digits is not None: 
            self.digits = digits
        self.minimum = 10 ** (self.digits - 1) if self.digits > 1 else 0
        self.maximum = (10 ** self.digits) - 1
        self.mysteriousNumber = random.randint(self.minimum, self.maximum)
        self.attempts = []
        self.counter = 0