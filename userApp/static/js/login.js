function CSRFToken() {
  const csrfInput = document.querySelector('[name="csrfmiddlewaretoken"]');

  return csrfInput ? csrfInput.value : "";
}

document.getElementById("logins").addEventListener("submit", function (event) {
  event.preventDefault();

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

  console.log("Login request:", data);
  fetch("/loginuser/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": CSRFToken(),
    },
    body: JSON.stringify(data),
  })
    .then(async (response) => {
      const responseData = await response.json();

      console.log("HTTP Status:", response.status);
      console.log("Server Response:", responseData);

      if (!response.ok) {
        throw new Error(responseData.error || "Login failed");
      }

      return responseData;
    })
    .then((data) => {
      if (data.message) {
        window.location.href = "/home/";
      }
    })
    .catch((error) => {
      console.error("Login error:", error);
      alert(error.message);
    });
});
