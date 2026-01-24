const toggleButton = document.getElementById("password-visibility");
const passwordInput = document.getElementById("password");

if (toggleButton && passwordInput) {
	toggleButton.addEventListener("click", function() {

		if (passwordInput.type === "password") {
			passwordInput.type = "text";
			toggleButton.innerHTML = "visibility_off"
		} else {
			passwordInput.type = "password";
			toggleButton.innerHTML = "visibility"
		}
	});
}