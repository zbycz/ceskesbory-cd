# -*- coding: cp1250 -*-

import layout, wx
import  wx.lib.scrolledpanel as wxscrolled
import  wx.lib.fancytext as wxfancytext

arrKraje = ["- nezáleží -", "Hlavní město Praha", "Středočeský kraj", "Jihočeský kraj", "Plzeňský kraj", "Karlovarský kraj", "Ústecký kraj", "Liberecký kraj", "Královéhradecký kraj", "Pardubický kraj", "Kraj Vysočina", "Jihomoravský kraj", "Olomoucký kraj", "Moravskoslezský kraj", "Zlínský kraj"]
arrDruh = ["- nezáleží -", "mužský sbor", "ženský sbor", "smíšený sbor", "dětský sbor", "dívčí sbor", "chlapecký sbor", "vokální noneto", "vokální okteto", "vokální septeto", "vokální sexteto", "vokální kvinteto", "vokální kvarteto", "vokální trio"]
arrChar = ["- nezáleží -", "sborová škola", "sokolský sbor", "sbor základní školy", "gymnaziální sbor", "akademický sbor", "chrámový sbor", "sbor základní umělecké školy", "středoškolský sbor", "sbor základní a základní umělecké školy", "sbor mateřské školy", "městský sbor", "skautský sbor", "projektový sbor", "školní sbor", "folklorní soubor"]
arrZanr = ["- nezáleží -", "bez omezení", "duchovní hudba", "chorál, liturgická hudba", "stará hudba (včetně barokní)", "hudba klasicismu a romantismu", "soudobá vážná hudba", "folklór a úpravy lidových písní", "jazz", "populární hudba a muzikál", "skladby českých autorů"]
arrOrder = ["- nezáleží -", "žánru", "sídla", "počtu členů", "druhu souboru", "roku založení"]

                


class UcpsSpltr(wx.SplitterWindow):
    PnlActive = False
    PnlFiltr = False
    PnlVysl = False
    PnlDetail = False
    
    def __init__(self, parent):
        wx.SplitterWindow.__init__(self, parent, -1)
        
        self.CreateFiltr()
        self.Initialize(self.PnlFiltr)
        self.PnlActive = self.PnlFiltr
        #self.Bind(wx.EVT_SIZE, self.OnSize, self)
    
    def OnSize(self, evt):
        self.Refresh()


    def CreateFiltr(self):
        self.PnlFiltr = wx.Panel(self)
        self.PnlFiltr.Hide()
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(layout.getTopSizer(self.PnlFiltr, "Zvolte filtr"), 0, wx.EXPAND)
        vbox.Add((-1,20))
        
        form = {}
        form['kraj'] = ['Kraj:', arrKraje]
        form['nazev'] = ['Název souboru, sídlo, příjmení sbormistra:', False]
        form['druh'] = ['Druh souboru:', arrDruh]
        form['char'] = ['Zvláštní charakteristika:', arrChar]
        form['zanr'] = ['Žánrové zaměření:', arrZanr]
        form['order'] = ['Výsledky řadit podle:', arrOrder]
        
        grid1 = wx.GridSizer(cols=2, vgap=5, hgap=5);
        for key in form:
            grid1.Add(wx.StaticText(self.PnlFiltr, -1, form[key][0]), 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
            
            if form[key][1] != False:
                tmp = wx.Choice(self.PnlFiltr, -1, choices = form[key][1])
                tmp.SetSelection(0)
            else:
                tmp = wx.TextCtrl(self.PnlFiltr, -1)
            form[key].append(tmp)
            grid1.Add(tmp)
        
        vbox.Add(grid1, 0, wx.ALL|wx.CENTER, 20)

        # vbox->button
        butt = wx.Button(self.PnlFiltr, -1, 'Zobrazit výsledky')
        vbox.Add(butt, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.OnSwitchVysl, butt)
        
        self.PnlFiltr.SetSizer(vbox)


    def CreateVysl(self):
        data = []
        data.append(["Berušky", "Klatovy | dětský sbor ", "| sbor základní školy | založen v roce 2001", "60 členů", "umělecký vedoucí: Dana Martinková"])

        #vytvoří panel
        self.PnlVysl = wx.Panel(self)
        self.PnlVysl.Hide()
        
        #sizer a obrázek
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(layout.getTopSizer(self.PnlVysl, "Výsledky vyhledávání"), 0, wx.EXPAND)

        #tlačítko 
        butt = wx.Button(self.PnlVysl, -1, 'Změnit filtr')
        vbox.Add(butt, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.OnSwitchFiltr, butt)
        vbox.Add((-1,20))


        panel1 = wxscrolled.ScrolledPanel(self.PnlVysl, -1, size=(140, 30),
                        style = wx.TAB_TRAVERSAL|wx.BORDER_NONE, name="panel1" )
        dataSzr = wx.BoxSizer(wx.VERTICAL)
        
        tc = wx.TextCtrl(panel1, -1, "aaa ", size=(-1, 30), 
                        style=wx.TE_RICH|wx.TE_READONLY|wx.TE_MULTILINE|wx.BORDER_SIMPLE )
        
        dataSzr.Add(tc, 0)
        panel1.SetSizer( dataSzr )
        panel1.SetAutoLayout(1)
        panel1.SetupScrolling()
        panel1.Refresh()
        vbox.Add(panel1, 1, wx.EXPAND)

        self.PnlVysl.SetSizer(vbox)
        tc.Refresh()


    def OnSwitchFiltr(self, event):
        self.PnlActive.Hide()
        self.PnlFiltr.Show()
        self.ReplaceWindow(self.PnlActive, self.PnlFiltr)
        self.PnlActive = self.PnlFiltr
        
    
    def OnSwitchVysl(self, event):
        if not self.PnlVysl:
            self.CreateVysl()
        self.PnlActive.Hide()
        self.PnlVysl.Show()
        self.ReplaceWindow(self.PnlActive, self.PnlVysl)
        self.PnlActive = self.PnlVysl



class UcpsFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "České-sbory.cz", (10, 10), (650, 400))
        self.CenterOnScreen()
        self.SetBackgroundColour((255,255,255))
        self.SetIcon(wx.Icon('icon.gif', wx.BITMAP_TYPE_GIF))
        
        
        self.StatusBar = self.CreateStatusBar(1)
        self.StatusBar.SetStatusText("Verze: 0.1, databáze: 21.1.2005", 0)
        
        self.Spltr = UcpsSpltr(self)
        self.Refresh()

class UcpsApp(wx.App):
    def OnInit(self):
        self.frame = UcpsFrame()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = UcpsApp(False) # False => vypisuj chyby při startu aplikace
    app.MainLoop()
