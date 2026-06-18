import os
import pytest
from datetime import datetime
from selenium import webdriver
from utils.logger_config import get_logger

# Inicializamos el logger para este archivo
log = get_logger("Conftest")

@pytest.fixture(scope="function")
def driver():
    """
    Fixture que inicializa el navegador. Activa el modo Headless de forma
    automática si detecta que la prueba se ejecuta en el entorno de GitHub Actions.
    """
    log.info("Iniciando el navegador Chrome para la prueba...")
    options = webdriver.ChromeOptions()
    
    # Si detecta que corre en la nube de GitHub Actions, usa modo Headless sin pantalla
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    else:
        # Si corre en tu computadora, abre la ventana maximizada normalmente
        options.add_argument("--start-maximized")
    
    options.add_argument("--disable-extensions")
    
    driver = webdriver.Chrome(options=options)
    
    yield driver
    
    log.info("Cerrando el navegador.")
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook de Pytest que intercepta el resultado de la prueba.
    Si el test falla en la fase de ejecución ('call') y utiliza Selenium,
    toma una captura de pantalla y la adjunta al reporte HTML de manera automática.
    """
    outcome = yield
    report = outcome.get_result()
    
    # Validamos si la prueba falló en su ejecución principal
    if report.when == "call" and report.failed:
        # Verificamos si el test que falló estaba usando la fixture 'driver'
        if "driver" in item.funcargs:
            driver_instance = item.funcargs["driver"]
            
            # Crear la carpeta de capturas si no existe
            carpeta_screenshots = os.path.join("reports", "screenshots")
            os.makedirs(carpeta_screenshots, exist_ok=True)
            
            # Estructurar nombre descriptivo: nombre_del_test_fecha_hora.png
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"{item.name}_{timestamp}.png"
            ruta_completa = os.path.join(carpeta_screenshots, nombre_archivo)
            
            # Guardar la captura física en el disco
            driver_instance.save_screenshot(ruta_completa)
            log.error(f"❌ TEST FALLIDO: Captura de pantalla guardada en {ruta_completa}")
            
            # Incrustar el screenshot de forma nativa en el reporte HTML generado por pytest-html
            html = item.config.pluginmanager.getplugin("html")
            if html:
                # Usamos la ruta relativa para que el HTML pueda renderizar la imagen correctamente
                ruta_relativa_html = f"screenshots/{nombre_archivo}"
                extra = html.extras.image(ruta_relativa_html)
                report.extra = getattr(report, "extra", [])
                report.extra.append(extra)