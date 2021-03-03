# Convert DBB HTML to JSON
A Python script that converts the contents of a fully downloaded DDB html page into a json file that can be imported as a Journal Entry in Foundry VTT.

## User instructions
To obtain the necessary html file, you need to save the "source code" of a chapter of a DBB adventure that you own. In Safari on MacOS this can be done through navigating Safari's menu bar as follows:

`File > Save as... > (make sure you select "Source code of page" as file structure)`

For easiest use it's recommended to save this html file in the same directory where you have saved `convertHTMLtoJSON.py`. Next, you need to open `convertHTMLtoJSON.py` and edit the variable `htmlName` to point at your html file. Finally, you can run the Python script and it should save a json file to the same directory.

## Limitations
As mentioned above, this Python script creates json files that can be imported into Foundry VTT as Journal Entries. It does not support the conversion of player characters, monsters, items, or spells.

## Dependencies
* `codecs` module
* `json` module
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup) library

## Known issues
* While the script converts tables, they might end up looking a little compressed.
* The script replaces `blockquote` tags with unsorted lists. This was suitable for the DBB adventure that this was tested on, but other adventures may use `blockquote` tags for area descriptions.
