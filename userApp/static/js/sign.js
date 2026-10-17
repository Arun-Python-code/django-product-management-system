
function getCSRFToken() {
    const csrfInput = document.querySelector(
        '[name="csrfmiddlewaretoken"]'
    );

    return csrfInput ? csrfInput.value : "";
}

document.getElementById("signIn").addEventListener("submit", function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm").value;
    const result = document.getElementById("result");

    // Check password confirmation
    if (password !== confirmPassword) {
        result.textContent = "Passwords do not match.";
        return;
    }

    const data = {
        username: username,
        email: email,
        password: password
    };

    fetch("/createuser/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify(data)
    })
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

        if (data.message) {
            result.textContent = "Signup successful! Please login.";
            document.getElementById("signIn").reset();

            // Redirect to login page
            setTimeout(() => {
                window.location.href = "/login/";
            }, 1000);
        }
    })
    .catch(error => {
        console.error("Signup error:", error);
        result.textContent = "Signup failed. Check your details and try again.";
    });
});
