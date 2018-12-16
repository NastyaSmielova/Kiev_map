var quizContainer ;
var resultsContainer ;
var submitButton ;
var answersContainer ;
var startButton ;

var questions =  [];
var questionIter = 0;
var numCorrect = 0;
var numErrors = 0;
var play = false;

var countDownDate = 0;




function init() {
    quizContainer = document.getElementById('quiz');
    resultsContainer = document.getElementById('results');
    submitButton = document.getElementById('submit');
    answersContainer = document.getElementById('answers');
    startButton = document.getElementById('start');

    startButton.onclick = function(){
                start();
    };

}
setInterval(function() {
      if (play){
      var now = new Date().getTime();

      var distance = countDownDate - now;

      var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      var seconds = Math.floor((distance % (1000 * 60)) / 1000);

      document.getElementById("clock").innerHTML = 'Час: ' +  minutes + " хв " + seconds + "с ";

      if (distance < 0) {
        if (play) {
            document.getElementById("clock").innerHTML = "час закінчився";

            play = false;
            stopGame();
        }
      }}
    }, 1000);

function addQuestion(question) {
    questions.push(question);
}


function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
}

function start() {
    shuffleArray(questions);
    questionIter = 0  ;
    numCorrect = 0;
    numErrors = 0;
    play = true;
    countDownDate =  new Date(new Date().getTime() + 0.51*60000).getTime() ;

    answersContainer.innerHTML = 'Запитання ';
    resultsContainer.innerHTML = ' ';
    document.getElementById('introText').innerHTML = "";
    startButton.style.visibility= 'hidden';
    submitButton.style.visibility= 'visible';
    quizContainer.style.visibility= 'visible';
    resultsContainer.style.visibility= 'visible';
    document.getElementById('answers').style.visibility= 'visible';
    document.getElementById('quizresult').style.visibility= 'hidden';
    generateQuiz(questions, quizContainer, resultsContainer, submitButton,answersContainer);
    document.getElementById('clock').style.visibility= 'visible';
}

function generateQuiz(questions, quizContainer, resultsContainer, submitButton,answersContainer){
    function showQuestions(questions, quizContainer){

        var output = [];
        var answers;
            i = questionIter;
            var question = (questions[i]);
            answers = [];
            for(letter in question[1]){
                answers.push(
                    '<label>'
                        + '<input type="radio" name="question'+i+'" value="'+letter+'">'
                        + letter + ': '
                        + question[1][letter]
                    + '</label><br>'
                );
            }

            output.push(
                '<div class="question" >' + questions[i][0] + '</div>'
                + '<div class="answers">' + answers.join('') + '</div>'
            );
        quizContainer.innerHTML = output.join('');
    }


    function showResults(questions, quizContainer, resultsContainer,answersContainer){
        var answerContainers = quizContainer.querySelectorAll('.answers');
        var userAnswer = '';

        i  = questionIter;

            userAnswer = (answerContainers[0].querySelector('input[name=question'+i+']:checked')||{}).value;

            if(userAnswer===questions[i][2]){
                numCorrect++;

            }
            else{
                answerContainers[0].style.color = 'red';
                numErrors++;
                if (numErrors >= 3){
                    play = false;
                    stopGame();
                }
            }

        resultsContainer.innerHTML = numCorrect +  ' / ' + (questionIter+1);
        answersContainer.innerHTML  = answersContainer.innerHTML +' '+ (questionIter+1).toString();
        if(numErrors===0){
                answersContainer.style.color = 'lightgreen';
            }
            else if(numErrors===1){
                answersContainer.style.color = 'orange';
            }
            else{
               answersContainer.style.color = 'red';
        }

        questionIter = questionIter+1;
        showQuestions(questions,quizContainer)
    }

    showQuestions(questions, quizContainer);

    submitButton.onclick = function(){
        showResults(questions, quizContainer, resultsContainer,answersContainer);
    }

}

function stopGame() {
    alert('game is over');
    document.getElementById('clock').style.visibility= 'hidden';
    document.getElementById('answers').style.visibility= 'hidden';
    quizContainer.style.visibility= 'hidden';
    startButton.style.visibility= 'visible';
    submitButton.style.visibility= 'hidden';
    resultsContainer.style.visibility= 'hidden';
    document.getElementById('quizresult').style.visibility= 'visible';
    document.getElementById('quizresult').innerHTML = "Ви набрали " + numCorrect.toString()+ " ! "
    document.getElementById('introText').innerHTML = "Потрібно обрати одну правильну відповідь на наведене запитання.<br> Після 3 помилки гра закінчується. <br>Час також є обмеженим. Щасти!"

}

