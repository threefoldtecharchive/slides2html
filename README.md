# slides2html

`slides2html` is a tool to convert Google presentations into html websites using [reveal.js](https://revealjs.com).

## How it works

The tool converts the slides of a (Google) presentation into images (PNG) using the Google API and generates entry point file with reveal.js templates.

### Get credentials

Using [Google console](https://console.developers.google.com/flows/enableapi?apiid=slides.googleapis.com)

### Normal account
You need to enable and download credentials files using [Google console](https://console.developers.google.com/flows/enableapi?apiid=slides.googleapis.com) or go to [Python Quickstart](https://developers.google.com/slides/quickstart/python) and choose enable slides API then download configurations.

### Service account 
- Create project 
- Create credentials (type service account)
You need to enable and download credentials files using  or go to [Python Quickstart](https://developers.google.com/slides/quickstart/python) and choose enable slides API then download configurations.
- Download credentials (as json and save it anywhere on your filesystem)

## Installation
- `git clone https://github.com/threefoldtech/slides2html`
- `pip3 install .` or `python3 setup.py install`
- in case of any dependency problems make sure to `pip install -r requirements.txt`

## Dev installation
- `git clone https://github.com/threefoldtech/slides2html`
- `cd slides2html && pipenv --three && pipenv shell`
- `pip3 install -e .` or `python3 setup.py install`
- in case of any dependency problems make sure to `pip install -r requirements.txt`

## Example usage

- Download basic release from https://github.com/hakimel/reveal.js
- Untar it into suitable directory (e.g `/tmp/revealjs`)
- Get credentials from [Google API Console](https://console.developers.google.com/apis/credentials) and save it on your filesystem (e.g `/tmp/credentials.json`)
- Convert using `slides2html`
```bash
slides2html --website /tmp/revealjs --id 147sFqkzjr_caJrh5f4ZpRRdD0SZP32aGSBkfDNH31PM  --credfile ~/credentials.json
```
- in `/tmp/revealjs` directory there will be entrypoint (customizable using `--indexfile` option) `147sFqkzjr_caJrh5f4ZpRRdD0SZP32aGSBkfDNH31PM.html` and directory named `147sFqkzjr_caJrh5f4ZpRRdD0SZP32aGSBkfDNH31PM`

```bash
~> ls /tmp/revealjs
147sFqkzjr_caJrh5f4ZpRRdD0SZP32aGSBkfDNH31PM       bower.json       css        Gruntfile.js  js   LICENSE       plugin     revealjs
147sFqkzjr_caJrh5f4ZpRRdD0SZP32aGSBkfDNH31PM.html  CONTRIBUTING.md  demo.html  index.html    lib  package.json  README.md  test

~> tree /tmp/revealjs/147sFqkzjr_caJrh5f4ZpRRdD0SZP32aGSBkfDNH31PM

/tmp/revealjs/147sFqkzjr_caJrh5f4ZpRRdD0SZP32aGSBkfDNH31PM
├── 00_g4b3e153e09_0_58.png
├── 01_g4b3e153e09_0_218.png
├── 02_g4b3e153e09_0_135.png
├── 03_g4b70871d28_0_0.png
├── 04_g4c087152a6_32_59.png
├── 05_g4a13b6e525_0_1316.png
├── 06_g4a13b6e525_0_1324.png
├── 07_g4a13b6e525_0_1344.png
├── 08_g4a13b6e525_0_1331.png
├── 09_g4b3e153e09_0_125.png
├── 10_g4b70871d28_0_121.png
├── 11_g4b70871d28_0_224.png
├── 12_g4b3e153e09_0_80.png
├── 13_g4b70871d28_0_425.png
├── 14_g4c087152a6_32_14.png
├── 15_g4b3e153e09_0_109.png
├── 16_g4b3e153e09_0_74.png
├── 17_g4b3e153e09_0_162.png
├── 18_g4b3e153e09_0_151.png
├── 19_g4b3e153e09_0_156.png
├── 20_g4b3e153e09_0_104.png
├── 21_g4b3e153e09_0_140.png
├── 22_g4b3e153e09_0_173.png
├── 23_g4b3e153e09_0_29.png
├── 24_g4b3e153e09_0_8.png
├── 25_g4b3e153e09_0_54.png
├── 26_g4b3e153e09_0_193.png
├── 27_g4b3e153e09_0_16.png
└── 28_g4b3e153e09_0_0.png


```

### Usage with service account

The only change you need is `--serviceaccount`
```bash
slides2html --website /tmp/revealjs --id 1N8YWE7ShqmhQphT6L29-AcEKZfZg2QripM4L0AK8mSU --credfile service_credentials.json --serviceaccount
```

## Usage
```bash
Usage: slides2html [OPTIONS]

Options:
  --website TEXT    Reveal.js site directory  [required]
  --id TEXT         presentation id  [required]
  --indexfile TEXT  index filename. will default to presentation id if
                    not provided.
  --imagesize TEXT  image size (MEDIUM, LARGE)
  --credfile TEXT   credentials file path
  --help            Show this message and exit.
  --themefile TEXT  Template file to use
  --serviceaccount  Use service account provider (mainly for server usages)
```

### Custom themes

```bash
slides2html --website /tmp/revealjs --id 1N8YWE7ShqmhQphT6L29-AcEKZfZg2QripM4L0AK8mSU  --credfile credentials.json --themefile themes/basictheme.html
```

### Creating custom theme

```html
    <!-- base html code ommitted-->
		<div class="reveal">
			<div class="slides">
                {% for slideinfo in slidesinfos %}
				<section>
					<div class="presentation-title">{{presentation_title}}</div>
					<!-- <div class="slide-meta">
						<ul>
						{% for el in slideinfo['slide_meta'] %}
							<li class="slide-meta-item">
								{{el}}
							</li>
						{% endfor %}
						<ul>
					</div> -->
					<div class="slide-image">
					{{slideinfo['slide_image']}}
					</div>
				</section>
                {% endfor %}
			</div>
    </div>
```

Templates are rendered with
- `presentation_title` title of the presentation
- `slidesinfos` list of slideinfo. `slideinfo['slide_meta']` has the links of the speakernotes, and `slideinfo['slide_image']` has the slide as image

## Owner
[@xmonader](https://github.com/xmonader)
