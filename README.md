# PDF Bookmark to HTML

A small command line tool to create a single HTML with PDF bookmarks and links to the page in each PDF from a directory of PDFs.

I wrote this in about 10 minutes so don't expect anything too fancy but feel free to open an issue or a PR if you like :)


## Usage

Clone the directory (`git clone git@github.com:Steven-N/pdfbookmark-to-html.git`)

Install the dependencies

```
cd pdfbookmark-to-html
pip3 install -r requirements.txt
```

Run the tool
```
python3 generate-bookmarks.py --input-dir /pdf/file/path/ --output-dir /my/output/path --output-filename test.html
```

The output HTML file will be written to the output directory you defined above.
