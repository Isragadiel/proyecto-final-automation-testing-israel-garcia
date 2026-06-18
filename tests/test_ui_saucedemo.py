import json
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.logger_config import get_logger

# Inicializamos el logger para el reporte de ejecución de UI
log = get_logger("Test_UI_SauceDemo")

def cargar_datos_login():
    """Función utilitaria para leer los usuarios desde el archivo JSON externo."""
    with open("data/usuarios_login.json", "r") as archivo:
        return json.load(archivo)

@pytest.mark.ui
class TestSauceDemo:

    # -------------------------------------------------------------------------
    # PRUEBAS 1, 2 y 3: Parametrización con JSON (Casos Exitosos y Negativos)
    # -------------------------------------------------------------------------
    @pytest.mark.parametrize("data", cargar_datos_login())
    def test_login_flujos(self, driver, data):
        """
        Valida dinámicamente el comportamiento del login ante usuarios
        válidos, bloqueados e inexistentes (Cubre el requerimiento de fuente externa).
        """
        log.info(f"--- Iniciando test_login_flujos con usuario: {data['usuario']} ---")
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        
        login_page.ingresar_a_la_plataforma()
        login_page.iniciar_sesion(data["usuario"], data["clave"])
        
        if data["debe_funcionar"]:
            # Aserción camino feliz
            assert inventory_page.obtener_titulo_pagina() == "Products", "Error: No se redirigió al catálogo."
            log.info("Acceso verificado exitosamente.")
        else:
            # Aserción escenario negativo (Manejo de errores visibles)
            mensaje_error = login_page.obtener_mensaje_error()
            assert "Epic sadface:" in mensaje_error, f"Error: No se mostró alerta de bloqueo/error esperado. Texto real: {mensaje_error}"
            log.info(f"Escenario negativo validado correctamente. Alerta capturada: {mensaje_error}")

    # -------------------------------------------------------------------------
    # PRUEBA 4: Validación de Elementos del Catálogo
    # -------------------------------------------------------------------------
    def test_verificar_catalogo_visible(self, driver):
        """Valida que un usuario logueado visualice la cabecera correcta del inventario."""
        log.info("--- Iniciando test_verificar_catalogo_visible ---")
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        
        login_page.ingresar_a_la_plataforma()
        login_page.iniciar_sesion("standard_user", "secret_sauce")
        
        titulo = inventory_page.obtener_titulo_pagina()
        assert titulo == "Products", f"El título de la página no coincide, se obtuvo: {titulo}"
        log.info("Encabezado del catálogo verificado correctamente.")

    # -------------------------------------------------------------------------
    # PRUEBA 5: Añadir Productos y Flujo de Carrito
    # -------------------------------------------------------------------------
    def test_agregar_productos_al_carrito(self, driver):
        """Valida que al clickear productos el contador del carrito se actualice en tiempo real."""
        log.info("--- Iniciando test_agregar_productos_al_carrito ---")
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        
        login_page.ingresar_a_la_plataforma()
        login_page.iniciar_sesion("standard_user", "secret_sauce")
        
        # Ejecutamos acciones definidas en el POM
        inventory_page.agregar_productos_al_carrito()
        
        # Validamos que el contador de la interfaz marque exactamente "2"
        cantidad = inventory_page.obtener_cantidad_carrito()
        assert cantidad == "2", f"Se esperaban 2 productos en el carrito, pero figura: {cantidad}"
        log.info("Contador del carrito validado con éxito (2 productos).")