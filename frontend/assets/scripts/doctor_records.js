
async function fetchDoctorPatientRecords() {
    console.log("Fetching doctor patient records...");
    const response = await fetch('/records/doctor/records');
    const records = await response.json();
    console.log("Doctor fetched records:", records);

    let recordsHtml = "";
    if (records.length === 0 || records.message) {
        recordsHtml = `<tr><td colspan="5">No patient records found</td></tr>`;
    } else {
        records.forEach(record => {
            recordsHtml += `
                <tr>
                    <td>${record.patient_name}</td>
                    <td>${record.appointment_date}</td>
                    <td>
                        <textarea class="form-control" id="doctor-notes-${record.record_id}">${record.doctor_notes || ""}</textarea>
                    </td>
                    <td>
                        <textarea class="form-control" readonly>${record.patient_notes || "No patient notes"}</textarea>
                    </td>
                    <td>
                        <button class="btn btn-primary btn-sm" onclick="updateDoctorNotes(${record.record_id})">Save</button>
                    </td>
                </tr>
            `;
        });
    }

    document.getElementById("doctor-patient-records").innerHTML = recordsHtml;
}

document.addEventListener("DOMContentLoaded", fetchDoctorPatientRecords);

async function updateDoctorNotes(recordId) {
    const notes = document.getElementById(`doctor-notes-${recordId}`).value;

    const response = await fetch(`/records/doctor/records/${recordId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ doctor_notes: notes })
    });

    const result = await response.json();
    alert(result.message);
}

document.addEventListener("DOMContentLoaded", fetchDoctorPatientRecords);
