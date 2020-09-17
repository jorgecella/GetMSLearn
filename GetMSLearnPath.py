from requests_html import HTML, HTMLSession
import requests
import io
import os

session = HTMLSession()

webURL = 'https://docs.microsoft.com/es-mx/learn/modules/intro-to-security-in-azure/2-shared-responsibility'
origenURL = 'https://docs.microsoft.com'

# path = os.getcwd()  +'\\'
path = 'C:\\Users\\jorgec\\OneDrive\\Philanthropy Latam\\LearnDownloader\\Sites\\'
r = session.get(webURL)
r.html.render()

image_files = []
css_files = []
filename= r.text


# create site folder
if not os.path.exists(path + webURL.split('/')[-2]):
    os.mkdir(path + webURL.split('/')[-2])
pathSite = path + webURL.split('/')[-2] + '\\'


# function to get images/css/etc
def getlinks(type, atribute, array_files):
    types = r.html.find(type)
    for link in types:
        try:
            array_files.append(link.attrs[atribute])
            #print(link.attrs[atribute])
        except:
            pass

# download files function
def download(url, file_name):
    print ('url: '+url)
    print ('file_name: ' + file_name)
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = requests.get(url)
        # write to file
        file.write(response.content)

getlinks('link','href', css_files)

getlinks('img','src', image_files)


# download css
for cssfiles in css_files:
    cssOK = (cssfiles.split('/')[-1].split('.')[-1])
    if 'css' in cssOK:
        if not os.path.exists(pathSite + '_themes'):
            os.mkdir(pathSite + '_themes')
        if not os.path.exists(pathSite + '_themes\\' + cssfiles.split('/')[-1]):
            download('https://docs.microsoft.com' + cssfiles[0:cssfiles.rfind('/')] + '/' + cssfiles.split('/')[-1].split('.')[-2] + '.css'  , pathSite + '_themes\\' + cssfiles.split('/')[-1].split('.')[-2] + '.css'  )
        # change links to css
        filename = filename.replace(cssfiles, '/Sites/_themes/' + cssfiles.split('/')[-1].split('.')[-2] + '.css' )

# download images
for linksImages in image_files:
        if not os.path.exists(pathSite+'media'):
                os.mkdir(pathSite+'media')
        print ('Imagenes: ' + webURL[0:webURL.rfind('/')] + "/" + linksImages )
        if not os.path.exists(linksImages):
                web = webURL[0:webURL.rfind('/')] + "/"
                if '/' in linksImages[0]:
                    web = origenURL        
                r = requests.get(web + linksImages)
                with open(pathSite + '\media\\' + linksImages.split('/')[-1].split('.')[-2] + '.' + linksImages.split('/')[-1].split('.')[-1]  , 'wb') as f:
                        f.write(r.content)
                filename = filename.replace(linksImages, 'media/' + linksImages.split('/')[-1].split('.')[-2] + '.' + linksImages.split('/')[-1].split('.')[-1] )

# download webpage
with io.open(pathSite + "index.html", "w") as f:
    f.write(filename)

