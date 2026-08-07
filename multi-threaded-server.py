import socket
from _thread import start_new_thread
import threading
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime, formatdate
import os
import base64
from queue import Queue


# Define frame size
FRAME_SIZE = 1024
# create shared queue for active framed responses
# thread safe
responseQueue = Queue()


#reference  https://www.geeksforgeeks.org/python/socket-programming-multi-threading-python/
# lock = threading.Lock()

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



# create a sender thread that:
# wait until queue is not empty
# Remove response at front of queue
# Send one frame of data to front of the queue
# If theres more frames to send, put response at end of queue
# If no frame remains, close client socket
def sender_thread():
    while True:
        clientSocket, frames = responseQueue.get()
        frame = frames.pop(0)
        print(f"Sending frame of size {len(frame)} bytes")
        clientSocket.sendall(frame)
        # if theres still frames leftover, it put back in the queue
        if frames:
            responseQueue.put((clientSocket,frames))
        # no more frames, done, close it
        else:
            clientSocket.close()



def handle_client(clientSocket):
    while True:
        request = clientSocket.recv(4096).decode()
        if not request:
            clientSocket.close()
           # lock.release()
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
        requestFile = requestLine[1].lstrip('/')
        filePath = "webServer/"+requestFile

        # header lines
        headerLines = linesRequest[1:]


        httpDate = formatdate(usegmt=True)


        # 505 HTTP version not supported
        # check last item in request line for http version
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
        if "private/data.txt" in filePath:
            auth_header = ""
            for item in headerLines:
                if item.startswith("Authorization: Basic "):
                    auth_header = item

            if not auth_header:
                response = (
                    "HTTP/1.1 403 Forbidden\r\n"
                    f"Date: {httpDate}\r\n"
                    "Content-Length: 0\r\n\r\n"
                )
                clientSocket.sendall(response.encode("utf-8"))
                continue

            
            encoded = auth_header[21:].strip()
            decoded = base64.b64decode(encoded).decode('utf-8')
            if decoded != "user:password":
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
            header = (
                "HTTP/1.1 404 Not Found\r\n"
                f"Date: {httpDate}\r\n"
                "Content-Length: 0\r\n\r\n"
            )
            clientSocket.sendall(header.encode("utf-8"))
            continue

        #200 OK
        with open(filePath, "rb") as f:
            body = f.read()
        header = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Length: {len(body)}\r\n"
            f"Date: {httpDate}\r\n"
            "Content-Type: text/html; charset=utf-8\r\n\r\n"
        )
        # Build HTTP response 
        # Split response body into frame_size chunks
        # First frame: response
        # add framed response to the shared response queue
        # return from this handler so only sender thread sends the response
        response = header.encode("utf-8")+body
        frames = []
        for i in range (0, len(response),FRAME_SIZE):
            frames.append(response[i:i+FRAME_SIZE])
        # Send it to sender thread
        responseQueue.put((clientSocket,frames))
        return;

def main():
    HOST = ''
    PORT = 8081

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST,PORT))

    server.listen(5)

    print(f"Listening on {HOST}: {PORT}")
    # start a dedicated sender thread
    start_new_thread(sender_thread, ())

    while True:
        clientSocket, clientAddr = server.accept()

        #lock.acquire()
        start_new_thread(handle_client, (clientSocket,))
        
        


if __name__ == '__main__':
    main()