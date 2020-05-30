jQuery(document).ready(function($) {
    $.extend($.validator.messages, {
        required: "تکمیل این فیلد اجباری است.",
        remote: "لطفا این فیلد را تصحیح کنید.",
        email: "لطفا یک ایمیل صحیح وارد کنید.",
        // url: "لطفا آدرس صحیح وارد کنید.",
        date: "لطفا تاریخ صحیح وارد کنید.",
        dateFA: "لطفا یک تاریخ صحیح وارد کنید.",
        dateISO: "لطفا تاریخ صحیح وارد کنید (ISO).",
        number: "لطفا عدد صحیح وارد کنید.",
        digits: "لطفا فقط عدد (انگلیسی) وارد کنید.",
        creditcard: "لطفا کریدیت کارت صحیح وارد کنید.",
        equalTo: "لطفا مقدار برابری وارد کنید.",
        extension: "لطفا مقداری وارد کنید که",
        alphanumeric: "لطفا مقدار را عدد  وارد کنید.",
        maxlength: $.validator.format("لطفا بیشتر از {0} حرف وارد نکنید."),
        minlength: $.validator.format("لطفا کمتر از {0} حرف وارد نکنید."),
        rangelength: $.validator.format("لطفا مقداری بین {0} تا {1} حرف وارد کنید."),
        range: $.validator.format("لطفا مقداری بین {0} تا {1} حرف وارد کنید."),
        max: $.validator.format("لطفا مقداری کمتر از {0} وارد کنید."),
        min: $.validator.format("لطفا مقداری بیشتر از {0} وارد کنید."),
        minWords: $.validator.format("لطفا حداقل {0} کلمه وارد کنید."),
        maxWords: $.validator.format("لطفا حداکثر {0} کلمه وارد کنید.")
    });

    $.validator.addMethod('customphone', function(value, element) {
        return this.optional(element) || /^(\+98)?09\d{9}$/.test(value);
    }, "لطفا شماره همراه درست وارد کنید");

    jQuery.validator.addMethod("lettersonlyen", function(value, element) {
        return this.optional(element) || /^[/a-z/0-9 ]+$/i.test(value);
    }, "فقط متن انگلیسی بنویسید");
    jQuery.validator.addMethod("letternumbe", function(value, element) {
        return this.optional(element) || /^[,/0-9]+$/i.test(value);
    }, "فقط عدد بنویسید");

    jQuery.validator.addMethod("lettersonly", function(value, element) {
        return this.optional(element) || /^[ا-ی/آ/ئ/ ]+$/i.test(value);
    }, "فقط متن فارسی بنویسید");

    jQuery.validator.addMethod("myEmail", function(value, element) {
        return this.optional(element) || (/^[a-z0-9]+([-._][a-z0-9]+)*@([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,4}$/.test(value) && /^(?=.{1,64}@.{4,64}$)(?=.{6,100}$).*/.test(value));
    }, 'لطفا ایمیل معتبر وارد کنید');

    jQuery.validator.addMethod("codemelli", function(value, element) {
        if (value == '1111111111' || value == '0000000000' || value == '2222222222' || value == '3333333333' || value == '4444444444' || value == '5555555555' || value == '6666666666' || value == '7777777777' || value == '8888888888' || value == '9999999999' || value == '0123456789') {
            return false
        }
        c = parseInt(value.charAt(9));
        n = parseInt(value.charAt(0)) * 10 + parseInt(value.charAt(1)) * 9 + parseInt(value.charAt(2)) * 8 + parseInt(value.charAt(3)) * 7 + parseInt(value.charAt(4)) * 6 + parseInt(value.charAt(5)) * 5 + parseInt(value.charAt(6)) * 4 + parseInt(value.charAt(7)) * 3 + parseInt(value.charAt(8)) * 2;
        r = n - parseInt(n / 11) * 11;
        if ((r == 0 && r == c) || (r == 1 && c == 1) || (r > 1 && c == 11 - r)) {
            return true
        }
    }, " لطفا کدملی درست وارد کنید");


    $(".smart-validate").validate({
        errorClass: "error",
        validClass: "success",
        errorElement: "em",
        errorPlacement: function(error, element) {
            var type = $(element).attr("type");
            if (type === "text") {
                element.closest('.gui-input').after(error);
            } else {
                error.insertAfter(element.parent());
            }
            if (element.is(":radio") || element.is(":checkbox")) {
                element.closest('.option-group').after(error);
            } else {
                error.insertAfter(element.parent());
            }
        },
    });
    // var web=$("#website");
    // web.change(function () {
    //     var str = $("#website").val(); 
    //     var n = str.includes("https://") || str.includes("http://");
    //     if(n==false && str.length > 0){
    //         $(web).attr('value', 'https://');
    //         $("#ddemo").html("لطفا آدرس صحیح وارد کنید")
    //         web.addClass("bordererror")
    //         console.log(2);  
    //     }else if(n==true || str.length == 0){
    //         $(web).attr('value', str);
    //         $("#ddemo").html("")
    //         web.removeClass("bordererror")
    //         console.log(1);
    //     }
    // })
    // var str = $("#website").val();
    // if(str){
    //     var n = str.includes("https://") || str.includes("http://");
    //     if(n==false){
    //         if(str== null){
    //             $(web).attr('value', 'https://');   
    //         }else{
                
    //         }
    //     }
    // }
});