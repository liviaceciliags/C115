import socket
import json
import threading

HOST = "0.0.0.0"
PORT = 50007

QUESTIONS = [
    {
        "pergunta": "Qual é a capital da Itália?",
        "opcoes": ["Roma", "Paris", "Lisboa", "Londres"],
        "correta": "A",  
    },
    {
        "pergunta": "Qual protocolo é comumente usado em APIs REST?",
        "opcoes": ["SMTP", "FTP", "HTTP/HTTPS", "SSH"],
        "correta": "C", 
    },
]

def send_json(conn, obj):
    data = (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8")
    conn.sendall(data)

def recv_json(conn):
    buff = b""
    while True:
        chunk = conn.recv(4096)
        if not chunk:
            return None
        buff += chunk
        if b"\n" in buff:
            line, buff = buff.split(b"\n", 1)
            try:
                return json.loads(line.decode("utf-8"))
            except json.JSONDecodeError:
                return None

def handle_client(conn, addr):
    try:
        respostas = []
        for idx, q in enumerate(QUESTIONS, start=1):
            payload = {
                "tipo": "pergunta",
                "indice": idx,
                "pergunta": q["pergunta"],
                "opcoes": {
                    "A": q["opcoes"][0],
                    "B": q["opcoes"][1],
                    "C": q["opcoes"][2],
                    "D": q["opcoes"][3],
                },
                "instrucoes": "Responda com A, B, C ou D.",
            }
            send_json(conn, payload)

            msg = recv_json(conn)
            if not msg or msg.get("tipo") != "resposta" or msg.get("indice") != idx:
                send_json(conn, {"tipo": "erro", "mensagem": "Resposta inválida."})
                return

            resp = str(msg.get("resposta", "")).strip().upper()
            if resp not in {"A", "B", "C", "D"}:
                send_json(conn, {"tipo": "erro", "mensagem": "Alternativa inválida."})
                return

            respostas.append(resp)

        acertos = 0
        detalhado = []
        for i, (q, r) in enumerate(zip(QUESTIONS, respostas), start=1):
            ok = (r == q["correta"])
            if ok:
                acertos += 1
            detalhado.append({
                "questao": i,
                "sua_resposta": r,
                "correta": q["correta"],
                "resultado": "acertou" if ok else "errou"
            })

        resultado = {
            "tipo": "resultado",
            "total_questoes": len(QUESTIONS),
            "acertos": acertos,
            "detalhado": detalhado
        }
        send_json(conn, resultado)
    finally:
        conn.close()

def main():
    print(f"Servidor ouvindo em {HOST}:{PORT} ...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            print("Cliente conectado:", addr)
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
