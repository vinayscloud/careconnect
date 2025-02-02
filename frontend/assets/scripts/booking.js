document.getElementById("bookingForm").addEventListener("submit", async (event) => {
    event.preventDefault();

    const response = await fetch("http://localhost:5000/api/appointments/book", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            doctorId: 1,
            doctorName: "Dr. John Doe",
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            phone: document.getElementById("phone").value,
            date: "2025-02-10",
            time: "10:00 AM",
            notes: "Need consultation"
        })
    });

    const data = await response.json();
    alert(data.message);
});
