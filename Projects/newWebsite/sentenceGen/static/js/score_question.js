var frm = $('#lightning_score_sentence');

frm.submit(function (ev) {
    $.ajax({
        type: frm.attr('method'),
        url: frm.attr('action'),
        data: frm.serialize(),
        success: function (data) {
            $('#lightning_answer').html(data);
            $('#score_submit_button').val("Try Again");
        },
        error: function (xhr, textStatus, errorThrown) {
            console.log("made it to repo comment function FAIL");
            if (!(xhr.status == 0 || xhr.status == '0' || errorThrown == 0 || errorThrown == '0' || xhr.response == 0 || xhr.response == '0')) {
                alert("Please report this error: " + errorThrown + xhr.status + xhr.responseText);

            }
        }
    });

    ev.preventDefault();
});