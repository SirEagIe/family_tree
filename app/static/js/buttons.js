var addButton = document.querySelector(".add-button");
var removeButton = document.querySelector(".remove-button");
var changeButton = document.querySelector(".change-button");
var placeholder = document.querySelector(".button-placeholder");
var addForm = document.querySelector(".add-human-form");
var removeForm = document.querySelector(".remove-human-form");
var changeForm = document.querySelector(".change-human-form");
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
};
