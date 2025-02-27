import socket
import concurrent.futures
import pickle
import bcrypt
import threading


def monitorar_threads():

    print(f" - Total de threads ativas no sistema: {threading.active_count()}\n")


usuarios = {}
emails = []

def mostrar_usuarios():
    print("\n===== Usuários Cadastrados =====")
    if usuarios:
        for username, info in usuarios.items():
            print(f"Usuário: {username} | Nome: {info['nome']}")
    else:
        print("Nenhum usuário cadastrado ainda.")
    print("===============================\n")



def handle_cliente(cliente_socket, endereco):
    try:
        
        dados = pickle.loads(cliente_socket.recv(4096))  
        
        
        if dados["acao"] == "cadastrar":
            username = dados["username"]
            
            if username in usuarios:
                resposta = f" {"-=" * 20}\nErro: Username já cadastrado. \n{"-=" * 20}\n "
            else:
                usuarios[username] = {"nome": dados["nome"], "senha": dados["senha"]}
                resposta = f"{"-=" * 20}\n CONTA CADASTRADA COM SUCESSO!\n{"-=" * 20}"
            cliente_socket.sendall(pickle.dumps(resposta))
            
        elif dados["acao"] == "login":
            username = dados["username"]
            senha = dados["senha"]            
            
            if username in usuarios:
                senha_hash = usuarios[username]["senha"].encode('utf-8')
                if bcrypt.checkpw(senha, senha_hash):
                    resposta = usuarios[username]["nome"]
            
            else:
                resposta = False

            cliente_socket.sendall(pickle.dumps(resposta))
           
            try: 
                if dados["acao"] == "enviar_email":
                    remetente = dados["remetente"]
                    destinatario = dados["destinatario"]

                    if destinatario not in usuarios:
                        retorno = "DESTINATÁRIO INEXISTENTE."
                        
                else:
                    emails.append(dados) 
                    retorno = "E-MAIL ENVIADO COM SUCESSO."

                cliente_socket.sendall(pickle.dumps(resposta))
            except Exception as e:
                print(f"Falha no envio do e-mail {endereco}: {e}")


    except Exception as e:
        print(f"Erro ao processar cliente {endereco}: {e}")
        
    finally:
        cliente_socket.close() 

    mostrar_usuarios()
    
    



def servidor():
    ip = "0.0.0.0"  
    porta = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, porta))
    server_socket.listen(15)
    print(f"Servidor rodando em {ip}:{porta}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        while True:
            cliente_socket, endereco = server_socket.accept()
            print(f"Nova conexão de {endereco}")
            executor.submit(handle_cliente, cliente_socket, endereco)
            monitorar_threads()



servidor()
