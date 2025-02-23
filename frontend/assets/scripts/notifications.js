document.addEventListener("DOMContentLoaded", () => {
    const badge = document.querySelector(".notification-badge");  // Red badge on bell icon
    const notificationsList = document.getElementById("notifications-list");
    const notificationIcon = document.querySelector(".notification-icon");

    function fetchNotifications() {
        fetch("/api/notifications", {
            method: "GET",
            headers: { 
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        })
        .then(response => response.json())
        .then(data => {
            notificationsList.innerHTML = "";

            if (data.error) {
                notificationsList.innerHTML = `<li class="no-notifications">${data.error}</li>`;
                updateBadgeCount(0);
                return;
            }

            if (data.length === 0) {
                notificationsList.innerHTML = '<li class="no-notifications">No new notifications.</li>';
                updateBadgeCount(0);
                return;
            }

            data.forEach(notification => {
                const li = document.createElement("li");
                li.className = "notification-item";
                li.innerHTML = `
                    <div class="content">${notification.message}</div>
                    <button class="mark-read" data-id="${notification.id}">Mark as read</button>
                `;
                notificationsList.appendChild(li);
            });

            updateBadgeCount(data.length);
        })
        .catch(error => console.error("❌ DEBUG: Error fetching notifications:", error));
    }

    notificationsList.addEventListener("click", (event) => {
        if (event.target.classList.contains("mark-read")) {
            const id = event.target.dataset.id;

            fetch(`/api/notifications/read/${id}`, { method: "POST" })
            .then(response => response.json())
            .then(() => {
                event.target.closest(".notification-item").remove(); // Remove from UI
                updateBadgeCount();
            })
            .catch(error => console.error("❌ DEBUG: Error marking as read:", error));
        }
    });

    function updateBadgeCount(count = null) {
        if (count === null) {
            count = document.querySelectorAll(".notification-item").length;
        }

        if (count > 0) {
            badge.textContent = count;
            badge.style.display = "block";  // Show badge
        } else {
            badge.style.display = "none";   // Hide badge if no notifications
            notificationsList.innerHTML = '<li class="no-notifications">No new notifications.</li>';
        }
    }

    fetchNotifications();
});
