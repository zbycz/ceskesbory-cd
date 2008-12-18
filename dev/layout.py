# -*- coding: utf8 -*-

import wx
import wx.html
import webbrowser
import db

btnevt = False
def processKeyEvt(event):
        print a + event.GetKeyCode()
        if event.GetKeyCode() == 8:
            btnevt(event)
        event.Skip()
#key:backspace
 

def getTopSizer(self, heading, btntxt=False):
    self.Bind(wx.EVT_KEY_DOWN, processKeyEvt, self) #key:backspace

    # vbox->hbox1->logo
    gifLogo = wx.Image('logo_cs.gif', wx.BITMAP_TYPE_GIF).ConvertToBitmap()
    logo = wx.StaticBitmap(self, -1, gifLogo, None, (gifLogo.GetWidth(), gifLogo.GetHeight())) #(250, 62)



    hbox1 = wx.BoxSizer(wx.HORIZONTAL)
    hbox1.Add((20,-1))
    
    vbox = wx.BoxSizer(wx.VERTICAL)

    if btntxt and btnevt:
        butt = wx.Button(self, -1, btntxt)
        self.Bind(wx.EVT_BUTTON, btnevt, butt) #key:backspace (pouzito global name btnevt)
        vbox.Add(butt, 0, wx.TOP, 30)
        vbox.Add((-1,10))

    # vbox->hbox1->heading
    if heading:
      font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Verdana')
      heading = wx.StaticText(self, -1, heading)
      heading.SetFont(font)
      vbox.Add(heading, 0, wx.TOP, 20)
    
    hbox1.Add(vbox, 1, wx.EXPAND)
    
    hbox1.Add(logo, 0, wx.ALIGN_RIGHT|wx.TOP|wx.RIGHT, 10)
    
    return hbox1;



