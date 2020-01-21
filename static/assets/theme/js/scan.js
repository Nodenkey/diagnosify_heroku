var input = document.querySelector('input');
var preview = document.querySelector('.preview')

// make picker invisible so user interacts with label
input.style.opacity = 0;

//add event listener to listen for changes for preview
input.addEventListener('change', updateImageDisplay);
var selected = false;

function updateImageDisplay() {
  while (preview.firstChild) {
    preview.removeChild(preview.firstChild);
  }

  var curFiles = input.files;
  if (curFiles.length === 0) {
    var para = document.createElement('p');
    para.textContent = 'No files currently selected for prediction';
    preview.appendChild(para);
    return false;
  } else {
    var descr = document.createElement('div');
    preview.appendChild(descr);
    for (var i = 0; i < curFiles.length; i++) {
      var para1 = document.createElement('p');
      var para = document.createElement('p');
      if (validFileType(curFiles[i])) {
        para.textContent = 'File name: ' + curFiles[i].name + ', file size: ' + returnFileSize(curFiles[i].size) + '.';
        var image = document.createElement('img');
        image.src = window.URL.createObjectURL(curFiles[i]);
        image.width = 300;
        image.height = 300;
        para1.appendChild(image);

        descr.appendChild(para1);
        descr.appendChild(para);
        selected = true;
        return true;
      } else {
        para.textContent = 'File name ' + curFiles[i].name + ': Not a valid file type. Update your selection.';
        descr.appendChild(para);
        return false;
      }
    }
  }
}

var fileTypes = [
  'image/jpeg',
  'image/pjpeg',
  'image/png'
]

function validFileType(file) {
  for (var i = 0; i < fileTypes.length; i++) {
    if (file.type === fileTypes[i]) {
      return true;
    }
  }

  return false;
}

function returnFileSize(number) {
  if (number < 1024) {
    return number + 'bytes';
  } else if (number >= 1024 && number < 1048576) {
    return (number / 1024).toFixed(1) + 'KB';
  } else if (number >= 1048576) {
    return (number / 1048576).toFixed(1) + 'MB';
  }
}

function validate(){
  if (updateImageDisplay() && selected == true){
    return true;
  }return false;
}