import socket
WEBSERVER_IP = "localhost"


#Status Code 200
okRequest = ("GET /test.html HTTP/1.1 \r\n"
f"Host: {WEBSERVER_IP}\r\n"
"\r\n"
             )


#Status Code 304: need if-modified-line
conditionalRequest = (
        "GET / HTTP/1.1 \r\n"
        f"Host: {WEBSERVER_IP} \r\n"
        "If-Modified-Since: Wed, 22 Jul 2026 18:30:00 GMT"
        "\r\n"
        )
#Status Code 304: call proxy server
conditionalRequestProxy = (
        "GET / HTTP/1.1 \r\n"
        f"Host: {WEBSERVER_IP} \r\n"
        "If-Modified-Since: Wed, 22 Jul 2025 18:30:00 GMT"
        "\r\n"
        )

#Status Code 403: forbidden
forbiddenRequest = (
        "GET /private/data.html HTTP /1.1 \r\n"
        f"Host: {WEBSERVER_IP} \r\n"
        "\r\n"
        )

#Status Code 404: File not found
notFoundRequest = (
        "GET /index2.html HTTP /1.1 \r\n"
        f"Host: {WEBSERVER_IP} \r\n"
        "\r\n"
        )

# Status Code 505 HTTP Version Not Supported
httpNotSupportedRequest = (
        "GET / HTTP/3.0 \r\n"
        f"Host: {WEBSERVER_IP} \r\n"
        "\r\n"
        )


clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('localhost',9000))
clientSocket.send(okRequest.encode())

response = clientSocket.recv(4096)
print(response.decode())

