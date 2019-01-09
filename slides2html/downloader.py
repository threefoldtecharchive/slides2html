import os
from concurrent.futures import ThreadPoolExecutor, wait
import requests



# The ID of a sample presentation.
DOWNLOAD_SLIDE_AS_JPEG_TEMPLATE =  "https://docs.google.com/presentation/d/{presentationId}/export/jpeg?id={presentationId}&pageid={pageId}" 


def download_entry(entry, destdir="/tmp"):
    url, save_as = entry
    destfile = os.path.join(destdir, save_as)
    r = requests.get(url)
    print(r.status_code, destfile)
    if r.status_code == 200 and not os.path.exists(destfile):
        with open(destfile, 'wb') as f:
            content = r.content
            f.write(content)
    print(destfile)
    return destfile

def download_entries(entries, destdir="/tmp"):
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
        slides = presentation.get('slides')
        slides_ids = [slide["objectId"] for slide in slides]
 
        links = []
        zerofills = len(str(len(slides)))
        for i, slide_id in enumerate(slides_ids):
            # slide_index = slide_id.split("_")[2]
            pageId = slide_id
            presentationId = self.presentation_id
            url = self.service.presentations().pages().getThumbnail(presentationId=presentationId, pageObjectId=pageId, thumbnailProperties_thumbnailSize=self.thumbnailsize).execute()["contentUrl"]
            image_id = str(i).zfill(zerofills)
            save_as = "{image_id}_{page_id}.png".format(image_id=image_id, page_id=pageId)
            # print(save_as)
            links.append((url, save_as))
        return links

    def download(self, destdir):
        """Download images of self.presentation_id to destination dir
        
        Arguments:
            destdir {str} -- destination dir.
        """
        entries = self._get_slides_download_info()
        download_entries(entries, destdir)
        print("done downloading.")

