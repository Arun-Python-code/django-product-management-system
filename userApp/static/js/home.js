// Load products and show them in the table
function loadProducts() {
  fetch("/productlist/")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to load products");
      }
      return response.json();
    })
    .then((products) => {
      const table = document.getElementById("productTable");
      let rows = "";

      console.log(products);

      if (products.length === 0) {
        rows = '<tr><td colspan="4">No products found.</td></tr>';
      }

      products.forEach((product, index) => {
        rows += `
                    <tr>
                        <td>${index + 1}</td>
                        <td>
                            <span class="product-name"
                                  onclick="showProductPopup(${product.id})">
                                ${escapeHtml(product.product_name)}
                            </span>
                        </td>
                        <td>${escapeHtml(product.product_category)}</td>
                        <td>${escapeHtml(product.product_price)}</td>
                    </tr>
                `;
      });

      table.innerHTML = rows; // set once, after the loop
    })
    .catch((error) => console.error("Product error:", error));
}

// Stops HTML inside product data from running in the page
function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = value;
  return div.innerHTML;
}

// Open popup
function showProductPopup(productId) {
  const popup = document.getElementById("productPopup");

  if (!popup) {
    console.error("productPopup element not found!");
    return;
  }

  popup.style.display = "flex";

  document.getElementById("updateBtn").onclick = function () {
    window.location.href = `/addproduct/?id=${productId}`;
  
  };

  document.getElementById("deleteBtn").onclick = function () {
    deleteProduct(productId);
  };
}

// Close popup
function closeProductPopup() {
  document.getElementById("productPopup").style.display = "none";
}

// Delete product
function deleteProduct(productId) {
  if (!confirm("Are you sure you want to delete this product?")) {
    return;
  }

  fetch(`/deleteproduct/${productId}/`, {
    method: "DELETE",
    headers: {
      "X-CSRFToken": getCSRFToken(),
    },
  })
    .then(async (response) => {
      const contentType = response.headers.get("content-type");

      if (!contentType || !contentType.includes("application/json")) {
        throw new Error(
          `Server returned HTTP ${response.status}. Check Django URL configuration.`,
        );
      }

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Delete failed");
      }

      return data;
    })
    .then((data) => {
      alert(data.message);

      closeProductPopup();
      loadProducts();
    })
    .catch((error) => {
      console.error("Delete error:", error);
      alert(error.message);
    });
}
// Read CSRF token from {% csrf_token %} in the page
function getCSRFToken() {
  const csrfInput = document.querySelector('[name="csrfmiddlewaretoken"]');
  return csrfInput ? csrfInput.value : "";
}

loadProducts();
