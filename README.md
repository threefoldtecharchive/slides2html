# presentation2html

`slides2html` is a tool to convert Google presentations into html website using [reveal.js](https://revealjs.com)

## How it works

Converts presentation's slides into images (png) using Google APIs and generate entry point file with reveal.js templates.


## Installation
- git clone https://github.com/threefoldtech/presentation2html
- pip3 install setup.py . e 

## Usage

- Download basic release from https://github.com/hakimel/reveal.js 
- Untar it into suitable directory (e.g `/tmp/revealjs`)
- Get credentials from [Google API Console](https://console.developers.google.com/apis/credentials) and save it on your filesystem (e.g `/tmp/credentials.json`)
- Convert using `slides2html`
```bash
slides2html --website revealjs --presentationid 147sFqkzjr_caJrh5f4ZpRRdD0SZP32
aGSBkfDNH31PM --imagesize large --credfile /tmp/credentials.json
```

- in `/tmp/revealjs` directory there will be entrypoint (customizable using `--indexfile` option) `147sFqkzjr_caJrh5f4ZpRRdD0SZP32aGSBkfDNH31PM.html` and directory named `147sFqkzjr_caJrh5f4ZpRRdD0SZP32aGSBkfDNH31PM`

```bash
~> ls /tmp/revealjs
147sFqkzjr_caJrh5f4ZpRRdD0SZP32aGSBkfDNH31PM       bower.json       css        Gruntfile.js  js   LICENSE       plugin     revealjs
147sFqkzjr_caJrh5f4ZpRRdD0SZP32aGSBkfDNH31PM.html  CONTRIBUTING.md  demo.html  index.html    lib  package.json  README.md  test
```
