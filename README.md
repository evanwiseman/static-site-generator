# Static Site Generator

The Static Site Generator builds a html website from markdown, i.e. converts .md or .markdown files to .html similarly to Jekyll for GitHub pages.

## Requirements

Python3

## Use

To use the Static Site Generator:
1. Place images and .css themese in static/
2. Put .md or .markdown content in the content folder nested to the layout of your webpage
3. Set the source and destination folders accordingly in main.py
4. Use main.sh to test your webpage usually defaults to "localhost:8888"
5. To build for GitHub Pages update the basepath from root ("/") to ("/REPO-NAME")
