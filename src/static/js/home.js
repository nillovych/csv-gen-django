function deleteRow(id) {
    $.ajax({
        url: "/delete_row/",
        type: "POST",
        data: {row_id: id},
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader('X-CSRFToken', $('input[name="csrfmiddlewaretoken"]').val());
        },
        success: function () {
            $("#" + id).remove();
        }
    });
}