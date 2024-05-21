import socket

# Server connection info
server_location = ('localhost', 10000)

# Establish client socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(server_location)

# Collect user credentials
user_id = input("Enter User ID: ")
user_pin = input("Enter your PIN: ")

print("Available actions:")
print("1. Pay for products (choose product IDs)")
print("2. Deposit funds (enter an amount)")
print("3. View your account balance")
# Interact with the server
action = input("Select action (pay, deposit, view_balance): ")

if action == 'pay':
    print("Products available:")
    print("1 - Starter Pack (1500)")
    print("2 - Advanced Pack (2500)")
    print("3 - Pro Pack (3500)")
    selected_products = input("Enter product ID : ")
    request = f"{user_id},{user_pin},{action},{selected_products}"

elif action == 'deposit':
    amount = input("Enter deposit amount: ")
    request = f"{user_id},{user_pin},{action},{amount}"

elif action == 'view_balance':
    request = f"{user_id},{user_pin},{action},"

else:
    print("Invalid action.")
    client.close()
    exit(0)

client.send(request.encode('utf-8'))

# Receive response from the server
server_reply = client.recv(1024).decode('utf-8')
print("Server:", server_reply)

# Close the client connection
client.close()
