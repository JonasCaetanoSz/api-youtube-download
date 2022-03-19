# ⚠️ aviso :

Este é um projeto criado apenas para estudo, portanto não me responsabilizo por nenhum uso indevido ou ato que seja contra os <a href="https://www.youtube.com/static?gl=BR&template=terms&hl=pt" target="_blank"> termos de serviço do Youtube</a>.



# :rocket: iniciando : 

### clone o projeto: 

    git clone https://github.com/JonasCaetanoSz/api-youtube-download.git

### satisfazendo os requisitos :

    cd api-youtube-download && pip3 install -r requirements.txt

### iniciando a aplicação:

    python api/main.py


# :books: documentação :

### buscando por vídeos:

Para buscar por vídeos use :

     /search?keyword="título do vídeo"
     
retorna o resultado de pesquisa do youtube:

![search](https://user-images.githubusercontent.com/87551778/154806023-2be2021a-a628-4d2c-a2de-c24e96148fce.PNG)


Para limitar o máximo de resultados:

     /search?keyword="título do video"&max_results= máximo de resultados desejado.

 nota : O parâmetro max_results é opcional, se não for pasado recebe 10 como seu valor padrão.
 
 <br>

### obter resoluções disponíveis:

Para obter use a rota resolutions:
  
    /resolutions?url_surfix="url surfix do video"

#### retorna as resoluções disponiveis : 

![resolutions](https://user-images.githubusercontent.com/87551778/154806104-ed6eacad-06be-42f5-896a-b45d4dd8e975.PNG)

<br>

### obtendo informações do vídeo:

Para obter informações como duração do vídeo, título do vídeo, thumbnail do vídeo é a url_surfix passada use:

    /details?url_surfix="url surfix do vídeo"

#### retorna as informações do video : 

![details](https://user-images.githubusercontent.com/87551778/154806116-3400feb3-eb82-4e79-a0f6-5264188261a6.PNG)


### baixando vídeos:

Para baixar vídeos você precisa informar 3 parâmetros obrigatórios, são eles:

 * url_surfix : url surfix do vídeo.

 * format : formato para download pode receber áudio ou vídeo.

 * resolution : qualidade do download se for vídeo envie a resolução + P se for áudio envie a qualidade + kbps .

#### Exemplos:

Baixar o áudio :

    /download?url_surfix="/watch?v=-ObdvMkCKws"&format=audio&resolution=160kbps

Baixar o vídeo : 

    /download?url_surfix="/watch?v=-ObdvMkCKws"&format=video&resolution=360p

#### retorna o link para download do arquivo:

![download](https://user-images.githubusercontent.com/87551778/154806129-99f50fd4-2639-46a4-b7a0-c2e1cf483682.PNG)
