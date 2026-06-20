from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class InventoryPage(BasePage):
    # Selectores (Locators)
    LBL_TITULO_PAGINA = (By.CSS_SELECTOR, ".title")
    BTN_AGREGAR_MOCHILA = (By.ID, "add-to-cart-sauce-labs-backpack")
    BTN_AGREGAR_REMERA = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    LBL_CONTADOR_CARRITO = (By.CSS_SELECTOR, ".shopping_cart_badge")
    BTN_CARRITO = (By.CSS_SELECTOR, ".shopping_cart_link")

    def __init__(self, driver):
        super().__init__(driver)

    def obtener_titulo_pagina(self):
        return self.obtener_texto(self.LBL_TITULO_PAGINA)

    def agregar_productos_al_carrito(self):

        self.hacer_clic(self.BTN_AGREGAR_MOCHILA)
        self.hacer_clic(self.BTN_AGREGAR_REMERA)

    def obtener_cantidad_carrito(self):
        return self.obtener_texto(self.LBL_CONTADOR_CARRITO)

    def ir_al_carrito(self):
        self.hacer_clic(self.BTN_CARRITO)