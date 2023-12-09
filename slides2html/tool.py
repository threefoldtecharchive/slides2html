import os
import os.path
import re
import click
from configparser import ConfigParser
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from google.oauth2 import service_account
from slides2html.google_links_utils import get_slide_id, get_presentation_id, link_info
from slides2html.image_utils import images_to_transparent_background, set_background_for_images, resize_images
from slides2html.generator import Generator
from slides2html.downloader import Downloader
from slides2html.revealjstemplate import BASIC_TEMPLATE


def dir_images_as_htmltags(directory):

    images = []
    files = [x for x in os.listdir(directory) if x.endswith("png") and "_" in x and "background_" not in x]
    files.sort(key=lambda k: int(k.split("_")[0]))
    for p in files:
        dirbasename = os.path.basename(directory)
        images.append(
            '<img src="./{dirbasename}/{p}" alt="{p}" />'.format(dirbasename=dirbasename, p=p))
    return images


def get_slides_info(directory):
    slides_infos = []
    main_meta = "presentations.meta"
    website_dir = os.path.dirname(directory)
    main_meta_path = os.path.join(website_dir, main_meta)

    parser = ConfigParser()

    parser.read(main_meta_path)
    presentation_id = os.path.basename(directory)
    presentation_title = parser.get(presentation_id, 'title')

    files = [x for x in os.listdir(
        directory) if x.endswith(".png") and "_" in x and "background" not in x]
    files.sort(key=lambda k: int(k.split("_")[0]))
    for p in files:
        dirbasename = os.path.basename(directory)
        meta = []
        metapath = os.path.join(directory, p + ".meta")
        if os.path.exists(metapath):
            with open(metapath, "r") as mp:
                meta_content = mp.read()
                meta = re.findall(r'(https?://\S+)', meta_content)
        print("extracted meta :", meta)
        image = '<img src="./{dirbasename}/{p}" alt="{p}" />'.format(
            dirbasename=dirbasename, p=p)
        slides_infos.append(
            {'slide_image': image, 'slide_meta': meta, 'title': presentation_title})

    return slides_infos


class Tool:
    def __init__(self, presentation_id, credfile="credentials.json", serviceaccount=True):
        """Initialize slides2html tool.

        Arguments:
            presentation_id {[str]} -- presentation id (e.g "147sFqkzjr_caJrh5f4ZpRRdD0SZP32aGSBkfDNH31PM or full url.")

        Keyword Arguments:
            credfile {str} -- [description] (default: {"credentials.json"})

        Raises:
            RuntimeError -- [In case of invalid credential files.]

        """
        self.presentation_id = presentation_id
        SCOPES = ['https://www.googleapis.com/auth/drive']

        if not os.path.exists(credfile):
            raise RuntimeError(
                "please provide valid credentials.json file. https://console.developers.google.com/apis/credentials")

        self.credfile = os.path.expanduser(credfile)
        print("credfile: ", self.credfile)

        credentials = None
        service = None
        print("USING SERVICE ACCOUNT: ", serviceaccount)
        if serviceaccount:
            credentials = service_account.Credentials.from_service_account_file(
                self.credfile, scopes=SCOPES)
            service = build('slides', 'v1', credentials=credentials)
        else:
            raise Exception('slides2html only supports service accounts')

        self.downloader = Downloader(presentation_id, service)
        self.generator = Generator(presentation_id)

    def build_revealjs_site(self, destdir="", entryfile="", presentation_dir="", template=BASIC_TEMPLATE):
        """Build reveal.js based website.

        Keyword Arguments:
            destdir {str} -- directory under reveal.js website directory (default: {""})
            entryfile {str} -- index file name (default: presentation id)
            presentation_dir {str} -- directory to save images (default: {""})
            template {[str]} -- [reveal.js template] (default: {BASIC_TEMPLATE})
        """
        self.downloader.download(destdir)
        slides_infos = get_slides_info(destdir)
        html = self.generator.generate_html(
            slides_infos, revealjs_template=template)
        if not entryfile:
            entryfile = self.presentation_id

        with open(entryfile, "w") as f:
            f.write(html)

    def convert_to_transparent_background(self, destdir):
        images_to_transparent_background(destdir)

    def set_images_background(self, destdir, bgpath):
        set_background_for_images(destdir, bgpath)


@click.command()
@click.option("--website", help="Reveal.js site directory", required=True)
@click.option("--id", help="presentation url or id", required=True)
@click.option("--indexfile", help="index filename. will default to presentation id if not provided.", required=False)
@click.option("--imagesize", help="image size (MEDIUM, LARGE)", default="medium", required=False)
@click.option("--credfile", help="credentials file path", default="credentials.json", required=False)
@click.option("--themefile", help="use your own reveal.js theme", default="", required=False)
@click.option("--background", help="background image to be used for all of the slides", required=False)
@click.option("--resize", help="resize image of (width,height)", required=False)
def cli(website, id, indexfile="", imagesize="medium", credfile="credentials.json", themefile="", background=None, resize=None):
    presentation_id = id
    try:
        presentation_id, slide_id = link_info(id)
    except ValueError:  # not a url, people using id as in old version.
        pass
    imagesize = imagesize.upper()
    if imagesize not in ["MEDIUM", "LARGE"]:
        raise ValueError("Invalid image size should be MEDIUM or LARGE")

    if resize and "," in resize:
        try:
            newwidth, newheight = map(lambda x: int(x.strip()), resize.split(","))
        except:
            raise ValueError("invalid size for --resize {}: should be 'width,height' ".format(resize))

    if not indexfile:
        indexfilepath = os.path.join(website, "{}.html".format(presentation_id))
    else:
        indexfilepath = os.path.join(website, "{}.html".format(indexfile))

    destdir = os.path.join(website, presentation_id)
    credfile = os.path.abspath(os.path.expanduser(credfile))
    serviceaccount = True #force it, don't know why it's not reflected
    print("CREDFILE PATH: ", credfile)
    
    if not os.path.exists(credfile):
        raise ValueError("Invalid credential file: {}".format(credfile))

    theme = ""
    themefilepath = os.path.expanduser(themefile)
    if os.path.exists(themefilepath):
        with open(themefilepath) as f:
            theme = f.read()
    else:
        theme = BASIC_TEMPLATE

    p2h = Tool(presentation_id, credfile, serviceaccount=serviceaccount)
    p2h.downloader.thumbnailsize = imagesize
    p2h.build_revealjs_site(destdir, indexfilepath, template=theme)

    if background is not None:
        bgpath = p2h.downloader.get_background(background, destdir)
        p2h.convert_to_transparent_background(destdir)
        p2h.set_images_background(destdir, bgpath)

    if resize and "," in resize:
        newwidth, newheight = map(lambda x: int(x.strip()), resize.split(","))
        resize_images(destdir, (newwidth, newheight))