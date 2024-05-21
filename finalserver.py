import socket
from threading import Thread
from twilio.rest import Client

# Server configuration
server_host = 'localhost'
server_port = 10000
address = (server_host, server_port)

# Twilio setup
twilio_sid = 'SID HERE'
twilio_token = 'TOKEN HERE'
twilio = Client(twilio_sid, twilio_token)

# Create server socket and bind to the address
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(address)
server.listen()

# User data and balances
user_data = {
    '1': {'pin': '1234', 'funds': 7500},
    '2': {'pin': '5678', 'funds': 8500},
    '3': {'pin': '9101', 'funds': 11000},
}

# Updated product catalog with IDs 1, 2, 3, 4
item_catalog = {
    '1': {'label': 'Starter Pack', 'cost': 1500},
    '2': {'label': 'Advanced Pack', 'cost': 2500},
    '3': {'label': 'Pro Pack', 'cost': 3500},
}

def handle_client(conn):
    # Receive and process client data
    received_data = conn.recv(1024).decode('utf-8')
    user_id, pin, action, *extra_info = received_data.split(',')

    if user_id in user_data and user_data[user_id]['pin'] == pin:
        if action == 'pay':
            total_cost = 0
            product_ids = extra_info[0].split(',')
            for product_id in product_ids:
                if product_id in item_catalog:
                    total_cost += item_catalog[product_id]['cost']
                else:
                    conn.send(f"Invalid product ID: {product_id}".encode('utf-8'))
                    conn.close()
                    return

            if user_data[user_id]['funds'] >= total_cost:
                user_data[user_id]['funds'] -= total_cost
                conn.send("Purchase completed.".encode('utf-8'))
                twilio.messages.create(
                    from_='+1------',
                    body='Payment successful. Your purchase has been completed.',
                    to='+201-------',
                )
            else:
                conn.send("Insufficient funds.".encode('utf-8'))
                twilio.messages.create(
                    from_='+12------',
                    body='Payment failed due to insufficient balance.',
                    to='+201--------',
                )
        elif action == 'deposit':
            deposit = int(extra_info[0])
            user_data[user_id]['funds'] += deposit
            conn.send(f"Deposit of {deposit} was successful.".encode('utf-8'))
            twilio.messages.create(
                from_='+12------',
                body='Deposit confirmed. Thank you!',
                to='+201-------',
            )
        elif action == 'view_balance':
            current_balance = user_data[user_id]['funds']
            conn.send(f"Your current balance is {current_balance}.".encode('utf-8'))
    else:
        conn.send("Invalid credentials.".encode('utf-8'))

    # Close the connection after processing
    conn.close()

# Accept client connections
while True:
    client_conn, client_addr = server.accept()
    # Start a new thread for each client
    client_thread = Thread(target=handle_client, args=(client_conn,))
    client_thread.start()
