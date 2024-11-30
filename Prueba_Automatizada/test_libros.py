import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

@pytest.fixture(scope="session")  # Cambiar el alcance a "session"
def driver():
    print("Iniciando el navegador Edge...")
    # Configurar Edge
    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    driver.maximize_window()
    yield driver
    print("Cerrando el navegador Edge...")
    driver.quit()

@pytest.fixture(scope="module")
def open_page(driver):
    # Accede a la URL solo una vez antes de todas las pruebas en el módulo
    driver.get("http://127.0.0.1:5500/Gestor_Libros/index.html")
    yield driver  # Esto permite que las pruebas se ejecuten sin recargar la página
    # No es necesario hacer nada después, ya que no necesitamos recargar la página entre las pruebas

# Ruta para el reporte HTML
@pytest.fixture(scope="session")  # Cambiar el alcance a "session"
def report_path():
    path = os.path.join(os.getcwd(), "reporte_resultados.html")
    with open(path, "w") as reporte:
        reporte.write("<html><head><title>Reporte de Pruebas Automatizadas</title></head><body>")
        reporte.write("<h1>Resultados de Pruebas Automatizadas</h1>")
        reporte.write("<table border='1' style='width:100%;border-collapse:collapse;'>")
        reporte.write("<tr><th>Historia</th><th>Resultado</th><th>Detalle</th><th>Captura</th></tr>")
    yield path
    with open(path, "a") as reporte:
        reporte.write("</table></body></html>")

# Fixture para cerrar el navegador y finalizar el reporte al finalizar las pruebas
@pytest.fixture(scope="session", autouse=True)
def finalize_report(driver, report_path):
    yield  # Esto permite que todas las pruebas se ejecuten primero
    # Cerrar el navegador
    driver.quit()
    # Finalizar el reporte HTML
    with open(report_path, "a") as reporte:
        reporte.write("</table></body></html>")

def tomar_captura(driver, nombre):
    path = os.path.join(os.getcwd(), nombre)
    driver.save_screenshot(path)
    return nombre

def agregar_a_reporte(report_path, historia, resultado, detalle, captura=None):
    with open(report_path, "a") as reporte:
        reporte.write(f"<tr><td>{historia}</td><td>{resultado}</td><td>{detalle}</td>")
        if captura:
            reporte.write(f"<td><a href='{captura}' target='_blank'>Ver Captura</a></td>")
        else:
            reporte.write("<td>No disponible</td>")
        reporte.write("</tr>")



@pytest.mark.order(1)
def test_registro_usuario(driver, report_path, open_page):
    # Solo se hace driver.get() una vez gracias a la fixture open_page
    register_link = driver.find_element(By.ID, "show-register")
    register_link.click()

    time.sleep(2)

    # Localizar los elementos
    rname_input = driver.find_element(By.ID, "rname")
    remail_input = driver.find_element(By.ID, "remail")
    rpassword_input = driver.find_element(By.ID, "rpassword")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit' and text()='Registrarse']")

    # Ingresar los datos en los campos de texto
    rname_input.send_keys("nuevo usuario")
    remail_input.send_keys("nuevo@gmail.com")
    rpassword_input.send_keys("Djth2712")

    # Esperar a que el botón sea clickeable y luego hacer clic
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(submit_button)).click()

    # Esperar que el formulario de inicio de sesión sea visible
    formulario_inicio = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "login-form"))
    )

    # Tomar la captura de pantalla
    captura = tomar_captura(driver, "registro_exitoso.png")

    # Verificar que el formulario de inicio de sesión se mostró
    assert formulario_inicio.is_displayed(), "No se mostró el formulario de inicio de sesión tras registrar el usuario."

    # Agregar los resultados al reporte
    agregar_a_reporte(report_path, "Prueba 1", "Éxito", "Registro de usuario exitoso.", captura)


@pytest.mark.order(2)
def test_login_exitoso(driver, report_path, open_page):
    time.sleep(2)

    driver.find_element(By.ID, "email").send_keys("nuevo@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Djth2712")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    time.sleep(2)

    formulario_agregarlibros = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "book-form"))
    )

    captura = tomar_captura(driver, "login_exitoso.png")

    assert formulario_agregarlibros.is_displayed(), "No se mostró el formulario de agregar libros tras iniciar sesión"
    
    agregar_a_reporte(report_path, "Prueba 2", "Éxito", "Inicio de sesión exitoso.", captura)

