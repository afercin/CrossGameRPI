from tv.baseTV import *
COOKIES = "//a[contains(text(), 'ACEPTAR Y CERRAR')]"
READY = "//div[@id='root']"

PLAY_BUTTON = "//p[text()='Continuar Directo']/preceding-sibling::button"


class atresplayerTV(tv):
    def __init__(self, driver):
        super().__init__(driver)
        self.COOKIES = COOKIES
        self.READY = READY

    def setChannel(self, url):
        super().setChannel(url)

        self.clickElement(PLAY_BUTTON)

        pyautogui.moveTo(1920, 540)
