// Login Form
/*document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    const result = await response.json();
    if (result.success) {
        window.location.href = 'dashboard.html';
    } else {
        alert('Invalid credentials');
    }
});

// Signup Form
document.getElementById('signupForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const college = document.getElementById('college').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('http://localhost:8000/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, college, email, password })
    });
    const result = await response.json();
    if (result.success) {
        window.location.href = 'index.html';
    } else {
        alert('Signup failed');
    }
});*/

// Login Form
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();
    if (result.success) {
        // Save user info to localStorage
        localStorage.setItem('user', JSON.stringify(result.user)); // expects { name, email, college }
        window.location.href = 'dashboard.html';
    } else {
        alert('Invalid credentials');
    }
});

// Signup Form
document.getElementById('signupForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value;
    const college = document.getElementById('college').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const response = await fetch('http://localhost:8000/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, college, email, password })
    });

    const result = await response.json();
    if (result.success) {
        // Save user info to localStorage
        localStorage.setItem('user', JSON.stringify({ name, email, college }));
        window.location.href = 'dashboard.html';
    } else {
        alert('Signup failed');
    }
});


// Quiz Submission (placeholder)
document.getElementById('quizForm')?.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Quiz submitted! (Evaluation logic TBD)');
});