import requests
import time
from datetime import datetime
import pytz

# ================= CONFIGURAÇÃO =================

BOT_TOKEN = "7977219722:AAGbvzzzmrmFHdOWBgZc-BQFBPjDkKNgbYU"
CHAT_ID = "6432086674"

URL_VFS = "https://visa.vfsglobal.com/ago/pt/prt/"

CHECK_INTERVAL = 180  # Verificação a cada 3 minutos

# Estados anteriores
last_status_nacional = None
last_status_schengen = None

# ================= FUNÇÕES =================

def hora_angola():
    tz = pytz.timezone("Africa/Luanda")
    return datetime.now(tz).strftime("%d/%m/%Y %H:%M:%S")

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": texto,
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print("Erro ao enviar mensagem:", e)

def verificar_vfs():
    global last_status_nacional, last_status_schengen
    try:
        response = requests.get(URL_VFS, timeout=15)
        conteudo = response.text.lower()

        # ----- VISTO NACIONAL -----
        nacional_aberto = "nacional" in conteudo and "appointment" in conteudo
        if nacional_aberto != last_status_nacional:
            last_status_nacional = nacional_aberto
            if nacional_aberto:
                enviar_mensagem(
                    f"🚨 VAGA ABERTA – VFS PORTUGAL 🇵🇹\n\n"
                    f"📌 Tipo: Visto Nacional\n"
                    f"🕒 Hora (Angola): {hora_angola()}\n"
                    f"🔗 Link direto:\n{URL_VFS}\n\n"
                    f"⚠️ Corra! As vagas fecham rápido."
                )

        # ----- VISTO SCHENGEN -----
        schengen_aberto = "schengen" in conteudo and "appointment" in conteudo
        if schengen_aberto != last_status_schengen:
            last_status_schengen = schengen_aberto
            if schengen_aberto:
                enviar_mensagem(
                    f"🚨 VAGA ABERTA – VFS PORTUGAL 🇪🇺\n\n"
                    f"📌 Tipo: Visto Schengen\n"
                    f"🕒 Hora (Angola): {hora_angola()}\n"
                    f"🔗 Link direto:\n{URL_VFS}\n\n"
                    f"⚠️ Entre imediatamente."
                )

    except Exception as e:
        print("Erro ao verificar VFS:", e)

# ================= LOOP 24H =================

if __name__ == "__main__":
    enviar_mensagem("🤖 Bot VFS Portugal iniciado.\nMonitoramento ativo 24h.")
    while True:
        verificar_vfs()
        time.sleep(CHECK_INTERVAL)