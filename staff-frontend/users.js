//const token = localStorage.getItem("token");

fetch("http://localhost:8000/admin/users", {
  method: "GET",
  headers: {
    "Authorization": `Bearer ${token}`
  }
})
.then(res => {
  if (!res.ok) {
    throw new Error("Unauthorized or failed to fetch users");
  }
  return res.json();
})
.then(users => {
  const tableBody = document.getElementById("usersTable");
  tableBody.innerHTML = "";

  users.forEach(user => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${user.name}</td>
      <td>${user.email}</td>
      <td>
        <select id="role-${user._id}">
          <option value="user" ${user.role === "user" ? "selected" : ""}>User</option>
          <option value="admin" ${user.role === "admin" ? "selected" : ""}>Admin</option>
          <option value="staff" ${user.role === "staff" ? "selected" : ""}>Staff</option>
        </select>
      </td>
      <td>${user.is_active ? "Approved" : "Pending"}</td>
      <td>
        <button onclick="approveUser('${user._id}')">
          ${user.is_active ? "Update" : "Approve"}
        </button>
      </td>
    `;

    tableBody.appendChild(row);
  });
})
.catch(err => {
  console.error(err);
  alert("Failed to load users");
});




function approveUser(userId) {
  const roleSelect = document.getElementById(`role-${userId}`);
  const selectedRole = roleSelect.value;
  alert(`Setting role to ${selectedRole} for User ID: ${userId}`);
  fetch(`http://localhost:8000/admin/users/${userId}/approve`, {
    method: "PUT",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      role: selectedRole
    })
  })
  .then(res => {
    if (!res.ok) {
      throw new Error("Failed to approve user");
    }
    return res.json();
  })
  .then(() => {
    alert("User updated successfully");
    location.reload();
  })
  .catch(err => {
    console.error(err);
    alert("Error updating user");
  });
}
