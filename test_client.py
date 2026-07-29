import socket

def run_test(test_name, request_string):
    print(f"--- Running Test: {test_name} ---")
    try:
        # Create a client socket and connect to your server's port
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 8081))
        
        # Send the raw HTTP request
        client.sendall(request_string.encode('utf-8'))
        
        # Receive and print the response
        response = client.recv(4096).decode('utf-8')
        print(f"Response:\n{response}\n")
    except Exception as e:
        print(f"Test failed with error: {e}\n")
    finally:
        client.close()

# Test Case 1: 505 HTTP Version Not Supported
# Triggers the requestLine[-1] != 'HTTP/1.1' check
run_test(
    "505 Version Not Supported", 
    "GET / HTTP/3.0\r\nHost: localhost\r\n\r\n"
)

# Test Case 2: 403 Forbidden
# Triggers the 'private' in filePath check
run_test(
    "403 Forbidden", 
    "GET private/data.txt HTTP/1.1\r\nHost: localhost\r\n\r\n"
)

# Test Case 3: 404 Not Found
# Triggers the os.path.exists(filePath) check
run_test(
    "404 Not Found", 
    "GET notFound.html HTTP/1.1\r\nHost: localhost\r\n\r\n"
)

# Test Case 4: 200 OK
# Create a dummy file called 'test.html' in your server's directory first!
run_test(
    "200 OK", 
    "GET test.html HTTP/1.1\r\nHost: localhost\r\n\r\n"
)