function download(url_surfix,format,resolution ){

    document.querySelector('.search').disabled = true
    document.querySelector('.download').hidden = true
    document.querySelector('.loadingdiv').hidden = false
    xhr = new XMLHttpRequest()
    xhr.open('GET' , `/download?url_surfix=${url_surfix}&format=${format}&resolution=${resolution}`)
    xhr.responseType = "json"
    xhr.onload = function () {document.querySelector('.successdownload').hidden = false

    document.querySelector('.loadingdiv').hidden = true
    document.querySelector('.search').disabled = false
    document.querySelector('.downfile').href = xhr.response.link_download
            
}
    xhr.send()

    }



    document.querySelector(".details").querySelectorAll('button').forEach( function(button) {
    
        button.addEventListener("click", function(event) {
        
        var el =  event.target
        var resolution = el.value
        var url_surfix = document.querySelector(".downloadthumb").id

        if( resolution.indexOf('kbps') == -1){

            format = 'video'
        }

        else{

            format = 'audio'
        }

        download(url_surfix,format,resolution)
      });
      
      })

      // teste

      /*
      document.querySelector('.download').hidden = true
      document.querySelector('.loadingdiv').hidden = true
      document.querySelector('.searchresults').hidden = true

      */