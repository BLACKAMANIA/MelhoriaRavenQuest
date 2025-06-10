import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
from PIL import Image, ImageTk
import subprocess
import psutil
import threading
import time
import os
import json
import shutil

CONFIG_FILE = "interface_config.json"
CAMINHO_PADRAO_JOGO = r"C:\\Program Files (x86)\\Tavernlight Games\\RavenQuest\\ravenquest_dx_BE.exe"
CAMINHO_PADRAO_LAUNCHER = r"C:\\Program Files (x86)\\Tavernlight Games\\RavenQuest Launcher\\launcher.exe"

class OtimizadorRPG:
    def __init__(self, root):
        self.root = root
        self.root.title("Otimizador RavenQuest")
        self.root.geometry("420x365")
        self.root.resizable(False, False)

        self.caminho_jogo = CAMINHO_PADRAO_JOGO
        self.caminho_launcher = CAMINHO_PADRAO_LAUNCHER

        bg_image = Image.open("background.png").resize((420, 365), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(root, width=420, height=365, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Consolas", 10, "bold"), padding=6,
                        background="#222244", foreground="#00ffff", relief="flat")
        style.map("TButton",
                  background=[("active", "#00aaff")],
                  foreground=[("active", "white")])

        self.status_label = self.canvas.create_text(12, 15, text="Status: Aguardando...",
                                                    fill="#00ffcc", anchor="nw", font=("Arial", 12, "bold"))
        self.cpu_label = self.canvas.create_text(12, 40, text="CPU Jogo: ---",
                                                 fill="#3399ff", anchor="nw", font=("Arial", 12, "bold"))

        self.canvas.create_text(210, 362, text="Criado por SanJéffersonBLK", anchor="s",
                                fill="#FFFDFD", font=("Consolas", 10, "bold"))

        self.btn_jogo = ttk.Button(root, text="Iniciar Jogo", command=self.iniciar_jogo)
        self.btn_launcher = ttk.Button(root, text="Launcher", command=self.iniciar_launcher)
        self.btn_caminho = ttk.Button(root, text="Selecionar Jogo", command=self.selecionar_jogo)
        self.btn_limpar = ttk.Button(root, text="Limpeza", command=self.limpar_temp)

        self.log_box = scrolledtext.ScrolledText(root, height=8, wrap=tk.WORD,
                                                 font=("Consolas", 9), bg="#111122",
                                                 fg="#00ffaa", insertbackground="white")

        self.canvas.create_window(60, 145, window=self.btn_jogo, width=110, height=30)
        self.canvas.create_window(215, 145, window=self.btn_limpar, width=110, height=30)
        self.canvas.create_window(360, 145, window=self.btn_launcher, width=110, height=30)
        self.canvas.create_window(360, 190, window=self.btn_caminho, width=110, height=30)
        self.canvas.create_window(210, 250, window=self.log_box, width=410, height=150)

        self.monitorar = True
        threading.Thread(target=self.atualizar_monitoramento, daemon=True).start()

    def iniciar_jogo(self):
        self.log("Iniciando o jogo, Aguarde o 'JOGO ESTA INICIANDO'...")
        if os.path.isfile(self.caminho_jogo):
            try:
                subprocess.Popen([self.caminho_jogo], creationflags=subprocess.CREATE_NO_WINDOW)
                self.canvas.itemconfig(self.status_label, text="Status: Jogo Iniciado", fill="#00ff88")
            except Exception as e:
                self.canvas.itemconfig(self.status_label, text="Status: Erro ao iniciar o jogo", fill="#ff4444")
                self.log(f"Erro: {e}")
        else:
            self.canvas.itemconfig(self.status_label, text="Status: Caminho do jogo não encontrado", fill="#ff4444")
            self.log(f"Arquivo não encontrado: {self.caminho_jogo}")

    def iniciar_launcher(self):
        self.log("Iniciando o launcher...")
        if os.path.isfile(self.caminho_launcher):
            try:
                subprocess.Popen([self.caminho_launcher], creationflags=subprocess.CREATE_NO_WINDOW)
                self.canvas.itemconfig(self.status_label, text="Status: Launcher Iniciado", fill="#00ff88")
            except Exception as e:
                self.canvas.itemconfig(self.status_label, text="Status: Erro ao iniciar launcher", fill="#ff4444")
                self.log(f"Erro: {e}")
        else:
            self.canvas.itemconfig(self.status_label, text="Status: Caminho do launcher não encontrado", fill="#ff4444")
            self.log(f"Launcher não encontrado: {self.caminho_launcher}")

    def selecionar_jogo(self):
        caminho = filedialog.askopenfilename(title="Selecione o executável do jogo",
                                             filetypes=[("Executável do Jogo", "*.exe")])
        if caminho:
            self.caminho_jogo = caminho
            self.log(f"Novo caminho do jogo definido: {caminho}")

    def limpar_temp(self):
        self.log("Iniciando limpeza das pastas temporárias...")
        paths = [os.getenv("TEMP"), os.getenv("TMP"), r"C:\\Windows\\Temp", r"C:\\Windows\\Prefetch"]
        total_deleted = 0
        errors = 0

        for path in paths:
            if path and os.path.exists(path):
                self.log(f"Limpando: {path}")
                try:
                    for filename in os.listdir(path):
                        file_path = os.path.join(path, filename)
                        try:
                            if os.path.isfile(file_path) or os.path.islink(file_path):
                                os.remove(file_path)
                                total_deleted += 1
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                                total_deleted += 1
                        except Exception as e:
                            self.log(f"Erro removendo {file_path}: {e}")
                            errors += 1
                except Exception as e:
                    self.log(f"Erro acessando {path}: {e}")
                    errors += 1

        self.log(f"Limpeza concluída: {total_deleted} itens removidos, {errors} erros.")

    def atualizar_monitoramento(self):
        while self.monitorar:
            self.atualizar_uso_cpu()
            time.sleep(2)

    def atualizar_uso_cpu(self):
        for proc in psutil.process_iter(['name', 'cpu_percent']):
            try:
                if "RavenQuest" in proc.info['name']:
                    uso_cpu = proc.cpu_percent(interval=1)
                    self.canvas.itemconfig(self.cpu_label, text=f"CPU Jogo: {uso_cpu:.1f}%")
                    return
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        self.canvas.itemconfig(self.cpu_label, text="CPU Jogo: ---")

    def log(self, msg):
        self.log_box.insert(tk.END, f"> {msg}\n")
        self.log_box.see(tk.END)

    def encerrar(self):
        self.monitorar = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = OtimizadorRPG(root)
    root.protocol("WM_DELETE_WINDOW", app.encerrar)
    root.mainloop()
