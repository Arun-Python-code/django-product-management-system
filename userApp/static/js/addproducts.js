// Read the hidden CSRF token used to protect product write requests.
function CSRFToken() {
  const csrfInput = document.querySelector('[name="csrfmiddlewaretoken"]');

  return csrfInput ? csrfInput.value : "";
}

// Find the submit button and product ID used to determine the form's mode.
const submitButton = document.querySelector("#productForm .btn");

// An id query parameter means the form is editing an existing product.
const productId = new URLSearchParams(window.location.search).get("id");

// Label the submit button to match whether the form creates or updates.
if (submitButton) {
  submitButton.textContent = productId ? "Update Product" : "Create Product";
}

// Retrieve existing values and fill the form when an ID is present.
if (productId) {
  fetch(`/getproduct/${productId}/`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to load product");
      }

      return response.json();
    })
    .then((data) => {
      // Populate the fields with the product values returned by the API.
      document.getElementById("name").value = data.product_name;

      document.getElementById("category").value = data.product_category;

      document.getElementById("price").value = data.product_price;
    })
    .catch((error) => {
      console.error("Loading error:", error);
    });
}

// Use one submit handler for both creation and partial updates.
document
  .getElementById("productForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    const data = {
      product_name: document.getElementById("name").value,

      product_category: document.getElementById("category").value,

      product_price: document.getElementById("price").value,
    };

    // Choose the endpoint and HTTP method based on create or update mode.
    const url = productId ? `/updateproduct/${productId}/` : "/createproduct/";

    const method = productId ? "PATCH" : "POST";

    // Send product fields as JSON with the CSRF token required for writes.
    fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": CSRFToken(),
      },
      body: JSON.stringify(data),
    })
      // Parse the API response and route non-success statuses to the error handler.
      .then(async (response) => {
        const responseData = await response.json();

        if (!response.ok) {
          throw new Error(JSON.stringify(responseData));
        }

        return responseData;
      })
      .then((responseData) => {
        console.log("Response:", responseData);

        // Return to the list after an update; clear the form after a creation.
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
