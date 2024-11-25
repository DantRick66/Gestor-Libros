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
        cls.report_path = os.path.join(os.getcwd(), "reporte_resultados.html")
        
        # Crear el archivo de reporte en formato HTML
        with open(cls.report_path, "w") as reporte:
            reporte.write("<html><head><title>Reporte de Pruebas Automatizadas</title></head><body>")
            reporte.write("<h1>Resultados de Pruebas Automatizadas</h1>")
            reporte.write("<table border='1' style='width:100%;border-collapse:collapse;'>")
            reporte.write("<tr><th>Historia</th><th>Resultado</th><th>Detalle</th><th>Captura</th></tr>")

    def setUp(self):
        # Navegar a la página de la gestión de libros antes de cada prueba
        self.driver.get("http://127.0.0.1:5500/Gestor_Libros/index.html")  

    # Función para tomar capturas de pantalla y guardarlas en el directorio actual
    def tomar_captura(self, nombre):
        path = os.path.join(os.getcwd(), nombre)
        self.driver.save_screenshot(path)
        return nombre

    # Función para agregar resultados al reporte en formato HTML
    def agregar_a_reporte(self, historia, resultado, detalle, captura=None):
        with open(self.report_path, "a") as reporte:
            reporte.write(f"<tr><td>{historia}</td><td>{resultado}</td><td>{detalle}</td>")
            if captura:
                reporte.write(f"<td><a href='{captura}' target='_blank'>Ver Captura</a></td>")
            else:
                reporte.write("<td>No disponible</td>")
            reporte.write("</tr>")

    def test_agregar_libro_correctamente(self):
        title_input = self.driver.find_element(By.ID, "title")
        author_input = self.driver.find_element(By.ID, "author")
        description_input = self.driver.find_element(By.ID, "description")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        
        # Completar el formulario
        title_input.send_keys("Libro de Prueba")
        author_input.send_keys("Autor de Prueba")
        description_input.send_keys("Descripción de prueba para el libro.")
        submit_button.click()

        # Esperar que el libro se haya agregado a la lista
        time.sleep(2)

        captura = self.tomar_captura("agregar_libro.png")

        # Verificar que el libro aparezca en la lista
        books = self.driver.find_elements(By.CSS_SELECTOR, ".book-item")
        self.assertGreater(len(books), 0, "No se agregó el libro correctamente.")
        self.assertIn("Libro de Prueba", books[0].text)
        self.assertIn("Autor de Prueba", books[0].text)

        self.agregar_a_reporte("prueba 1", "Éxito", "Libro agregado correctamente.", captura)

    def test_agregar_libro_con_campos_vacios(self):
        title_input = self.driver.find_element(By.ID, "title")
        author_input = self.driver.find_element(By.ID, "author")
        description_input = self.driver.find_element(By.ID, "description")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        
        title_input.clear()
        author_input.clear()
        description_input.clear()
        submit_button.click()

        time.sleep(2)

        captura = self.tomar_captura("agregar_libro_error.png")

        # Verificar mensaje de error
        error_message = self.driver.find_element(By.CSS_SELECTOR, ".message.error")
        self.assertTrue(error_message.is_displayed(), "No se mostró el mensaje de error.")
        self.assertEqual(error_message.text, "Por favor, completa todos los campos.")

        self.agregar_a_reporte("Prueba 2", "Éxito", "Error mostrado al dejar campos vacíos.", captura)

    def test_eliminar_libro(self):
        title_input = self.driver.find_element(By.ID, "title")
        author_input = self.driver.find_element(By.ID, "author")
        description_input = self.driver.find_element(By.ID, "description")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        
        title_input.send_keys("Libro para Eliminar")
        author_input.send_keys("Autor para Eliminar")
        description_input.send_keys("Descripción para eliminar el libro.")
        submit_button.click()

        time.sleep(2)
        book_item = self.driver.find_element(By.XPATH, "//li[contains(text(), 'Libro para Eliminar')]")
        delete_button = book_item.find_element(By.TAG_NAME, "button")
        delete_button.click()

        time.sleep(2)
        captura = self.tomar_captura("eliminar_libro.png")

        # Verificar que el libro haya sido eliminado
        books = self.driver.find_elements(By.CSS_SELECTOR, ".book-item")
        self.assertNotIn("Libro para Eliminar", [book.text for book in books], "El libro no fue eliminado correctamente.")

        self.agregar_a_reporte("Prueba 3", "Éxito", "Libro eliminado correctamente.", captura)

    def test_buscar_libro(self):
        title_input = self.driver.find_element(By.ID, "title")
        author_input = self.driver.find_element(By.ID, "author")
        description_input = self.driver.find_element(By.ID, "description")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        
        title_input.send_keys("Libro de Búsqueda")
        author_input.send_keys("Autor de Búsqueda")
        description_input.send_keys("Descripción para buscar el libro.")
        submit_button.click()

        time.sleep(2)

        search_input = self.driver.find_element(By.ID, "search")
        search_input.send_keys("Búsqueda")
        time.sleep(2)

        captura = self.tomar_captura("buscar_libro.png")

        # Verificar resultados de búsqueda
        book_items = self.driver.find_elements(By.CSS_SELECTOR, ".book-item")
        self.assertGreater(len(book_items), 0, "No se encontraron resultados para la búsqueda.")
        self.assertIn("Libro de Búsqueda", book_items[0].text)

        self.agregar_a_reporte("Prueba 4", "Éxito", "Resultados de búsqueda correctos.", captura)

    def test_ver_detalles_libro(self):
        title_input = self.driver.find_element(By.ID, "title")
        author_input = self.driver.find_element(By.ID, "author")
        description_input = self.driver.find_element(By.ID, "description")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        
        title_input.send_keys("Libro Detalles")
        author_input.send_keys("Autor Detalles")
        description_input.send_keys("Descripción del libro detalles.")
        submit_button.click()

        time.sleep(2)

        book_item = self.driver.find_element(By.XPATH, "//li[contains(text(), 'Libro Detalles')]")
        book_item.click()

        captura = self.tomar_captura("ver_detalles_libro.png")

        # Verificar que los detalles se muestren correctamente
        details_panel = self.driver.find_element(By.CSS_SELECTOR, ".book-details")
        self.assertTrue(details_panel.is_displayed(), "No se mostraron los detalles del libro.")

        self.agregar_a_reporte("Prueba 5", "Éxito", "Detalles del libro mostrados correctamente.", captura)

    def test_verificar_libro_en_lista(self):
        title_input = self.driver.find_element(By.ID, "title")
        author_input = self.driver.find_element(By.ID, "author")
        description_input = self.driver.find_element(By.ID, "description")
        submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
        
        title_input.send_keys("Libro en Lista")
        author_input.send_keys("Autor en Lista")
        description_input.send_keys("Descripción del libro en lista.")
        submit_button.click()

        time.sleep(2)
        captura = self.tomar_captura("verificar_libro_en_lista.png")

        # Verificar que el libro está en la lista
        books = self.driver.find_elements(By.CSS_SELECTOR, ".book-item")
        self.assertIn("Libro en Lista", [book.text for book in books], "El libro no se encuentra en la lista.")

        self.agregar_a_reporte("Prueba 6", "Éxito", "Libro encontrado en la lista.", captura)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        with open(cls.report_path, "a") as reporte:
            reporte.write("</table></body></html>")

if __name__ == "__main__":
    unittest.main()
