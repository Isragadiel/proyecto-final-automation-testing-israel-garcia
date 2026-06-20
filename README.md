# Framework de Automatización de Pruebas - Trabajo Final Integrador

Este proyecto consiste en el desarrollo de un framework de automatización de pruebas de extremo a extremo (E2E) robusto y mantenible, desarrollado en **Python**. Implementa pruebas funcionales de interfaz de usuario (UI) sobre la plataforma **SauceDemo** y pruebas de servicios backend (API) utilizando la plataforma **ReqRes**.

El diseño del framework sigue las mejores prácticas de la industria, aplicando patrones arquitectónicos como **Page Object Model (POM)**, inyección de datos externa, generación de reportes interactivos y pipelines de **Integración Continua (CI/CD)**.

---

## 🛠️ Tecnologías y Herramientas Utilizadas

* **Lenguaje Base:** Python 3.11+
* **Framework de Testing:** Pytest (gestión de suites, fixtures y parametrización)
* **Automatización de UI:** Selenium WebDriver (interacción avanzada con elementos web)
* **Pruebas de API:** Requests (consumo y validación de endpoints REST)
* **Reportabilidad:** Pytest-HTML (generación de dashboards interactivos con screenshots embebidos)
* **Control de Versiones y CI/CD:** Git, GitHub y GitHub Actions

---

## 📂 Estructura General del Proyecto

```text
├── .github/workflows/
│   └── pytest-ci.yml         # Pipeline de automatización en la nube (CI/CD)
├── data/
│   └── usuarios_login.json   # Datos externos para escenarios de login (Positivos/Negativos)
├── logs/
│   └── suite_ejecucion.log   # Historial transaccional de pasos de ejecuciones
├── pages/                    # Componentes del patrón Page Object Model (POM)
│   ├── base_page.py          # Envolturas de Selenium y esperas explícitas
│   ├── login_page.py         # Elementos y acciones de la página de Login
│   └── inventory_page.py     # Elementos y acciones del catálogo de productos
├── reports/                  # Reportes generados automáticamente
│   ├── reporte_final.html    # Dashboard interactivo final
│   └── screenshots/          # Capturas de pantalla generadas automáticamente ante fallos
├── tests/                    # Definición de Casos de Prueba independientes
│   ├── test_ui_saucedemo.py  # Suite de interfaz de usuario (5 casos automatizados)
│   └── test_api_reqres.py    # Suite de API con encadenamiento de peticiones (3 casos)
├── utils/
│   └── logger_config.py      # Configuración del sistema de Logging dual (consola/archivo)
├── conftest.py               # Fixtures globales de Selenium y Hooks de captura de pantalla
├── pytest.ini                # Configuración global y flags de Pytest
└── requirements.txt          # Lista de dependencias del proyecto

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/usuario/proyecto-final-automation-testing-israel-garcia.git
cd proyecto-final-automation-testing-israel-garcia
```

Crear entorno virtual:

```bash
python -m venv .venv
```

Activar entorno:

```bash
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución de Pruebas

Ejecutar todas las pruebas:

```bash
pytest
```

Ejecutar solo UI:

```bash
pytest -m ui
```

Ejecutar solo API:

```bash
pytest -m api
```

## Reportes

Al finalizar la ejecución se genera:

```text
reports/reporte_final.html
```

El reporte muestra:

- Casos ejecutados
- Estado (Pass/Fail)
- Tiempo de ejecución
- Logs de error
- Capturas de pantalla automáticas para pruebas fallidas