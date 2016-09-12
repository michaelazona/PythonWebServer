import socket, os.path, time, datetime, signal, sys

class Server:
    
    def __init__(self, host = '', port = 80, directory = 'www'):
        self.host = host
        self.port = port
        self.directory = directory

    def start(self):
        try:
            self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listen_socket.bind((self.host, self.port))
            self.listen_socket.listen(3)

            self.connectionHandler()
                        
        except Exception as e:
            print "Unable to start the server: " + str(e)

    def getHeaders(self, code):

         header = ''
         
         if (code == 200):
            header = 'HTTP/1.1 200 OK\n'
            
         elif(code == 404):
            header = 'HTTP/1.1 404 Not Found\n'

         currentTime = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
         header = header + 'Date: ' + currentTime +'\n'
         header = header + 'Server: httpServer\n'
         header = header + 'Connection: close\n\n'  

         return header

    def connectionHandler(self):

        while True:
            try:
                print "Waiting for connection..."
                clientConnection, clientAddress = self.listen_socket.accept()
                #accepts TCP client connection
                
                print "Received connection from " + clientAddress[0] + " at " + str(datetime.datetime.now()).split('.')[0]
                
                clientConnection.settimeout(2)
                message = clientConnection.recv(1024)
                message = message.split(' ')
                #recieves TCP message - turns into list

                try:
                    fileRequested = message[1]
                    #second element in array is file requested
                except:
                    continue
                    #unable to process request - skip and wait for next request
                    #'continue' means to start the loop from the top

                if(fileRequested == "/"):
                    fileRequested = "/index.html"
                    #changes fileRequested to default file if none requested

                if(fileRequested == "/favicon.ico"):
                    continue
                    #browser send second request for ico file - ignore this and return to top of loop

                fileRequested = "www\\" + fileRequested[1:]
                #add HTML directory to fileRequested path and remove preceeding '/' character

                if(os.path.isfile(fileRequested)):
                    fileHandler  = open(fileRequested, 'rb')
                    content      = fileHandler.read()
                    httpResponse = self.getHeaders(200) + content
                    fileHandler.close()
                    #if file exists, save all html to variable

                else:
                    content      = "<html><body><p>Error 404: File not found.</p></body></html>"
                    httpResponse = self.getHeaders(404) + content
                    #if file not found, set content to generic 404 html

                print "Serving file: " + fileRequested + "\n"
                
                clientConnection.sendall(httpResponse)
                clientConnection.close()
                #send the response and then close the connection

            except socket.timeout:
                print "A known error has occured: Socket timeout.\n"

            except Exception as e:
                print "There was an unkown error that occured: " + str(e)

server = Server()
server.start()

        
        
