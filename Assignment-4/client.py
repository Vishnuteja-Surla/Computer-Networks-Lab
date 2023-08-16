import socket
import threading

class ClientRunnable(threading.Thread):
    def __init__(self, s):
        super().__init__()
        self.socket = s
        self.input = self.socket.makefile('r')

    def run(self):
        try:
            while True:
                response = self.input.readline().strip()
                print(response)
        except Exception as e:
            print("Error occurred:", e)
        finally:
            try:
                self.input.close()
            except Exception as e:
                print("Error occurred:", e)

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket:
            socket.connect(('localhost', 5000))

            # Reading the input from the server
            input_stream = socket.makefile('r')
            
            # Returning the output to the server
            output = socket.makefile('w')

            scanner = input
            user_input = ""
            client_name = "empty"

            client_run = ClientRunnable(socket)
            threading.Thread(target=client_run.run).start()

            # Loop closes when the user enters the "exit" command
            while user_input != "exit":
                if client_name == "empty":
                    print("Enter your name:")
                    user_input = scanner()
                    client_name = user_input
                    output.write(user_input + '\n')
                    output.flush()
                    if user_input == "exit":
                        break
                else:
                    message = f"({client_name}) message: "
                    print(message, end="")
                    user_input = scanner()
                    output.write(message + " " + user_input + '\n')
                    output.flush()
                    if user_input == "exit":
                        break

    except Exception as e:
        print("Exception occurred in client main:", e)

if __name__ == "__main__":
    main()
