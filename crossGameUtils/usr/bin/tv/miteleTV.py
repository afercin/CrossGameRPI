from tv.baseTV import *
COOKIES = "//span[text()='Aceptar']/parent::button"
READY = "//ins[@data-ad-status='unfilled']"

PLAY_BUTTON = "//div[contains(@class, 'infoText__offerContentBlock-2Kxm')]/button[contains(@class, 'playCircle__button-LMT8')]"


class miteleTV(tv):
    def __init__(self, driver):
        super().__init__(driver)
        self.COOKIES = COOKIES
        self.READY = READY

    def setChannel(self, url):
        super().setChannel(url)
        
        # Click on block notifications
        pyautogui.click(230, 105)
        self.clickElement(PLAY_BUTTON)

        pyautogui.moveTo(1920, 540)
