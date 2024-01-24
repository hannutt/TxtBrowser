from tkinter import*
from tkinter import ttk
import tkinter
import customtkinter
import sqlite3
from tkinter import filedialog
from bs4 import BeautifulSoup
import requests
from tkinter.font import Font
from gtts import gTTS
from tkinter import messagebox



pages = []
clicks = 0 
selectReady = False
   



def getText(e):
    clearText()
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
            lastidx = '%s+%dc' % (idx,len(s))
            textbox.tag_add('found',idx,lastidx)
            idx=lastidx
            textbox.tag_config('found',foreground='red')
        searchInput.focus_set()

    



root = Tk() 
root.configure(background = 'grey1')
root.title('TxtBrowser')

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



titlefont = Font(family = 'Segoe Print')
labelfont = Font (family = 'High Tower Text')
frame1 = Frame(root,background = 'grey42')

frame2 = Frame(root)
frame3 = Frame(root, background = 'grey1')
frame4 = Frame(root)
frame5 = Frame(root,background = 'grey1')
frame6 = Frame(root,background = 'grey1')
scrollbar = Scrollbar(frame2)
scrollbar.pack(side = RIGHT, fill = Y)

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
fontPlus = Button(frame5,text="+",bg='grey1',fg='white',command=increaseFont)
fontMinus = Button(frame5,text="-",bg='grey1',fg='white',command=decreaceFont)
searchBtn = Button(frame6,text='search from text',bg='grey1',fg='white',command=findTxt)
searchInput = Entry(frame6)


#delBtn = Button(root, text = 'Delete', command = delUrl)

titlelbl.pack()
frame1.pack()
frame2.pack()
frame3.pack()
frame4.pack()
frame5.pack()
frame6.pack()
prevBtn.pack(side=LEFT,pady=5,padx=5)
pageEntry.pack(side=LEFT)
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
textbox.pack()
tree.pack()
historyBtn.pack(side=LEFT,pady=5,padx=5)

#delBtn.pack()
#bindataan tuplaklikkaus ja clicker- funktio joka toteutetaan klikkausten jälkeen
tree.bind("<Double-1>",selectUrl)
tree.bind("<Control-d>",delUrl)
root.bind("<Return>",getText)
root.mainloop()



