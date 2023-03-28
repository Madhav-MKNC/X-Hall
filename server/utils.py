# helper functions

# for unique usernames
unique_username = 1
def get_username():
    global unique_username
    unique_username += 1
    return "user{unique_username}"


def filterinfo(ip,port):
    try:
        port = int(port)
# other host names also valid so will update this using sockets
        if ip=='localhost':
            if 0<port<65535:
                return ip, port
# use IPv4 filtering here
        elif all(0<i<256 for i in list(map(int,ip.split('.')))) and 0<port<2**16: 
            return ip, port
    except:
        pass
    
    print("[!] using default [localhost:1234]")
    return 'localhost',1234
    # default host => 'localhost'
    # default port => 1234

