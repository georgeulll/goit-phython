import json
import logging
import pathlib
import urllib.parse
import mimetypes
import socket
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

BASE_DIR = pathlib.Path()
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000


def send_data_to_socket(body):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(body, (SERVER_IP, SERVER_PORT))
    client_socket.close()


class HttpHandler(BaseHTTPRequestHandler): # ми формуэмо выдповыдь #Обробка requests from clients

    def do_POST(self):
    #     #self.send_html('contact.html')
        body = self.rfile.read(int(self.headers['Content-Length']))  #отримана дата з форми, rfile-це поток читаємо поток считування
        send_data_to_socket(body)
        self.send_response(302) #redirect команда браузеру куди треба перейти
        self.send_header('location', '/') # Встановлюємо спец хедер локатіон
        self.end_headers()  #закрить хедер

    # request parce те що приходе - розбирає текст, яка прийшла команда
    def do_GET(self):
        route = (urllib.parse.urlparse(self.path))
        #print(route.path)
        match route.path:  #маршрутизация
            case '/':
                self.send_html('index.html')
            case '/message':
                self.send_html('message.html')
            case _:  # якщо щось не знайшли, любий запрос
                # self.send_html('error.html', 404)
                file = BASE_DIR/route.path[1:] # записуємо шлях в змінну файл -це шлях path тип
                # print(file)
                if file.exists():  # перевіряємо чи файл існує
                    self.send_static(file) # якщо так передаємо шлях до методу відправка-статік
                    # print(True)
                else:
                    self.send_html('error.html', 404)


    def send_html(self, filename, status_code=200):
        self.send_response(status_code) #повинні повертати статус
        self.send_header('Content-Type', 'text/html') #Content-Type: text/html    # для браузера надо указывать header
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())

    def send_static(self, filename,):
        self.send_response(200)  # повинні повертати статус
        mime_type, *rest = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header('Content-Type', mime_type)  # Content-Type: text/html    # для браузера надо указывать header
        else:
            self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())

def run_socket_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    server_socket.bind(server)
    try:
        while True:
            data, address = server_socket.recvfrom(1024)
            save_data(data) #метод
    except KeyboardInterrupt:
        logging.info('Socker server is stopped')
    finally:
        server_socket.close()


def save_data(data):
    # print(self.headers['Content-Length'])# Показує кількість байтів в даті
    body = urllib.parse.unquote_plus(data.decode())
    payload = {}
    for el in body.split('&'):
        key, value = el.split('=')
        payload[key] = value
    # payload = {key: value for key, value in [el.split('=') for el in body.split('&')]}
    # message = {datetime.now().strftime('%Y-%m-%d %H:%M:%S'): key, value}
    try:
        with open(BASE_DIR.joinpath('storage/data.json'), 'r', encoding='utf-8') as fd:
            storage = json.load(fd)
    except ValueError:
            storage={}
    storage.update({datetime.now().strftime('%Y-%m-%d %H:%M:%S'):payload})
    with open(BASE_DIR.joinpath('storage/data.json'), 'w', encoding='utf-8') as fd:
        json.dump(storage, fd, ensure_ascii=False)


def run(server=HTTPServer, handler=HttpHandler):  # функцыя яка буде запускати сервер
    address = ('0.0.0.0', 3000)  # localhost
    http_server = server(address, handler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
    STORAGE_DIR =pathlib.Path().joinpath('storage')
    FILE_STORAGE = STORAGE_DIR/'data.json'
    if FILE_STORAGE.exists():
        with open(FILE_STORAGE, 'w', encoding='utf-8') as fd:
            json.dump({}, fd, ensure_ascii=False)
    thread_server = Thread(target=run)
    thread_server.start()

    thread_socket = Thread(target=run_socket_server(SERVER_IP, SERVER_PORT))
    thread_socket.start()