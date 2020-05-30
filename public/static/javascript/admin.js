jQuery(document).ready(function($) {
    //Json

    var searchRequest = null;
    var minlength = 3;
    var shahidAPI = "api/?birthday=dsd";
    $("#shahid").on('input', function() {
        clearTimeout(this.delay);
        this.delay = setTimeout(function() {

            var id, title, that = this,
                value = $(this).val();
            var resultid = 'sws-result'
            if (value.length >= minlength) {

                $.getJSON(shahidAPI, {
                    title: value,
                }).done(function(data) {

                    var output = '<ul class="searchresult">';
                    $.each(data.result, function(i, item) {
                        output += '<li data-id="' + item.id + '" data-name="' + item.title + '">';
                        output += '<span>' + item.title + '</span>';
                        output += '</li>';
                        if (i === 8) {
                            return false;
                        }
                    });
                    output += '</ul>';
                    $('#' + resultid).show().html(output);
                }).fail(function() {
                    console.log("error");
                }).always(function() {

                });
            } else {
                $('#' + resultid).html('').hide();
            }
        }.bind(this), 500);
    });

    $(document).on('click', '#sws-result .searchresult li', function() {
        var id = $(this).data("id");
        var name = $(this).data("name");
        $('#shahid-id').val(id);
        $('#shahid').val(name);
        $('#sws-result').hide()
    })

    /*
    $("body").on("click",'.addquestion',function(){
    	$('.question-box:last').clone().appendTo(".str").find("input:text").val("").end();
    })
    */
    $("body").on("click", '.removequestion', function() {
        $(this).parent().remove().end();
    });
    /*
    $('#postexcerpt span').text(function(index,text){
        return text.replace('چکیده','شرح شهادت');
    });
    */
})