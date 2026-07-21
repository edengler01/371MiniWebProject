WEBSERVER_IP = 172.16.85.93


#Status Code 200
okRequest = "GET / HTTP1.1 \r\n"+
"Host: {WEBSERVER_IP}+\r\n"
#Status Code 304
notModifiedRequest = 
    "GET / HTTP1.1 \r\n"+
    "Host: {WEBSERVER_IP}" +
    "If-Modified-Since: CURRENT DATE"
#Status Code 403 Forbidden
forbiddenRequestFail =     
    "GET / HTTP1.1 \r\n"+
    "Host: {WEBSERVER_IP}" +
    "If-Modified-Since: CURRENT DATE"

#Status Code 505 HTTP Version not supported
invalidHTTPVersion =     
    "GET / HTTP1.1 \r\n"+
    "Host: {WEBSERVER_IP}" +
    "If-Modified-Since: CURRENT DATE"