def CreateFiltrPnl(self, db):
    self.PnlFiltr = wx.Panel(self)
    self.PnlFiltr.Hide()
    
    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(getTopSizer(self.PnlFiltr, False, u"<< Zpět na úvod"), 0, wx.EXPAND)
    vbox.Add((-1,20))

    font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Verdana')
    heading = wx.StaticText(self.PnlFiltr, -1, "Zvolte filtr")
    heading.SetFont(font)
    vbox.Add(heading, 0, wx.ALIGN_CENTER)

    
    grid1 = wx.GridSizer(cols=2, vgap=5, hgap=5);
    for item in self.form:
        grid1.Add(wx.StaticText(self.PnlFiltr, -1, item[1]), 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
        
        if item[2] != False:
            tmp = wx.Choice(self.PnlFiltr, -1, choices = db.arr[item[0]])
            tmp.SetSelection(0)
        else:
            tmp = wx.TextCtrl(self.PnlFiltr, -1, size=(240,20))
        item.append(tmp)
        grid1.Add(tmp)
    
    vbox.Add(grid1, 0, wx.ALL|wx.CENTER, 20)

    # vbox->button
    butt = wx.Button(self.PnlFiltr, -1, u'Zobrazit výsledky')
    vbox.Add(butt, 0, wx.ALIGN_CENTER)
    self.Bind(wx.EVT_BUTTON, self.OnSwitchVysl, butt)
    
    self.PnlFiltr.SetSizer(vbox)




def CreateHtmlPnl(parent, heading, htmldata, btntxt=False):
    #vytvoří panel
    Pnl = wx.Panel(parent)
    Pnl.Hide()
    
    #sizer a obrázek
    vbox = wx.BoxSizer(wx.VERTICAL)
    vbox.Add(getTopSizer(Pnl, heading, btntxt), 0, wx.EXPAND)
    vbox.Add((-1,5))

    Pnl.html = HtmlWin(Pnl, -1)
    Pnl.html.SetPage(htmldata)

    #ir = Pnl.html.GetInternalRepresentation()
    #ir.SetIndent(0, wx.html.HTML_INDENT_ALL)
    #html.SetSize((ir.GetWidth(), ir.GetHeight()-50))
              
    vbox.Add(Pnl.html, 1, wx.EXPAND)
    Pnl.SetSizer(vbox)
    return Pnl


class HtmlWin(wx.html.HtmlWindow):
    def OnLinkClicked(self, linkinfo):
        href = linkinfo.GetHref()
        if href[:6] == 'order-':
            ucps = self.GetParent().GetParent()
            ucps.userdata['orderby'] = href[6:]

            htmldata = db.getVysledky(ucps.userdata);
            ucps.PnlVysl.html.SetPage(htmldata)

        elif href[:3] == 'id-':
            self.GetParent().GetParent().OnSwitchDetail(int(href[3:]))
        
        else:
            try:
                webbrowser.open(href)
            except:
                wx.MessageBox(u"Adresa: %s" % href, u"Nelze spustit webový prohlížeč", wx.OK | wx.CENTRE | wx.ICON_ERROR)






abouttext = u"""
<p><b>Katalog pěveckých sborů a vokálních ansámblů</b> v ČR připravila Unie českých pěveckých sborů ve spolupráci s NIPOS ARTAMA a dalšími partnery v rámci projektu <b>České sbory</b>. Jeho cílem je zjištění počtu a zmapování aktivit neprofesionálních pěveckých sborů existujících v současné době na území České republiky. Dřívější veřejně přístupné údaje o tomto významném segmentu neprofesionální kultury zahrnovaly pouze malou část skutečně fungujících souborů, dnes však již víme, že se sborovému zpěvu u nás věnuje více než tisíc neprofesionálních sborů a ansámblů, v nichž pracuje několik desítek tisíc dětských i dospělých zpěvaček a zpěváků.
<p>Katalog vychází ve třech podobách – kromě tištěné verze a verze na CD, kterou lze spustit i na počítačích bez internetového připojení, je to především internetový katalog umožňující stálé průběžné aktualizace a propojení sborových profilů s dalšími službami portálu České sbory. Tuto verzi naleznete na adrese <a href="http://www.ceske-sbory.cz/">www.ceske-sbory.cz</a>

<p><b>Unie českých pěveckých sborů</b> je střešní organizace pro sborový zpěv v České republice. Sdružuje stovky českých sborových těles, jako jediná organizace však zastupuje celé české sborové hnutí u nás i v zahraničí. Vznikla v roce 1969 a přímo navazuje na činnost předcházejících sborových organizací, jejichž tradice sahá do roku 1868. Zaměřuje se zejména na podporu estetické výchovy a sborového zpěvu dětí a mládeže. Kromě toho také soustavně mapuje sborový život v ČR, je pořadatelem a spolupořadatelem řady festivalů, soutěží a jiných uměleckých projektů. Uděluje národní i regionální sborová a sbormistrovská ocenění. Vydává odborně-společenský magazín CANTUS a provozuje nejrozsáhlejší český internetový portál věnovaný sborovému umění. 

<p><b>Národní informační a poradenské středisko pro kulturu (NIPOS)</b> bylo zřízeno Ministerstvem kultury ČR jako jeho příspěvková organizace k 1. lednu 1991. Jeho základním posláním je podpora rozvoje kultury, především rozvoje kulturněspolečenských a tvůrčích aktivit občanů v místech a regionech, se zřetelem k oblasti neprofesionálních uměleckých aktivit a k veřejnému užití autorských děl, poskytování informačních služeb a odborných konzultací. <b>ARTAMA</b> je útvar pro neprofesionální umělecké aktivity zabezpečující z pověření MK ČR státní reprezentaci v oblasti neprofesionálního umění. ARTAMA nabízí a zajišťuje odborný servis v oblastech neprofesionálního umění a dětských estetických aktivit, pořádá nebo odborně zajišťuje dílny a semináře, přehlídky, festivaly, soutěže, shromažďuje dokumentaci a zpracovává odborné expertizy pro orgány státní správy a samosprávy.

<br>
<br>

<p><b>České sbory</b>
<br>Katalog pěveckých sborů a vokálních ansámblů

<p>připravila Unie českých pěveckých sborů ve spolupráci s NIPOS-ARTAMA za podpory Nadace Český hudební fond, Ministerstva kultury ČR a dalších subjektů

<p>koordinátor projektu: dr. Roman Michálek
<br>redakce: Jan Popelka, Josefa Volfová, Tereza Bystřická
<br>programování a realizace CD: Pavel Zbytovský

<p>&copy; Unie českých pěveckých sborů, 2005-2008
<br><a href="http://www.ceske-sbory.cz/">www.ceske-sbory.cz</a>
"""

