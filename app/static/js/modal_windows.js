document.ready = function() {
  $("#draggable").draggable();
  document.querySelector('.transp-draggable').onclick = function() {
    document.querySelector('#draggable').style.top = "50px";
    document.querySelector('#draggable').style.left = "0";
  };
  document.querySelectorAll('[name="titleBackground"]').forEach(title => {
    title.style.background = "#084006";
  });
  document.querySelector('#draggable').style.top = "50px";
  document.querySelector('.famdiagram').style.minWidth = "100%";
  document.querySelector('.famdiagram').style.minHeight = "100vh";
  var items = document.querySelectorAll('[name="tree_item"]');
  var humans = document.querySelectorAll(".window-with-human");
  var addButton = document.querySelector(".add-button");
  var removeButton = document.querySelector(".remove-button");
  var changeButton = document.querySelector(".change-button");
  var placeholder = document.querySelector(".placeholder-modal");
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
  addDeath.disabled = 1;
  items.forEach(item => item.id = item.querySelector('[name="title"]').id);
  items.forEach(item => {
    item.onclick  = function() {
      humans.forEach(human => {
          if(human.id == item.id) {
            placeholder.style.display = "block";
            human.style.display = "block";
          }
      });
    };
  });
  placeholder.onclick = function() {
    placeholder.style.display = "none";
    humans.forEach(human => {
        human.style.display = "none";
    });
    addForm.style.display = "none";
    removeForm.style.display = "none";
    changeForm.style.display = "none";
    chooseHuman.style.display = "block";
    changeHuman.style.display = "none";
  };
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
  chooseButton.onclick = function() {
    changeAlive.checked = 1;
    changeDeath.disabled = 1;
    chooseHuman.style.display = "none";
    changeHuman.style.display = "block";
    var humans = document.querySelectorAll(".choose-human input");
    choosenHumanID = 0;
    humans.forEach(human => {
      if(human.checked)
        choosenHumanID = human.value;
    });
    famdata.forEach(human => {
      if(human.id == choosenHumanID) {
        console.log(human);
        if(human.parents != undefined) {
          document.querySelectorAll(".change-human #first_parent input").forEach(item => {
            if(item.value == human.parents[0])
              item.checked = 1;
          });
          document.querySelectorAll(".change-human #second_parent input").forEach(item => {
            if(item.value == human.parents[1])
              item.checked = 1;
          });
        }
        else {
          document.querySelector(".change-human #first_parent input").checked = 1;
          document.querySelector(".change-human #second_parent input").checked = 1;
        }
        document.querySelector(".change-human #name").value = human.title;
        document.querySelector(".change-human #description").value = human.description;
        document.querySelector(".change-human #date_of_birthday").value = human.date_of_birthday;
        if(human.is_alive == 'True') {
          changeAlive.checked = 1;
          changeDeath.disabled = 1;
        }
        else {
          changeAlive.checked = 0;
          changeDeath.disabled = 0;
          document.querySelector(".change-human #date_of_death").value = human.date_of_death;
        }
      }
    });
  }
};
