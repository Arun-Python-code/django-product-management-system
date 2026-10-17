function CSRFToken() {
  const csrfInput = document.querySelector('[name="csrfmiddlewaretoken"]');

  return csrfInput ? csrfInput.value : "";
}

// Get button element
const submitButton = document.querySelector("#productForm .btn");

// Get product ID from URL
const productId = new URLSearchParams(window.location.search).get("id");

// Change button text based on Create or Update mode
if (submitButton) {
  submitButton.textContent = productId ? "Update Product" : "Create Product";
}

// Load product details when updating
if (productId) {
  fetch(`/getproduct/${productId}/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to load product");
      }

      return response.json();
    })
    .then((data) => {
      document.getElementById("name").value = data.product_name;

      document.getElementById("category").value = data.product_category;

      document.getElementById("price").value = data.product_price;
    })
    .catch((error) => {
      console.error("Loading error:", error);
    });
}

// Common form submit handler
document
  .getElementById("productForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const data = {
      product_name: document.getElementById("name").value,

      product_category: document.getElementById("category").value,

      product_price: document.getElementById("price").value,
    };

    // Select API and method based on mode
    const url = productId ? `/updateproduct/${productId}/` : "/createproduct/";

    const method = productId ? "PATCH" : "POST";

    fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": CSRFToken(),
      },
      body: JSON.stringify(data),
    })
      .then(async (response) => {
        const responseData = await response.json();

        if (!response.ok) {
          throw new Error(JSON.stringify(responseData));
        }

        return responseData;
      })
      .then((responseData) => {
        console.log("Response:", responseData);

        if (productId) {
          alert("Product updated successfully!");
          window.location.href = "/home/";
        } else {
          alert("Product created successfully!");
          document.getElementById("productForm").reset();
        }
      })
      .catch((error) => {
        console.error("Product error:", error);
        alert(error.message);
      });
  });
