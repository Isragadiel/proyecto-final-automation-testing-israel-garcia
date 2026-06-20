from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.logger_config import get_logger


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.log = get_logger(self.__class__.__name__)

    def abrir_url(self, url):
        self.log.info(f"Navegando a: {url}")
        self.driver.get(url)

    def encontrar_elemento(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def hacer_clic(self, locator):
        self.log.info(f"Haciendo clic en el elemento con selector: {locator}")

        elemento = self.wait.until(
            EC.element_to_be_clickable(locator)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);",
            elemento
        )

        self.driver.execute_script(
            "arguments[0].click();",
            elemento
        )

    def escribir(self, locator, texto):
        self.log.info(f"Escribiendo '{texto}' en el elemento: {locator}")

        elemento = self.encontrar_elemento(locator)
        elemento.clear()
        elemento.send_keys(texto)

    def obtener_texto(self, locator):
        texto = self.encontrar_elemento(locator).text
        self.log.info(f"Texto obtenido del elemento {locator}: '{texto}'")
        return texto