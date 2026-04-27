import socket
import datetime

# Configurações do servidor
HOST = '127.0.0.1'
PORTA = 8080

def iniciar_servidor():
    # Cria socket TCP (SOCK_STREAM)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reusar a porta imediatamente após fechar o programa
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    server_socket.bind((HOST, PORTA))
    server_socket.listen(5)
    
    print(f"[*] Servidor Web TCP ativo em http://{HOST}:{PORTA}")
    print("[*] Aguardando requisições do navegador...\n")

    while True:
        # Requisito: Atender mais de uma requisição sequencialmente
        client_conn, addr = server_socket.accept()
        
        try:
            request = client_conn.recv(1024).decode()
            if not request:
                continue

            # Requisito: Exibir logs das requisições
            primeira_linha = request.split('\n')[0]
            print(f"[LOG] {datetime.datetime.now()} - Cliente {addr} solicitou: {primeira_linha}")

            # Extrai o caminho (Ex: / ou /contato)
            caminho = primeira_linha.split()[1]

            # Requisito: Gerar resposta dinâmica e tratamento de erro 404
            if caminho == "/":
                status = "200 OK"
                corpo = f"""
                <html>
                    <head><title>Servidor TCP</title></head>
                    <body>
                        <h1>Bem-vindo ao Servidor Web Simples</h1>
                        <p><b>Resposta Dinâmica:</b> A hora atual é {datetime.datetime.now().strftime('%H:%M:%S')}</p>
                        <p>Status do Servidor: <span style='color: green'>Online</span></p>
                    </body>
                </html>
                """
            else:
                # Requisito: Tratamento básico de erros (404)
                status = "404 Not Found"
                corpo = "<html><body><h1>Erro 404: Pagina nao encontrada</h1></body></html>"

            # Monta o cabeçalho HTTP
            response = f"HTTP/1.1 {status}\r\n"
            response += "Content-Type: text/html; charset=utf-8\r\n"
            response += f"Content-Length: {len(corpo)}\r\n"
            response += "Connection: close\r\n"
            response += "\r\n"
            response += corpo

            client_conn.sendall(response.encode())
            
        except Exception as e:
            print(f"[ERRO] Falha ao processar requisição: {e}")
        finally:
            client_conn.close()

if __name__ == "__main__":
    iniciar_servidor()