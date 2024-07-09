document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".type").forEach(select => {
        select.addEventListener("change", handleChange);
    });

    const maxForms = 6;
    const formTemplate = document.getElementById('form-template').innerHTML;
    const formsContainer = document.getElementById('forms-container');
    const addFormBtn = document.getElementById('add-form-btn');
    const submitBtn = document.getElementById('submit-btn');

    document.addEventListener('click', event => {
        if (event.target.classList.contains('delete-form-btn')) {
            handleDeleteForm(event.target);
        }
    });

    addFormBtn.addEventListener('click', handleAddForm);
    submitBtn.addEventListener('click', handleSubmit);

    function handleDeleteForm(button) {
        const form = button.closest('form');
        form.remove();
        if (formsContainer.querySelectorAll('form').length < maxForms) {
            addFormBtn.style.display = 'block';
        }
    }

    function handleAddForm() {
        const formCount = formsContainer.querySelectorAll('form').length + 1;

        if (formCount <= maxForms) {
            const newForm = formTemplate.replace(/__prefix__/g, formCount);
            formsContainer.insertAdjacentHTML('beforeend', newForm);

            if (formCount >= maxForms) {
                addFormBtn.style.display = 'none';
            }
        }
    }

    function handleSubmit(event) {
        event.preventDefault();

        const selects = document.querySelectorAll('select[name="type"]');
        const values = Array.from(selects).map(select => select.value);

        if (hasDuplicates(values)) {
            alert('You cannot choose the same types for different columns!');
            return;
        }

        if (!validateForms()) {
            alert('Please fill in all fields');
            return;
        }

        const inputOrders = formsContainer.querySelectorAll('input[name="order"]');
        const orders = {};

        let allValid = Array.from(inputOrders).every(inputOrder => {
            const orderValue = inputOrder.value.trim();

            if (!Number.isInteger(+orderValue) || orders[orderValue]) {
                return false;
            }

            orders[orderValue] = true;
            return true;
        });

        if (!allValid) {
            alert("There are invalid or non-unique input values.");
            return;
        }

        if (!checkIntFields()) {
            return;
        }

        const input1Value = document.querySelector('input[name="input1"]').value;
        const input2Value = document.querySelector('input[name="input2"]').value;

        if (Number(input2Value) <= Number(input1Value)) {
            alert('Value in field "To" must be bigger than in "From"');
            return;
        }

        submitForm();
    }

    function hasDuplicates(array) {
        return new Set(array).size !== array.length;
    }

    function validateForms() {
        const fields = document.querySelectorAll('#schema-info input, #schema-info select, #forms-container input, #forms-container select');
        return Array.from(fields).every(field => field.value.trim() !== '');
    }

    function checkIntFields() {
        const intFields = document.querySelectorAll('.int_field');
        const isInteger = Array.from(intFields).every(field => Number.isInteger(Number(field.value)));

        if (!isInteger) {
            alert("Please enter integer values in all From-To fields.");
            return false;
        }
        return true;
    }

    function submitForm() {
        const fullVal = {};
        const forms = document.querySelectorAll("#forms-container form");

        const sep = document.querySelector("#schema-info select[name='sep']").value;
        const stch = document.querySelector("#schema-info select[name='stch']").value;
        const name = document.querySelector("#schema-info input[name='name']").value;

        fullVal.name = name;
        fullVal.sep = sep;
        fullVal.stch = stch;

        forms.forEach(form => {
            const colName = form.querySelector("input[name='col_name']").value;
            const type = form.querySelector("select[name='type']").value;
            const order = form.querySelector("input[name='order']").value;

            if (type === 'Integer') {
                const input1 = form.querySelector("input[name='input1']").value;
                const input2 = form.querySelector("input[name='input2']").value;
                fullVal[type] = {input1, input2, col_name: colName, order};
            } else {
                fullVal[type] = {col_name: colName, order};
            }
        });

        $.ajax({
            url: '/getting/',
            method: 'POST',
            data: {'values': JSON.stringify(fullVal)},
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', document.querySelector('input[name="csrfmiddlewaretoken"]').value);
            },
            dataType: 'json',
            success: function () {
                window.location.replace('/');
            },
            error: function () {
                alert('Error!');
            }
        });
    }

    function handleChange(event) {
        const select = event.target;
        const selectedValue = select.value;

        if (selectedValue === "Integer") {
            addIntegerFields(select);
        } else {
            removeIntegerFields(select);
        }
    }

    function addIntegerFields(select) {
        const input1 = createIntegerField("input1", "From");
        const input2 = createIntegerField("input2", "To");

        select.parentNode.insertAdjacentElement("afterend", input2);
        select.parentNode.insertAdjacentElement("afterend", input1);
    }

    function createIntegerField(name, placeholder) {
        const input = document.createElement("input");
        input.setAttribute("type", "text");
        input.setAttribute("name", name);
        input.setAttribute("placeholder", placeholder);
        input.setAttribute("class", "int_field");
        input.setAttribute("style", "width:70px");
        return input;
    }

    function removeIntegerFields(select) {
        let nextElement = select.parentNode.nextElementSibling;
        while (nextElement && nextElement.classList.contains("int_field")) {
            nextElement.remove();
            nextElement = select.parentNode.nextElementSibling;
        }
    }
});
