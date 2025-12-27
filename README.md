# Wrong Side Up

Reorders PDF pages for documents scanned on a single sided scanner with a document feeder. Launch the program and drag and drop the PDF files that you want to fix into the window.

PDF files are updated in place, so make sure to take a backup of any important PDF files before dropping them in!

## Development

Create a Python virtual environment with `python -m venv env` and then activate with `source env/bin/activate`. Install dependencies with `pip install -r requirements.txt`.

Run with `python main.py` for development.

## Packaging

To bundle the application into an executable, run `pyinstaller main.spec`. This will create the application in the `dist` folder.