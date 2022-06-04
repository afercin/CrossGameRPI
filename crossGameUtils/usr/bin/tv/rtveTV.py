from tv.baseTV import *
COOKIES = "//button[contains(@id, 'onetrust-accept')]"
READY = "//div[contains(@class, 'vjs-playing')]"

CONTROL_BAR = "//div[contains(@class, 'vjs-control-bar')]"
VOLUME_MUTED = "//span[contains(text(), 'Activar volumen')]/parent::button"
FULL_SCREEN_BUTTON = "//button[contains(@class, 'fullscreen')]"


class rtveTV(tv):
    def __init__(self, driver):
        super().__init__(driver)
        self.COOKIES = COOKIES
        self.READY = READY

    def setChannel(self, url):
        super().setChannel(url)

        self.clickElement(VOLUME_MUTED)
        self.clickElement(FULL_SCREEN_BUTTON)

        pyautogui.moveTo(1920, 540)
