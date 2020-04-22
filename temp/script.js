function teste(){
    window.alert("sometext");
}

let picker = document.getElementById('picker')

picker.addEventListener('change', (event) => {
  let files = event.target.files
  let list = document.getElementById('list')
  list.innerHTML = 'You selected these files:'

  for (let i = 0; i < files.length; i++) {
    let file = files[i]
    list.innerHTML += '<br>' + file.webkitRelativePath
  }
})

