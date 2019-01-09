import sys
import os
import json
import shutil
import click
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from slides2html.generator import Generator
from slides2html.downloader import Downloader
from slides2html.revealjstemplate import BASIC_TEMPLATE


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
        """Initialize slides2html tool.
        
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

        userdir = os.path.expanduser("~")
        tokenjson = os.path.join(userdir, ".token.json")
        store = file.Storage(tokenjson)
        creds = store.get()
        self.credfile = os.path.expanduser(credfile) 
        print("credfile: ", credfile)
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(self.credfile, SCOPES)
            creds = tools.run_flow(flow, store)
            
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


@click.command()
@click.option("--website", help="Reveal.js site directory", required=True)
@click.option("--id", help="presentation id", required=True)
@click.option("--indexfile", help="index filename. will default to presentation id if not provided.", required=False)
@click.option("--imagesize", help="image size (MEDIUM, LARGE)", default="medium", required=False)
@click.option("--credfile", help="credentials file path", default="credentials.json", required=False)
def cli(website, id, indexfile="", imagesize="medium", credfile="credentials.json"):

    imagesize = imagesize.upper()
    if imagesize not in ["MEDIUM", "LARGE"]:
        raise ValueError("Invalid image size should be MEDIUM or LARGE")
    if not indexfile:
        indexfilepath = os.path.join(website, "{}.html".format(id))
    else:
        indexfilepath = os.path.join(website, "{}.html".format(indexfile))
    destdir = os.path.join(website, id)
    credfile = os.path.abspath(os.path.expanduser(credfile))
    if not os.path.exists(credfile):
        raise ValueError("Invalid credential file: {}".format(credfile))
    
    # somehow the argv gets ruined when used from the flow tool.
    sys.argv = [] # TODO: find better solution
    p2h = Tool(id, credfile)
    p2h.downloader.thumbnailsize = imagesize
    p2h.build_revealjs_site(destdir, indexfilepath)