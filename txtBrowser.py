from tkinter import*
from tkinter import ttk
#from tkinter.ttk import*
import tkinter
import customtkinter
import sqlite3
from tkinter import filedialog
from bs4 import BeautifulSoup
import requests
from tkinter.font import Font
from gtts import gTTS
from tkinter import messagebox
import keyboard
import time
from fpdf import FPDF


generalUrls = ['is.fi','cnn.com','yle.fi','mtv.fi','hs.fi','bbc.co.uk','cbn.com','abc.com']
pages = []
clicks = 0 
selectReady = False
global temp
temp = []


    #return webPage

def saveToPdf():
    content = textbox.get('1.0','end-1c')
    convertContent = content.encode('latin-1','replace').decode('latin-1')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Helvetica',size=12)
    pdf.multi_cell(h=5.0,w=0,text=convertContent)
    pdf.output('pagePdf.pdf')
def findLinks():
    linkPage = Toplevel()
   
    container = Text(linkPage,wrap='char')
    container.pack(fill="both",expand=True)
    #linkBox = Text(linkPage)
    #linkBox.pack()
    Links = []
    externals = []
    webPage = (Entry.get(pageEntry))
    page = requests.get('https://www.'+webPage)
    soup = BeautifulSoup(page.content,'html.parser')
    #haetaan kaikki a tagit
    links = soup.find_all('a')
    ExtCBvar = IntVar()
    if ExtCBvar.get()==0:
        for link in soup.select('a[href^="https://"]'):
            externals.append(link['href'])
            #container.window_create("end",window=externals)
        for i in range(len(externals)):
             extLbl = Button(container,text=externals[i])
             container.window_create("end",window=extLbl)
        container.configure(state="disabled")
    
    for link in links:
        
         #print("Link:", link.get("href"), "Text:", link.string)
        Links.append(link.get("href"))
        #välilyönnin lisäys jokaisen linkin jälkeen
        x='\n'.join(Links)
        #Links.append(link.get(link.string))
    #lisäys text-komponenttiin silmukan ulkopuolella, niin ohjelma ei ala jumittamaan
    #linkBox.insert(INSERT,Links,END)
        #luodaan silmukalla niin monta buttonia, kuin listassa on alkioita.
        j=0
    for i in range(len(Links)):
        j=j+1
        #lamdba viittaus ja muuttujamäärittely funktiolle, jolla saadaan buttonin teksti
        #win ja buttonText on muuttujia, jotka lähetetään getLinkUrl funktiolle
        #container on Text komponentti, jonka sisälle kääritään buttonit
        linklLbl = Button(container,text=Links[i],command=lambda win=linkPage, buttonText=Links[i]:getLinkUrl(buttonText,win))
        #buttonin taustaväri sen mukaan onko buttonin jaollinen 2 vai ei, eli joka toinen buttoni on eriväriä.,
        if j % 2 == 0:
            linklLbl.configure(bg="lightblue")
            
        else:
            linklLbl.configure(bg="lightcyan3")
            
        container.window_create("end",window=linklLbl)
    container.configure(state="disabled")
    totalLbl = Label(linkPage,text="Links total: "+str(j))
    
    externalCB = Checkbutton(linkPage,text='External links only?',variable=ExtCBvar,onvalue=1,offvalue=0)
    externalCB.pack()
    
    totalLbl.pack()
    linkPage.mainloop()
    return container

    
    

   
def getLinkUrl(link,winName):
    #iconify pienentään ikkunan task bariin
    winName.iconify()
    x=str(link)
    clearText()
    webPage = (Entry.get(pageEntry))
    #jos x alkaa / merkillä, 0,1 on merkkijonon etsintäalue
    if x.startswith("/",0,1):
        fullUrl = "https://"+webPage+link
        print(fullUrl)
        page = requests.get(fullUrl)
        soup = BeautifulSoup(page.text,'html.parser')
        result = soup.find_all('html')
        pageEntry.delete(0,END)
        pageEntry.insert(END,fullUrl)
    else:
         page = requests.get(link)
         soup = BeautifulSoup(page.text,'html.parser')
         result = soup.find_all('html')
        
    

    
    
    for r in result:
        final = r.text
        #tyhjä väli kirjainten väliin
        #Final = ' '.join(final)
        textbox.insert(INSERT,'\n ',END)
        textbox.insert(INSERT,final,END)
        textbox.insert(INSERT,'\n ',END)
        #pageNum +=1
        break
    textbox.insert(INSERT,'\n',END)
    barUpdate()
    

def barUpdate():
    progressbar['value']=50
    root.update_idletasks()
    time.sleep(1)
    progressbar['value']=100
    root.update_idletasks()

