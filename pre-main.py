from abc import abstractproperty
from concurrent.futures.thread import ThreadPoolExecutor
import asyncio
import io

import pytesseract
import numpy as np
from PIL import Image
from ppadb.client_async import ClientAsync as AdbClient

class BruhError(Exception):
    ...

def primes(n):
    primfac = []
    d = 2
    while d * d <= n:
        while (n % d) == 0:
            primfac.append(d)
            n //= d
        d += 1
    if n > 1:
        primfac.append(n)
    return primfac


"""
the coordinates in your device might be different
be sure to modify the variable `number`
the following position is only for insane mode
"""

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

async def img(device):
    pil_image = Image.open('Image.jpg').convert('RGB') 
    open_cv_image = np.array(pil_image) 
    open_cv_image = open_cv_image[:, :, ::-1].copy() 

async def _ocr(device):
    result = pytesseract.image_to_string(
                Image.open(io.BytesIO(await device.screencap())).crop(
                    (165, 370, 665, 730)
                ),
                config="nobatch digits -l eng --oem 3 --psm 6 -c tessedit_char_whitelist=0123456789",
                )
    return int(''.join(filter(str.isdigit, result))) if result != "" else _ocr(device)

async def main():
    client = AdbClient()

    device = await client.devices()
    device = device[0]

    input()

    while True:
        try:
            result = await _ocr(device)
            print(result)
            p = primes(result)
            with ThreadPoolExecutor() as executor:
                for n in p:
                    if n not in numbers.keys():
                        print("bruh")
                        raise BruhError("Ignore this error, this only happens when number from _ocr is wrong")
                    n2 = numbers[n]
                    executor.submit(asyncio.run, device.shell(f"input tap {n2[0]} {n2[1]}"))
            await device.shell(f"input tap 600 1335")
            await asyncio.sleep(1.7)
        except Exception as e:
            print(e.__class__.__name__, e)

asyncio.run(main())

input()
