async function fetchPatientRecords() {
  showLoader();
  const res = await fetch("/records/patient/records");
  const data = await res.json();

  let html = "";
  data.forEach((record) => {
    html += `
        <tr>
          <td>${record.doctor_name}</td>
          <td>${record.appointment_date}</td>
  
          <td><textarea class="form-control" readonly>${
            record.doctor_notes || ""
          }</textarea></td>
          <td><textarea class="form-control" id="patient-note-${
            record.record_id
          }">${record.patient_notes || ""}</textarea></td>
  
          <td><span class="badge bg-info">${
            record.status_tag || "New"
          }</span></td>
  
          <td>
            ${
              record.attachment_url
                ? `<a href="/${record.attachment_url}" download target="_blank">Download PDF</a>`
                : "N/A"
            }
          </td>
  
          <td>
            <button class="btn btn-primary btn-sm" onclick="savePatientNote(${
              record.record_id
            })">Save Note</button>
            <button class="btn btn-secondary btn-sm" onclick="viewHistory(${
              record.record_id
            })">History</button>  
          </td>
        </tr>`;
  });

  document.getElementById("patient-records-body").innerHTML = html;
  hideLoader();
}

async function savePatientNote(recordId) {
  showLoader();
  const note = document.getElementById(`patient-note-${recordId}`).value;
  await fetch(`/records/patient/records/${recordId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ patient_notes: note }),
  });
  alert("Note saved.");
  hideLoader();
}

async function viewHistory(recordId) {
  showLoader();
  const res = await fetch(`/records/history/${recordId}`);
  const history = await res.json();

  let html = "<ul class='list-group'>";
  history.forEach((item) => {
    html += `<li class='list-group-item'>
        <strong>${item.username}</strong>: ${item.action} <br>
        <small>${new Date(item.timestamp).toLocaleString()}</small>
      </li>`;
  });
  html += "</ul>";

  document.getElementById("historyContent").innerHTML = html;
  new bootstrap.Modal(document.getElementById("historyModal")).show();
  hideLoader();
}

document.addEventListener("DOMContentLoaded", fetchPatientRecords);

function showLoader() {
  document.getElementById("loader").style.display = "block";
}

function hideLoader() {
  document.getElementById("loader").style.display = "none";
}
