import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from PIL import Image, ImageTk
import subprocess
import psutil
import threading
import time
import os
import json
import shutil

CONFIG_FILE = "interface_config.json"

class OtimizadorRPG:
    def __init__(self, root):
        self.root = root
        self.root.title("Otimizador RavenQuest")
        self.root.geometry("420x365")  # altura aumentada
        self.root.resizable(False, False)

        self.widget_refs = {}
        self.widget_sizes = {}

        bg_image = Image.open("background.png")
        bg_image = bg_image.resize((420, 365), Image.LANCZOS)  # altura ajustada
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.canvas = tk.Canvas(root, width=420, height=365, highlightthickness=0)  # altura ajustada
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

        # Rodapé centralizado
        self.canvas.create_text(210, 362, text="Criado por SanJéffersonBLK", anchor="s",
                                fill="#FFFDFD", font=("Consolas", 10, "bold"))

        self.btn_jogo = ttk.Button(root, text="Iniciar Jogo", command=self.iniciar_jogo)
        self.btn_launcher = ttk.Button(root, text="Launcher", command=self.iniciar_launcher)
        self.btn_limpar = ttk.Button(root, text="Limpeza", command=self.limpar_temp)

        self.log_box = scrolledtext.ScrolledText(root, height=8, wrap=tk.WORD,
                                                 font=("Consolas", 9), bg="#111122",
                                                 fg="#00ffaa", insertbackground="white")

        self.default_config = {
            "btn_jogo": {"x": 60.0, "y": 145.0, "width": 110, "height": 30},
            "btn_limpar": {"x": 215.0, "y": 145.0, "width": 110, "height": 30},
            "btn_launcher": {"x": 360.0, "y": 145.0, "width": 110, "height": 30},
            "log_box": {"x": 210.0, "y": 250.0, "width": 410, "height": 150},
        }

        widgets = {
            "btn_jogo": self.btn_jogo,
            "btn_launcher": self.btn_launcher,
            "btn_limpar": self.btn_limpar,
            "log_box": self.log_box,
        }

        for name, widget in widgets.items():
            cfg = self.default_config.get(name, {"x": 100, "y": 100, "width": 100, "height": 30})
            win_id = self.canvas.create_window(cfg["x"], cfg["y"], window=widget,
                                               width=cfg["width"], height=cfg["height"])
            self.widget_refs[name] = win_id
            self.widget_sizes[name] = [cfg["width"], cfg["height"]]

        self.load_config()

        self.drag_data = {"item": None, "x": 0, "y": 0}
        self.resize_data = {"item": None, "x": 0, "y": 0, "w": 0, "h": 0}

        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Motion>", self.on_mouse_motion)

        self.monitorar = True
        threading.Thread(target=self.atualizar_monitoramento, daemon=True).start()

    def iniciar_jogo(self):
        self.log("Iniciando o jogo...")
        try:
            subprocess.Popen(["RavenQuest.exe"], creationflags=subprocess.CREATE_NO_WINDOW)
            self.canvas.itemconfig(self.status_label, text="Status: Jogo Iniciado", fill="#00ff88")
        except Exception as e:
            self.canvas.itemconfig(self.status_label, text="Status: Erro ao iniciar o jogo", fill="#ff4444")
            self.log(f"Erro: {e}")

    def iniciar_launcher(self):
        self.log("Iniciando o launcher...")
        try:
            subprocess.Popen(["Launcher.exe"], creationflags=subprocess.CREATE_NO_WINDOW)
            self.canvas.itemconfig(self.status_label, text="Status: Launcher Iniciado", fill="#00ff88")
        except Exception as e:
            self.canvas.itemconfig(self.status_label, text="Status: Erro ao iniciar launcher", fill="#ff4444")
            self.log(f"Erro: {e}")

    def limpar_temp(self):
        self.log("Iniciando limpeza das pastas temporárias...")
        paths_to_clean = []

        temp_env = os.getenv("TEMP")
        tmp_env = os.getenv("TMP")
        system_temp = r"C:\Windows\Temp"
        prefetch = r"C:\Windows\Prefetch"

        for p in [temp_env, tmp_env, system_temp, prefetch]:
            if p and os.path.exists(p) and p not in paths_to_clean:
                paths_to_clean.append(p)

        total_deleted = 0
        errors = 0

        for path in paths_to_clean:
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

    def on_mouse_down(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        for name, win_id in self.widget_refs.items():
            if win_id == item[0]:
                self.drag_data["item"] = name
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
                w, h = self.widget_sizes[name]
                coords = self.canvas.coords(win_id)
                if coords:
                    x, y = coords[0], coords[1]
                    if (x + w - 10) <= event.x <= (x + w) and (y + h - 10) <= event.y <= (y + h):
                        self.resize_data["item"] = name
                        self.resize_data["x"] = event.x
                        self.resize_data["y"] = event.y
                        self.resize_data["w"] = w
                        self.resize_data["h"] = h
                        self.drag_data["item"] = None
                break

    def on_mouse_move(self, event):
        if self.drag_data["item"]:
            name = self.drag_data["item"]
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            coords = self.canvas.coords(self.widget_refs[name])
            if coords:
                new_x = max(0, min(coords[0] + dx, 420))
                new_y = max(0, min(coords[1] + dy, 365))
                self.canvas.coords(self.widget_refs[name], new_x, new_y)
                self.drag_data["x"] = event.x
                self.drag_data["y"] = event.y
        elif self.resize_data["item"]:
            name = self.resize_data["item"]
            dw = event.x - self.resize_data["x"]
            dh = event.y - self.resize_data["y"]
            new_w = max(30, self.resize_data["w"] + dw)
            new_h = max(20, self.resize_data["h"] + dh)
            self.widget_sizes[name] = [new_w, new_h]
            self.canvas.itemconfig(self.widget_refs[name], width=new_w, height=new_h)

    def on_mouse_up(self, event):
        if self.drag_data["item"] is not None or self.resize_data["item"] is not None:
            self.save_config()
        self.drag_data["item"] = None
        self.resize_data["item"] = None

    def on_mouse_motion(self, event):
        for name, win_id in self.widget_refs.items():
            coords = self.canvas.coords(win_id)
            if coords:
                x, y = coords[0], coords[1]
                w, h = self.widget_sizes[name]
                if (x + w - 10) <= event.x <= (x + w) and (y + h - 10) <= event.y <= (y + h):
                    self.canvas.config(cursor="size_nw_se")
                    return
        self.canvas.config(cursor="arrow")

    def save_config(self):
        config = {}
        for name, win_id in self.widget_refs.items():
            coords = self.canvas.coords(win_id)
            w, h = self.widget_sizes[name]
            config[name] = {
                "x": coords[0],
                "y": coords[1],
                "width": int(w),
                "height": int(h)
            }
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f, indent=4)
            self.log("Configuração salva.")
        except Exception as e:
            self.log(f"Erro salvando configuração: {e}")

    def load_config(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                for name, data in config.items():
                    if name in self.widget_refs:
                        self.canvas.coords(self.widget_refs[name], data["x"], data["y"])
                        self.widget_sizes[name] = [data["width"], data["height"]]
                        self.canvas.itemconfig(self.widget_refs[name], width=data["width"], height=data["height"])
                self.log("Layout carregado do arquivo.")
        except Exception as e:
            self.log(f"Erro ao carregar configuração: {e}")

    def encerrar(self):
        self.monitorar = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = OtimizadorRPG(root)
    root.protocol("WM_DELETE_WINDOW", app.encerrar)
    root.mainloop()
