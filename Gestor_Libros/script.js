// Función para mostrar mensajes
function showMessage(message, type = 'success') {
    const messageContainer = document.getElementById('message-container');
    
    // Crear el mensaje
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`; // Añadimos una clase según el tipo de mensaje
    messageDiv.textContent = message;

    // Agregar el mensaje al contenedor
    messageContainer.appendChild(messageDiv);

    // Eliminar el mensaje después de 3 segundos
    setTimeout(() => {
        messageDiv.remove();
    }, 3000);
}

// Escucha el evento de envío del formulario para agregar un libro
document.getElementById('book-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const title = document.getElementById('title').value.trim();
    const author = document.getElementById('author').value.trim();
    const description = document.getElementById('description').value.trim();
    const bookList = document.getElementById('books');

    // Limpiar mensajes anteriores
    const messageContainer = document.getElementById('message-container');
    messageContainer.innerHTML = '';

    // Validación de los campos
    if (!title || !author || !description) {
        showMessage('Por favor, completa todos los campos.', 'error');
    } else if (description.length < 2) {
        showMessage('La descripción debe tener al menos dos caracteres.', 'error');
    } else {
        const bookItem = document.createElement('li');
        bookItem.classList.add('book-item');
        bookItem.innerHTML = `${title} - ${author}`;


        
        // Crear un botón de eliminar
        const deleteButton = document.createElement('button');
        deleteButton.textContent = "Eliminar";
        deleteButton.onclick = function() {
            bookList.removeChild(bookItem);

            // Mostrar mensaje de eliminación exitosa
            showMessage(`El libro "${title}" fue eliminado.`, 'success');
            
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
            if (e.target.tagName !== 'BUTTON') {
                const detailsVisible = bookDetails.style.display === 'block';
                bookDetails.style.display = detailsVisible ? 'none' : 'block';
            }
        };

        bookList.appendChild(bookItem);

        // Limpiar los campos del formulario
        document.getElementById('title').value = '';
        document.getElementById('author').value = '';
        document.getElementById('description').value = '';
        
        // Eliminar el mensaje "No hay libros disponibles" si existe
        const noBooksMessage = bookList.querySelector('li:first-child');
        if (noBooksMessage && noBooksMessage.textContent === 'No hay libros disponibles.') {
            noBooksMessage.remove();
        }

        
        // Mostrar mensaje de adición exitosa
        showMessage(`El libro "${title}" fue agregado correctamente.`, 'success');
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
    const noResultMessage = document.querySelector('.no-result');
    if (foundBooks === 0) {
        if (!noResultMessage) {
        const noResultMessageDiv = document.createElement('li');
        noResultMessageDiv.textContent = "No se encontraron libros que coincidan con la búsqueda.";
        noResultMessageDiv.classList.add('no-result');
        document.getElementById('books').appendChild(noResultMessageDiv);
        }

    } else if (noResultMessage) {
        noResultMessage.remove();
    }
}

document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Evitar recarga de la página

    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value.trim();

    // Limpiar mensajes anteriores
    const messageContainer = document.getElementById('message-container');
    messageContainer.innerHTML = '';

    // Validaciones básicas
    if (!email || !password) {
        showMessage("Por favor, completa todos los campos.", "error");
        return;
    }

    // Validar formato del correo electrónico
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        showMessage("El correo electrónico no tiene un formato válido.", "error");
        return;
    }

    // Obtener el usuario almacenado en localStorage
    const storedUser = JSON.parse(localStorage.getItem('user'));

    // Simular autenticación
    if (!storedUser || email !== storedUser.email || password !== storedUser.password) {
        showMessage("Credenciales incorrectas. Por favor, intente nuevamente.", "error");
    } else {
        showMessage("Inicio de sesión exitoso. Cargando el gestor de libros...", "success");
        setTimeout(() => {
            document.getElementById('login-container').classList.add('hidden');

            // Mostrar el mensaje de bienvenida
            document.getElementById('welcome-message').style.display = 'block';
            document.getElementById('user-name').textContent = `Bienvenido, ${storedUser.name}`;

            // Mostrar el gestor de libros
            document.getElementById('gestor-libros').style.display = 'block';
        }, 2000);
    }
});


// Opción de "Olvidé mi contraseña"
document.getElementById('forgot-password').addEventListener('click', function () {
    showMessage("Enlace de recuperación enviado a su correo.", "success");
});


// Escucha el evento de envío del formulario de registro
document.getElementById('register-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const name = document.getElementById('register-name').value.trim();
    const email = document.getElementById('register-email').value.trim();
    const password = document.getElementById('register-password').value.trim();

    // Limpiar mensajes anteriores
    const messageContainer = document.getElementById('message-container');
    messageContainer.innerHTML = '';

    // Validación básica
    if (!name || !email || !password) {
        showMessage("Todos los campos son obligatorios.", "error");
    } else if (password.length < 8 || !/[A-Z]/.test(password) || !/\d/.test(password)) {
        showMessage("La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.", "error");
    } else {
        // Guardar usuario en localStorage
        localStorage.setItem('user', JSON.stringify({ name, email, password }));
        
        showMessage("Registro exitoso. Revise su correo para activar su cuenta.", "success");


        // Simular redirección al login
        setTimeout(() => {
            document.getElementById('register-container').classList.add('hidden');
            document.getElementById('login-container').classList.remove('hidden');
        }, 2000);
    }
});

document.getElementById('show-register').addEventListener('click', function (e) {
    e.preventDefault();
    document.getElementById('login-container').classList.add('hidden');
    document.getElementById('register-container').classList.remove('hidden');
});


