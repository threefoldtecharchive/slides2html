import os
from jinja2 import Template
from slides2html.revealjstemplate import BASIC_TEMPLATE


class Generator:
    def __init__(self, presentation_id):
        """Generator for the presentation website
        
        Arguments:
            presentation_id {str} -- google docs presentation
        """
        self.presentation_id = presentation_id
  
    def generate_html(self, slides_infos, revealjs_template=BASIC_TEMPLATE):
        """Generate rendered HTML page from presentation (presentation_id)
        
        Keyword Arguments:
            slides_as_images {[str]} -- image tags to be injected in the reveal.js template(default: {None})
            revealjs_template {str} -- reveal.js template. (default: {BASIC_TEMPLATE})
        
        Returns:
            str -- rendered webpage as entry point for presentation (presentation_id) website.
        """
        # if not self.slides_as_images:
        #     raise RuntimeError("need to run self.save_slides_to_dir first.")
        
        template = Template(revealjs_template)
        print(slides_infos)
        return template.render(slidesinfos=slides_infos)
