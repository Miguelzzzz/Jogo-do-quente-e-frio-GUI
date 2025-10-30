import tkinter as tk
from tkinter import ttk, messagebox
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Game.game_logic import Game

sns.set(style="whitegrid")

class HotColdApp(tk.Tk):
    """Interface grafica do jogo."""

    def __init__(self):
        super().__init__()
        self.title("Jogo do Quente ou Frio – Fase 2")
        self.geometry("1000x620")
        self.resizable(False, False)

        self.game: Game | None = None 
        self.buildStartScreen()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def buildStartScreen(self):
        self.clear()
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Quente ou Frio", font=("Segoe UI", 26, "bold")).pack(pady=10)
        ttk.Label(frame, text="Versão Gráfica", font=("Segoe UI", 10)).pack(pady=(0, 15))

        ttk.Label(frame, text="Digite seu nome:").pack(pady=5)
        self.nameVar = tk.StringVar()
        ttk.Entry(frame, textvariable=self.nameVar, width=30).pack()

        ttk.Button(frame, text="Iniciar", command=self.openDifficultyScreen).pack(pady=20)

    def openDifficultyScreen(self):
        name = self.nameVar.get().strip() or "Jogador"
        self.clear()

        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True)
        ttk.Label(frame, text=f"Olá, {name}!", font=("Segoe UI", 14)).pack(pady=10)
        ttk.Label(frame, text="Escolha quantos digitos terá o numero misterioso:").pack(pady=8)

        self.digitsVar = tk.IntVar(value=1)
        ttk.Spinbox(frame, from_=1, to=8, textvariable=self.digitsVar, width=5).pack(pady=5)

        ttk.Button(frame, text="Começar Jogo", command=lambda: self.startGame(name)).pack(pady=15)
        ttk.Button(frame, text="Voltar", command=self.buildStartScreen).pack(pady=5)

    def startGame(self, name):
        digits = int(self.digitsVar.get())
        self.game = Game(name, digits)
        self.buildGameScreen()

    def buildGameScreen(self):
        self.clear()
        g = self.game
        frame = ttk.Frame(self, padding=15)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text=f"Adivinhe o numero ({g.minimum}–{g.maximum})", font=("Segoe UI", 14)).pack(pady=10)
        self.feedbackVar = tk.StringVar(value="O numero foi gerado! Tente adivinhar.")
        ttk.Label(frame, textvariable=self.feedbackVar).pack(pady=5)

        entryFrame = ttk.Frame(frame)
        entryFrame.pack(pady=10)
        ttk.Label(entryFrame, text="Seu chute:").pack(side="left", padx=5)
        self.guessVar = tk.StringVar()
        entry = ttk.Entry(entryFrame, textvariable=self.guessVar, width=10)
        entry.pack(side="left")
        entry.bind("<Return>", lambda e: self.submitGuess())
        entry.focus()

        ttk.Button(frame, text="Enviar", command=self.submitGuess).pack(pady=10)

        self.logBox = tk.Text(frame, width=50, height=8, state="disabled")
        self.logBox.pack(pady=10)

        ttk.Button(frame, text="Desistir", command=self.giveUp).pack(pady=5)
        ttk.Button(frame, text="Voltar ao inicio", command=self.buildStartScreen).pack(pady=5)

    def submitGuess(self):
        g = self.game
        try:
            value = int(self.guessVar.get())
        except ValueError:
            messagebox.showerror("Erro", "Digite um numero inteiro.")
            return

        if not (g.minimum <= value <= g.maximum):
            messagebox.showerror("Fora do intervalo", f"Digite entre {g.minimum} e {g.maximum}.")
            return

        result = g.guess(value)
        self.logAttempt(value)

        if result == "acertou":
            self.buildResultScreen()
        elif result == "menor":
            self.feedbackVar.set("O numero jogado é menor que o misterioso.")
        else:
            self.feedbackVar.set("O numero jogado é maior que o misterioso.")
        self.guessVar.set("")

    def logAttempt(self, value):
        g = self.game
        self.logBox.configure(state="normal")
        self.logBox.insert("end", f"Tentativa {g.counter}: {value}\n")
        self.logBox.configure(state="disabled")
        self.logBox.see("end")

    def giveUp(self):
        if messagebox.askyesno("Desistir", "Deseja revelar o número misterioso?"):
            self.buildResultScreen(revealed=True)

    def buildResultScreen(self, revealed=False):
        self.clear()
        g = self.game
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True, fill="both")

        title = "Numero Revelado" if revealed else "Parabéns, Você acertou!"
        ttk.Label(frame, text=title, font=("Segoe UI", 18, "bold")).pack(pady=10)
        ttk.Label(frame, text=f"Numero misterioso: {g.mysteriousNumber}", font=("Segoe UI", 12)).pack()
        ttk.Label(frame, text=f"Tentativas: {g.counter}", font=("Segoe UI", 12)).pack(pady=5)
        ttk.Label(frame, text=f"Jogador: {g.playerName}", font=("Segoe UI", 10)).pack(pady=5)

        buttonFrame = ttk.Frame(frame)
        buttonFrame.pack(pady=10)

        ttk.Button(buttonFrame, text="Jogar novamente", command=self.restart).pack(side="left", padx=5)
        ttk.Button(buttonFrame, text="Sair", command=self.exit).pack(side="left", padx=5)

        if g.attempts:
            xs = [a[0] for a in g.attempts]
            ys = [a[1] for a in g.attempts]

            fig, ax = plt.subplots(figsize=(9, 4), dpi=100)
            ax.set_title("Desempenho das Jogadas")
            ax.set_xlabel("Tentativa")
            ax.set_ylabel("Valor chutado")

            sns.lineplot(x=xs, y=ys, ax=ax, marker="o")
            ax.axhline(g.mysteriousNumber, ls="--", label="Numero Misterioso")
            ax.legend()

            fig.tight_layout() 

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.get_tk_widget().pack(pady=8)
            canvas.draw()

        else:
            ttk.Label(frame, text="Nenhuma jogada registrada.").pack(pady=10)

    def restart(self):
        if messagebox.askyesno("Reiniciar", "Deseja jogar novamente?"):
            self.buildStartScreen()

    def exit(self):
        messagebox.showinfo("Até logo", "Obrigado por jogar!")
        self.destroy()