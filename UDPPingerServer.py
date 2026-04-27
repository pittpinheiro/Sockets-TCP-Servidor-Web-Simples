# UDPPingerServer.py
import random
from socket import *

# Cria um socket UDP (SOCK_DGRAM) 
serverSocket = socket(AF_INET, SOCK_DGRAM)

# Atribui o endereço IP e o número da porta ao socket 
# O '' vazio significa que ele aceita conexões de qualquer IP na porta 12000
serverSocket.bind(('', 12000))

print("[*] Servidor UDP aguardando pings na porta 12000...")

while True:
    # Gera um número aleatório de 0 a 10 
    rand = random.randint(0, 10)
    
    # Recebe o pacote do cliente junto com o endereço de origem 
    message, address = serverSocket.recvfrom(1024)
    
    # Transforma a mensagem em letras maiúsculas 
    message = message.upper()
    
    # Simulação de perda: Se rand for menor que 4, ignoramos o pacote 
    if rand < 4:
        print(f"[PERDA] Pacote de {address} descartado propositalmente.")
        continue
    
    # Caso contrário, o servidor responde ao cliente 
    serverSocket.sendto(message, address)
    print(f"[OK] Resposta enviada para {address}")