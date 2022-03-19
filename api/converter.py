import moviepy.editor as mp
import re
import os
import shutil

# definir upload_folder e tgt_folder 

tgt_folder = "api/src/converter"
upload_folder = "api/src/uploads"

class converter:
    
    def to_mp3(stream, resolution):

        file_extension = str(stream.mime_type).replace('audio/' , '')
 
        for file in [n for n in os.listdir(tgt_folder) if re.search(file_extension,n)]:

            full_path = os.path.join(tgt_folder, file)
            output_path = os.path.join(upload_folder, os.path.splitext(file)[0] + f" ({resolution})"+ '.mp3')
            clip = mp.AudioFileClip(full_path)
            clip.write_audiofile(output_path)
            os.remove(f'{tgt_folder}/{file}')
            return str(f"{file} ({resolution}).mp3").replace("." + file_extension,'')

    def to_mp4(stream, resolution):

        file_extension = str(stream.mime_type).replace('video/' , '')
        filename = stream.default_filename

        if stream.mime_type == "video/mp4" : # verifica se o arquivo ja esta em mp4.

            if filename in os.listdir(upload_folder) :

                # o arquivo ja existe na pasta uploads então apaga o existente e move o novo
                os.remove(f'{upload_folder}/{filename}')
                shutil.move(f"{tgt_folder}/{filename}", upload_folder)
                try:
                    os.rename(f"{upload_folder}/{filename}" , f'{upload_folder}/({resolution}) ' + filename)
                except:

                    pass # o nome do arquivo ja tem  aresolução.
                

            else:
                # se não mover o arquivo para pasta uploads.

                shutil.move(f"{tgt_folder}/{filename}", upload_folder)
                try:
                    os.rename(f"{upload_folder}/{filename}" , f'{upload_folder}/({resolution}) ' + filename)
                except:
                    
                     pass # o nome do arquivo ja tem  aresolução.
                

        else: # se não estiver em mp4 converter e enviar para pasta uploads e deletar o video em tgt_folder

            clip = mp.VideoFileClip(f"{tgt_folder}/{filename}")
            clip.write_videofile(f"{upload_folder}/{f'({resolution}) ' + filename.replace(f'{file_extension}' , 'mp4')}")
            os.remove(f'{tgt_folder}/{filename}')

        return str(f"({resolution}) {filename}").replace(file_extension , 'mp4') #filename.replace(file_extension , 'mp4')
