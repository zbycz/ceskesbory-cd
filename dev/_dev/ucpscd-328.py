# -*- coding: cp1250 -*-

import layout, wx


arrKraje = ["- nezáleží -", "Hlavní město Praha", "Středočeský kraj", "Jihočeský kraj", "Plzeňský kraj", "Karlovarský kraj", "Ústecký kraj", "Liberecký kraj", "Královéhradecký kraj", "Pardubický kraj", "Kraj Vysočina", "Jihomoravský kraj", "Olomoucký kraj", "Moravskoslezský kraj", "Zlínský kraj"]
arrDruh = ["- nezáleží -", "mužský sbor", "ženský sbor", "smíšený sbor", "dětský sbor", "dívčí sbor", "chlapecký sbor", "vokální noneto", "vokální okteto", "vokální septeto", "vokální sexteto", "vokální kvinteto", "vokální kvarteto", "vokální trio"]
arrChar = ["- nezáleží -", "sborová škola", "sokolský sbor", "sbor základní školy", "gymnaziální sbor", "akademický sbor", "chrámový sbor", "sbor základní umělecké školy", "středoškolský sbor", "sbor základní a základní umělecké školy", "sbor mateřské školy", "městský sbor", "skautský sbor", "projektový sbor", "školní sbor", "folklorní soubor"]
arrZanr = ["- nezáleží -", "bez omezení", "duchovní hudba", "chorál, liturgická hudba", "stará hudba (včetně barokní)", "hudba klasicismu a romantismu", "soudobá vážná hudba", "folklór a úpravy lidových písní", "jazz", "populární hudba a muzikál", "skladby českých autorů"]
arrOrder = ["- nezáleží -", "žánru", "sídla", "počtu členů", "druhu souboru", "roku založení"]





class MyPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        # vbox
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # vbox->hbox1 
        vbox.Add(layout.getTopSizer(self, "Zvolte filtr"), 0, wx.EXPAND)
        
        # vbox->spacer
        vbox.Add((-1,20))
        
        # vbox->grid1
        grid1 = wx.GridSizer(cols=2, vgap=5, hgap=5); # cols, vgap, hgap
        form = {}
        form['kraj'] = ['Kraj:', arrKraje]
        form['nazev'] = ['Název souboru, sídlo, příjmení sbormistra:', False]
        form['druh'] = ['Druh souboru:', arrDruh]
        form['char'] = ['Zvláštní charakteristika:', arrChar]
        form['zanr'] = ['Žánrové zaměření:', arrZanr]
        form['order'] = ['Výsledky řadit podle:', arrOrder]
        
        
        for key in form:
            grid1.Add(wx.StaticText(self, -1, form[key][0]), 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
            
            if form[key][1] != False:
                tmp = wx.Choice(self, -1, choices = form[key][1])
                tmp.SetSelection(0)
            else:
                tmp = wx.TextCtrl(self, -1)
            form[key].append(tmp)
            grid1.Add(tmp)
        
        vbox.Add(grid1, 0, wx.ALL|wx.CENTER, 20)

        
#         # vbox->grid1->first line
#         style = wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT
#         grid1.Add(wx.StaticText(self, -1, 'Kraj:'), 0, style)
#         inputKraje = wx.Choice(self, -1, choices = arrKraje)
#         #
#         grid1.Add(inputKraje)
#         
#         grid1.Add(wx.StaticText(self, -1, 'Název souboru, sídlo, příjmení sbormistra:'), 0, style)
#         grid1.Add(form[0])
# 
#         grid1.Add(wx.StaticText(self, -1, 'Druh souboru:'), 0, style)
#         inputDruh = wx.Choice(self, -1, choices = arrDruh)
#         inputDruh.SetSelection(0)
#         grid1.Add(inputDruh)
# 
#         grid1.Add(wx.StaticText(self, -1, 'Zvláštní charakteristika:'), 0, style)
#         inputChar = wx.Choice(self, -1, choices = arrChar)
#         inputChar.SetSelection(0)
#         grid1.Add(inputChar)
# 
#         grid1.Add(wx.StaticText(self, -1, 'Žánrové zaměření:'), 0, style)
#         kraje = wx.Choice(self, -1, choices = arrZanr)
#         kraje.SetSelection(0)
#         grid1.Add(kraje)
# 
#         grid1.Add(wx.StaticText(self, -1, 'Výsledky řadit podle:'), 0, style)
#         kraje = wx.Choice(self, -1, choices = arrOrder)
#         kraje.SetSelection(0)
#         grid1.Add(kraje)

        # vbox->button
        butt = wx.Button(self, -1, 'Zobrazit výsledky')
        vbox.Add(butt, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.GetParent().GetParent().UkazVysledky, butt)
        
        self.SetSizer(vbox)
        


class MyPanelVysl(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(layout.getTopSizer(self, "Výsledky"), 0, wx.EXPAND)
        vbox.Add((-1,20))

        butt = wx.Button(self, -1, 'Změnit filtr')
        vbox.Add(butt, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.GetParent().GetParent().UkazFiltr, butt)
        
        self.SetSizer(vbox)


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, (10, 10), (650, 400))
        self.CenterOnScreen()
        self.SetBackgroundColour((255,255,255))
        
        self.SetIcon(wx.Icon('icon.gif', wx.BITMAP_TYPE_GIF))
        
        StatusBar = self.CreateStatusBar(1)
        StatusBar.SetStatusText("Verze: 0.1, databáze: 21.1.2005", 0)
        
        self.splitter = wx.SplitterWindow(self, -1)       
        self.FiltrPanel = MyPanel(self.splitter)
        self.FiltrPanel.Hide()
        self.VysledkyPanel = MyPanelVysl(self.splitter)
        self.VysledkyPanel.Hide()
        self.splitter.Initialize(self.FiltrPanel)
        
        
    def UkazVysledky(self, evt):
        self.FiltrPanel.Hide()
        self.VysledkyPanel.Show()
    
        self.splitter.ReplaceWindow(self.FiltrPanel, self.VysledkyPanel)
        self.Refresh()
        self.Fit()

    def UkazFiltr(self, evt):
        self.FiltrPanel.Show()
        self.VysledkyPanel.Hide()
    
        self.splitter.ReplaceWindow(self.VysledkyPanel,self.FiltrPanel)
        self.Refresh()
        self.Fit()
        

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, title="České-sbory.cz")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = MyApp(False) # False => vypisuj chyby při startu aplikace
    app.MainLoop()
