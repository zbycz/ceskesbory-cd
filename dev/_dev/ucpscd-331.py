# -*- coding: cp1250 -*-

import layout, wx


arrKraje = ["- nezáleží -", "Hlavní město Praha", "Středočeský kraj", "Jihočeský kraj", "Plzeňský kraj", "Karlovarský kraj", "Ústecký kraj", "Liberecký kraj", "Královéhradecký kraj", "Pardubický kraj", "Kraj Vysočina", "Jihomoravský kraj", "Olomoucký kraj", "Moravskoslezský kraj", "Zlínský kraj"]
arrDruh = ["- nezáleží -", "mužský sbor", "ženský sbor", "smíšený sbor", "dětský sbor", "dívčí sbor", "chlapecký sbor", "vokální noneto", "vokální okteto", "vokální septeto", "vokální sexteto", "vokální kvinteto", "vokální kvarteto", "vokální trio"]
arrChar = ["- nezáleží -", "sborová škola", "sokolský sbor", "sbor základní školy", "gymnaziální sbor", "akademický sbor", "chrámový sbor", "sbor základní umělecké školy", "středoškolský sbor", "sbor základní a základní umělecké školy", "sbor mateřské školy", "městský sbor", "skautský sbor", "projektový sbor", "školní sbor", "folklorní soubor"]
arrZanr = ["- nezáleží -", "bez omezení", "duchovní hudba", "chorál, liturgická hudba", "stará hudba (včetně barokní)", "hudba klasicismu a romantismu", "soudobá vážná hudba", "folklór a úpravy lidových písní", "jazz", "populární hudba a muzikál", "skladby českých autorů"]
arrOrder = ["- nezáleží -", "žánru", "sídla", "počtu členů", "druhu souboru", "roku založení"]



class UcpsWindow(wx.Panel):
    PnlFiltr = False
    PnlVysl = False
    PnlActive = False
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, style=wx.BORDER_SUNKEN)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        vbox.Add(layout.getTopSizer(self), 0, wx.EXPAND)
        
        # vbox->spacer
        vbox.Add((-1,20))

        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_NOBORDER)
        self.CreateFiltr()
        self.splitter.Initialize(self.PnlFiltr)
        self.PnlActive = self.PnlFiltr
        layout.heading.SetLabel(self.PnlActive.heading)
        
        vbox.Add(self.splitter, 1, wx.EXPAND);
        self.SetSizer(vbox)
        
        
    def CreateFiltr(self):
        self.PnlFiltr = wx.Panel(self.splitter)
        self.PnlFiltr.Hide()
        self.PnlFiltr.heading = "Zvolte filtr"
        
        form = {}
        form['kraj'] = ['Kraj:', arrKraje]
        form['nazev'] = ['Název souboru, sídlo, příjmení sbormistra:', False]
        form['druh'] = ['Druh souboru:', arrDruh]
        form['char'] = ['Zvláštní charakteristika:', arrChar]
        form['zanr'] = ['Žánrové zaměření:', arrZanr]
        form['order'] = ['Výsledky řadit podle:', arrOrder]
        
        vbox = wx.BoxSizer(wx.VERTICAL)
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
        self.PnlVysl = wx.Panel(self.splitter)
        self.PnlVysl.Hide()
        self.PnlVysl.heading = "Výslekdy"
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        butt = wx.Button(self.PnlVysl, -1, 'Změnit filtr')
        vbox.Add(butt, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.OnSwitchFiltr, butt)
        self.PnlVysl.SetSizer(vbox)
        
                
    def OnSwitchFiltr(self, event):
        self.PnlActive.Hide()
        self.PnlFiltr.Show()
        self.splitter.ReplaceWindow(self.PnlActive, self.PnlFiltr)
        self.PnlActive = self.PnlFiltr
        layout.heading.SetLabel(self.PnlActive.heading)
        
    
    def OnSwitchVysl(self, event):
        if not self.PnlVysl:
            self.CreateVysl()
        self.PnlActive.Hide()
        self.PnlVysl.Show()
        self.splitter.ReplaceWindow(self.PnlActive, self.PnlVysl)
        self.PnlActive = self.PnlVysl
        layout.heading.SetLabel(self.PnlActive.heading)



class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "České-sbory.cz", (10, 10), (650, 400))
        self.CenterOnScreen()
        self.SetBackgroundColour((255,255,255))
        
        self.SetIcon(wx.Icon('icon.gif', wx.BITMAP_TYPE_GIF))
        
        StatusBar = self.CreateStatusBar(1)
        StatusBar.SetStatusText("Verze: 0.1, databáze: 21.1.2005", 0)
        
        UcpsWindow(self)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = MyApp(False) # False => vypisuj chyby při startu aplikace
    app.MainLoop()