def autoText(e):
    if CBvar.get()==0:

        value = e.widget.get()
        print(value)
        if value=='':
            data=generalUrls
        else:
            data = []
        #listan läpikäynti item on aina yksittäinen listan alkio
        for item in generalUrls:
            #jos käyttäjän syöttämällä (value) merkkijonolla/merkillä löytyy listalta tuloksia, lisätään tulokset data ja temp listoihin
            if value.lower() in item.lower():
                data.append(item)
                #lisäys globaaliin listaan
                temp.append(item)
                print(temp)
                pageEntry.delete(0,END)
                #break komennon avulla näytetään vain yksi arvo, eli break keskeyttää for-silmukan toiston
                for item in data:
                    pageEntry.insert(END,item)
                    break
                
                
                
    #updateText(data)



'''
def updateText(data):
    
    #global i
    #i=0
    #poistaa käyttäjän syöttee
    pageEntry.delete(0,END)
    for item in data:
       # i=i+1
        pageEntry.insert(END,item)
        break
'''


    #nextPrediction(data,i)
#tämä päivittää j-muuttujaa ja näyttää sen avulla aina seuraavan alkion listalta
#next prediction funktion parametri saa rivillä 368 lambda viittauksella arvoksi
j = 0
def nextPrediction():
    global j
    j=j+1
    
    print(temp)
    try:
        pageEntry.delete(0,END)    
        pageEntry.insert(END,temp[j])
        #try/exceptillä saadaan tulostettua allaoleva ilmoitus kun kohdataan indexerror
    except IndexError:
        messagebox.showinfo('Info','No more predictions available')

        
        
        




def clearAddress(e):
    pageEntry.delete(0,END)
    pageEntry.delete(END,'')


def getText(e):
    clearText()
    getPageUrl()
    #globaalin muuttujat, että niitä voidaan käyttää myös muissa funktioissa
    global pages
    global pageNum
    pageNum = 0
    webPage = (Entry.get(pageEntry))
    pages.append(webPage)
    #jos webpage muuttuja alkaa merkkijonolla www. korvataan se tyhjällä
    if webPage.startswith('www.'):
        webPage=webPage.replace("www.","")
    elif webPage.startswith('https://www'):
        webPage=webPage.replace('https://www.','')

    page = requests.get('https://www.'+webPage)
    soup = BeautifulSoup(page.text,'html.parser')
    result = soup.find_all('html')
    

    

    for r in result:
        final = r.text
        #tyhjä väli kirjainten väliin
        #Final = ' '.join(final)
        textbox.insert(INSERT,'\n ',END)
        textbox.insert(INSERT,final,END)
        textbox.insert(INSERT,'\n ',END)
        pageNum +=1
        break
    textbox.insert(INSERT,'\n',END)
    barUpdate()
    

#nettisivun tekstin tallennus äänitiedostoksi.
def TxtTospeech():
    global selectLng
    selectLng = Toplevel()
    selectLbl = Label(selectLng,text="Select the language of the text to be saved")
    selectLbl.pack()
    global languages
    languages = ttk.Combobox(selectLng,values=['en','fi'])
    
    languages.pack()
    setBtn = Button(selectLng,text="Set",command=setLng)
    setBtn.pack()
    selectLng.mainloop()
    

def clearLngWin():
    selectLng.destroy()



def setLng():
    savetxt = textbox.get("1.0",END)
    selectedLng = languages.get()
    print(selectedLng)

    filetype = [('MP-3','*.mp3')]
    savefile = filedialog.asksaveasfilename(filetypes = filetype, defaultextension = filetype)
    #käytetään final-muuttujaa eli tallennetaan sen sisältämä teksti
    myobj = gTTS(text = savetxt, lang = selectedLng, slow=False)
    myobj.save(savefile)
    clearLngWin()
    

def goBack():
    clearText()
    global pageNum
    pageNum = pageNum -1
    prevPage = pages[pageNum]
    page = requests.get('https://www.'+prevPage)
    soup = BeautifulSoup(page.text,'html.parser')
    result = soup.find_all('html')

    for r in result:
        textbox.insert(INSERT,'\n',END)
        final = r.text 
        textbox.insert(INSERT,'\n',END)    
        textbox.insert(INSERT,final,END)
        textbox.insert(INSERT,'\n',END)
       
       
                       

def goForward():
    clearText()
    global pageNum
    pageNum +=1
    nextPage = pages[pageNum]
    page = requests.get('https://www.'+nextPage)
    soup = BeautifulSoup(page.text,'html.parser')
    result = soup.find_all('html')
   

    for r in result:
        textbox.insert(INSERT,'\n',END)
        final = r.text
        textbox.insert(INSERT,'\n',END)    
        textbox.insert(INSERT,final,END)
        textbox.insert(INSERT,'\n',END)
    