@pytest.mark.order(3)
def test_agregar_libro_correctamente(driver, report_path, open_page):
    driver.get("http://127.0.0.1:5500/Gestor_Libros/index.html")  
    time.sleep(2)  # Esperar para que la página de login cargue completamente
    
    # Realizar el login
    driver.find_element(By.ID, "email").send_keys("nuevo@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Djth2712")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    time.sleep(2)  # Esperar a que la página cargue después del login
    
    # Verificar que el login fue exitoso, por ejemplo, buscando un elemento específico
    formulario_agregarlibros = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "book-form"))
    )
    
    # Agregar libro
    driver.find_element(By.ID, "title").send_keys("Libro de Prueba")
    driver.find_element(By.ID, "author").send_keys("Autor de Prueba")
    driver.find_element(By.ID, "description").send_keys("Descripción de prueba para el libro.")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    time.sleep(2)  # Esperar a que el libro se agregue

    # Verificar que el mensaje de éxito aparezca
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message-container"))
    )

    captura = tomar_captura(driver, "agregar_libro.png")
    assert 'El libro "Libro de Prueba" fue agregado correctamente.', "El mensaje de éxito no se mostró correctamente."
    # Agregar reporte de la prueba
    agregar_a_reporte(report_path, "Prueba 3", "Éxito", "Libro agregado correctamente.", captura)


@pytest.mark.order(4)
def test_agregar_libro_con_campos_vacios(driver, report_path, open_page):
    driver.get("http://127.0.0.1:5500/Gestor_Libros/index.html")  
    time.sleep(2)  # Esperar para que la página de login cargue completamente
    
    # Realizar el login
    driver.find_element(By.ID, "email").send_keys("nuevo@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Djth2712")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    time.sleep(2)  # Esperar a que la página cargue después del login
    
    # Verificar que el login fue exitoso, por ejemplo, buscando un elemento específico
    formulario_agregarlibros = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "book-form"))
    )

    time.sleep(3)

    driver.find_element(By.XPATH, "//input[@type='submit']").click()
   
    time.sleep(2)
    # Verificar que el mensaje de error aparezca
    error_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "message-container"))
    )

    captura = tomar_captura(driver, "agregar_libro_campos_vacios.png")
    assert "Por favor, completa todos los campos.", "El mensaje de error no se mostró correctamente."

    agregar_a_reporte(report_path, "Prueba 4", "Éxito", "Error mostrado al dejar campos vacíos.", captura)

@pytest.mark.order(5)
def test_eliminar_libro(driver, report_path, open_page):
    driver.get("http://127.0.0.1:5500/Gestor_Libros/index.html")  
    time.sleep(2)  # Esperar para que la página de login cargue completamente
    
    # Realizar el login
    driver.find_element(By.ID, "email").send_keys("nuevo@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Djth2712")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    time.sleep(2)  # Esperar a que la página cargue después del login
    
    # Verificar que el login fue exitoso, por ejemplo, buscando un elemento específico
    formulario_agregarlibros = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "book-form"))
    )

    driver.find_element(By.ID, "title").send_keys("Libro para Eliminar")
    driver.find_element(By.ID, "author").send_keys("Autor para Eliminar")
    driver.find_element(By.ID, "description").send_keys("Descripción para eliminar el libro.")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()

    time.sleep(2)
    # Esperar hasta que el contenedor de botones sea visible
    button_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "book-item-buttons"))
    )

    # Encontrar el botón específico dentro del contenedor
    delete_button = button_container.find_element(By.CLASS_NAME, "delete-button")

    # Hacer clic en el botón de eliminar
    delete_button.click()

    time.sleep(2)
    captura = tomar_captura(driver, "eliminar_libro.png")

    # Verificar que el libro haya sido eliminado
    books = driver.find_elements(By.CSS_SELECTOR, ".book-item")
    assert "Libro para Eliminar" not in [book.text for book in books], "El libro no fue eliminado correctamente."

    agregar_a_reporte(report_path, "Prueba 5", "Éxito", "Libro eliminado correctamente.", captura)

@pytest.mark.order(6)
def test_buscar_libro(driver, report_path, open_page):
    driver.get("http://127.0.0.1:5500/Gestor_Libros/index.html")  
    time.sleep(2)  # Esperar para que la página de login cargue completamente
    
    # Realizar el login
    driver.find_element(By.ID, "email").send_keys("nuevo@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Djth2712")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    time.sleep(2)  # Esperar a que la página cargue después del login
    
    # Verificar que el login fue exitoso, por ejemplo, buscando un elemento específico
    formulario_agregarlibros = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "book-form"))
    )

    driver.find_element(By.ID, "title").send_keys("Libro de Búsqueda")
    driver.find_element(By.ID, "author").send_keys("Autor de Búsqueda")
    driver.find_element(By.ID, "description").send_keys("Descripción para buscar el libro.")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()

    time.sleep(2)

    search_input = driver.find_element(By.ID, "search")
    search_input.send_keys("Libro de Búsqueda")
    time.sleep(2)

    captura = tomar_captura(driver, "buscar_libro.png")

    # Verificar resultados de búsqueda
    book_items = driver.find_elements(By.CSS_SELECTOR, ".book-item")
    assert len(book_items) > 0, "No se encontraron resultados para la búsqueda."
    assert "Libro de Búsqueda" in book_items[0].text

    agregar_a_reporte(report_path, "Prueba 6", "Éxito", "Resultados de búsqueda correctos.", captura)

