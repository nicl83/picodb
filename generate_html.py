import json, io

htmlBasicPageTemplate = """
<html>
<head>
<link rel="stylesheet" type="text/css" href="pdbStyle.css">
</head>
<body>
<div class="container-container">
<div class="container-container-item">
<p><h1>Welcome to picoDB!</h1></p>
</div>
<div class="container-container-item">
<div class="grid-container">{0}</div>
</div>
</div>
</body>
</html>
"""
htmlImgElement = '<p><img src="{0}" alt="{1}"><p>'
htmlParagraphElement = '<p>{0}</p>'
htmlQRCodeElementTemplate = '\n<div class="grid-item">\n<h2>{0}</h2>\n{1}\n{2}\n</div>\n'
htmlGridDivTemplate = ''

with open("picodbInfo.json") as pdbInfoFile:
    picoDBInfo = json.load(pdbInfoFile)

def buildQRPageElement(qrCodeLocation, description, name):
    currentQRElement = htmlImgElement.format(qrCodeLocation, name)
    currentNameElement = htmlParagraphElement.format(name)
    currentDescriptionElement = htmlParagraphElement.format(description)
    currentPageElement = htmlQRCodeElementTemplate.format(currentNameElement, currentDescriptionElement, currentQRElement)
    return currentPageElement

qrCodeElements = ""
for source in picoDBInfo:
    print("debug: processing source {0}".format(source))
    currentSourceInfo = picoDBInfo[source]
    sourceQRElement = buildQRPageElement(currentSourceInfo["latestQR"], currentSourceInfo["description"], source)
    qrCodeElements += sourceQRElement

document = htmlBasicPageTemplate.format(qrCodeElements)
print(document)

with io.open("picodb.html", 'w', encoding="utf8") as htmlFileOut:
    htmlFileOut.write(document)