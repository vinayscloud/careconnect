document.addEventListener("DOMContentLoaded", function() {
    fetchProfile();

    document.getElementById("profileForm").addEventListener("submit", function(event) {
        event.preventDefault();
        updateProfile();
    });

    document.getElementById("passwordForm").addEventListener("submit", function(event) {
        event.preventDefault();
        changePassword();
    });
});

// Fetch and Autofill Profile Data
function fetchProfile() {
    fetch("/profile")
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById("profileMessage").textContent = data.error;
        } else {
            document.getElementById("full_name").value = data.full_name;
            document.getElementById("email").value = data.email;
            document.getElementById("phone").value = data.phone;
        }
    });
}

// Enable Editing When Pencil Icon is Clicked
function makeEditable(fieldId) {
    let field = document.getElementById(fieldId);
    field.readOnly = false;
    field.focus();
    field.style.background = "#fff";
}

// Update Profile API Call
function updateProfile() {
    const profileData = {
        email: document.getElementById("email").value,
        phone: document.getElementById("phone").value
    };

    fetch("/profile/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(profileData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("profileMessage").textContent = data.message || data.error;
    });
}

// Change Password API Call
function changePassword() {
    const newPassword = document.getElementById("new_password").value;

    fetch("/profile/change-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ old_password: document.getElementById("old_password").value, new_password: newPassword })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("passwordMessage").textContent = data.message || data.error;
    });
}
