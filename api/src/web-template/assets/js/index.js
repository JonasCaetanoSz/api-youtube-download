function nocpyrightsouds(){

    document.querySelector('.loadingdiv').hidden = false
    index = 0
    video_node = document.querySelectorAll('.video')
    var nocopyrightsouds_json = null

    xhr = new XMLHttpRequest()
    xhr.open('GET', `/search?keyword=guerra%20na%20ucrania&max_results=20`)
    xhr.responseType = 'json'
    xhr.onload = function () {nocopyrightsouds_json = xhr.response

        for (video of video_node ){

        video.querySelector('.thumb').src = nocopyrightsouds_json.videos[index].thumbnails[0]
        video.querySelector('.videotitle').textContent = nocopyrightsouds_json.videos[index].title
        video.querySelector('.duration').textContent = nocopyrightsouds_json.videos[index].duration == 0 ? '00:00' : nocopyrightsouds_json.videos[index].duration 
        video.querySelector('.thumb').id = nocopyrightsouds_json.videos[index].url_suffix
        index++}
        document.querySelector('.searchresults').hidden = false
        document.querySelector('.loadingdiv').hidden = true
        }
    xhr.send()

  }

    function search(){

      if (document.querySelector('.keyword').value != ''  ) {
        document.querySelector('.loadingdiv').hidden = false
        document.querySelector('.searchresults').hidden = true
        document.querySelector('.download').hidden = true
        document.querySelector('.successdownload').hidden = true
    
        index = 0
        video_node = document.querySelectorAll('.video')
        keyword = document.querySelector('.keyword').value
        movies = null
        var xhr = new XMLHttpRequest()
        xhr.onload = function () {movies = xhr.response ; display_videos(movies)}
        xhr.onerror = function() {alert('api retornou um error')}
        xhr.open('GET', `/search?keyword=${keyword}&max_results=20` , true)
        xhr.responseType = "json"
        xhr.send(null)
    
        function display_videos(movies){
    
        for (video of video_node ){
    
          if(index < movies.videos.length){

            video.hidden = false
            video.querySelector('.thumb').src = movies.videos[index].thumbnails[0]
            video.querySelector('.videotitle').textContent = movies.videos[index].title
            video.querySelector('.duration').textContent = movies.videos[index].duration == '0' ? '00:00': movies.videos[index].duration
            video.querySelector('img').id = movies.videos[index].url_suffix
            index++
        document.querySelector('.loadingdiv').hidden = true
        document.querySelector('.searchresults').hidden = false}

        else{break;}
      document.querySelector('.search').disabled = false


        }}}
      
        else{
          alert('por favor, digite o link ou titulo do video.')
          document.querySelector('.search').disabled = false
        }

      }
    

function download(){


}

function download_by_search(url_suffix){

  document.querySelector('.searchresults').hidden = true
  document.querySelector('.loadingdiv').hidden = false
  document.querySelector('.downloadthumb').id = url_suffix
  document.querySelector('.downloadthumb').src = document.getElementById(url_suffix).src
  document.querySelector('.titlevideodown').textContent = document.getElementById(url_suffix).querySelector('div > p')
  document.querySelector('.download').hidden = false
  document.querySelector('.loadingdiv').hidden = true
  document.querySelector('.successdownload').hidden = true

  for (video of document.querySelectorAll('.video')){

    if (video.querySelector('img').id == url_suffix){


      document.querySelector('.titlevideodown').textContent = video.querySelector('p').textContent
    }
}}

document.querySelectorAll(".thumb").forEach( function(video) {
    
  video.addEventListener("click", function(event) {
  
  var el =  event.target
  var url_suffix = el.id;
  download_by_search(url_suffix)


});

})



document.querySelector('.search').addEventListener('click', check_value_keyword)
nocpyrightsouds()


function check_value_keyword(){

  value = document.querySelector('.keyword').value
  document.querySelector('.search').disabled = true

  if(value.indexOf('youtube.com') == -1 && value.indexOf('youtu.be') == -1 ){

      search()
  }

  else{

    download_by_link()
  }

  
}


function download_by_link(){

document.querySelector('.searchresults').hidden = true
document.querySelector('.loadingdiv').hidden = false
document.querySelector('.successdownload').hidden = true
document.querySelector('.download').hidden = true


var url_suffix = document.querySelector('.keyword').value
var url_suffix =  url_suffix.replace('https://youtube.com' , "")
var url_suffix =  url_suffix.replace('https://youtu.be' , "")
xhr = new XMLHttpRequest()
xhr.open('GET', `/details?url_surfix=/${url_suffix}`)
xhr.onload = function () {document.querySelector('.download').hidden = false
document.querySelector('.loadingdiv').hidden = false
document.querySelector('.loadingdiv').hidden = true
document.querySelector('.search').disabled = false
document.querySelector('.titlevideodown').textContent = xhr.response.title
document.querySelector('.downloadthumb').id = xhr.response.url_surfix
document.querySelector('.downloadthumb').src = xhr.response.thumb

}
xhr.responseType = "json"
xhr.send()

}



  document.addEventListener("keypress", function(e) {
    if(e.key === 'Enter') {
    
     check_value_keyword()
    
    }
  });