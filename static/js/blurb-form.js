$(function() {
    $('body').data('attachmentid', 0);
    $('li.required label').each(function() {
        $(this).html($(this).html() + ' <span style="color: red;">*</span>');
    });
    $('#more-attachments').click(function(e) {
        e.preventDefault();
        var id = $('body').data('attachmentid');
        $('body').data('attachmentid', id + 1);
        var newfield = $('<ul>');
        newfield.append('<li>What is it? <br/>\n');
        var title = $('<input type="text" maxlength="50">');
        title.attr('id', 'id_document_set-' + id + '-title');
        title.attr('name', 'document_set-' + id + '-title');
        newfield.append(title);
        newfield.append('\n</li>\n');
        var file = $('<input type="file">');
        file.attr('id', 'id_document_set-' + id + '-data');
        file.attr('name', 'document_set-' + id + '-data');
        newfield.append('<li>');
        newfield.append(file);
        newfield.append('</li>');
        $('#attachment-list').append(newfield);
        $('#id_document_set-TOTAL_FORMS').val(id + 1);
    });
}); 
