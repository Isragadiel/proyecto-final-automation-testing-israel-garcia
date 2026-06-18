import pytest
import requests
from utils.logger_config import get_logger

# Inicializamos el logger para el reporte de API
log = get_logger("Test_API_ReqRes")

@pytest.mark.api
class TestReqResAPI:
    URL_BASE = "https://reqres.in/api"

    # -------------------------------------------------------------------------
    # PRUEBA 1: Método GET - Validar lista de usuarios y estructura JSON
    # -------------------------------------------------------------------------
    def test_obtener_usuarios_page2(self):
        """Valida que la consulta de usuarios retorne un código 200 y campos consistentes."""
        log.info("--- Iniciando test_obtener_usuarios_page2 (GET) ---")
        url = f"{self.URL_BASE}/users?page=2"
        
        respuesta = requests.get(url)
        log.info(f"Status Code recibido: {respuesta.status_code}")
        
        # Validaciones principales
        assert respuesta.status_code == 200, f"Se esperaba 200 pero se obtuvo {respuesta.status_code}"
        
        # Validar estructura y contenido del JSON
        datos_json = respuesta.json()
        assert "page" in datos_json, "Falta el campo 'page' en la respuesta"
        assert "data" in datos_json, "Falta el campo 'data' en la respuesta"
        assert len(datos_json["data"]) > 0, "La lista de usuarios en 'data' llegó vacía"
        
        # Validar tipo de datos de un elemento
        primer_usuario = datos_json["data"][0]
        assert "email" in primer_usuario, "El usuario no contiene la clave 'email'"
        log.info(f"Primer usuario validado con éxito: {primer_usuario['email']}")

    # -------------------------------------------------------------------------
    # PRUEBA 2: Método POST - Crear un nuevo recurso
    # -------------------------------------------------------------------------
    def test_crear_usuario(self):
        """Valida que el envío de un payload válido cree un recurso y retorne un 201."""
        log.info("--- Iniciando test_crear_usuario (POST) ---")
        url = f"{self.URL_BASE}/users"
        payload = {
            "name": "Israel Garcia",
            "job": "QA Automation Engineer"
        }
        
        respuesta = requests.post(url, json=payload)
        log.info(f"Status Code recibido: {respuesta.status_code}")
        
        assert respuesta.status_code == 201, f"Se esperaba 201 pero se obtuvo {respuesta.status_code}"
        
        datos_json = respuesta.json()
        assert datos_json["name"] == payload["name"], "El nombre guardado no coincide con el enviado"
        assert datos_json["job"] == payload["job"], "El puesto guardado no coincide con el enviado"
        assert "id" in datos_json, "El servidor no generó un 'id' para el nuevo registro"
        log.info(f"Usuario registrado de forma exitosa. ID asignado: {datos_json['id']}")

    # -------------------------------------------------------------------------
    # PRUEBA 3: Encadenamiento de Peticiones y Método DELETE (Opcional Avanzado)
    # -------------------------------------------------------------------------
    def test_ciclo_vida_usuario_encadenado(self):
        """
        Flujo de Integración: Crea un usuario (POST), extrae su ID
        y procede a eliminarlo (DELETE). Satisface el encadenamiento de peticiones.
        """
        log.info("--- Iniciando test_ciclo_vida_usuario_encadenado (POST -> DELETE) ---")
        
        # FASE 1: Crear el usuario
        url_creacion = f"{self.URL_BASE}/users"
        payload = {"name": "Usuario Temporal", "job": "Tester"}
        
        respuesta_post = requests.post(url_creacion, json=payload)
        assert respuesta_post.status_code == 201, "Falló la fase de creación del usuario en el flujo encadenado"
        
        # Extraemos el ID dinámicamente del cuerpo de la respuesta
        nuevo_id = respuesta_post.json()["id"]
        log.info(f"Encadenamiento: ID capturado dinámicamente -> {nuevo_id}")
        
        # FASE 2: Eliminar el usuario utilizando el ID obtenido
        url_eliminacion = f"{self.URL_BASE}/users/{nuevo_id}"
        log.info(f"Enviando solicitud DELETE a: {url_eliminacion}")
        
        respuesta_delete = requests.delete(url_eliminacion)
        log.info(f"Status Code recibido en eliminación: {respuesta_delete.status_code}")
        
        # Validar código estándar internacional de eliminación exitosa (204 No Content)
        assert respuesta_delete.status_code == 204, f"Se esperaba 204, se obtuvo {respuesta_delete.status_code}"
        
        # Validar tiempo de respuesta / SLA de rendimiento menor a 1.5 segundos
        tiempo_respuesta = respuesta_delete.elapsed.total_seconds()
        log.info(f"Tiempo de respuesta del servidor: {tiempo_respuesta} segundos")
        assert tiempo_respuesta < 1.5, f"La API demoró demasiado en procesar el DELETE: {tiempo_respuesta}s"
        log.info("Flujo completo de encadenamiento e integración de API finalizado con éxito.")