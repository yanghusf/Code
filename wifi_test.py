import pywifi

def Check_state():
    wifi = pywifi.PyWiFi()
    ifaces = wifi.interfaces()[0]
    result = ifaces.scan_results()
    for data in result:
        print(data.ssid)
        print(data.akm[0])

Check_state()