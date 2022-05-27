from tv.baseTV import *
import pyautogui
COCKIES = "//button[contains(@id, 'onetrust-accept')]"
FULL_SCREEN_BUTTON = "//button[contains(@class, 'fullscreen')]"
CONTROL_BAR = "//div[contains(@class, 'vjs-control-bar')]"
VOLUME_MUTED = "//span[contains(text(), 'Activar volumen')]/parent::button"


class rtveTV(tv):
    def __init__(self, driver):
        super().__init__(driver)
        self.firstTime = True

    def setChannel(self, url):
        print(f"[INFO] Setting url: {url}")
        self.driver.get(url)

        while not self.isElementVisible(COCKIES) and self.firstTime:
            pass
        if self.firstTime:
            self.clickElement(COCKIES)

        self.firstTime = False
        self.clickElement(CONTROL_BAR)
        self.clickElement(VOLUME_MUTED)
        self.clickElement(FULL_SCREEN_BUTTON)
        pyautogui.moveTo(1920, 540)
