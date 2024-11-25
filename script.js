// script.js
function showSection(sectionId) {
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');
}

function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    // Add login logic here
    alert(`Logged in as ${username}`);
}

function unlockDoor() {
    // Add unlock door logic here
    alert('Unlock command sent');
}

function createUser() {
    const firstName = document.getElementById('first-name').value;
    const lastName = document.getElementById('last-name').value;
    const email = document.getElementById('email').value;
    // Add create user logic here
    alert(`User created: ${firstName} ${lastName}`);
}

function loadUsers() {
    const users = [
        { userId: 1, firstName: 'John', lastName: 'Doe', email: 'john@example.com', lastEntry: '2023-10-01 12:00' },
        // Add more users here
    ];
    const userTableBody = document.getElementById('user-table-body');
    userTableBody.innerHTML = '';
    users.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${user.userId}</td>
            <td>${user.firstName}</td>
            <td>${user.lastName}</td>
            <td>${user.email}</td>
            <td>${user.lastEntry}</td>
        `;
        userTableBody.appendChild(row);
    });
}

function loadEntryLog() {
    const entries = [
        { userId: 1, timestamp: '2023-10-01 12:00', action: 'Login' },
        // Add more entries here
    ];
    const entryLogBody = document.getElementById('entry-log-body');
    entryLogBody.innerHTML = '';
    entries.forEach(entry => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${entry.userId}</td>
            <td>${entry.timestamp}</td>
            <td>${entry.action}</td>
        `;
        entryLogBody.appendChild(row);
    });
}

// Load initial data
document.addEventListener('DOMContentLoaded', () => {
    loadUsers();
    loadEntryLog();
});