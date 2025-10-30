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
        self._build_start_screen()

    def _clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _build_start_screen(self):
        self._clear()
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Quente ou Frio", font=("Segoe UI", 26, "bold")).pack(pady=10)
        ttk.Label(frame, text="Versão Gráfica", font=("Segoe UI", 10)).pack(pady=(0, 15))

        ttk.Label(frame, text="Digite seu nome:").pack(pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.name_var, width=30).pack()

        ttk.Button(frame, text="Iniciar", command=self._open_difficulty_screen).pack(pady=20)

    def _open_difficulty_screen(self):
        name = self.name_var.get().strip() or "Jogador"
        self._clear()

        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True)
        ttk.Label(frame, text=f"Olá, {name}!", font=("Segoe UI", 14)).pack(pady=10)
        ttk.Label(frame, text="Escolha quantos digitos terá o numero misterioso:").pack(pady=8)

        self.digits_var = tk.IntVar(value=1)
        ttk.Spinbox(frame, from_=1, to=8, textvariable=self.digits_var, width=5).pack(pady=5)

        ttk.Button(frame, text="Começar Jogo", command=lambda: self._start_game(name)).pack(pady=15)
        ttk.Button(frame, text="Voltar", command=self._build_start_screen).pack(pady=5)

    def _start_game(self, name):
        digits = int(self.digits_var.get())
        self.game = Game(name, digits)
        self._build_game_screen()

    def _build_game_screen(self):
        self._clear()
        g = self.game
        frame = ttk.Frame(self, padding=15)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text=f"Adivinhe o numero ({g.minimum}–{g.maximum})", font=("Segoe UI", 14)).pack(pady=10)
        self.feedback_var = tk.StringVar(value="O numero foi gerado! Tente adivinhar.")
        ttk.Label(frame, textvariable=self.feedback_var).pack(pady=5)

        entry_frame = ttk.Frame(frame)
        entry_frame.pack(pady=10)
        ttk.Label(entry_frame, text="Seu chute:").pack(side="left", padx=5)
        self.guess_var = tk.StringVar()
        entry = ttk.Entry(entry_frame, textvariable=self.guess_var, width=10)
        entry.pack(side="left")
        entry.bind("<Return>", lambda e: self._submit_guess())
        entry.focus()

        ttk.Button(frame, text="Enviar", command=self._submit_guess).pack(pady=10)

        self.log_box = tk.Text(frame, width=50, height=8, state="disabled")
        self.log_box.pack(pady=10)

        ttk.Button(frame, text="Desistir", command=self._give_up).pack(pady=5)
        ttk.Button(frame, text="Voltar ao inicio", command=self._build_start_screen).pack(pady=5)

    def _submit_guess(self):
        g = self.game
        try:
            value = int(self.guess_var.get())
        except ValueError:
            messagebox.showerror("Erro", "Digite um numero inteiro.")
            return

        if not (g.minimum <= value <= g.maximum):
            messagebox.showerror("Fora do intervalo", f"Digite entre {g.minimum} e {g.maximum}.")
            return

        result = g.guess(value)
        self._log_attempt(value)

        if result == "acertou":
            self._build_result_screen()
        elif result == "menor":
            self.feedback_var.set("O numero jogado é menor que o misterioso.")
        else:
            self.feedback_var.set("O numero jogado é maior que o misterioso.")
        self.guess_var.set("")

    def _log_attempt(self, value):
        g = self.game
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"Tentativa {g.counter}: {value}\n")
        self.log_box.configure(state="disabled")
        self.log_box.see("end")

    def _give_up(self):
        if messagebox.askyesno("Desistir", "Deseja revelar o número misterioso?"):
            self._build_result_screen(revealed=True)

    def _build_result_screen(self, revealed=False):
        self._clear()
        g = self.game
        frame = ttk.Frame(self, padding=20)
        frame.pack(expand=True, fill="both")

        title = "Numero Revelado" if revealed else "Parabéns, Você acertou!"
        ttk.Label(frame, text=title, font=("Segoe UI", 18, "bold")).pack(pady=10)
        ttk.Label(frame, text=f"Numero misterioso: {g.mysterious_number}", font=("Segoe UI", 12)).pack()
        ttk.Label(frame, text=f"Tentativas: {g.counter}", font=("Segoe UI", 12)).pack(pady=5)
        ttk.Label(frame, text=f"Jogador: {g.player_name}", font=("Segoe UI", 10)).pack(pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Jogar novamente", command=self._restart).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Sair", command=self._exit).pack(side="left", padx=5)

        if g.attempts:
            xs = [a[0] for a in g.attempts]
            ys = [a[1] for a in g.attempts]

            fig, ax = plt.subplots(figsize=(8, 4), dpi=100)
            ax.set_title("Desempenho das Jogadas")
            ax.set_xlabel("Tentativa")
            ax.set_ylabel("Valor chutado")

            sns.lineplot(x=xs, y=ys, ax=ax, marker="o")
            ax.axhline(g.mysterious_number, ls="--", label="Numero Misterioso")
            ax.legend()

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.get_tk_widget().pack(pady=8)
            canvas.draw()
        else:
            ttk.Label(frame, text="Nenhuma jogada registrada.").pack(pady=10)

    def _restart(self):
        if messagebox.askyesno("Reiniciar", "Deseja jogar novamente?"):
            self._build_start_screen()

    def _exit(self):
        messagebox.showinfo("Até logo", "Obrigado por jogar!")
        self.destroy()