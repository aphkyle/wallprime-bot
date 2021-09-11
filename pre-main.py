import threading
import asyncio
import io

import pytesseract
from PIL import Image
from ppadb.client_async import ClientAsync as AdbClient


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


async def main():
    client = AdbClient()

    device = await client.devices()
    device = device[0]

    input()

    while True:
        try:
            result = int(
                pytesseract.image_to_string(
                    Image.open(io.BytesIO(await device.screencap())).crop(
                        (167, 374, 665, 928)
                    ),
                    config="outputbase nobatch digits --psm 6 --oem 3 -c tessedit_char_whitelist=0123456789",
                ),
            )
            print(result)
            for n in primes(result):
                threading.Thread(
                    target=asyncio.run,
                    args=(device.shell(f"input tap {(n := numbers[n])[0]} {n[1]}"),),
                ).start()
            await device.shell(f"input tap 600 1335")
            await asyncio.sleep(3)
        except Exception as e:
            print(type(e), e)


asyncio.run(main())

input()
