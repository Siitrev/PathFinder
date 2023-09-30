const upload_button = document.getElementById("fake-file")
upload_button.addEventListener("click",_=>{
    document.getElementById("file").click()
})
const file_input = document.getElementById('file');
file_input.onchange = () => {
  const selected_file = file_input.files[0];

  document.getElementById('fake-filename').value = selected_file.name;
}