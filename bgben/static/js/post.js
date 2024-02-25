const shareButton = document.getElementById('shareButton');
const X = document.getElementById('X')
const title = document.title
const header = document.getElementById('post_title').innerText;

let shareData = {
  title,
  header,
  url: window.document.location.href
}

$(document).ready(function () {

  // Delete Post Confirmation Modal
  $('.modal-open-post').click(function () {
    $('#modal-delete-post-confirm').css('visibility', 'visible')
  })
  $('.cancel-btn').click(function () {
    $('#modal-delete-post-confirm').css({ 'visibility': 'hidden' })
  })
  // Delete Comment Confirmation Modal
  $('.modal-open-comment-delete').click(function () {
    $('#modal-delete-comment-confirm').css('visibility', 'visible')
  })
  $('.cancel-btn').click(function () {
    $('#modal-delete-comment-confirm').css({ 'visibility': 'hidden' })
  })

  // Please Sign-in Modal Close
  $('#cancel-sign-in-btn1').click(function () {
    $('#modal-sign-in1').css('visibility', 'hidden')
  })
  $('#cancel-sign-in-btn2').click(function () {
    $('#modal-sign-in2').css('visibility', 'hidden')
  })


  // Share API
  if (navigator.share) {
    shareButton.style.display = "inline"
    X.style.display = "none"
    $("#shareButton").click(function () {
      navigator.share(shareData)
    })
  } else {
    url = `https://twitter.com/intent/tweet?text=${shareData.title}+${shareData.header}&url=${shareData.url}`
    shareButton.style.display = "none"
    X.style.display = "inline"
    $("#X").click(function () {
      window.open(url)
    })
  }

  // Prevent submit with Enter key
  $(window).keydown(function (event) {
    if (event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });
})




