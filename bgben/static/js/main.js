// Flash message - after login
let login_success_div = document.querySelector('.alert-login-success')
if (login_success_div) {
  let alert_wrapper_div = document.querySelector('.flash-alert')
  alert_wrapper_div.classList.remove('alert')
  alert_wrapper_div.classList.add('alert-login-success-wrapper')
}

// Line Animation
let div1 = document.querySelector("#line-container1"),
  style1 = window.getComputedStyle(div1),
  display1 = style1.getPropertyValue('display');

let div2 = document.querySelector("#line-container2"),
  style2 = window.getComputedStyle(div2),
  display2 = style2.getPropertyValue('display');

let div3 = document.querySelector("#line-container3"),
  style3 = window.getComputedStyle(div3),
  display3 = style3.getPropertyValue('display');

let div4 = document.querySelector("#line-container4"),
  style4 = window.getComputedStyle(div4),
  display4 = style4.getPropertyValue('display');

let div5 = document.querySelector("#line-container5"),
  style5 = window.getComputedStyle(div5),
  display5 = style5.getPropertyValue('display');

let path;

if (display1 == "block") {
  path = document.querySelector("#LinePath1")
} else if (display2 == "block") {
  path = document.querySelector("#LinePath2")
} else if (display3 == "block") {
  path = document.querySelector("#LinePath3")
} else if (display4 == "block") {
  path = document.querySelector("#LinePath4")
} else if (display5 == "block") {
  path = document.querySelector("#LinePath5")
}

if (path) {
  let pathLength = path.getTotalLength()
  path.style.strokeDasharray = pathLength + ' ' + pathLength

  path.style.strokeDashoffset = pathLength

  window.addEventListener("scroll", () => {
    // what % down is it?
    let scrollPercentage = (document.documentElement.scrollTop + document.body.scrollTop)
      / (document.documentElement.scrollHeight - document.documentElement.clientHeight);
    // length to offset the dashes

    let drawLength;
    if (display5 == "block") {
      drawLength = pathLength * scrollPercentage * 2;
    } else {
      drawLength = pathLength * scrollPercentage * 1.2;
    }
    // draw in reverse
    path.style.strokeDashoffset = pathLength - drawLength;

    const target = document.querySelectorAll('.scroll');
    target.forEach((elem) => {
      let pos = window.scrollY * elem.dataset.rate
      if (elem.dataset.direction === 'vertical') {
        return (elem.style.transform = `translateY(${pos}px)`)
      }
    })
    /** Cannot do .map() because A DOM Elements Collection is not an Array object 
     * (it’s an instance of a different class) but you create an Array containing 
     * the data of the collection with Array.prototype.slice */
  })
}


// Starseed Test
let starseedQuestions;

let questionDivs, starseedScore, questionsCompleted, unansweredQs, unansweredQnumbers, starseedValuationRestult;

function startStarseedQuiz() {

  questionDivs = $(".test-question"); // Question text div
  starseedScore = 0; // Total score
  questionsCompleted = 0; // Total questions completed
  unansweredQs = []; // Total unanswered questions
  unansweredQnumbers = [] // Numbers of total unanswered questions
  starseedValuationRestult = "" // Test Result Text Part
  hundredsDivs = $(".hundreds");
  tensDivs = $(".tens")
  singleDivs = $(".single")


  // Insert question text into each question text div
  $.each(questionDivs, function (i, item) {
    questionDivs[i].innerText = starseedQuestions[0][i].text
  })
  // Get answers group for each question
  let answersDivs = $(".test-answer-wrapper")
  // For each answer group, get individual answer buttons
  $.each(answersDivs, function (i, item) {
    let childrenArray = answersDivs[i].children;
    let answersArray = starseedQuestions[0][i].answers;
    let questionNo = i + 1
    // Mark each question as unanswered
    answersDivs[i].dataset.complete = 0;
    // Insert corresponding [i]answer text [ii]question number 
    // [iii]score [iv]class name to each button
    for (i = 0; i < 4; i++) {
      button = childrenArray[i]
      button.innerText = answersArray[i].answer;
      button.dataset.qestionNumber = questionNo;
      button.dataset.score = answersArray[i].score;
      button.classList.add("answer-button")
    }
  })
  // Set score (100s, 10s, 1s) cards to 0
  $.each(hundredsDivs, function (i, item) {
    hundredsDivs[i].innerText = 0;
  })
  $.each(tensDivs, function (i, item) {
    tensDivs[i].innerText = 0;
  })
  $.each(singleDivs, function (i, item) {
    singleDivs[i].innerText = 0;
  })

  // Handle answer clicks
  $(".answer-button").on("click", function (e) {
    handleAnswerBtn(e)
  })
}

