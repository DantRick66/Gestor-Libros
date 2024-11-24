import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

class TestGestionDeLibros(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configuración inicial del navegador
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.maximize_window()

    def setUp(self):
        # Navegar a la página de la gestión de libros antes de cada prueba
        self.driver.get("http://127.0.0.1:5500/Gestor_Libros/index.html")  

    # Función para tomar capturas de pantalla y guardarlas en el directorio actual
    def tomar_captura(self, nombre):
        path = os.path.join(os.getcwd(), nombre)  
        self.driver.save_screenshot(path)

    # Función para agregar resultados al reporte
    def agregar_a_reporte(self, historia, resultado, detalle=""):
        with open("reporte_resultados.txt", "a") as reporte:
            reporte.write(f"{historia}: {resultado} - {detalle}\n")

    def test_agregar_libro_correctamente(self):
        # Agregar un libro correctamente
        title_input = self.driver.find_element(By.ID, "title")
        author_input = self.driver.find_element(By.ID, "author")
        description_input = self.driver.find_element(By.ID, "description")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        
        # Completar el formulario
        title_input.send_keys("Libro de Prueba")
        author_input.send_keys("Autor de Prueba")
        description_input.send_keys("Descripción de prueba para el libro.")
        
        # Enviar el formulario
        submit_button.click()
        
        # Esperar que el libro se haya agregado a la lista
        time.sleep(2)

        # Tomar captura de pantalla de la página actual
        self.tomar_captura("agregar_libro.png")

        # Verificar que el libro aparezca en la lista
        books = self.driver.find_elements(By.CSS_SELECTOR, ".book-item")
        self.assertGreater(len(books), 0, "No se agregó el libro correctamente.")
        self.assertIn("Libro de Prueba", books[0].text)
        self.assertIn("Autor de Prueba", books[0].text)

        # Verificar el mensaje de éxito
        success_message = self.driver.find_element(By.CSS_SELECTOR, ".message.success")
        self.assertTrue(success_message.is_displayed(), "No se mostró el mensaje de éxito.")
        self.agregar_a_reporte("Historia 1", "Éxito")

    def test_agregar_libro_con_campos_vacios(self):
        # Intentar agregar un libro sin completar los campos
        title_input = self.driver.find_element(By.ID, "title")
        author_input = self.driver.find_element(By.ID, "author")
        description_input = self.driver.find_element(By.ID, "description")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        
        # Dejar los campos vacíos y enviar el formulario
        title_input.clear()
        author_input.clear()
        description_input.clear()
        submit_button.click()
        
        # Esperar que se muestre el mensaje de error
        time.sleep(2)
        
        # Tomar captura de pantalla de la página actual
        self.tomar_captura("agregar_libro_error.png")

        # Verificar que aparezca el mensaje de error
        error_message = self.driver.find_element(By.CSS_SELECTOR, ".message.error")
        self.assertTrue(error_message.is_displayed(), "No se mostró el mensaje de error.")
        self.assertEqual(error_message.text, "Por favor, completa todos los campos.")
        self.agregar_a_reporte("Historia 2", "Éxito")

    def test_eliminar_libro(self):
        # Agregar un libro primero
        title_input = self.driver.find_element(By.ID, "title")
        author_input = self.driver.find_element(By.ID, "author")
        description_input = self.driver.find_element(By.ID, "description")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        
        # Completar el formulario
        title_input.send_keys("Libro para Eliminar")
        author_input.send_keys("Autor para Eliminar")
        description_input.send_keys("Descripción para eliminar el libro.")
        submit_button.click()
        
        # Esperar que el libro se haya agregado a la lista
        time.sleep(2)
        
        # Encontrar el libro agregado y el botón de eliminar
        book_item = self.driver.find_element(By.XPATH, "//li[contains(text(), 'Libro para Eliminar')]")
        delete_button = book_item.find_element(By.TAG_NAME, "button")
        delete_button.click()
        
        # Esperar que el libro se haya eliminado
        time.sleep(2)
        
        # Tomar captura de pantalla de la página después de eliminar el libro
        self.tomar_captura("eliminar_libro.png")
        
        # Verificar que el libro haya sido eliminado
        books = self.driver.find_elements(By.CSS_SELECTOR, ".book-item")
        self.assertNotIn("Libro para Eliminar", [book.text for book in books], "El libro no fue eliminado correctamente.")
        
        # Verificar el mensaje de eliminación exitosa
        success_message = self.driver.find_element(By.CSS_SELECTOR, ".message.success")
        self.assertTrue(success_message.is_displayed(), "No se mostró el mensaje de éxito.")
        self.assertIn("fue eliminado", success_message.text)
        self.agregar_a_reporte("Historia 3", "Éxito")

    def test_buscar_libro(self):
        # Agregar un libro para búsqueda
        title_input = self.driver.find_element(By.ID, "title")
        author_input = self.driver.find_element(By.ID, "author")
        description_input = self.driver.find_element(By.ID, "description")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        
        # Completar el formulario
        title_input.send_keys("Libro de Búsqueda")
        author_input.send_keys("Autor de Búsqueda")
        description_input.send_keys("Descripción para buscar el libro.")
        submit_button.click()
        
        # Esperar que el libro se haya agregado a la lista
        time.sleep(2)

        # Buscar el libro
        search_input = self.driver.find_element(By.ID, "search")
        search_input.send_keys("Búsqueda")

        # Esperar que los resultados se filtren
        time.sleep(2)

        # Tomar captura de pantalla de la búsqueda
        self.tomar_captura("buscar_libro.png")

        # Verificar que el libro aparezca en la lista filtrada
        book_items = self.driver.find_elements(By.CSS_SELECTOR, ".book-item")
        self.assertGreater(len(book_items), 0, "No se encontraron resultados para la búsqueda.")
        self.assertIn("Libro de Búsqueda", book_items[0].text)
        self.agregar_a_reporte("Historia 4", "Éxito")

    def test_no_resultados_busqueda(self):
        # Buscar un libro que no exista
        search_input = self.driver.find_element(By.ID, "search")
        search_input.send_keys("Libro Inexistente")

        # Esperar que se muestre el mensaje de no resultados
        time.sleep(2)

        # Verificar que se muestre el mensaje de "No se encontraron libros"
        no_result_message = self.driver.find_element(By.CSS_SELECTOR, ".no-result")
        self.assertTrue(no_result_message.is_displayed(), "No se mostró el mensaje de no resultados.")
        self.assertEqual(no_result_message.text, "No se encontraron libros que coincidan con la búsqueda.")
        self.agregar_a_reporte("Historia 5", "Éxito")

    @classmethod
    def tearDownClass(cls):
        # Cerrar el navegador después de todas las pruebas
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main()
