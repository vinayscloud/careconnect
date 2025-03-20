async function fetchPatientRecords() {
    console.log("Fetching patient records...");
    const response = await fetch('/records/patient/records');
    const records = await response.json();
    console.log("Patient fetched records:", records);

    let recordsHtml = "";
    if (records.length === 0 || records.message) {
        recordsHtml = `<tr><td colspan="5">No medical records found</td></tr>`;
    } else {
        records.forEach(record => {
            recordsHtml += `
                <tr>
                    <td>${record.doctor_name}</td>
                    <td>${record.appointment_date}</td>
                    <td><textarea class="form-control" readonly>${record.doctor_notes || "No notes available"}</textarea></td>
                    <td><textarea class="form-control" id="patient-notes-${record.record_id}">${record.patient_notes || ""}</textarea></td>
                    <td>
                        <button class="btn btn-primary btn-sm" onclick="updatePatientNotes(${record.record_id})">Save</button>
                    </td>
                </tr>
            `;
        });
    }

    document.getElementById("patient-records").innerHTML = recordsHtml;
}


async function updatePatientNotes(recordId) {
    const notes = document.getElementById(`patient-notes-${recordId}`).value;

    const response = await fetch(`/records/patient/records/${recordId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ patient_notes: notes })
    });

    const result = await response.json();
    alert(result.message);
}

document.addEventListener("DOMContentLoaded", fetchPatientRecords);
