from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs

class Scraper:
    driver: WebDriver
    wait: WebDriverWait[WebDriver]
    initialized: bool = False
    push_approved: bool = False
    qr_approved: bool = False

    def __init__(self):
        if not self.initialized:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("detach", True)  # pyright: ignore[reportUnknownMemberType]

            self.driver = webdriver.Chrome(options=options)
            self.driver.get("http://www.tributi.regione.lombardia.it/Portale/")

            self.wait = WebDriverWait(self.driver, 30)
            self.initialized = True

    def get_cie_page_elements(self) -> dict[str, str]:
        if self.driver.current_url == "https://idpcwrapper.crs.lombardia.it/PublisherMetadata/SSOService":
            cie_login_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form[action='AuthRequestCieService']")))
            cie_login_btn.click()

            qr_img = self.wait.until(EC.presence_of_element_located((
                By.CSS_SELECTOR, "figure#qrFigure img"
            )))
            qr_str = qr_img.get_attribute("src")  # pyright: ignore[reportUnknownMemberType]

            parsed_url = urlparse(self.driver.current_url)
            url_args = parse_qs(parsed_url.query)

            opId = url_args.get('opId', [None])[0]
            challenge = url_args.get('challenge', [None])[0]


            return {
                "qr_str": qr_str or "",
                "opId": opId or "",
                "challenge": challenge or ""
            }

        return {}

    def qr_approve(self, timeout:int):
        wait_qr = WebDriverWait(self.driver, timeout)
        try:
            btn = wait_qr.until(
                    EC.visibility_of_element_located((By.NAME, "_eventId_proceed"))
            )

            btn.click()
            self.qr_approved = True
        except TimeoutError:
            pass


    def perform_login(self, username:str, password:str) -> bool:
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.clear()
        username_field.send_keys(username)

        password_field = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        password_field.clear()
        password_field.send_keys(password)

        proceed_btn = self.driver.find_element(By.CSS_SELECTOR, "form#loginUP button[type='submit']")
        proceed_btn.click()

        # wait for either success or failure
        _ = self.wait.until(EC.any_of(
            EC.staleness_of(proceed_btn), # success: button is not there anymore
            EC.visibility_of_element_located((By.ID, "statusHandlerMsg"))
        ))

        # now that we know we either got success or failure, we check if we find the failure element
        errors = self.driver.find_elements(By.ID, "statusHandlerMsg")
        # if there is an error, credentials were not valid
        if len(errors) > 0:
            return False

        return True

    def approve(self, timeout:int):
        wait_notification = WebDriverWait(self.driver, timeout)

        try:
            btn = wait_notification.until(
                    EC.visibility_of_element_located((By.NAME, "_eventId_proceed"))
            )

            btn.click()
            self.push_approved = True
        except TimeoutError:
            print("User did not approve push notification!")