function handleAnswerBtn(e) {
  // Identify button clicked, retrieve the assigned score 
  // and it's parentDiv(=question)
  e.stopPropagation();
  e.stopImmediatePropagation();
  let buttonClicked = e.target
  let testScore = parseInt(buttonClicked.dataset.score);
  let parentDiv = buttonClicked.parentElement;

  // add the clicked button's score to the total score
  starseedScore += testScore;
  // mark the question as completed
  parentDiv.setAttribute('data-complete', '1');

  // add 1 to "questions completed"
  questionsCompleted += parseInt(parentDiv.dataset.complete);
  // change the color of of the clicked answer button
  buttonClicked.style.backgroundColor = buttonClicked.dataset.color;
  // highlight the answer selected
  buttonClicked.style.color = "#ffffff";
  buttonClicked.style.fontWeight = "600";
  buttonClicked.style.fontSize = "1.2rem";
  // disable all other answer buttons in the same question
  [...parentDiv.children].forEach(child => {
    child.disabled = true;
    child.style.cursor = "no-drop";
  })
  // display which questions are still unanswered, if any
  $(".unanswered-questions").css("display", "block");
  unansweredQnumbers = []
  unansweredQs = document.querySelectorAll("[data-complete='0']");
  [...unansweredQs].forEach(unanswered => {
    questionNumber = unanswered.dataset.qnumber
    unansweredQnumbers.push(questionNumber)
  })
  $(".unansweredQ").text(unansweredQnumbers)

  // check if all questions are completed
  if (questionsCompleted === 10) {
    // if all complete, display result panel & hide unanswered question msg
    $(".test-result").css("display", "block");
    $(".unanswered-questions").css("display", "none");
    $(".test-result-wrapper-water").css("display", "none");
  }
}

function flipAllCards(_score) {
  let score = _score
  let digits = [...score + ''].map(n => +n)
  const singleDigits = digits.slice(-1)[0] ? digits.slice(-1)[0] : 0;
  const tensDigits = digits.slice(-2, -1)[0] ? digits.slice(-2, -1)[0] : 0;
  const hundredsDigits = digits.slice(-3, -2)[0] ? digits.slice(-3, -2)[0] : 0;

  if (flip(document.querySelector("[data-single]"), singleDigits, "single")
    && flip(document.querySelector("[data-tens]"), tensDigits, "tens")
    && flip(document.querySelector("[data-hundreds]"), hundredsDigits, "hundreds")
  ) {
    return
  } else {
    flip(document.querySelector("[data-single]"), singleDigits, "single")
    flip(document.querySelector("[data-tens]"), tensDigits, "tens")
    flip(document.querySelector("[data-hundreds]"), hundredsDigits, "hundreds")
  }
}

function flip(flipCard, score, digit) {
  const topHalf = flipCard.querySelector(`.top#${digit}`)
  const startNumber = parseInt(topHalf.textContent);
  if (score === startNumber) {
    return { "score": 0 }
  };

  const newNumber = startNumber + 1
  const bottomHalf = flipCard.querySelector(".bottom");
  const topFlip = document.createElement("div");
  topFlip.classList.add("top-flip");
  const bottomFlip = document.createElement("div")
  bottomFlip.classList.add("bottom-flip");

  topHalf.textContent = startNumber;
  bottomHalf.textContent = startNumber;
  topFlip.textContent = startNumber;
  bottomFlip.textContent = newNumber;

  topFlip.addEventListener("animationstart", e => {
    topHalf.textContent = newNumber
  })
  topFlip.addEventListener("animationend", e => {
    topFlip.remove()
  })
  bottomFlip.addEventListener("animationend", e => {
    bottomHalf.textContent = newNumber
    bottomFlip.remove()
  })
  flipCard.append(topFlip, bottomFlip);
}