def clearText():
    textbox.delete(1.0,END)


#selaushistoria näyttö erillisessä ikkunassa
def showHistory():
    historyWindow = Toplevel(root)
    historyWindow.geometry('200x200')
    textbox = Text(historyWindow)
    for page in pages:
        textbox.insert(END,page+'\n')
    textbox.pack()

#tallennettujen kirjanmerkkien näyttö omassa ikkunassaan widget parametri sisältää tree komponentin joka lähetetään
#funktiolle funktiokutsussa rivillä 242 jos click on jaollinen 1:llä niin piilotetaan bookmarks ikkuna, jos 2:lla niin
#näyetään ikkuna uudelleen
def showBookmarks(widget):
    global clicks
    clicks = clicks +1
    print(clicks)
    #print(clicks)
    if clicks %1==0:
        widget.pack_forget()
      
    if clicks %2==0:
        widget.pack()
        connection = sqlite3.connect('bookmarks.db')
        cursor = connection.execute('SELECT * FROM PAGES')
        for row in cursor:
            
        #tietokannan data asetetaan values komennolla
            tree.insert(parent='', index='end',iid=row[0],values=(row))
    
    

def saveAdd():
    addr = (Entry.get(pageEntry))
    connection = sqlite3.connect('bookmarks.db')
    cursor = connection.execute('INSERT INTO PAGES (URL) VALUES (?)', (addr,))
    connection.commit()

#tällä funktiolla valitaan treeviewsta url osoite ja siirretään se osoitekenttään tuplaklikkauksella
#event parametrilla otetaan tuplaklikkaus vastaan
def selectUrl(event):
    selected = tree.focus()
    values = tree.item(selected, 'values')
    pageEntry.insert(0,values[1])

#kirjanmerkin poisto treeview:sta ja kannasta
def delUrl(event=''):
    connection = sqlite3.connect('bookmarks.db')
    #selected_item on hiirellä valittu osoite (tree.selection())
    for selected_item in tree.selection():
        #paritetaan selected_item ja ID niminen treeview:n sarake + poisto kannasta
        cursor = connection.execute("DELETE FROM PAGES WHERE IDNUM=?",(tree.set(selected_item,'ID'),))
        connection.commit()
        #poisto treeviwe:sta
    tree.delete(selected_item)
    
'''
def clicker(event):
    selectUrl()
'''

#fontin pienennys/suurennos
def increaseFont():
    global fontSize
    fontSize=fontSize+1
    textFont.configure(size=fontSize)

def decreaceFont():
    global fontSize
    fontSize=fontSize-1
    textFont.configure(size=fontSize)


def findTxt():
    textbox.tag_remove('found','1.0',END)
    #muuttujaan s tallennetaan srcENtry kenttään syötetty teksti
    s = searchInput.get()
    if s:
        #haun aloituspaikka, eli ensimmäinen kohta tekstilaatikosta
        idx='1.0'
        while 1:
            idx = textbox.search(s,idx,nocase=1,stopindex=END)
            if not idx:break
            #lastidx eli viimeinen indeksipaikka huomaa len funktio joka laskee textboxin merkkijonon pituuden
            lastidx = '%s+%dc' % (idx,len(s))
            textbox.tag_add('found',idx,lastidx)
            idx=lastidx
            textbox.tag_config('found',foreground='red')
        searchInput.focus_set()

    



root = Tk() 
root.configure(background = 'grey1')
root.title('TxtBrowser')
menubar = Menu(root)
root.config(menu=menubar)
optionsMenu = Menu(menubar)

optionsMenu.add_command(
    label='Save to PDF',
    command=saveToPdf
)

menubar.add_cascade(label='Options',menu=optionsMenu)



#treeview näkymä ja sen tyylimäärittelyt
style = ttk.Style()
style.configure('Treeview', background='silver',foreground='black',
                    fieldbackground='silver')
#valitun tietueen taustavärin vaihto
style.map('Treeview', background=[('selected','green')])
#treeview näkymän luonti
tree = ttk.Treeview(root)
tree['columns'] =('Bookmark')

tree['columns'] =('ID','Bookmark')
#poistetaan ensimmäinen sarake näkyvistä
tree.column('#0' ,width=0, stretch=NO)
tree.column('ID',anchor=W)
tree.column('Bookmark',anchor=W)  

#sarakkeiden otsikointi, bookmark sarakkeen otsikko on url jne.
   
