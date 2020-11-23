from bs4 import BeautifulSoup
import argparse, sys, requests, socket

MAX_BYTES = 65535
HOST = '127.0.0.1'
PORT = 4488

class Server:
    def __init__(self, interface, port):
        self.interface = interface
        self.port = port

    def serve(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.interface, self.port))
        sock.listen(1)

        print(f"[SERVER] is started at {sock.getsockname()}")

        while True:
            conn, addr = sock.accept()
            print("Accepted a connection from ", addr)
            url_address = (conn.recv(MAX_BYTES)).decode('ascii')
            data_to_send = "The number of images is " + str(self.image_count(url_address)) +"\n" + "The number of leaf paragraphs is " + str(self.leaf_count(url_address))
            conn.sendall(data_to_send.encode('ascii'))

            print(f"Web page scrapped and results were sent to the client {conn.getpeername()}")
        sock.close()

    def image_count(self, url_address):
        page = requests.get(url_address)
        soup = BeautifulSoup(page.content, 'html.parser')
        images = soup.find_all('img')
        return(len(images))

    def leaf_count(self, url_address):
        page = requests.get(url_address)
        soup = BeautifulSoup(page.content, 'html.parser')
        l_count = 0
        leaves = soup.find_all('p')
        for leaf in leaves:
            if not leaf.find_all('p'):
                l_count += 1
        return l_count


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port =port

    def start(self, url_address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))

        sock.sendall(url_address.encode('ascii'))

        print("Here is the result sent by server:")
        result = sock.recv(MAX_BYTES).decode('ascii')
        print(result)

        sock.close()

def main():
    parser = argparse.ArgumentParser(description="Web Page Scrapping")
    roles = {'client': Client, 'server': Server}

    parser.add_argument("role", choices=roles, help="role choices: server or client")
    if sys.argv[1] == 'client':
        parser.add_argument('-p', metavar='PAGE', type=str, help='URL address of the web page')
    args = parser.parse_args()

    if args.role == 'server':
        Server(HOST, PORT).serve()
    elif args.role == 'client':
        Client(HOST, PORT).start(args.p if "http://" in args.p or "https://" in args.p else f"https://{args.p}")

if __name__ == "__main__":
    main()
