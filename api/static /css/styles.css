$(document).ready(function() {
    $("#prediction-form").submit(function(event) {
        event.preventDefault();
        
        var form = $(this);
        var data = {
            "pclass": form.find("#pclass").val(),
            "sex": form.find("#sex").val(),
            "age": form.find("#age").val(),
            "fare": form.find("#fare").val(),
            "embarked": form.find("#embarked").val(),
            "title": form.find("#title").val(),
            "isAlone": form.find("#isAlone").val(),
            "ageClass": form.find("#ageClass").val()
        };
        
        $.ajax({
            url: "/predict",
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json",
            success: function(response) {
                $("#result").text("Prediction: " + response.prediction);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});
