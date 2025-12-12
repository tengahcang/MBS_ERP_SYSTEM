document.addEventListener("DOMContentLoaded", function () {
    const typeField = document.getElementById("id_customer_type");
    const businessFieldRow = document.querySelector(".form-row.field-business_entity_type");

    function toggleBusinessField() {
        if (!typeField || !businessFieldRow) return;

        if (typeField.value === "company") {
            businessFieldRow.style.display = "";
        } else {
            businessFieldRow.style.display = "none";
        }
    }

    // Run on load
    toggleBusinessField();

    // Run when dropdown changes
    typeField.addEventListener("change", toggleBusinessField);
});