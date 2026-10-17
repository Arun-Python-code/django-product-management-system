// Fetch the signed-in user's product list and render its rows in the table.
function loadProducts() {
  fetch("/productlist/")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to load products");
      }
      return response.json();
    })
    .then((products) => {
      // Build the table body from the product data returned by the API.
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

      // Update the DOM once after all product rows have been assembled.
      table.innerHTML = rows; // set once, after the loop
    })
    .catch((error) => console.error("Product error:", error));
}

// Escape product text before inserting it into the generated table markup.
function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = value;
  return div.innerHTML;
}

// Display the action popup and attach handlers for the selected product.
function showProductPopup(productId) {
  const popup = document.getElementById("productPopup");

  if (!popup) {
    console.error("productPopup element not found!");
    return;
  }

  popup.style.display = "flex";

  // Pass this product's ID to the edit page or deletion function.
  document.getElementById("updateBtn").onclick = function () {
    window.location.href = `/addproduct/?id=${productId}`;
  
  };

  document.getElementById("deleteBtn").onclick = function () {
    deleteProduct(productId);
  };
}

// Hide the product action popup.
function closeProductPopup() {
  document.getElementById("productPopup").style.display = "none";
}

// Ask for confirmation, then send a CSRF-protected DELETE request.
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
    // Check the response type before parsing JSON, then surface HTTP failures.
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
      // Notify the user and refresh the list after successful deletion.
      alert(data.message);

      closeProductPopup();
      loadProducts();
    })
    .catch((error) => {
      console.error("Delete error:", error);
      alert(error.message);
    });
}

// Read the CSRF token rendered in the page so the DELETE request is accepted.
function getCSRFToken() {
  const csrfInput = document.querySelector('[name="csrfmiddlewaretoken"]');
  return csrfInput ? csrfInput.value : "";
}

// Populate the table when the page script is loaded.
loadProducts();