tree.heading('Bookmark',text = 'URL')
tree.heading('ID', text= 'Id-number')

CBvar = IntVar()
disableCB = Checkbutton(root,text='Disable predictive',variable=CBvar,onvalue=1,offvalue=0)
disableCB.place(x=50,y=30) 



titlefont = Font(family = 'Segoe Print')
labelfont = Font (family = 'High Tower Text')
frame1 = Frame(root,background = 'grey42')

frame2 = Frame(root)
frame3 = Frame(root, background = 'grey1')
frame4 = Frame(root)
frame5 = Frame(root,background = 'grey1')
frame6 = Frame(root,background = 'grey1')
frame7 = Frame(root,background = 'grey1')

scrollbar = Scrollbar(frame2)
scrollbar.pack(side = RIGHT, fill = Y)
progressbar = ttk.Progressbar(frame2,orient=HORIZONTAL,length=100,mode='determinate')

titlelbl = Label(root, text = 'Txt Browser', font = titlefont,bg='grey1',fg='white')
pageEntry = Entry(frame1)
fontSize=14
textFont = Font(family="Time New Roman",size=fontSize)
textbox = Text(frame2,width=50,height=20,yscrollcommand = scrollbar.set,fg='blue', relief=SUNKEN,font=textFont)

scrollbar.config(command = textbox.yview)
#getBtn = Button(frame1, text='GO', command = getText)
saveBtn = Button(frame1, text = 'Save', command = saveAdd)
clearBtn = Button(frame3, text = 'Clear', command = clearText,fg='white',bg='grey1')
#linksBtn = Button(frame3, text = 'Page links',command = getLinks)
prevBtn = Button(frame1, text = '<-', command = goBack,bg='grey1',fg='white')
nextBtn = Button(frame1, text = '->', command = goForward,bg='grey1',fg='white')
historyBtn = Button(frame3, text = 'History', command = showHistory,bg='grey1',fg='white')
speechBtn = Button(frame3, text = 'txt to speech', command = TxtTospeech,bg='grey1',fg='white')
#showbookmarks lähettää lambda-viittuksena commandin funktiokutsussa treeview-komponentin parametrina itse funktiolle
bookBtn = Button(root, text = 'Show/Hide bookmarks', command  = lambda:showBookmarks(tree),bg='grey1',fg='white')
linksBtn = Button(root,text=' Links',command=findLinks,bg='grey1',fg="white")

#funktio muuttaa linksbuttonin tekstiö configure komennolla
def getPageUrl():
    webPage = (Entry.get(pageEntry))
    linksBtn.configure(text='Show '+webPage+' links')

fontPlus = Button(frame5,text="+",bg='grey1',fg='white',command=increaseFont)
fontMinus = Button(frame5,text="-",bg='grey1',fg='white',command=decreaceFont)
searchBtn = Button(frame6,text='search from text',bg='grey1',fg='white',command=findTxt)
searchInput = Entry(frame6)
nextPredic = Button(root,text='Next prediction',command=nextPrediction,bg='grey1',fg='white')


#delBtn = Button(root, text = 'Delete', command = delUrl)

titlelbl.pack()
frame1.pack()
frame2.pack()
frame3.pack()
frame4.pack()
frame5.pack()
frame6.pack()
#frame7.pack()
nextPredic.place(x=420,y=36)
prevBtn.pack(side=LEFT,pady=5,padx=5)
pageEntry.pack(side=LEFT)
#nextBtn.pack()
nextBtn.pack(side=LEFT)
fontPlus.pack(side=LEFT,pady=5,padx=5)
fontMinus.pack(side=RIGHT,pady=5,padx=5)
searchInput.pack(side=RIGHT)
searchBtn.pack(side=LEFT)

#getBtn.pack(side=RIGHT,pady=5, padx=5)
saveBtn.pack(side=RIGHT)
clearBtn.pack(side=RIGHT,pady=5,padx=5)

speechBtn.pack(side=LEFT)
bookBtn.pack(pady=5,padx=5)
linksBtn.pack()
progressbar.pack(side=TOP)
textbox.pack()
tree.pack()
historyBtn.pack(side=LEFT,pady=5,padx=5)

#delBtn.pack()
#bindataan tuplaklikkaus ja clicker- funktio joka toteutetaan klikkausten jälkeen
tree.bind("<Double-1>",selectUrl)
tree.bind("<Control-d>",delUrl)
root.bind("<Return>",getText)
root.bind("<KeyRelease>",autoText)
#bindataan pelkästään backspacen vapautus
root.bind("<KeyRelease-BackSpace>",clearAddress)
root.mainloop()



