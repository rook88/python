import telnetlib

def ping_port(host = '127.0.0.1', port = '80', timeout = 3):
    tn = telnetlib.Telnet()
    try:
        tn.open(host, port, timeout)
        tn.close()
        return True
    except:
        return False


       
