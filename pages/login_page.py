from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Selectores (Locators)
    TXT_USUARIO = (By.ID, "user-name")
    TXT_CLAVE = (By.ID, "password")
    BTN_LOGIN = (By.ID, "login-button")
    LBL_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.saucedemo.com/"

    def ingresar_a_la_plataforma(self):
        self.abrir_url(self.url)

    def iniciar_sesion(self, usuario, clave):
        self.escribir(self.TXT_USUARIO, usuario)
        self.escribir(self.TXT_CLAVE, clave)
        self.hacer_clic(self.BTN_LOGIN)

    def obtener_mensaje_error(self):
        return self.obtain_text(self.LBL_ERROR) if self.obtener_texto(self.LBL_ERROR) else ""