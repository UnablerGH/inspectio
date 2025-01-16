// Fetch and render user data
async function fetchUsers() {
    const response = await fetch('/api/users');
    const users = await response.json();

    const tableBody = document.querySelector("#userTable tbody");
    tableBody.innerHTML = "";

    users.forEach(user => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
        `;
        tableBody.appendChild(row);
    });
}

// Add a new user
async function addUser() {
    const name = prompt("Enter the user's name:");
    const email = prompt("Enter the user's email:");
    if (name && email) {
        await fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email })
        });
        fetchUsers(); // Refresh the user list
    } else {
        alert("Both name and email are required.");
    }
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
    fetchUsers();
    document.getElementById("addUserBtn").addEventListener("click", addUser);
});
