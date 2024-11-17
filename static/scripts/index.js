function toggleDetails(event) {
  const details = document.getElementById("detailsContainer");
  if (event.target.value === "yes") {
    details.classList.remove("hidden");
  } else {
    details.classList.add("hidden");
  }
}

function enableSubmit() {
  const isValid = document.querySelector(
    'input[name="report_landfill"]:checked'
  );
  document.getElementById("submitBtn").disabled = !isValid;
}

function updateReportObjects() {
  const otherInput = document.querySelector('input[name="report_objects"]');
  const checkedBoxes = document.querySelectorAll(
    'input[name="waste_type"]:checked'
  );
  const values = Array.from(checkedBoxes).map((box) => box.value);

  if (otherInput.value.trim()) {
    values.push(otherInput.value.trim());
  }

  otherInput.value = values.join(",");
}
