var pipeline = {
    new_category: function (name) {
        var cat = $('<div class="category">');
        var header = $('<div class="category-header">');
        header.html(name);
        var list = $('<div class="category-list">');
        list.sortable({
            connectWith: '#blurb-list, div.category-list'
        });
        header.click(function() {
            if ($(this).find('button').length)
                return;
            var ok = $('<button>Ok</button>');
            var input = $('<input type="text" value="' + $(this).html() + '"/>');
           
            var that = $(this);
            input.click(function() {
                return false;
            }); 
            ok.click(function() {
                that.html(input.val());
                return false;
            }); 
            $(this).html('');
            $(this).append(input);
            $(this).append(ok);
        });
        cat.append(header);
        cat.append(list);
        cat.dblclick(function() {
            $(this).find('div.blurb').each(function () {
                $('#blurb-list').append($(this));
        });
        $(this).remove();
        });
        $('#pipeline').append(cat);
    },

    new_event: function(lines) {
        var newevent = $('<div class="event">');
        var title = $('<div class="event-title">');
        title.html(lines[0]);
        var content = $('<div class="event-description">');
        content.html(lines.slice(1).join("<br/>"));
        newevent.append(title);
        newevent.append(content);
        $('#events').append(newevent);
        newevent.dblclick(function() {
            $(this).remove();
        });
        $('#new-event').val('');  
    },

    get: function() {
        var headers = [];
        $('#pipeline .category').each(function() {
            var blurbs = [];
            $(this).find('.blurb').each(function() {
                blurbs.push(parseInt($(this).attr('id')));
            });
            headers.push({
                'title': $(this).find('.category-header').html(),
                'blurbs': blurbs
            });
        });
        var events = [];
        var index = 1;
        $('#events .event').each(function() {
            events.push({
                'index': index,
                'title': $(this).find('.event-title').html(),
                'lines': $(this).find('.event-description').html().split("<br>")
            });
            index = index + 1;
        });
        return JSON.stringify({
            'headers': headers,
            'events': events
        });
    },
};

$(function() {
    $('#pipeline').sortable();
    $('#events').sortable();
    $('#blurb-list').sortable({
        connectWith: 'div.category-list'
    });
    $('#new-category').click(function() {
        var name = prompt('Category name', '');
        if (name)
            pipeline.new_category(name);
    });
    $('#preview, #download').submit(function() {
        var input = $('<input>');
        input.attr('type', 'hidden');
        input.attr('name', 'pipeline');
        input.attr('value', pipeline.get());
        $(this).append(input);
    });
    $('#add-event').click(function() {
        if ($('#new-event').val()) {
            var lines = $('#new-event').val().split("\n");
            pipeline.new_event(lines);
        }
    });
});  
