import socket
import os
from _thread import start_new_thread

HOST_PROXY = "localhost"
HOST_PORT = 9000

SERVER_HOST = "localhost"
SERVER_PORT = 8081

def get_last_modified(response):
    headers = response.split(b"\r\n\r\n", 1)[0]
    for line in headers.split(b"\r\n"):
        if line.lower().startswith(b"last-modified:"):
            return line.split(b":", 1)[1].strip()
    return None

def handle_client(clientSocket):
    try:
        request = clientSocket.recv(4096)
        #if request is garbled, return
        if not request:
            return

        #split the request 
        requestLine = request.decode("utf-8").split("\r\n")[0]
        #split the get line to extract filepath
        parts = requestLine.split()
        #if the parts is less than 3, something went wrong
        if len(parts) < 3:
            return
        requestFile = parts[1]
        #if there file is blank or just /, go to home page
        if requestFile == "/":
            requestFile ="/index.html"
        cachePath = "cache" + requestFile
        #check if the cache path is valid in current file system
        if os.path.isfile(cachePath):
            print("Cache hit")
            with open(cachePath, "rb") as file:
                cachedResponse = file.read()
            lastModified = get_last_modified(cachedResponse)
            if lastModified:
                requestText = request.decode("utf-8")
                #add headers
                requestHeaders, separator, requestBody = requestText.partition("\r\n\r\n")
                validationRequest = (
                    requestHeaders +
                    "\r\nIf-Modified-Since: " +
                    lastModified.decode("utf-8") +
                    "\r\n\r\n" + 
                    requestBody
                ).encode("utf-8")

                # check with origin server
                serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

                try:
                    serverSocket.connect((SERVER_HOST, SERVER_PORT))
                    serverSocket.sendall(validationRequest)
                    responseChunks = []

                    while True:
                        chunk = serverSocket.recv(4096)
                        if not chunk:
                            break
                        responseChunks.append(chunk)
                    originResponse = b"".join(responseChunks)
                finally:
                    serverSocket.close()

                if originResponse.startswith(b"HTTP/1.1 304"):
                    print("Cache file is still valid")
                    response = cachedResponse
                # update cache
                elif originResponse.startswith(b"HTTP/1.1 200"):
                    print("Cache is outdated")
                    response = originResponse
                    with open(cachePath,"wb") as file:
                        file.write(response)

                else:
                    response = originResponse
            else: 
                response = cachedResponse

        else:
            print ("Cache miss")
            serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                serverSocket.connect((SERVER_HOST, SERVER_PORT))
                serverSocket.sendall(request)
                responseChunks = []
                while True:
                    chunk = serverSocket.recv(4096)
                    #print(f"Received chunk: {len(chunk)} bytes")
                    #print(chunk)
                    if not chunk:
                        #print("Web server closed connection")
                        break
                    responseChunks.append(chunk)
                response = b"".join(responseChunks)
            finally:
                serverSocket.close()
            # check response, if 200, store it in the cache
            if response.startswith(b"HTTP/1.1 200 OK"):
                with open(cachePath, "wb") as file:
                    file.write(response)

        clientSocket.sendall(response)
    
    finally:
        clientSocket.close()

def main():
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # prevent Address already in use, from: https://stackoverflow.com/questions/66627418/python-socket-oserror-errno-98-address-already-in-use
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy.bind((HOST_PROXY, HOST_PORT))
    proxy.listen(5)

    print(f"Proxy listening on {HOST_PROXY}:{HOST_PORT}")
    while True:
        clientSocket, clientAddr = proxy.accept()
        print(f"Client connected: {clientAddr}")

        start_new_thread(
            handle_client, (clientSocket,)
        )
if __name__ == "__main__":
    main()
        