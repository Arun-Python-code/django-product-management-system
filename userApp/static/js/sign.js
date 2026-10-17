
// Read the hidden CSRF form field for the account-creation POST request.
function getCSRFToken() {
    const csrfInput = document.querySelector(
        '[name="csrfmiddlewaretoken"]'
    );

    return csrfInput ? csrfInput.value : "";
}

// Validate and submit the signup form without navigating through a page reload.
document.getElementById("signIn").addEventListener("submit", function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm").value;
    const result = document.getElementById("result");

    // Stop locally if the two password entries do not match.
    if (password !== confirmPassword) {
        result.textContent = "Passwords do not match.";
        return;
    }

    const data = {
        username: username,
        email: email,
        password: password
    };

    // Send registration fields as JSON and include Django's CSRF header.
    fetch("/createuser/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify(data)
    })
    // Read the API result and route non-success status codes into the error handler.
    .then(async response => {
        const responseData = await response.json();

        if (!response.ok) {
            throw new Error(
                JSON.stringify(responseData)
            );
        }

        return responseData;
    })
    .then(data => {
        console.log(data);

        // Show success, clear the form, and then open the login page.
        if (data.message) {
            result.textContent = "Signup successful! Please login.";
            document.getElementById("signIn").reset();

            // Redirect to login page
            setTimeout(() => {
                window.location.href = "/login/";
            }, 1000);
        }
    })
    // Log technical details and show a simple error message in the page.
    .catch(error => {
        console.error("Signup error:", error);
        result.textContent = "Signup failed. Check your details and try again.";
    });
});
