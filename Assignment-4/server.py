import socket
import threading

class ServerThread(threading.Thread):
    def __init__(self, socket, thread_list):
        super().__init__()
        self.socket = socket
        self.thread_list = thread_list
        self.output = None

    def run(self):
        try:
            # Reading the input from the client
            input_stream = self.socket.makefile('r')
            
            # Returning the output to the client
            self.output = self.socket.makefile('w')

            # Infinite loop for the server
            while True:
                output_string = input_stream.readline().strip()
                
                # If user types "exit" command
                if output_string == "exit":
                    break
                
                self.print_to_all_clients(output_string)
                print("Server received:", output_string)

        except Exception as e:
            print("Error occurred:", e)

    def print_to_all_clients(self, output_string):
        for thread in self.thread_list:
            thread.output.write(output_string + '\n')
            thread.output.flush()

def main():
    # List to add all the client threads
    thread_list = []

    try:
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind(('localhost', 5000))
        serversocket.listen(5)

        while True:
            client_socket, client_address = serversocket.accept()
            server_thread = ServerThread(client_socket, thread_list)
            
            # Starting the thread
            thread_list.append(server_thread)
            server_thread.start()

    except Exception as e:
        print("Error occurred in main:", e)

if __name__ == "__main__":
    main()
