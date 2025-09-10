import socket
import json

HOST = "127.0.0.1"  
PORT = 50007

def send_json(sock, obj):
    data = (json.dumps(obj, ensure_ascii=False) + "\n").encode("utf-8")
    sock.sendall(data)

def recv_json(sock):
    buff = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            return None
        buff += chunk
        if b"\n" in buff:
            line, buff = buff.split(b"\n", 1)
            try:
                return json.loads(line.decode("utf-8"))
            except json.JSONDecodeError:
                return None

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Conectado ao servidor.\n")

        while True:
            msg = recv_json(s)
            if not msg:
                print("Conexão encerrada.")
                break

            tipo = msg.get("tipo")

            if tipo == "pergunta":
                idx = msg["indice"]
                print(f"Questão {idx}: {msg['pergunta']}")
                for k, v in msg["opcoes"].items():
                    print(f"  {k}) {v}")
                ans = input("Sua resposta (A/B/C/D): ").strip().upper()
                send_json(s, {"tipo": "resposta", "indice": idx, "resposta": ans})
                print()

            elif tipo == "resultado":
                print("=== Resultado ===")
                print(f"Acertos: {msg['acertos']} / {msg['total_questoes']}")
                for item in msg["detalhado"]:
                    print(f"Q{item['questao']}: você {item['resultado']} "
                          f"(sua: {item['sua_resposta']} / correta: {item['correta']})")
                print("\nFim.\n")
                break

            elif tipo == "erro":
                print("Erro do servidor:", msg.get("mensagem"))
                break

if __name__ == "__main__":
    main()
