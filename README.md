# Computational Biology Lab @ IRIBHM website
Our website is currently hosted on github pages. It is a static website although it is being generated *semi* dynamically using Python.

Here are our dependencies:
-  [Jinja2](https://jinja.palletsprojects.com/en/stable/$0) for handling HTML templates,
-  [OpenAlex](https://openalex.org/) for the automatic publications scrapping (see `generation/requests_openalex.py`),
- [mammoth](https://pypi.org/project/mammoth/) for DOCX file conversion. 
- As well as `pandas`.

The notebook to generate the website is located at `generation/generate_pages.ipynb`.

Further, the `static/` folder contains our stylesheet as well as all images (logos, profile pictures). 