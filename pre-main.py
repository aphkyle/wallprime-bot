import threading
import time
import io

import cv2
import numpy as np
import pytesseract
from PIL import Image
from ppadb.client import Client as AdbClient

"""
the coordinates in your device might be different
be sure to modify the variable `number`
the following position is only for insane mode
"""

GREY_HIGH = np.array([20, 20, 20])
GREY_LOW = np.array([190, 190, 190])

numbers = {
    2: (100, 1095),
    11: (100, 1195),
    23: (100, 1295),
    41: (100, 1395),
    3: (200, 1095),
    13: (200, 1195),
    29: (200, 1295),
    43: (200, 1395),
    5: (300, 1095),
    17: (300, 1195),
    31: (300, 1295),
    47: (300, 1395),
    7: (400, 1095),
    19: (400, 1195),
    37: (400, 1295),
    53: (400, 1395),
}

def _ocr(device):
    b = np.array(np.frombuffer(io.BytesIO(device.screencap())).crop(
                    (165, 370, 665, 900)
            ).convert("RGB"))
     
    hsv = cv2.cvtColor(b, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, GREY_LOW, GREY_HIGH)
    b[mask > 0] = (17, 17, 19)


    result = ''.join(filter(str.isdigit, pytesseract.image_to_string(
                Image.fromarray(b),
                lang="eng",
                config="--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789",
            )
        )
    )

    cv2.imwrite('testing.png', b) # this line is for testing, you can remove if you wanted to

    return int(result) if result != "" else _ocr(device)

def prime_tap(device, n):
    threads = []
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            if d in numbers:
                n2 = numbers[d]
                t = threading.Thread(target=device.shell, args=(f"input tap {n2[0]} {n2[1]}",))
                threads.append(t)
                t.start()
            else:
                return
            n //= d
        d += 1
    if n > 1:
        if n in numbers:
            n2 = numbers[n]
            t = threading.Thread(target=device.shell, args=(f"input tap {n2[0]} {n2[1]}",))
            threads.append(t)
            t.start()
        else:
            return
    for thread in threads:
        thread.join()
    device.shell("input tap 600 1335",)

def main():
    client = AdbClient()

    device = client.devices()
    device = device[0]

    input() # press enter

    while True:
        try:
            result = _ocr(device)
            print(result)
            prime_tap(device, result)
            time.sleep(2.6)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(e.__class__.__name__, e)

main()
