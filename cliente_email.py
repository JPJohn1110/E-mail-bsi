import socket
import bcrypt
import pickle
from datetime import datetime


def configurar_servidor():
    while True:
        ip = input("Digite o IP do servidor: ")
        porta = int(input("Digite a porta do servidor: "))

        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.settimeout(3)  
            cliente.connect((ip, porta))
            print("Serviço Disponível.")
            return ip, porta
        
        except (socket.timeout, ConnectionRefusedError):
            print("Erro: Servidor não disponível. Tente novamente.")
            
        except ValueError:
            print("Erro: Porta inválida. Digite um número válido.")
            
        except Exception as e:
            print(f"Erro inesperado: {e}. Tente novamente.")

        
    
def cadastrar_conta(ip, porta):
    nome = input("Digite seu nome completo: ")
    username = input("Digite um nome de usuário (sem espaços): ").strip().replace(" ", "")
    senha = input("Digite sua senha: ").encode('utf-8')

    senha_hash = bcrypt.hashpw(senha, bcrypt.gensalt()).decode('utf-8')

    dados = {"acao": "cadastrar", "nome": nome, "username": username, "senha": senha_hash}

    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((ip, porta))
        
        cliente_socket.sendall(pickle.dumps(dados))

        resposta = pickle.loads(cliente_socket.recv(4096))
        print(resposta)


    except Exception as e:
        print("Erro ao conectar ao servidor:", e)
    finally:
        cliente_socket.close()




def acessar_email(ip, porta):
    username = input("Digite seu nome de usuário: ").strip()
    senha = input("Digite sua senha: ").encode('utf-8')

    dados = {"acao": "login", "username": username, "senha": senha}

    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((ip, porta))

        cliente_socket.sendall(pickle.dumps(dados))

        resposta = pickle.loads(cliente_socket.recv(4096))
        
        if resposta:
            print(f'{'-='*20}\nSEJA BEM-VINDO << {resposta} >>\n{'-='*20}')
            return username
        else:
            print("USUÃRIO OU SENHA INCORRETA")
            return resposta


    except Exception as e:
        print("Erro ao conectar ao servidor:", e)
        return False


def enviar_email(ip, porta, username):
    destinatario = input("Destinatário: ").strip()
    assunto = input("Digite o assunto do e-mail: ").strip()
    corpo = input("Digite a mensagem do e-mail:\n")

    dados = {
        "acao": "enviar_email",
        "remetente": username,
        "destinatario": destinatario,
        "data_hora": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "assunto": assunto,
        "corpo": corpo
    }

    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((ip, porta))

        cliente_socket.sendall(pickle.dumps(dados))

        retorno = pickle.loads(cliente_socket.recv(4096))
        print(retorno)

    except Exception as e:
        print("Erro ao conectar ao servidor:", e)


def receber_emails(ip, porta, username):
   
    dados = {"acao": "receber_emails", "username": username}

    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente_socket.connect((ip, porta))

        cliente_socket.sendall(pickle.dumps(dados))

        resposta = pickle.loads(cliente_socket.recv(4096))

        if not resposta:
            print(f"{"-="*20}\nNENHUM EMAIL ENCONTRADO.\n{"-="*20}\n")
            return
        while resposta:
            print(f"{"-="*20}\nEMAILS RECEBIDOS:\n{"-="*20}\n")
            for i, email in enumerate(resposta, start=1):
                print(f"\n[{i}] {email['remetente']} : {email['assunto']}")
            
            escolha = int(input("\nDigite o número do e-mail para ler (ou ENTER para sair): "))
            if escolha:
                escolha = escolha - 1
                if 0 <= escolha < len(resposta):
                    email = resposta[escolha]
                    print("\n" + "-" * 50)
                    print(f"De: {email['remetente']}")
                    print(f"Para: {email['destinatario']}")
                    print(f"Data: {email['data_hora']}")
                    print(f"Assunto: {email['assunto']}")
                    print(f"\n{email['corpo']}")
                    print("-" * 50)
            elif escolha == '':
                print(f"{"-="*20}\nSAINDO....\n{"-="*20}\n")
                break

            
    except Exception as e:
        print("SAINDOOOO ...")
    finally:
        cliente_socket.close()





def tela_email(ip, porta, username):
    
    while True:

        print(f'''
    {"-=" * 20}
    SEJA BEM-VINDO AO SEU E-MAIL <{username}>
    [4] Enviar E-mail
    [5] Receber E-mails
    [6] Logout
    {"-=" * 20}
                    ''')
        a = int(input("ESCOLHA UMA DAS OPÇÕES: "))
            
        if a == 6: 
            print(f"{"-=" * 20}\nLOGOUT REALIZADO COM SUCESSO\n{"-=" * 20}")
            return    
        elif a==4:
            enviar_email(ip, porta, username)
        elif a == 5:
            receber_emails(ip, porta, username)

    
def main():
    
    
    servidor_ip = ''
    servidor_porta = 0
   
    try:
        while True:
            print(
            f'''
            {"-=" * 20}
            CLIENTE E-MAIL SERVCE BSI ONLINE
            [1] Apontar Servidor
            {"-=" * 20}
                        ''')
            
            a = int(input('DIGITE A OPÇÃO [1]: '))
            if a == 1:
                servidor_ip, servidor_porta = configurar_servidor()
                break
            
            
        
        
        while True:    
            print(
                f'''
        {"-=" * 20}
        CLIENTE E-MAIL SERVCE BSI ONLINE
        [1] Apontar Outro Servidor
        [2] Cadastrar Conta
        [3] Acessar Email
        {"-=" * 20}
        
                '''
            )
            
            
            a = int(input("ESCOLHA UMA DAS OPÇÕES: "))
        
            if a == 1:
                servidor_ip, servidor_porta = configurar_servidor()
                if servidor_ip == None:
                    break
            elif a == 2:
                cadastrar_conta(servidor_ip,servidor_porta)

            elif a == 3:
                autentic = acessar_email(servidor_ip, servidor_porta)
                if autentic:
                    tela_email(servidor_ip, servidor_porta, autentic)
            
    except Exception as e:
        print("SAINDOOOO ...")

                

main()