function fetchResult(result) {
  fetch(`${window.origin}/starseed_result?r=${result}`)
    .then((response) => response.json())
    .then((data) => {
      starseedValuationRestult = data['result'];
    })
}

function showResult() {
  // Test-Result Flip-Card
  let score = starseedScore;
  let numbers = [...score + ''].map(n => +n);
  let maxNumber = Math.max(...numbers)

  // Determine valuation
  switch (true) {
    case (score >= 33 && score <= 54):
      fetchResult('a')
      break;
    case (score >= 55 && score <= 76):
      fetchResult('b')
      break;
    case (score >= 77):
      fetchResult('c')
      break;
    default:
      starseedValuationRestult = "";
  }

  // Fade away cover div, flip cards with the score
  $(".test-result-cover").fadeOut();
  if (score > 0) {
    let obj = setInterval(function () {
      flipAllCards(score);
      maxNumber--;
      if (maxNumber == 0) {
        clearInterval(obj)
        $(".test-result-description").animate({ 'opacity': 0 }, 500, function () {
          $(this).text(starseedValuationRestult);
        }).animate({ 'opacity': 1 }, 200);
      }
    }, 100)
  }
}

function reset() {
  // reset complete status
  answersDivs = document.querySelectorAll(".test-answer-wrapper")
  answersDivs.forEach(div => {
    div.setAttribute('data-complete', '0');
  })

  // re-enable all answer buttons & remove cursor no-drop
  $(".answer-button").prop("disabled", false)
  $(".answer-button").css("cursor", "pointer")

  // reverse colors back for all answer buttons
  let answerButtons = document.querySelectorAll(".answer-button");
  answerButtons.forEach(button => {
    button.style.backgroundColor = button.dataset.origcolor;
    button.style.color = "#383838";
    button.style.fontSize = "1rem";
    button.style.fontWeight = "200";
  })

  // reset visual effect [hide test result & unanswered Q Nos, water effect]
  $(".test-result").css("display", "none");
  $(".test-result-cover").fadeIn();
  $(".test-result-description").text("");
  $(".unanswered-questions").css("display", "none");
  $(".test-result-wrapper-water").css("display", "block");

}

$(document).ready(function () {
  // Startseed Test
  $.get(`${window.origin}/starseed_test`, function (data) {
    starseedQuestions = Object.values(data)
    startStarseedQuiz()
  });

  // View result
  $(".test-result-button").on("click", function () {
    showResult()
  });

  // Reset Test
  $(".retry").click(function () {
    $.get(`${window.origin}/starseed_test`, function (data) {
      starseedQuestions = Object.values(data)
      startStarseedQuiz(starseedQuestions)
    });
    reset()
  })

  // Newsletter Subscription
  $("#aside-ad-nl-button").click(function () {
    $('#modal-wrapper').css({ 'display': 'block', 'background-color': '#fd8c1484' })
    $('#modal-nl-subscription').css('visibility', 'visible')
  })
  $('.cancel-nl-subscription-btn').click(function () {
    $('#modal-wrapper').css('display', 'none')
    $('#modal-nl-subscription').css('visibility', 'hidden')
    $('#email').val('')
    $('#nl-input-errors').text('')
    $('#result_page').text('')
    $('#result_page').css('display', 'none')
    $('#subscription_page').css('display', 'block')
  })

  // Footsteps
  $(window).scroll(function () {
    $('.footstep').each(function () {
      // WindowTop - ElementTop = distance btn window top and element top
      let targetEl = $(this).offset().top;
      // How much has been scrolled (starting from the initial window bottom)
      // i.e. additional part
      let scroll = $(window).scrollTop();
      // Total 
      let windowHeight = $(window).height();
      if (scroll > targetEl - windowHeight + 70) {
        $(this).addClass('visible')
      } else {
        $(this).removeClass('visible')
      }
    })

  });
})
