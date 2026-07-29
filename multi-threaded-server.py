import socket
from _thread import start_new_thread
import threading
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime, formatdate
import os

#reference  https://www.geeksforgeeks.org/python/socket-programming-multi-threading-python/
lock = threading.Lock()

'''
handle client requests

Request Template
--------------------
request line\r\n (*method *file *HTTP version)
header lines\r\n
\r\n
payload (might not have)
---------------------
'''
def handle_client(clientSocket):
    while True:
        request = clientSocket.recv(4096).decode()
        if not request:
            lock.release()
            break
        
        # parse payout out of request
        parsedRequest = request.split('\r\n\r\n')

        if len(parsedRequest) > 1:
            payload = parsedRequest[1]

        # parse each line of request
        linesRequest = parsedRequest[0].split('\r\n')
        # Request line
        requestLine = linesRequest[0].split(' ')
        # file path
        filePath = requestLine[1]
        # header lines
        headerLines = linesRequest[1:]


        httpDate = formatdate(usegmt=True)


        # 505 HTTP version not supported
        # check last item in request line for http version
        #TODO
        if requestLine[-1] != 'HTTP/1.1':
            response = (
                f"HTTP/1.1 505 HTTP Version Not Supported\r\n"
                f"Content-Length: 0\r\n"
                f"Connection: close\r\n\r\n"
            )

            clientSocket.sendall(response.encode("utf-8"))
            continue

        # 304 Not Modified
        # check If-modified-since headerline
        # if it is equal to or newer than file's modified date then send reponse

        #find the If-Modified-Since line
        modifiedSince = "If-Modified-Since"
        modifiedSinceHeaderLine = ""
        for item in headerLines:
            if item[:len(modifiedSince)] == modifiedSince:
                modifiedSinceHeaderLine = item

        # if it exists, find the date and check it with the file    
        if len(modifiedSinceHeaderLine) != 0:
            # If-Modified-Since: <day-name>, <day> <month> <year> <hour>:<minute>:<second> GMT
            clientDate = modifiedSinceHeaderLine[len("If-Modified-Since: "):]
            fileMtime = os.path.getmtime(filePath)
            fileTimestamp = datetime.fromtimestamp(fileMtime, timezone.utc).replace( microsecond=0 )
            headerTime = parsedate_to_datetime(clientDate)

            if fileTimestamp < headerTime:
                response = (
                    "HTTP/1.1 304 Not Modified\r\n"
                    f"Date: {httpDate}\r\n\r\n"
                )
                clientSocket.sendall(response.encode("utf-8"))
                continue

        # 403 forbidden
        # if client trying to access private server, send 403
        if "private" in filePath:
            response = (
                "HTTP/1.1 403 Forbidden\r\n"
                f"Date: {httpDate}\r\n"
                "Content-Length: 0\r\n\r\n"
            )
            clientSocket.sendall(response.encode("utf-8"))
            continue

        # 404 Not found
        # if the file doesn't exist, send 404
        if not os.path.exists(filePath):
            error_body = b"404 Not Found"
            header = (
                "HTTP/1.1 404 Not Found\r\n"
                f"Date: {httpDate}\r\n"
                f"Content-Length: {len(error_body)}\r\n"
                "Content-Type: text/plain\r\n\r\n"
            )
            clientSocket.sendall(header.encode("utf-8") + error_body)
            continue

        #202 OK
        with open(filePath, "rb") as f:
            body = f.read()
        header = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"Date: {httpDate}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n\r\n"
        )
        clientSocket.sendall(header.encode("utf-8") + body)

        '''
        # determine which method is being requested
        
        match requestLine[0]:
            case "GET":
                print("GET")
            case "POST":
                print("POST")
            case "HEAD":
                print("HEAD")
            case "PUT":
                print("PUT")
            case "DELETE":
                print("DELETE")
        '''
    clientSocket.close()

def main():
    HOST = ''
    PORT = 8081

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST,PORT))

    server.listen(5)

    print(f"Listening on {HOST}: {PORT}")
    while True:
        clientSocket, clientAddr = server.accept()

        lock.acquire()
        start_new_thread(handle_client, (clientSocket,))
        


if __name__ == '__main__':
    main()