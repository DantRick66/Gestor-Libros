// Escucha el evento de envío del formulario para agregar un libro
document.getElementById('book-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const title = document.getElementById('title').value.trim();
    const author = document.getElementById('author').value.trim();
    const description = document.getElementById('description').value.trim();
    const bookList = document.getElementById('books');

        // Validación de los campos
        if (title && author && description) {
            const bookItem = document.createElement('li');
            bookItem.classList.add('book-item');
            bookItem.innerHTML = `${title} - ${author}`;

        
                    // Crear un botón de eliminar
        const deleteButton = document.createElement('button');
        deleteButton.textContent = "Eliminar";
        deleteButton.onclick = function() {
            bookList.removeChild(bookItem);
            if (bookList.children.length === 0) {
                const noBooksMessage = document.createElement('li');
                noBooksMessage.textContent = "No hay libros disponibles.";
                bookList.appendChild(noBooksMessage);
            }
        };

        bookItem.appendChild(deleteButton);

        // Crear los detalles del libro (inicialmente ocultos)
        const bookDetails = document.createElement('div');
        bookDetails.classList.add('book-details');
        bookDetails.textContent = description;
        
        // Añadir los detalles del libro a la lista
        bookItem.appendChild(bookDetails);

        // Mostrar detalles del libro al hacer clic en el libro
        bookItem.onclick = function() {
            const detailsVisible = bookDetails.style.display === 'block';
            bookDetails.style.display = detailsVisible ? 'none' : 'block';
        };

        bookList.appendChild(bookItem);

        // Limpiar los campos del formulario
        document.getElementById('title').value = '';
        document.getElementById('author').value = '';
        document.getElementById('description').value = '';

        // Eliminar el mensaje "No hay libros disponibles" si existe
        if (bookList.firstChild && bookList.firstChild.textContent === 'No hay libros disponibles.') {
            bookList.firstChild.remove();
        }
    } else {
        alert('Por favor, completa todos los campos.');
    }
});

// Función para buscar libros en la lista
function searchBooks() {
    const query = document.getElementById('search').value.toLowerCase();
    const bookItems = document.querySelectorAll('#books li');
    let foundBooks = 0;

    // Iterar sobre los libros y mostrarlos u ocultarlos según la búsqueda
    bookItems.forEach(item => {
        const bookText = item.textContent.toLowerCase();
        if (bookText.includes(query)) {
            item.style.display = '';
            foundBooks++;
        } else {
            item.style.display = 'none';
        }
    });

    // Si no se encuentran resultados, mostrar mensaje
    if (foundBooks === 0) {
        const noResultMessage = document.createElement('li');
        noResultMessage.textContent = "No se encontraron libros que coincidan con la búsqueda.";
        noResultMessage.classList.add('no-result');
        document.getElementById('books').appendChild(noResultMessage);
    } else {
        // Eliminar mensaje de "no resultados" si existen
        const noResultMessage = document.querySelector('.no-result');
        if (noResultMessage) {
            noResultMessage.remove();
        }
    }
}