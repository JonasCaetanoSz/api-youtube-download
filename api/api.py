from flask import Flask, redirect, request, jsonify,abort , send_file , render_template
from flask_cors import CORS 
from pytube import YouTube
from youtube_search import YoutubeSearch
from converter import converter
from urllib.parse import quote as format_url
import tageditor
import traceback
import os

tgt_folder = "api/src/converter"
upload_folder = "api/src/uploads"


class API: 

    app = Flask(__name__ , static_url_path="/assets")
    app.template_folder = "src/web-template"
    app.static_folder = "src/web-template/assets"
    CORS(app)
    

    @app.route('/')
    def index_html():

        return render_template('index.html')

    @app.route('/search')
    def videos_search():

        """ buscar videos no youtube."""
        if "keyword" in request.args and not request.args["keyword"].isspace() and request.args["keyword"] != "":
            
            if "max_results" in request.args:

                try:
                    max_results = int(request.args["max_results"])
                except:
                    # o valor de max_results não e um numero ou e um numero de ponto fluatuante.
                    max_results = 10
            else:
                max_results = 10
            
            results = YoutubeSearch(str(request.args["keyword"]), max_results=max_results).to_json()
            return results
        
        else: 
            return jsonify(erro=True, reason="No search keyword submitted.") , 400
    @app.route("/resolutions")
    def resolutions():

        """ retorna as resoluções disponiveis para dowloand."""

        if "url_surfix" in request.args and "watch?" in request.args["url_surfix"] and not "youtube.com" in request.args["url_surfix"]:

            try:
                video_url = f"https://youtube.com{request.args['url_surfix']}"
                yt = YouTube(video_url)
                resolutions_obj ={"video":[], "audio":[]}
                for stream in yt.streams.filter(progressive=True , type="video"):
                    # listar resoluões disponiveis para download

                    if not stream.resolution in resolutions_obj["video"]: resolutions_obj["video"].append(stream.resolution)
                
                for stream in yt.streams.filter(only_audio=True):
                    # listar qualidades de audio dispnivel para download
                    if not stream.abr in resolutions_obj["audio"]: resolutions_obj["audio"].append(stream.abr)
                
                return resolutions_obj
            
            except:
                # se acontecer um erro interno ou o url_surfix conter um link que não e do youtube.
 
                return jsonify(erro=True, reason="this url_surfix is invalid or not youtube.") , 400
        else:

            return jsonify(erro=True, reason="please send the url_surfix argument.") , 400
    
    @app.route('/details')
    def details_video():
        
        url_surfix = request.args["url_surfix"]
        yt = YouTube(f'https://youtube.com/{url_surfix}')
        return jsonify(title=yt.title , duration=yt.length, thumb=yt.thumbnail_url , url_surfix=url_surfix)
    
    @app.route('/download')
    def download_in_server():
        """ baixa o conteudo no servidor e retorna o link pra download"""

        try:

            if "url_surfix" and "format" and "resolution" in request.args:
            
                video_url = f"https://youtube.com{request.args['url_surfix']}"
                to_format = request.args["format"]
                resolution = request.args["resolution"]
                yt = YouTube(video_url)
                download_success = None
                
                if to_format == "video":

                    for stream in yt.streams.filter(type="video" , progressive=True):

                        if stream.resolution == resolution:

                            stream.download(output_path=tgt_folder)
                            file = converter.to_mp4(stream, resolution)
                            download_success = True
                            break;

                else: # então format == audio
                    for stream in yt.streams.filter(only_audio=True):

                        if stream.abr == resolution:

                            stream.download(output_path=tgt_folder)
                            file = converter.to_mp3(stream,resolution)
                            tageditor.metadataEditAudio(yt , file)
                            download_success = True
                            break;

                if download_success : return jsonify(link_download=(f"{request.base_url.replace('http://' , 'https://')}/{format_url(file)}"))
                
                else: return jsonify(erro=True, reason="unknown error when downloading the file.") , 400


            else: return jsonify(erro=True, reason=f"invalid arguments or this url is not from youtube.")

        except Exception as e: # em caso de erro interno desconhecido.

            traceback.print_exc()
            return jsonify(erro=True, reason="unknown error"),400

    @app.route('/download/<filename>')
    def client_download(filename):
        
        try:

            for file in [n for n in os.listdir('api/src/uploads') if n == filename ]:
                
                return send_file(path_or_file=f"src/uploads/{filename}" , as_attachment=True),200

            else:

                return "arquivo não encotrado.", 404
        except:

            return abort(400)
    
    @app.route('/watch')
    def redirect_for_youtube():

        return redirect(f"https://youtube.com/{request.full_path}")

    def start(self, port=5000, host="127.0.0.1", debug=False , ssl_context=None):

        self.app.run(debug=debug, port=port, host=host, ssl_context=ssl_context)
