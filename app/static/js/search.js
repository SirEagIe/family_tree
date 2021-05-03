function search(form) {
  var input, filter, ul, li, txtValue;
  input = document.querySelector(form + ' input');
  filter = input.value.toUpperCase();
  ul = document.querySelector(form + ' ul');
  li = document.querySelectorAll(form + ' li');
  for (var i = 0; i < li.length; i++) {
    txtValue = li[i].textContent;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      li[i].style.display = "";
    } else {
      li[i].style.display = "none";
    }
  }
}
