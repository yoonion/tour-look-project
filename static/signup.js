const duplicationBtn = document.getElementById("duplication");
const signUpBtn = document.getElementById("signUpBtn");

const newUserId = document.getElementById("user_id");
const userName = document.getElementById("user_name");
const userPwd1 = document.getElementById("user_pwd1");
const userPwd2 = document.getElementById("user_pwd2");

// 회원가입 버튼 클릭시 유효성 체크
signUpBtn.addEventListener("click", () => {
  if(newUserId.value.length < 1) {
    alert('아이디를 입력해주세요.');
    return false;
  } 
  if(userName.value.length < 1) {
    alert('이름(닉네임)을 입력해주세요.');
    return false;
  } 
  if(userPwd1.value.length < 1) {
    alert('비밀번호를 입력해주세요.');
    return false;
  } 
  if(userPwd2.value.length < 1) {
    alert('비밀번호 확인을 입력해주세요.');
    return false;
  } 
  if(userPwd1.value != userPwd2.value) {
    alert('비밀번호화 비밀번호 확인이 일치하지 않습니다.');
    return false;
  }

  // 다 유효하면 괜찮으면 회원가입
  document.getElementById("signUpForm").submit();
});

// 중복 체크 버튼
duplicationBtn.addEventListener("click", () => {
  userId = newUserId.value;
  idDuplicationCheck(userId);
});

const idDuplicationCheck = (userId) => {
  fetch("/signup/duplicate_check", {
    method: "POST",
    body: JSON.stringify({"userId": userId}),
    headers: {
      "Content-Type": "application/json"
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if(data.result=='success') {
        alert('회원 가입 가능한 아이디 입니다.')
        document.getElementById('user_id').focus;
      } else {
        alert('중복된 아이디 입니다.')
      }
    })
    .catch((error) => console.log(error));
};


