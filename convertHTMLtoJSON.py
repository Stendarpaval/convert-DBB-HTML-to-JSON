import codecs
import json
from bs4 import BeautifulSoup


# Html attributes to be removed
remove_attributes = ['name','lang','language','onmouseover','script','style',
	'font','dir','face','size','color','style','class',
	'width','height','hspace','border','valign','background',
	'bgcolor','text','link','vlink','alink','cellpadding',
	'cellspacing', 'data-content-chunk-id','alt','src',
	'data-tooltip-href','href','id','title','data-href',
	'data-layout','data-next-link','data-prev-link',
	'data-next-title']

# Name of html file to be converted to a journal entry
htmlName = "example.html"

htmlFile = codecs.open(htmlName,'r')
htmlData = htmlFile.read()
htmlStr = str(htmlData)

# Begin parsing of html
soup = BeautifulSoup(htmlStr, features="html.parser")

# Unwrap various web layout html tags
for tag in soup.find_all(['span','div','header','article']):
	tag.unwrap()

# Convert blockquate tags to unsorted lists
for blockquote in soup.find_all('blockquote'):
	blockquote.wrap(soup.new_tag('ul'))
	for tag in blockquote.find_all('p'):
		tag.wrap(soup.new_tag('li'))
		tag.unwrap()
	blockquote.unwrap()

# Insert line break before the main title
for tag in soup.find_all(['h2']):
	tag.insert_before(soup.new_tag('br'))

# Insert line break wedged between horizontal ruler before all other titles
# (This is akin to Roll20's method of structuring journal entries)
for tag in soup.find_all(['h3','h4']):
	tag.insert_before(soup.new_tag('br'))
	tag.insert_before(soup.new_tag('hr'))
	tag.insert_before(soup.new_tag('br'))

# Replace hyperlinks with bold text
for tag in soup.find_all(['a']):
	tag.wrap(soup.new_tag('strong'))
	tag.unwrap()

# Remove problematic html attributes
for attribute in remove_attributes:
	for tag in soup.find_all(attrs={attribute: True}):
		del tag[attribute]

# Extract certain tags that don't translate well to journal entries
for script in soup(["script", "style", "select","img"]):
	script.extract()


# Determine the relevant scope for upcoming convertion steps
contentStartIndex_rough = str(soup.html).find("<!-- Main Title -->")
contentStartIndex = str(soup.html)[contentStartIndex_rough:].find("<h1>") + contentStartIndex_rough
contentEndIndex = str(soup.html).find("<!-- FOOTER -->")

output = str(soup.html)[contentStartIndex:contentEndIndex]

numLines = len(output.splitlines())
lines = [0]*numLines
i = 0

# Remove html commments
for line in output.splitlines():
	if line.startswith("<!--") and line.endswith("-->"):
		lines[i] = ""
	else:
		lines[i] = line
	i += 1
output = ' '.join(lines)

# Find journal name based on header tags
h1StartIndex = contentStartIndex + len("<h1>")
h1EndIndex = str(soup.html)[h1StartIndex:].find("</h1>") + h1StartIndex
journalName = str(soup.html)[h1StartIndex:h1EndIndex]

# Prepare json format for saving results
jsonFormat = {
	"name": journalName,
	"sort": 260000, 
	"flags": {
		"exportSource": {
			"world": "example-world", 
			"system": "dnd5e", 
			"coreVersion": 
			"0.7.9", 
			"systemVersion": "1.2.0"
		}
	}, 
	"content": output,
	"_id": "JKs46PwKkpTZamrS"
}
# Save converted html to a json file
with open(journalName.replace(':','') + '.json','w') as jsonFile:
	json.dump(jsonFormat, jsonFile)
