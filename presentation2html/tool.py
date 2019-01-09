import os
import json
import shutil
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from presentation2html.generator import Generator
from presentation2html.downloader import Downloader
from presentation2html.revealjstemplate import BASIC_TEMPLATE

def dir_images_as_htmltags(directory):

    images = []
    files = [x for x in os.listdir(directory) if "png" in x and "_" in x ]
    files.sort(key=lambda k: int(k.split("_")[0]))
    for p in files:
        dirbasename = os.path.basename(directory) #os.path.dirname(directory)
        images.append('<img src="./{dirbasename}/{p}" alt="{p}" />'.format(dirbasename=dirbasename, p=p))
    return images

class Tool:
    def __init__(self, presentation_id, credfile="credentials.json"):
        """Initialize presentation2html tool.
        
        Arguments:
            presentation_id {[str]} -- presentation id (e.g "147sFqkzjr_caJrh5f4ZpRRdD0SZP32aGSBkfDNH31PM")
        
        Keyword Arguments:
            credfile {str} -- [description] (default: {"credentials.json"}) 
        
        Raises:
            RuntimeError -- [In case of invalid credential files.]
        """
        self.presentation_id = presentation_id
        self.credfile = credfile
        SCOPES = 'https://www.googleapis.com/auth/drive'
        if not os.path.exists(credfile):
            raise RuntimeError("please provide valid credentials.json file. https://console.developers.google.com/apis/credentials")

        store = file.Storage('token.json')
        creds = store.get()
        
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(credfile, SCOPES)
            creds = tools.run_flow(flow, store)
    
        # drive_service = build('drive', 'v3', http=creds.authorize(Http()))
        service = build('slides', 'v1', http=creds.authorize(Http()))

        self.downloader = Downloader(presentation_id, service)
        self.generator = Generator(presentation_id)

    def build_revealjs_site(self, destdir="", entryfile="", presentation_dir="", template=BASIC_TEMPLATE):
        """Build reveal.js based website
        
        Keyword Arguments:
            destdir {str} -- directory under reveal.js website directory (default: {""})
            entryfile {str} -- index file name (default: presentation id)
            presentation_dir {str} -- directory to save images (default: {""})
            template {[str]} -- [reveal.js template] (default: {BASIC_TEMPLATE})
        """
        self.downloader.download(destdir)
        slides_as_images = dir_images_as_htmltags(destdir)
        html = self.generator.generate_html(slides_as_images, revealjs_template=BASIC_TEMPLATE)
        if not entryfile:
            entryfile = self.presentation_id

        with open(entryfile, "w") as f:
            f.write(html)
