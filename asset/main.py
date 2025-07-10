import http.server
import socketserver
import os
import mimetypes

PORT = 5000


class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.end_headers()

    def guess_type(self, path):
        """Melhorar detecção de tipos MIME"""
        mimetype, encoding = mimetypes.guess_type(path)
        if mimetype is None:
            if path.endswith('.css'):
                mimetype = 'text/css'
            elif path.endswith('.js'):
                mimetype = 'application/javascript'
            elif path.endswith('.html'):
                mimetype = 'text/html'
            elif path.endswith('.png'):
                mimetype = 'image/png'
            elif path.endswith('.jpg') or path.endswith('.jpeg'):
                mimetype = 'image/jpeg'
            elif path.endswith('.gif'):
                mimetype = 'image/gif'
            elif path.endswith('.svg'):
                mimetype = 'image/svg+xml'
            else:
                mimetype = 'application/octet-stream'
        return mimetype, encoding

    def do_GET(self):
        print(f"🔍 DEBUG: Requisição para: {self.path}")

        # Mapear rotas para arquivos HTML
        original_path = self.path
        if self.path == '/':
            self.path = 'index.html'
        elif self.path == '/premios':
            self.path = '/premios.html'
        elif self.path == '/doacao':
            self.path = '/doacao.html'
        elif self.path == '/quemsomos':
            self.path = '/quemsomos.html'
        elif self.path == '/brindes-catolicos':
            self.path = '/brindes-catolicos.html'

        # Corrigir caminhos que começam com /asset/
        if self.path.startswith('/asset/'):
            self.path = self.path[6:]  # Remove '/asset' do início

        # Mapear caminhos comuns do WordPress
        if self.path.startswith('/wp-content/'):
            # Já está correto
            pass
        elif self.path.startswith('/wp-includes/'):
            # Já está correto
            pass
        elif self.path.startswith('/ajax/'):
            # Já está correto
            pass
        elif self.path.startswith('/cdn-cgi/'):
            # Já está correto
            pass
        elif self.path.startswith('/sdks/'):
            # Já está correto
            pass

        # Remover query parameters para verificação de arquivo
        path_without_query = self.path.split('?')[0]

        # Verificar se o arquivo existe
        file_path = os.path.join(os.getcwd(), path_without_query.lstrip('/'))
        print(f"📁 DEBUG: Procurando arquivo em: {file_path}")

        if os.path.exists(file_path) and os.path.isfile(file_path):
            print(f"✅ DEBUG: Arquivo encontrado!")
            return super().do_GET()
        else:
            print(f"❌ DEBUG: Arquivo não encontrado!")

            # Se for uma rota de brinde, tentar encontrar o arquivo correto
            if '/brindes/brinde' in original_path:
                brinde_num = original_path.split('brinde')[1].split(
                    '/')[0].split('?')[0]
                if brinde_num.isdigit():
                    brinde_file = f'/brindes/brinde{brinde_num}.html'
                    if os.path.exists(
                            os.path.join(os.getcwd(),
                                         brinde_file.lstrip('/'))):
                        self.path = brinde_file
                        print(f"🔄 DEBUG: Redirecionando para: {brinde_file}")
                        return super().do_GET()

            # Listar arquivos disponíveis para debug
            print(f"📂 DEBUG: Arquivos disponíveis no diretório atual:")
            try:
                for item in os.listdir(os.getcwd()):
                    print(f"   - {item}")
            except Exception as e:
                print(f"   Erro ao listar: {e}")

            # Retornar 404 se arquivo não encontrado
            self.send_error(404, f"File not found: {original_path}")
            return


if __name__ == "__main__":
    # Define o diretório da pasta asset como raiz para arquivos estáticos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Configurar tipos MIME
    mimetypes.init()
    mimetypes.add_type('application/javascript', '.js')
    mimetypes.add_type('text/css', '.css')

    try:
        with socketserver.TCPServer(("0.0.0.0", PORT),
                                    MyHTTPRequestHandler) as httpd:
            print(f"✅ Servidor rodando em http://0.0.0.0:{PORT}")
            print("🛑 Pressione Ctrl+C para parar o servidor")
            httpd.serve_forever()
    except OSError as e:
        if e.errno == 98:  # Address already in use
            print(f"❌ Erro: A porta {PORT} já está em uso!")
            print("💡 Tentando usar uma porta alternativa...")
            PORT = 5001
            try:
                with socketserver.TCPServer(("0.0.0.0", PORT),
                                            MyHTTPRequestHandler) as httpd:
                    print(f"✅ Servidor rodando em http://0.0.0.0:{PORT}")
                    print("🛑 Pressione Ctrl+C para parar o servidor")
                    httpd.serve_forever()
            except OSError:
                print(
                    "❌ Erro: Não foi possível iniciar o servidor em nenhuma porta disponível."
                )
        else:
            print(f"❌ Erro inesperado: {e}")
    except KeyboardInterrupt:
        print("\nServidor finalizado.")
