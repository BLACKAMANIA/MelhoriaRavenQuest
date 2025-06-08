import psutil
import time

# Processos a monitorar
processos_alvo = ["launcher.exe", "ravenquest_dx_BE.exe", "BattlEye"]

def monitorar_processos():
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        if proc.info['name'] in processos_alvo:
            print(f"[{proc.info['name']}] PID: {proc.info['pid']} | CPU: {proc.info['cpu_percent']}%")
            if proc.info['cpu_percent'] > 40:
                print("⚠️ Processo consumindo muito recurso!")

monitorar_processos()
