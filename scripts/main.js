let myHeading = document.querySelector("h2");
myHeading.textContent = "hello World!!";
//alert("hello!"); //팝업창에 전달받은 인자 출력


//이미지 클릭하면 다른 이미지 출력(?)
let myImage = document.querySelector("img");

myImage.onclick = function () {
  let mySrc = myImage.getAttribute("src").toLowerCase();
  if (mySrc === "images/tomato.jpg") {
    myImage.setAttribute("src", "images/tomato.jpg");
  } else {
    myImage.setAttribute("src", "images/farm.jpg");
  }
};




/*
//변수 선언 
let a;
var b;

//함수 선언 
function multiply(num1, num2) {
    let result = num1 * num2;
    return result;
  }
  multiply(1, 2)

  //클릭 이벤트
  document.querySelector("html").onclick = function () {
    alert("Ouch! Stop poking me!");
  };
  */