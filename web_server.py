import network


def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Connecting to WiFi SSID: {ssid} ...")
        wlan.connect(ssid, password)
        # Wait for connection with timeout
        import time

        timeout = 10  # seconds
        start = time.time()
        while not wlan.isconnected():
            if time.time() - start > timeout:
                print("Failed to connect to WiFi: Timeout")
                return False
            time.sleep(1)
    print("WiFi is connected")
    print("Network config:", wlan.ifconfig())
    return True


if __name__ == "__main__":
    try:
        ssid = "your_wifi_ssid"
        password = "your_wifi_password"
        connect_wifi(ssid, password)
    except Exception as e:
        print(f"Error connecting to WiFi: {e}")
