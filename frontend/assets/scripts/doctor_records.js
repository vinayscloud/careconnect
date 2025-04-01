async function fetchDoctorPatientRecords() {
  showLoader();
  const res = await fetch("/records/doctor/records");
  const data = await res.json();

  let html = "";
  data.forEach((record) => {
    html += `
      <tr>
        <td>${record.patient_name}</td>
        <td>${record.appointment_date}</td>

        <td><textarea id="doctor-notes-${
          record.record_id
        }" class="form-control">${record.doctor_notes || ""}</textarea></td>
        <td><textarea class="form-control" readonly>${
          record.patient_notes || ""
        }</textarea></td>

        <td>
          <select class="form-select" onchange="updateStatusTag(${
            record.record_id
          }, this.value)">
            <option ${
              !record.status_tag || record.status_tag === "New"
                ? "selected"
                : ""
            }>New</option>
            <option ${
              record.status_tag === "Follow-up" ? "selected" : ""
            }>Follow-up</option>
            <option ${
              record.status_tag === "Resolved" ? "selected" : ""
            }>Resolved</option>
          </select>
        </td>

        <td>
          ${
            record.attachment_url
              ? `<a href="/${record.attachment_url}" target="_blank">View</a>`
              : ""
          }
          <input type="file" onchange="uploadFile(${record.record_id}, this)">
        </td>

        <td>
          <button class="btn btn-primary btn-sm" onclick="updateDoctorNotes(${
            record.record_id
          })">Save Notes</button>
          <button class="btn btn-secondary btn-sm" onclick="viewHistory(${
            record.record_id
          })">History</button>
        </td>
      </tr>`;
  });

  document.getElementById("doctor-patient-records").innerHTML = html;
  hideLoader();
}

async function updateDoctorNotes(recordId) {
  showLoader();
  const notes = document.getElementById(`doctor-notes-${recordId}`).value;
  await fetch(`/records/doctor/records/${recordId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ doctor_notes: notes }),
  });
  alert("Notes updated.");
  hideLoader();
}

async function updateStatusTag(recordId, tag) {
  showLoader();
  await fetch(`/records/doctor/records/status/${recordId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status_tag: tag }),
  });
  alert("Status tag updated.");
  hideLoader();
}

async function uploadFile(recordId, input) {
  showLoader();
  const file = input.files[0];
  const formData = new FormData();
  formData.append("file", file);

  await fetch(`/records/doctor/records/upload/${recordId}`, {
    method: "POST",
    body: formData,
  });
  alert("File uploaded successfully.");
  await fetchDoctorPatientRecords(); // refresh table
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

document.addEventListener("DOMContentLoaded", fetchDoctorPatientRecords);

function showLoader() {
  document.getElementById("loader").style.display = "block";
}

function hideLoader() {
  document.getElementById("loader").style.display = "none";
}
