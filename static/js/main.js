$( document ).ready(function() {
    function removeBindings() {
        // Remove binding from all buttons
        $( "button" ).off("click");
    }

    function showCorrectAnswer() {
        var list = $("[value='" + correct_answer + "']");
        $(list).addClass("btn-success");
        $(list).removeClass("btn-light");
    }

    $( "button" ).click(function() {
        chosen_answer = $(this).prop("value");

        if (chosen_answer == correct_answer) {
            showCorrectAnswer()
        } else {
            $(this).addClass("btn-danger");
            $(this).removeClass("btn-light");

            showCorrectAnswer()
        }

        // Set the timer to end.
        bar.set(1.0);
        removeBindings()
    });

    // ProgressBar code
  container = document.getElementById('progressbar_container')
  var bar = new ProgressBar.Circle(container, {
      color: '#aaa',
      // This has to be the same size as the maximum width to
      // prevent clipping
      strokeWidth: 4,
      trailWidth: 1,
      easing: 'linear',
      duration: 20000, // milliseconds
      text: {
        autoStyleContainer: false
      },
      from: { color: '#aaa', width: 1 },
      to: { color: '#333', width: 4 },
      // Set default step function for all animate calls
      step: function(state, circle) {
        circle.path.setAttribute('stroke', state.color);
        circle.path.setAttribute('stroke-width', state.width);

        var value = circle.value();
        if (value === 0) {
          circle.setText('');
        }
        else if (value === 1) {
          circle.setText("<a class='nexthref' href='./next'>Дальше</a>");
          showCorrectAnswer()
          removeBindings()
          circle.stop();
        }
        else {
          circle.setText(Math.round(value*20));
        }

      }
    });

    bar.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
    bar.text.style.fontSize = '2rem';

    bar.animate(1.0, {duration: 10000});
});