# MediumToMarkdown

Convert your Medium posts to Markdown files effortlessly with MediumToMarkdown. This GUI application allows you to import a ZIP file containing your exported Medium data and convert all posts to Markdown format while preserving the original formatting.

## Features

- Convert HTML posts to Markdown with a simple, user-friendly GUI.
- Option to skip converting comments.
- Customize the output filenames by removing dates and replacing hyphens with spaces.

## How to Export Data from Medium

1. On your Medium homepage, click on your profile picture and select `Settings`.
2. Navigate to the `Security and apps` tab.
3. Click on `Download your information`.
4. Confirm the export by clicking `Export`.
5. A link to download your archive will be sent to your email once the export is complete.

## Usage

1. Clone this repository or download the `MediumToMarkdown.exe` file.
2. Run `MediumToMarkdown.exe`.
3. Click `Select Input ZIP` to choose the ZIP file containing your exported Medium data.
4. Click `Select Output Directory` to choose where you want the Markdown files to be saved.
5. (Optional) Customize the output filenames by checking/unchecking the provided options.
6. Click `Convert` to start the conversion process.
7. A success message will be displayed once the conversion is complete.

## Dependencies

- Python 3.x
- tkinter
- html2text

## Building from Source

If you wish to build the executable from source, ensure you have all the dependencies installed, and run the following command:

```bash
pyinstaller --onefile --windowed main.py
```
