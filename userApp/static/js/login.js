// Read the CSRF token rendered into the login form for Django's POST check.
function CSRFToken() {
  const csrfInput = document.querySelector('[name="csrfmiddlewaretoken"]');

  return csrfInput ? csrfInput.value : "";
}

// Intercept the form so credentials can be sent to the login API as JSON.
document.getElementById("logins").addEventListener("submit", function (event) {
  event.preventDefault();

  // Require an explicit role choice before sending the account credentials.
  const selectedRole = document.querySelector('input[name="role"]:checked');

  if (!selectedRole) {
    alert("Please select your role.");
    return;
  }

  const data = {
    role: selectedRole.value,
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
  };

  // POST the login details with JSON content and the CSRF header.
  console.log("Login request:", data);
  fetch("/loginuser/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": CSRFToken(),
    },
    body: JSON.stringify(data),
  })
    // Parse the JSON response and turn HTTP failures into handled errors.
    .then(async (response) => {
      const responseData = await response.json();

      console.log("HTTP Status:", response.status);
      console.log("Server Response:", responseData);

      if (!response.ok) {
        throw new Error(responseData.error || "Login failed");
      }

      return responseData;
    })
    // Navigate to the home page after the server confirms successful login.
    .then((data) => {
      if (data.message) {
        window.location.href = "/home/";
      }
    })
    // Display server or network errors to the user.
    .catch((error) => {
      console.error("Login error:", error);
      alert(error.message);
    });
});
