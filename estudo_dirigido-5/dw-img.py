import socket

url = input("Escreva a URL completa da imagem: ")
url = url.split('/')
url.remove("")

url_host = url[1]
url_image = url[2:]
url_image = '/'.join(url_image)
#Retirar informações extras não referentes a url da imagem
try:
    url_image = url_image.split('?')[0]
except:
    pass
#Lembrar de abrir e fechar conexão ou ira executar infinitamente
url_request = f'GET {url_image} HTTP/1.1\r\nHost: {url_host}\r\nConnection: close\r\n\r\n'

HOST_PORT   = 80
BUFFER_SIZE = 4058


sock_img = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_img.connect((url_host, HOST_PORT))
sock_img.sendall(url_request.encode())

print('\nBaixando a imagem...')
# Montado a variável que armazenará os dados de retorno
data_ret = b''

while True:
    data = sock_img.recv(BUFFER_SIZE)
    if not data: break
    data_ret += data

sock_img.close()

# Obtendo o tamanho da imagem
img_size = -1
tmp = data_ret.split('\r\n'.encode())
for line in tmp:
   if 'Content-Length:'.encode() in line:
      img_size = int(line.split()[1])
      break
print(f'\nTamanho da Imagem: {img_size} bytes')

# Separando o Cabeçalho dos Dados
delimiter = '\r\n\r\n'.encode()
position  = data_ret.find(delimiter)
headers   = data_ret[:position]
image     = data_ret[position+4:]

# Salvando a imagem
file_output = open(url_image, 'wb')
file_output.write(image)
file_output.close()