import time

import bs4, requests, cv2
import numpy
import pyautogui
from PIL import Image
from ppadb.client import Client as AdbClient
from io import BytesIO
from pyrect import Box

device = None

def scrapeCodes():
    req = requests.get("http://www.googolexikon.de/socialgamingnetworksites/downtownmafia/")
    bs = bs4.BeautifulSoup(req.content, "html.parser")
    codes = []
    for value_set in [str(val).split("</td>") for val in bs.find_all("tr") if str(val).startswith("<tr><td>")]:
        for raw_value in value_set:
            if "<b>" and "</b>" in raw_value:
                value = raw_value[raw_value.find("<b>")+3:raw_value.find("</b>")]
                if value.isdigit():
                    codes.append(value)

    return codes

def getLocationFromBackground(image_location, update_background=False, device=None):
    if update_background:
        image = Image.open(BytesIO(device.screencap()))
        image.save("screenshot.png")

    search_image = cv2.imread(image_location)

    _, _, mnLoc, _ = cv2.minMaxLoc(cv2.matchTemplate(search_image, cv2.imread("screenshot.png"), cv2.TM_SQDIFF_NORMED))

    boxed_loc = Box(*mnLoc, len(search_image[0]), len(search_image))

    return boxed_loc.left + (boxed_loc.width // 2), boxed_loc.top + (boxed_loc.height // 2)


def startInjection():
    codes = scrapeCodes()
    client = AdbClient()

    device = None
    if len(codes) > 0:
        if len(client.devices()) == 1:
            device = client.devices()[0]


    if device is not None:
        box_input_location = getLocationFromBackground(image_location="mobbox.png", update_background=True, device=device)
        inv_input_location = getLocationFromBackground(image_location="invitebox.png")

        remove_input_location = None
        codes_entered = 0
        if box_input_location is not None and inv_input_location is not None:
            for code in codes:
                print("Currently entered {} codes".format(codes_entered))
                # select the box & input text
                device.input_tap(*box_input_location)
                device.input_text(code)
                time.sleep(1)

                # select the invite location
                device.input_tap(0, 0)
                device.input_tap(*inv_input_location)
                time.sleep(1)

                # (get remove input location if not set &) remove the input.
                if remove_input_location is None:
                    remove_input_location = getLocationFromBackground("removeinput.png", update_background=True, device=device)

                device.input_tap(*remove_input_location)
                time.sleep(0.2)
                device.input_tap(0, 0)
                time.sleep(0.2)
                codes_entered += 1

startInjection()
