import socket
import datetime
import urllib.parse
import re

HOST = '127.0.0.1'
PORTA = 8080

# Banco de dados temporário
historico_chat = ["<b>Servidor:</b> Chat TCP do Cinema Online iniciado."]
contador_usuarios = 0

def iniciar_servidor():
    global contador_usuarios
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORTA))
    server_socket.listen(5)
    
    print(f"[*] Servidor Web TCP ativo em http://{HOST}:{PORTA}")
    print("[*] Monitoramento de rede e identificação por Cookies ativos.\n")

    while True:
        client_conn, addr = server_socket.accept()
        
        try:
            # Recebe a requisição bruta
            raw_request = client_conn.recv(2048).decode('utf-8')
            if not raw_request:
                continue

            # --- LÓGICA DE IDENTIFICAÇÃO (COOKIE) ---
            match = re.search(r"user_id=(\d+)", raw_request)
            set_cookie_header = ""
            
            if match:
                user_id = match.group(1)
            else:
                contador_usuarios += 1
                user_id = str(contador_usuarios)
                set_cookie_header = f"Set-Cookie: user_id={user_id}; Path=/; HttpOnly\r\n"
            
            nome_usuario = f"Usuario {user_id}"

            # --- ANÁLISE TÉCNICA DA REQUISIÇÃO ---
            tamanho_requisicao = len(raw_request.encode('utf-8'))
            primeira_linha = raw_request.split('\n')[0].strip()
            caminho = primeira_linha.split()[1] if len(primeira_linha.split()) > 1 else "/"
            
            # --- EXTRAÇÃO ANTECIPADA DA MENSAGEM PARA O LOG ---
            msg_texto = ""
            if "?" in caminho:
                query = caminho.split("?")[1]
                params = urllib.parse.parse_qs(query)
                msg_texto = params.get('msg', [''])[0]

            print("-" * 65)
            hora_log = datetime.datetime.now().strftime('%H:%M:%S')
            print(f"[LOG TCP] {hora_log} | {addr} | {nome_usuario}")
            print(f"Comando: {primeira_linha}")
            
            if msg_texto:
                print(f"Tamanho da Requisição: {tamanho_requisicao} bytes | Mensagem: {msg_texto}")
            else:
                print(f"Tamanho da Requisição: {tamanho_requisicao} bytes")

            status_code = "200 OK"
            
            if caminho == "/" or caminho.startswith("/?"):
                html_mensagens = "<br>".join(historico_chat)
                corpo = f"""
                <html>
                <head><meta charset="utf-8"><title>CineSync P2P</title><meta http-equiv="refresh" content="5"></head>
                <body style="font-family: sans-serif; background-color: #1a1a1a; color: #ddd; padding: 20px;">
                    <h2 style="color: #e50914;">🎬 CineSync P2P Online - Chat TCP</h2>
                    <p>Sessão de: <b>{nome_usuario}</b></p>
                    <div style="background: #262626; padding: 15px; height: 300px; overflow-y: auto; border: 1px solid #333;">
                        {html_mensagens}
                    </div><br>
                    <form action="/enviar" method="GET">
                        <input type="text" name="msg" placeholder="Comente sobre o filme..." required style="padding: 8px; width: 70%;">
                        <button type="submit" style="padding: 8px; background: #e50914; color: white; border: none;">Enviar</button>
                    </form>
                </body>
                </html>
                """

            elif caminho.startswith("/enviar"):
                if msg_texto:
                    hora_msg = datetime.datetime.now().strftime('%H:%M:%S')
                    historico_chat.append(f"<span style='color:#888'>[{hora_msg}]</span> <b>{nome_usuario}:</b> {msg_texto}")
                
                status_code = "303 See Other"
                resposta = f"HTTP/1.1 {status_code}\r\nLocation: /\r\n"
                if set_cookie_header: resposta += set_cookie_header
                resposta += "\r\n"
                
                client_conn.sendall(resposta.encode('utf-8'))
                print(f"Resposta Enviada: {status_code}")
                print("-" * 65)
                continue

            else:
                status_code = "404 Not Found"
                corpo = "<h1>404 - Pagina nao encontrada</h1>"

            response = f"HTTP/1.1 {status_code}\r\n"
            response += "Content-Type: text/html; charset=utf-8\r\n"
            response += f"Content-Length: {len(corpo.encode('utf-8'))}\r\n"
            if set_cookie_header: response += set_cookie_header
            response += "Connection: close\r\n\r\n"
            response += corpo

            client_conn.sendall(response.encode('utf-8'))
            print(f"Resposta Enviada: {status_code}")
            print("-" * 65)
            
        except Exception as e:
            pass # Ignora silenciosamente se o navegador abortar a conexão
        finally:
            client_conn.close()

if __name__ == "__main__":
    iniciar_servidor()