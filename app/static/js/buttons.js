var addButton = document.querySelector(".add-button");
var removeButton = document.querySelector(".remove-button");
var changeButton = document.querySelector(".change-button");
var placeholder = document.querySelector(".button-placeholder");
var addForm = document.querySelector(".add-human-form");
var removeForm = document.querySelector(".remove-human-form");
var changeForm = document.querySelector(".change-human-form");
var chooseButton = document.querySelector(".choose-button");
var chooseHuman = document.querySelector(".choose-human");
var changeHuman = document.querySelector(".change-human");
var addAlive = document.querySelector(".add-alive");
var addDeath = document.querySelector(".add-death");
var changeAlive = document.querySelector(".change-alive");
var changeDeath = document.querySelector(".change-death");
addAlive.checked = 1;
changeAlive.checked = 1;
addDeath.disabled = 1;
changeDeath.disabled = 1;
addAlive.onchange = function() {
  if (addAlive.checked) {
    addDeath.disabled = 1
	}
	else {
		addDeath.disabled = 0
	}
};
changeAlive.onchange = function() {
  if (changeAlive.checked) {
    changeDeath.disabled = 1
	}
	else {
		changeDeath.disabled = 0
	}
};
addButton.onclick = function() {
  placeholder.style.display = "block";
  addForm.style.display = "block";
};
removeButton.onclick = function() {
  placeholder.style.display = "block";
  removeForm.style.display = "block";
};
changeButton.onclick = function() {
  placeholder.style.display = "block";
  changeForm.style.display = "block";
};
placeholder.onclick = function() {
  placeholder.style.display = "none";
  addForm.style.display = "none";
  removeForm.style.display = "none";
  changeForm.style.display = "none";
  chooseHuman.style.display = "block";
  changeHuman.style.display = "none";
};
chooseButton.onclick = function() {
  chooseHuman.style.display = "none";
  changeHuman.style.display = "block";
};
