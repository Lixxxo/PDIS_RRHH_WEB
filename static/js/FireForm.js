

// dynamic elements
const salary_lbl = document.getElementById("salary_lbl");
const contract_id = document.getElementById("contract_id");
const contract_salary = document.getElementById("contract_salary");
const total_salary = document.getElementById("total_salary");

// employee has active contracts
if (contracts.length > 0){
  // update elements with data
  salary_lbl.innerText = "Sueldo en el proyecto: " + contracts[0]["project"]["name"];
  contract_id.value = contracts[0]["project"]["name"];
  contract_salary.value = contracts[0]["salary"];
  total_salary.value = employee["total_salary"];

  // update visual elements with fetch request
  format_numbers([contract_salary, total_salary]);

}
// create event listener onChange select tag
const selectedProject = document.querySelector('.projectSelect');
selectedProject.addEventListener('change', (event) => {
  // get selected option
  let selectedOption = selectedProject.options[selectedProject.selectedIndex];

  // update elements with data
  salary_lbl.innerText = "Sueldo en el proyecto: "+ selectedOption.text;
  contract_id.value = contracts[selectedProject.selectedIndex]["id"];
  contract_salary.value = contracts[selectedProject.selectedIndex]["salary"];
  total_salary.value = employee["total_salary"];

  // update visual elements with fetch request
  format_numbers([contract_salary, total_salary]);

});