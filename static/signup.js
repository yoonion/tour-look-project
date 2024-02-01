const duplicationBtn = document.getElementById("duplication");
const newUserId = document.getElementById("user_id");

const idDuplicationCheck = (userId) => {
  fetch("/url 입력", {
    method: "POST",
    // headers: {},
  })
    .then((response) => response.json())
    .then((data) => console.log(data))
    .catch((error) => console.log(error));
};

duplicationBtn.addEventListener("click", () => {
  userId = newUserId.value;
  idDuplicationCheck(userId);
});
