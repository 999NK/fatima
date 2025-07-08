import http.server
import socketserver
import os

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        elif self.path == '/premios':
            self.path = '/premios.html'
        elif self.path == '/doacao':
            self.path = '/doacao.html'
        return super().do_GET()

if __name__ == "__main__":
    os.chdir('.')  # Define o diretório como raiz para arquivos estáticos

    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
            print(f"✅ Servidor rodando em http://localhost:{PORT}")
            print("🛑 Pressione Ctrl+C para parar o servidor")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ Erro: A porta {PORT} já está em uso!")
            print("💡 Tentando usar uma porta alternativa...")
            PORT = 8081
            try:
                with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
                    print(f"✅ Servidor rodando em http://localhost:{PORT}")
                    print("🛑 Pressione Ctrl+C para parar o servidor")
                    httpd.serve_forever()
            except OSError:
                print("❌ Erro: Não foi possível iniciar o servidor em nenhuma porta disponível.")
        else:
            print(f"❌ Erro inesperado: {e}")
    except KeyboardInterrupt:
        print("\nServidor finalizado.")
