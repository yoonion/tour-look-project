const duplicationBtn = document.getElementById("duplication");
const newUserId = document.getElementById("user_id");

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

duplicationBtn.addEventListener("click", () => {
  userId = newUserId.value;
  idDuplicationCheck(userId);
});
