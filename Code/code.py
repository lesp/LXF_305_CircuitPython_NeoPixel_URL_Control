import board
import wifi
import socketpool
import ampule
import time
from rainbowio import colorwheel
import neopixel

pixel_pin = board.GP16
num_pixels = 12
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

headers = {
    "Content-Type": "application/json; charset=UTF-8",
    "Access-Control-Allow-Origin": '*',
    "Access-Control-Allow-Methods": 'GET, POST',
    "Access-Control-Allow-Headers": 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
}

def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()
    time.sleep(0.5)

def rainbow_cycle(wait):
    for k in range(10):
        for j in range(255):
            for i in range(num_pixels):
                rc_index = (i * 256 // num_pixels) + j
                pixels[i] = colorwheel(rc_index & 255)
            pixels.show()
            time.sleep(wait)

@ampule.route("/rainbow")
def rainbow(request):
    rainbow_cycle(0)
    return (200, headers, '{"Lights": RAINBOW!!}')

@ampule.route("/rgb")
def rgb_set(request):
    value = request.params["value"]
    rgb_value = tuple(map(int, value.split(',')))
    print(type(rgb_value))
    print(rgb_value)
    color_chase(rgb_value, 0.1)
    return (200, {}, "RGB value is %s!" % value)
  

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets not found in secrets.py")
    raise

try:
    print("Connecting to %s..." % secrets["ssid"])
    print("MAC: ", [hex(i) for i in wifi.radio.mac_address])
    wifi.radio.connect(secrets["ssid"], secrets["password"])
except:
    print("Error connecting to WiFi")
    raise

pool = socketpool.SocketPool(wifi.radio)
socket = pool.socket()
socket.bind(['0.0.0.0', 80])
socket.listen(1)
print("Connected to %s, IPv4 Addr: " % secrets["ssid"], wifi.radio.ipv4_address)

while True:
    ampule.listen(socket)