@pytest.mark.order(7)
def test_ver_detalles_libro(driver, report_path, open_page):
    driver.get("http://127.0.0.1:5500/Gestor_Libros/index.html")  
    time.sleep(2)  # Esperar para que la página de login cargue completamente
    
    # Realizar el login
    driver.find_element(By.ID, "email").send_keys("nuevo@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Djth2712")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    time.sleep(2)  # Esperar a que la página cargue después del login
    
    # Verificar que el login fue exitoso, por ejemplo, buscando un elemento específico
    formulario_agregarlibros = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "book-form"))
    )
    driver.find_element(By.ID, "title").send_keys("Libro Detalles")
    driver.find_element(By.ID, "author").send_keys("Autor Detalles")
    driver.find_element(By.ID, "description").send_keys("Descripción del libro detalles.")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    
    time.sleep(2)

    book_item = driver.find_element(By.XPATH, "//li[contains(text(), 'Libro Detalles')]")
    book_item.click()

    captura = tomar_captura(driver, "ver_detalles_libro.png")

    # Verificar que los detalles se muestren correctamente
    details_panel = driver.find_element(By.CSS_SELECTOR, ".book-details")
    assert details_panel.is_displayed(), "No se mostraron los detalles del libro."

    agregar_a_reporte(report_path, "Prueba 7", "Éxito", "Detalles del libro mostrados correctamente.", captura)

@pytest.mark.order(8)
def test_verificar_libro_en_lista(driver, report_path, open_page):
    driver.get("http://127.0.0.1:5500/Gestor_Libros/index.html")  
    time.sleep(2)  # Esperar para que la página de login cargue completamente
    
    # Realizar el login
    driver.find_element(By.ID, "email").send_keys("nuevo@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Djth2712")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    time.sleep(2)  # Esperar a que la página cargue después del login
    
    # Verificar que el login fue exitoso, por ejemplo, buscando un elemento específico
    formulario_agregarlibros = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "book-form"))
    )
    driver.find_element(By.ID, "title").send_keys("Libro en Lista")
    driver.find_element(By.ID, "author").send_keys("Autor en Lista")
    driver.find_element(By.ID, "description").send_keys("Descripción del libro en lista.")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    
 
    time.sleep(2)
    captura = tomar_captura(driver, "verificar_libro_en_lista.png")

    # Verificar que el libro está en la lista
    books = driver.find_elements(By.CSS_SELECTOR, ".book-item")

    agregar_a_reporte(report_path, "Prueba 8", "Éxito", "Libro encontrado en la lista.", captura)

@pytest.mark.order(9)
def test_marcar_libro_como_leido(driver, report_path, open_page):
    driver.get("http://127.0.0.1:5500/Gestor_Libros/index.html")  
    time.sleep(2)  # Esperar para que la página de login cargue completamente
    
    # Realizar el login
    driver.find_element(By.ID, "email").send_keys("nuevo@gmail.com")
    driver.find_element(By.ID, "password").send_keys("Djth2712")
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    time.sleep(2)  # Esperar a que la página cargue después del login
    
    # Verificar que el login fue exitoso, por ejemplo, buscando un elemento específico
    formulario_agregarlibros = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "book-form"))
    )
    # Agregar un libro para marcar como leído
    driver.find_element(By.ID, "title").send_keys("Libro Leído")
    driver.find_element(By.ID, "author").send_keys("Autor Leído")
    driver.find_element(By.ID, "description").send_keys("Descripción del libro leído.")
    driver.find_element(By.XPATH, "//input[@type='submit']").click()
    

    time.sleep(2)

    # Esperar hasta que el contenedor de botones sea visible
    button_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "book-item-buttons"))
    )
    # Encontrar el contenedor del libro usando CSS, ejemplo: .book-item
    book_item = driver.find_element(By.CSS_SELECTOR, ".book-item")

    # Encontrar el botón específico dentro del contenedor
    read_button = button_container.find_element(By.CLASS_NAME, "read-button")

    # Hacer clic en el botón de Marcar libro
    read_button.click()

    # Verificar que el libro tiene la clase 'read'
    assert "read" in book_item.get_attribute("class"), "El libro no se marcó como leído."

    # Verificar si el estilo de texto tachado se ha aplicado al libro usando CSS
    text_decoration = book_item.value_of_css_property('text-decoration')
    assert "line-through" in text_decoration, "El estilo de texto tachado no se aplicó correctamente al marcar como leído."

    # Verificar que el texto del botón cambió a "Marcar como no leído"
    assert read_button.text == "Marcar como no leído", "El texto del botón no cambió correctamente."

    # Captura de pantalla
    captura = tomar_captura(driver, "marcar_libro_como_leido.png")

    agregar_a_reporte(report_path, "Prueba 9", "Éxito", "Libro marcado como leído correctamente.", captura)

