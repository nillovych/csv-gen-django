$(document).ready(function () {
    $('#gen-btn').click(function (event) {
        event.preventDefault();
        var rowsInput = document.getElementsByName("rows")[0];
        if (!rowsInput.value) {
            alert("Please enter a value for rows.");
            return;
        }
        var full_val = {
            num_gen: rowsInput.value,
            main_id: "{{main_rows.0.id}}"
        };
        var genbi = $('#gen-btn');
        genbi.prop('disabled', true);

        var newRow = $('<tr></tr>');
        var newCell1 = $('<th></th>').text($('#dataset-table tr').length);
        var now = new Date();
        var newCell2 = $('<td></td>').text(now.getFullYear() + '-' + ('0' + (now.getMonth() + 1)).slice(-2) + '-' + ('0' + now.getDate()).slice(-2));
        var newCell3 = $('<td></td>').html('<label class="bg-secondary text-white border rounded p-1">Processing</label>');

        newRow.append(newCell1);
        newRow.append(newCell2);
        newRow.append(newCell3);

        $('#dataset-table').append(newRow);

        $.ajax({
            url: '/generate/',
            method: 'POST',
            data: {
                'values': JSON.stringify(full_val)
            },
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val());
            },
            dataType: 'json',
            success: function (response) {
                var newRow = $('#dataset-table tr:last');
                genbi.prop('disabled', false);
                newRow.find('td:nth-child(3)').html('<label class="bg-success text-white border rounded p-1">Ready</label>');
                var newCell4 = $('<td></td>').html('<a href="/download_csv/' + response.dataset_id + '/" download>Download</a>');
                newRow.append(newCell4);
            },
            error: function (xhr, errmsg, err) {
                alert('Error!');
            }
        });
    });
});