const products = [
  {
    id: 1,
    name: "Paracetamol",
    category: "Medicine",
    price: 50,
    stock: 120,
    image: "images/logo2.jpeg"
  },
  {
    id: 2,
    name: "Surgical Gloves",
    category: "Medical Equipment",
    price: 300,
    stock: 50,
    image: "images/logo2.jpeg"
  }
];

const table = document.getElementById("productsTable");

if (table) {
  products.forEach(p => {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td><img src="${p.image}" class="product-img" /></td>
      <td>${p.name}</td>
      <td>${p.category}</td>
      <td>${p.price}</td>
      <td>${p.stock}</td>
      <td>
        <button class="btn btn-role">Edit</button>
        <button class="btn btn-approve">Delete</button>
      </td>
    `;

    table.appendChild(tr);
  });
}
