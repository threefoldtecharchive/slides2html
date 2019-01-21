import os
import logging
from concurrent.futures import ThreadPoolExecutor, wait
import requests
from configparser import ConfigParser

# logging.basicConfig()
# logger = logging.getLogger('downloader')

# The ID template for google presentation.
DOWNLOAD_SLIDE_AS_JPEG_TEMPLATE =  "https://docs.google.com/presentation/d/{presentationId}/export/jpeg?id={presentationId}&pageid={pageId}" 

def download_entry(entry, destdir="/tmp"):
    """Download single entry
    
    Arguments:
        entry: Tuple -- (url, save_as, slide_meta, presentation_title)
    
    Keyword Arguments:
        destdir {str} -- destination directory (default: {"/tmp"})
    
    Returns:
        string -- [destination file to download]
    """

    url, save_as, slide_meta, presentation_title = entry
    destfile = os.path.join(destdir, save_as)

    print("Downloading {} to {}".format(url, destfile))
    metapath = destfile + ".meta"
    print("Metapath: ", metapath)
    with open(metapath, 'w') as f:
        f.write("".join(slide_meta))

    r = requests.get(url)
    # logger.debug("{} fetching {}".format(r.status_code, destfile))
    if r.status_code == 200 and not os.path.exists(destfile):
        with open(destfile, 'wb') as f:
            content = r.content
            f.write(content)

    return destfile

def download_entries(entries, destdir="/tmp"):
    """Download slides to destination website directory 
    
    Arguments:
        entries List[(url, save_as, slide_meta, presentation_title)] -- [description]
    
    Keyword Arguments:
        destdir {str} -- [description] (default: {"/tmp"})
    """

    results = []
    os.makedirs(destdir, exist_ok=True)

    with ThreadPoolExecutor(max_workers=10) as executor:
        for entry in entries:
            future = executor.submit(download_entry, entry, destdir)
            results.append(future)
    wait(results)


class Downloader:
    def __init__(self, presentation_id, service, thumbnailsize="MEDIUM"):
        """
        Download class responsible for downloading slides as images 
        Arguments:
            presentation_id {str} -- presentation id from google presentation id
            service {Service} -- Google api service (created by build)
            thumbnailsize {str} -- image size (medium or large)
        """

        self.presentation_id = presentation_id
        self.service = service 
        self.thumbnailsize = thumbnailsize.upper() # "LARGE."
        if thumbnailsize not in ["MEDIUM", "LARGE"]:
            raise ValueError("invalid thumbnailsize should be large or medium")

    def _get_slides_download_info(self):
        presentation = self.service.presentations().get(
            presentationId=self.presentation_id).execute()
        presentation_title = presentation['title']
        slides = presentation.get('slides')
        slides_ids = [slide["objectId"] for slide in slides]
 
        links = []
        zerofills = len(str(len(slides)))
        for i, slide_id in enumerate(slides_ids):
            # slide_index = slide_id.split("_")[2]
            slide = slides[i]
            slide_meta = []
            notesPage = slide['slideProperties']['notesPage']
            # speakerNotesObjectId = notesPage['notesProperties']['speakerNotesObjectId'] #i3

            pageElements = notesPage['pageElements']
            for page_element in pageElements:
                # if page_element['objectId'] == speakerNotesObjectId:
                shape = page_element['shape']
                if 'text' in shape and 'textElements' in shape['text']:
                    for text_element in shape['text']['textElements']:
                        if 'textRun' in text_element and 'content' in text_element['textRun']:
                            slide_meta.append(text_element['textRun']['content'])
            pageId = slide_id
            presentationId = self.presentation_id
            url = self.service.presentations().pages().getThumbnail(presentationId=presentationId, pageObjectId=pageId, thumbnailProperties_thumbnailSize=self.thumbnailsize).execute()["contentUrl"]
            image_id = str(i).zfill(zerofills)
            save_as = "{image_id}_{page_id}.png".format(image_id=image_id, page_id=pageId)
            links.append((url, save_as, slide_meta, presentation_title))
        return links, presentation_title

    def download(self, destdir):
        """Download images of self.presentation_id to destination dir
        
        Arguments:
            destdir {str} -- destination dir.
        """

        entries, title = self._get_slides_download_info()

        parser = ConfigParser()

        website_dir = os.path.dirname(destdir)
        presentations_meta_path = os.path.join(website_dir, "presentations.meta" )
        if os.path.exists(presentations_meta_path):
            parser.read(presentations_meta_path)
        if not parser.has_section(self.presentation_id):
            parser.add_section(self.presentation_id)
        parser.set(self.presentation_id, 'title', title)
        with open(presentations_meta_path, "w") as metafile:
            parser.write(metafile)
        

        download_entries(entries, destdir)
        print("done downloading.")

