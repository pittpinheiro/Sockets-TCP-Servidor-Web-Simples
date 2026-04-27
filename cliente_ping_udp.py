import socket
import time

def iniciar_cliente():
    # Cria socket UDP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Requisito: Aguardar até 1 segundo por resposta
    client_socket.settimeout(1.0)
    
    servidor = ('127.0.0.1', 12000)
    tempos_rtt = []
    perdidos = 0

    print("[*] Iniciando experimento: Enviando 10 pings UDP...\n")

    # Requisito: Enviar exatamente 10 mensagens
    for i in range(1, 11):
        envio = time.time()
        mensagem = f"ping {i} {envio}"
        
        try:
            client_socket.sendto(mensagem.encode(), servidor)
            
            # Tenta receber a resposta
            data, addr = client_socket.recvfrom(1024)
            chegada = time.time()
            
            # Requisito: Calcular RTT
            rtt = (chegada - envio) * 1000
            tempos_rtt.append(rtt)
            print(f"Resposta de {addr}: {data.decode()} | RTT: {rtt:.2f}ms")
            
        except socket.timeout:
            # Requisito: Indicar perdas
            perdidos += 1
            print(f"Solicitação {i}: Esgotado o tempo de espera.")

    # --- Extensão Obrigatória: Estatísticas ---
    total = 10
    taxa_perda = (perdidos / total) * 100
    rtt_medio = sum(tempos_rtt) / len(tempos_rtt) if tempos_rtt else 0

    print("\n" + "="*40)
    print("      RELATÓRIO FINAL DO EXPERIMENTO")
    print("="*40)
    print(f"Pacotes Enviados: {total}")
    print(f"Pacotes Recebidos: {total - perdidos}")
    print(f"Taxa de Perda: {taxa_perda:.1f}%")
    print(f"RTT Médio: {rtt_medio:.2f}ms")
    print("="*40)

    client_socket.close()

if __name__ == "__main__":
    iniciar_cliente()