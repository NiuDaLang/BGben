// Q & As
let questions;

const qNo = document.querySelector("#quiz-number")
const questionElement = document.querySelector("#quiz-question");
const answerButtons = document.querySelector("#quiz-answers")
const nextButton = document.querySelector("#next-button")
const toRegister = document.querySelector("#toRegister")
const linkButton = document.querySelector("#link-button")
const questionNumbers = document.querySelector("#question-numbers")

let currentQuestionIndex = 0;
let score = 0;
let registerOk = false;

async function getJson(selection) {
  let response = await fetch(`${window.origin}/register_test_quiz`, {
    method: 'POST',
    credentials: 'include',
    body: JSON.stringify({
      selection: selection
    }),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json",
      "X-CSRF-TOKEN": csrf_token
    }),
  })
  let data = response.json()
  return data
}

function startQuiz() {
  const lang = document.getElementById('lang').innerText;
  currentQuestionIndex = 0;
  score = 0;
  if (lang == 'zh') {
    nextButton.innerHTML = "下一题";
  } else if (lang == 'ja') {
    nextButton.innerHTML = "次の問題";
  } else {
    nextButton.innerHTML = "NEXT";
  }
  showQuestion();
}
function showQuestion() {
  resetState() //Delete all answers for the preveious questions one-by-one
  let currentQuestion = questions[currentQuestionIndex];
  let questionNo = currentQuestionIndex + 1;
  qNo.innerHTML = questionNo
  questionElement.innerHTML = currentQuestion.question;
  currentQuestion.answers.forEach(answer => {
    const button = document.createElement("button");
    button.innerHTML = answer.text;
    button.classList.add("quiz-answer");
    answerButtons.appendChild(button);
    if (answer.correct) {
      button.dataset.correct = answer.correct;
    }
    button.addEventListener("click", selectAnswer);
  })
}
function resetState() {
  nextButton.style.display = "none";
  while (answerButtons.firstChild) {
    answerButtons.removeChild(answerButtons.firstChild)
  }
}
function selectAnswer(e) {
  const selectedBtn = e.target;
  const isCorrect = selectedBtn.dataset.correct === "true";
  const lang = document.getElementById('lang').innerText;

  if (isCorrect) {
    selectedBtn.classList.add("correct");
    score += 1
  } else {
    selectedBtn.classList.add("incorrect");
  }
  // Disable buttons after answer clicked
  Array.from(answerButtons.children).forEach(button => {
    if (button.dataset.correct === 'true') {
      button.classList.add("correct")
    }
    button.disabled = true;
  });

  if (currentQuestionIndex + 1 < questions.length) {
    if (lang == 'zh') {
      nextButton.innerHTML = "下一题";
    } else if (lang == 'ja') {
      nextButton.innerHTML = "次の問題";
    } else {
      nextButton.innerHTML = "NEXT";
    }
  } else {
    if (lang == 'zh') {
      nextButton.innerHTML = "看结果";
    } else if (lang == 'ja') {
      nextButton.innerHTML = "結果を見る";
    } else {
      nextButton.innerHTML = "RESULT";
    }
  }
  nextButton.style.display = "block";
}
function showScore() {
  const lang = document.getElementById('lang').innerText;
  resetState();
  if (lang == 'zh') {
    questionElement.innerHTML = `您的总得分是${score} / ${questions.length}分！`
  } else if (lang == 'ja') {
    questionElement.innerHTML = `あなたの総得点は${score} / ${questions.length}点です！`
  } else {
    questionElement.innerHTML = `Your total score is ${score} / ${questions.length}！`
  }

  if (score >= 8) {
    nextButton.style.display = 'none';
    toRegister.style.display = 'block';
    linkButton.style.display = 'block';
    questionNumbers.style.display = 'none'
    questionElement.style.textAlign = 'center'
    registerOk = true;
  } else {
    if (lang == 'zh') {
      nextButton.innerHTML = "再来一遍!";
    } else if (lang == 'ja') {
      nextButton.innerHTML = "もう一度挑戦!";
    } else {
      nextButton.innerHTML = "Try again!";
    }

    nextButton.style.display = "block"
  }
  // nextButton.style.display = "block"
}
function handleNextButton() {
  currentQuestionIndex++;
  if (currentQuestionIndex < questions.length) {
    showQuestion();
  } else {
    showScore()

  }
}

$(document).ready(function () {
  $("#register-test").on("submit", function (e) {
    e.preventDefault();

    // get selection of quiz topic
    const form = document.querySelector("#register-test")
    const formData = new FormData(form);
    const values = [...formData.entries()];
    selection = values[0][1];

    console.log(selection)
    // fetch quiz questions from backend
    // start quiz
    if (selection != 0) {
      getJson(selection).then(data => {
        questions = data['selected_questions']

        $(".intro-page").css({ "display": "none" });
        $("#register-test-container").css({
          "background": "#ffffff",
          "box-shadow": "14px 14px 20px #95954e, -14px -14px 20px #f6f6b5"
        });
        $(".quiz-container").css({ "display": "block" })

        // Start Quiz
        startQuiz()

        // Handle Next Option
        nextButton.addEventListener("click", () => {
          if (currentQuestionIndex < questions.length) {
            handleNextButton();
          } else {
            if (registerOk === true) {
              $(".next-button").css("display", "none")
              $(".quiz-container").css("display", "none")
              $(".register-test-container").css({ "width": "60%", "background": "#ffffb0", "box-shadow": "14px 14px 20px #f9f987, -14px -14px 20px #fcfc93" })
              $("#register-form").css("display", "block")
            } else {
              startQuiz()
            }
          }
        })
      });
    } else {
      $('.modal-confirm').css('visibility', 'visible')
      $('#modal-select-close').click(function () {
        $('.modal-confirm').css('visibility', 'hidden')
      })
    }
  })
})
