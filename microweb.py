import network
import time
import socket
import os
import machine

def start_webserver():
    
    led = machine.Pin("LED", machine.Pin.OUT)
    ap = network.WLAN(network.AP_IF)
    ap.config(ssid="MicroWeb", password="microweb")
    ap.config(hostname="microweb")
    ap.active(True)
    led.value(0)

    while not ap.isconnected():
        print("Not connected!")
        time.sleep(2)
        
    ip4=ap.ifconfig()[0]

    print("Connected!")
    print(f"IP: {ip4}")

    led.value(1)

    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    
    print(f"Listening on: http://{ip4}")
    
    while True:
        cl, addr = s.accept()
        print("Client connection:", addr)
        request = cl.recv(1024)
        request = str(request)
        led_on = request.find("led=on")
        led_off = request.find("led=off")
        
        if led_on == 8:
            led.value(1)
        if led_off == 8:
            led.value(0)
        
        try:
            with open("html.html", "r") as file:
                html = file.read()
                file.close()
        except:
            html = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
Please make sure to create a html.html file to set up your HTML Document Response!"""
        
        cl.send(html)
        cl.close()

if __name__ == "__main__":
    start_webserver()
