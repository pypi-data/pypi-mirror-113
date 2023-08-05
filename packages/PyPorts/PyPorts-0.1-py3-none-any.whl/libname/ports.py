import socket
def scan():
    ip = input("enter an ip > ")
    ports = [80, 20, 21, 22, 23, 25, 53, 443, 110, 161, 143, 993, 995] 
    print("STARTED SCANNING", ip)
    for port in ports:                                       
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))                   
        if result == 0:                                       
            print('port', port, '[!]' )
        else:
            print('port', port, '[X]' )
    print("scan done")