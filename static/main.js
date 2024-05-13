function updateLab(e) {
    file_input = document.getElementById('files')
    alert(python_labs)
    file_input.accept = '.cpp'
}

function toggleColor(button) {
    button.classList.toggle("toggled");
}