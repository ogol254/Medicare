
var form_validation = function() {
    var e = function() {
            jQuery(".form-valide").validate({
                ignore: [],
                errorClass: "invalid-feedback animated fadeInDown",
                errorElement: "div",
                errorPlacement: function(e, a) {
                    jQuery(a).parents(".form-group > div").append(e)
                },
                highlight: function(e) {
                    jQuery(e).closest(".form-group").removeClass("is-invalid").addClass("is-invalid")
                },
                success: function(e) {
                    jQuery(e).closest(".form-group").removeClass("is-invalid"), jQuery(e).remove()
                },
                rules: {
                    "val-fname": {
                        required: !0,
                        minlength: 3
                    },
                    "val-lname": {
                        required: !0,
                        minlength: 3
                    },
                    "val-password": {
                        required: !0,
                        minlength: 5
                    },
                    "val-confirm-password": {
                        required: !0,
                        equalTo: "#val-password"
                    },
                    "val-address": {
                        required: !0,
                        minlength: 5
                    },
                    "val-role": {
                        required: !0
                    },
                    "val-phoneus": {
                        required: !0
                    },
                    "val-id-num": {
                        required: !0,
                        digits: !0
                    },
                    "val-name": {
                        required: !0,
                        minlength: 5
                    },
                    "val-description":{
                        required: !0,
                        minlength: 30
                    },
                    "val-type": {
                        required: !0
                    }
                },
                messages: {
                    "val-fname": {
                        required: "Please enter a First name",
                        minlength: "Your First name must consist of at least 3 characters"
                    },
                    "val-lname": {
                        required: "Please enter a last name",
                        minlength: "Your last name must consist of at least 3 characters"
                    },
                    "val-password": {
                        required: "Please provide a password",
                        minlength: "Your password must be at least 5 characters long"
                    },
                    "val-confirm-password": {
                        required: "Please provide a password",
                        minlength: "Your password must be at least 5 characters long",
                        equalTo: "Please enter the same password as above"
                    },
                    "val-addres": "What do you stay?",
                    "val-role": "Whats his role!",
                    "val-type": "Choose a type below!",
                    "val-phoneus": "Please enter a KE phone!",
                    "val-id-num": "Please enter only digits!",
                    "val-name": {
                        required: "Please enter your full name",
                        minlength: "Your name must consist of at least 5 characters"
                    },
                    "val-description": {
                        required: "Add some description",
                        minlength: "Description must consist of at least 30 characters"
                    }
                }
            })
        }
    return {
        init: function() {
            e(), a(), jQuery(".js-select2").on("change", function() {
                jQuery(this).valid()
            })
        }
    }
}();
jQuery(function() {
    form_validation.init()
});