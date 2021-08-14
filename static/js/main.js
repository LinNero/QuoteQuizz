$( document ).ready(function() {
    $( "button" ).click(function() {
        chosen_answer = $(this).prop("value");

        if (chosen_answer == correct_answer) {
            $(this).addClass("btn-success");
            $(this).removeClass("btn-light");
            $("#message").append("Это правильный ответ!")
        } else {
            $(this).addClass("btn-danger");
            $(this).removeClass("btn-light");

            var list = $("[value='" + correct_answer + "']");
            $(list).addClass("btn-success");
            $(list).removeClass("btn-light");

            $("#message").append("Это неправильный ответ!")
        }

        $( "button" ).off("click");
        $("#message").append("<div><a href='./next'>Следующий вопрос</a></div>")
    });
});