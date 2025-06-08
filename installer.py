import os
import subprocess
import sys
import tkinter as tk
from tkinter import scrolledtext

class Installer:
def __init__(self, master):
self.master = master
self.master.title("Instalador de Dependências")
self.text_area = scrolledtext.ScrolledText(master, width=80, height=20)
self.text_area.pack()

self.check_requirements()

def check_requirements(self):
try:
# Supondo que 'requirements.txt' esteja na mesma pasta do script.
with open('requirements.txt') as f:
requirements = f.readlines()

for requirement in requirements:
requirement = requirement.strip()
self.text_area.insert(tk.END, f"Instalando {requirement}...\n")
self.master.update() # Atualiza a interface gráfica

# Comando para instalar pacotes
subprocess.check_call([sys.executable, '-m', 'pip', 'install', requirement])
self.text_area.insert(tk.END, f"{requirement} instalado com sucesso.\n")

except Exception as e:
self.text_area.insert(tk.END, f"Erro: {str(e)}\n")

if __name__ == "__main__":
root = tk.Tk()
app = Installer(root)
root.mainloop()