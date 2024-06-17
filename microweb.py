import network
import time
import socket
import os
import machine

def start_webserver():
    
    ssid = "MicroWeb"
    password = "microweb"
    
    led = machine.Pin("LED", machine.Pin.OUT)
    ap = network.WLAN(network.AP_IF)
    ap.config(ssid=ssid, password=password)
    ap.active(True)
    led.value(0)

    while not ap.isconnected():
        print("Not connected!")
        time.sleep(2)
        
    ip4=ap.ifconfig()[0]

    print(f"\nSet up WLAN Access Point:\nSSID: {ssid}\nPassword: {password}")
    print(f"\nIP: {ip4}")

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
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MicroWeb</title>
</head>

<style>
    body{
        background-color: #ccc;
        display: flex;
        justify-content: center;
    }
    button {
        padding-block: 1em;
        background-color: lightblue;
        border: 1px solid black;
        padding-inline: 2em;
        border-radius: 5px;
        transition: 0.5s;

    }
    button:hover {
        transform: scale(1.05);
    }
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 50px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0px 0px 10px 5px black;
        margin-top: 100px;
    }
    form {
        margin-top: 50px;
        display: flex;
        flex-direction: column;
        gap: 25px;
    }
    span{
        color: orange;
    }
</style>

<body>
    
    <div class="container">
        <h1>MicroWeb</h1>
        <p>This is just a sample html file for the MicroWeb<br>to show you what is possible with <span>microweb</span>.</p>
        <form>
            <button name="led" value="on">Led on</button>
            <button name="led" value="off">Led off</button>
        </form>
    </div>

</body>

</html>"""
        
        cl.send(html)
        cl.close()

if __name__ == "__main__":
    start_webserver()
