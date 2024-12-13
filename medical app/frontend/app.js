document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerBtn = document.getElementById('register-btn');
    const uploadForm = document.getElementById('upload-form');

    // Handle user login
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.token) {
                    localStorage.setItem('token', data.token);
                    window.location.href = 'upload.html';
                } else {
                    alert('Login failed');
                }
            });
        });
    }

    // Redirect to registration page
    if (registerBtn) {
        registerBtn.addEventListener('click', () => {
            window.location.href = 'register.html';
        });
    }

    // Handle file upload
    if (uploadForm) {
        uploadForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const data = document.getElementById('data').value;
            const token = localStorage.getItem('token');

            fetch('/api/upload', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify({ data }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Data uploaded successfully');
                } else {
                    alert('Error uploading data');
                }
            });
        });
    }
});
