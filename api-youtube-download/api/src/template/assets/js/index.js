const baseurl = 'https://api-youtube-download.herokuapp.com'
const loading = document.querySelector('.loading')

function recomendados(){
  
    var nocopyrightsouds_json = null
    xhr = new XMLHttpRequest()
    xhr.open('GET', `${baseurl}/search?keyword=guerra%20na%20ucrania&max_results=20`)
    xhr.responseType = 'json'
    xhr.onload = function () {mostrar_videos(videos=xhr.response); loading.hidden = true}
    xhr.send()
}

function mostrar_videos(videos){
  
  for (video of videos.videos){
    
    div = document.createElement('div')
    div.className = 'video'
    divthubnail = document.createElement('div')
    divthubnail.className = 'thumbnail'
    thumimg = document.createElement('img')
    thumimg.className = 'video-thumb'
    divthubnail.append(thumimg)
    thumimg.src = video.thumbnails[0]
    thumimg.id = video.url_suffix
  duration = document.createElement('div')
  duration.className = 'duration'
  duration.textContent = video.duration
  title = document.createElement('p')
  title.textContent = video.title
  title.className = 'title'
  div.append(divthubnail,duration,title)
  document.querySelector('.containe').append(div)
  }  imgeventadd()
}

function pesquisa(){
  
  apagar_videos()
  loading.hidden = false
  palavrachave = document.querySelector('.keyword').value
  document.querySelector('.loading').hidden = false
  document.querySelector('.download-preview').hidden = true
  document.querySelector('.download-sucess').hidden = true
  xhr = new XMLHttpRequest()
  xhr.open('GET' , `${baseurl}/search?keyword=${palavrachave}&max_results=20`)
  xhr.responseType = 'json'
  xhr.onload = function () {mostrar_videos(videos=xhr.response); loading.hidden=true; scroll(0,200);
    document.querySelector('.containe').hidden = false
    document.querySelector('.loading').hidden = true
  }
  xhr.send()
}

function apagar_videos(){
  
  videos = document.querySelectorAll('.video')
  
  for (video of videos){
    
    video.remove()
  }
}

document.querySelector('.ir').addEventListener('click', pesquisa)


function download() {
  
var selectedis =document.querySelector('.res').selectedIndex
document.querySelector('.res').selectedIndex

var url_surfix = document.querySelector('.preview-thumb').id
switch (selectedis) {
  case 1:
    var res = '144p'; formatt = 'video'
    break;
    
  case 2: 
    var res = '360p'; formatt = 'video'
    break;
    
  case 3: 
    var res = '720p'; formatt = 'video'
    break;
    
  case 5: 
    var res = '48kbps'; formatt = 'audio'
    break;
  case 6:
    var res = '50kbps'; formatt = 'audio'
    break;
    
  case 7:
    var res = '70kbps'; formatt = 'audio'
    break;
  case 8: 
    
    var res = '128kbps'; formatt = 'audio'
    break;
  case 9:
    var res = '160kbps'; formatt = 'audio'
    break;}
    
    document.querySelector('.loading').hidden = false
    document.querySelector('.download-preview').hidden = true
    
    xhr = new XMLHttpRequest()
    xhr.open('GET', `${baseurl}/download?url_surfix=${url_surfix}&format=${formatt}&resolution=${res}`)
    xhr.responseType = 'json'
    xhr.onload = function (){
      
      document.querySelector('.loading').hidden = true
      document.querySelector('.download-sucess > div > a').href = xhr.response.link_download
      document.querySelector('.download-sucess').hidden = false
    }
    xhr.send()
}

function downloadpreview(url_suffix, thumburl){
  document.querySelector('.containe').hidden = true
  document.querySelector('.preview-thumb').src = thumburl
  document.querySelector('.preview-thumb').id = url_suffix
  document.querySelector('.loading').hidden = true
  document.querySelector('.download-preview').hidden = false
}



document.querySelector('.down').addEventListener('click', download)

function imgeventadd(){
document.querySelectorAll(".video-thumb").forEach( function(video) {
    
  video.addEventListener("click", function(event) {
  
  var url_suffix = event.target.id
  var thumburl = event.target.src
  downloadpreview(url_suffix, thumburl)

});

})

}

recomendados()

document.addEventListener("keypress", function(e) {
    if(e.key === 'Enter') {
    
     document.activeElement.blur()
     pesquisa()
    
    }
  });