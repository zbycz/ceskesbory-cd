# -*- coding: cp1250 -*-

import layout, wx


arrKraje = ["- nez�le�� -", "Hlavn� m�sto Praha", "St�edo�esk� kraj", "Jiho�esk� kraj", "Plze�sk� kraj", "Karlovarsk� kraj", "�steck� kraj", "Libereck� kraj", "Kr�lov�hradeck� kraj", "Pardubick� kraj", "Kraj Vyso�ina", "Jihomoravsk� kraj", "Olomouck� kraj", "Moravskoslezsk� kraj", "Zl�nsk� kraj"]
arrDruh = ["- nez�le�� -", "mu�sk� sbor", "�ensk� sbor", "sm�en� sbor", "d�tsk� sbor", "d�v�� sbor", "chlapeck� sbor", "vok�ln� noneto", "vok�ln� okteto", "vok�ln� septeto", "vok�ln� sexteto", "vok�ln� kvinteto", "vok�ln� kvarteto", "vok�ln� trio"]
arrChar = ["- nez�le�� -", "sborov� �kola", "sokolsk� sbor", "sbor z�kladn� �koly", "gymnazi�ln� sbor", "akademick� sbor", "chr�mov� sbor", "sbor z�kladn� um�leck� �koly", "st�edo�kolsk� sbor", "sbor z�kladn� a z�kladn� um�leck� �koly", "sbor mate�sk� �koly", "m�stsk� sbor", "skautsk� sbor", "projektov� sbor", "�koln� sbor", "folklorn� soubor"]
arrZanr = ["- nez�le�� -", "bez omezen�", "duchovn� hudba", "chor�l, liturgick� hudba", "star� hudba (v�etn� barokn�)", "hudba klasicismu a romantismu", "soudob� v�n� hudba", "folkl�r a �pravy lidov�ch p�sn�", "jazz", "popul�rn� hudba a muzik�l", "skladby �esk�ch autor�"]
arrOrder = ["- nez�le�� -", "��nru", "s�dla", "po�tu �len�", "druhu souboru", "roku zalo�en�"]



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
        form['nazev'] = ['N�zev souboru, s�dlo, p��jmen� sbormistra:', False]
        form['druh'] = ['Druh souboru:', arrDruh]
        form['char'] = ['Zvl�tn� charakteristika:', arrChar]
        form['zanr'] = ['��nrov� zam��en�:', arrZanr]
        form['order'] = ['V�sledky �adit podle:', arrOrder]
        
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
        butt = wx.Button(self.PnlFiltr, -1, 'Zobrazit v�sledky')
        vbox.Add(butt, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.OnSwitchVysl, butt)
        
        self.PnlFiltr.SetSizer(vbox)
        

    def CreateVysl(self):
        self.PnlVysl = wx.Panel(self.splitter)
        self.PnlVysl.Hide()
        self.PnlVysl.heading = "V�slekdy"
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        butt = wx.Button(self.PnlVysl, -1, 'Zm�nit filtr')
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
        wx.Frame.__init__(self, None, -1, "�esk�-sbory.cz", (10, 10), (650, 400))
        self.CenterOnScreen()
        self.SetBackgroundColour((255,255,255))
        
        self.SetIcon(wx.Icon('icon.gif', wx.BITMAP_TYPE_GIF))
        
        StatusBar = self.CreateStatusBar(1)
        StatusBar.SetStatusText("Verze: 0.1, datab�ze: 21.1.2005", 0)
        
        UcpsWindow(self)


class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = MyApp(False) # False => vypisuj chyby p�i startu aplikace
    app.MainLoop()
