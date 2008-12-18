# -*- coding: cp1250 -*-

import layout, wx


arrKraje = ["- nez�le�� -", "Hlavn� m�sto Praha", "St�edo�esk� kraj", "Jiho�esk� kraj", "Plze�sk� kraj", "Karlovarsk� kraj", "�steck� kraj", "Libereck� kraj", "Kr�lov�hradeck� kraj", "Pardubick� kraj", "Kraj Vyso�ina", "Jihomoravsk� kraj", "Olomouck� kraj", "Moravskoslezsk� kraj", "Zl�nsk� kraj"]
arrDruh = ["- nez�le�� -", "mu�sk� sbor", "�ensk� sbor", "sm�en� sbor", "d�tsk� sbor", "d�v�� sbor", "chlapeck� sbor", "vok�ln� noneto", "vok�ln� okteto", "vok�ln� septeto", "vok�ln� sexteto", "vok�ln� kvinteto", "vok�ln� kvarteto", "vok�ln� trio"]
arrChar = ["- nez�le�� -", "sborov� �kola", "sokolsk� sbor", "sbor z�kladn� �koly", "gymnazi�ln� sbor", "akademick� sbor", "chr�mov� sbor", "sbor z�kladn� um�leck� �koly", "st�edo�kolsk� sbor", "sbor z�kladn� a z�kladn� um�leck� �koly", "sbor mate�sk� �koly", "m�stsk� sbor", "skautsk� sbor", "projektov� sbor", "�koln� sbor", "folklorn� soubor"]
arrZanr = ["- nez�le�� -", "bez omezen�", "duchovn� hudba", "chor�l, liturgick� hudba", "star� hudba (v�etn� barokn�)", "hudba klasicismu a romantismu", "soudob� v�n� hudba", "folkl�r a �pravy lidov�ch p�sn�", "jazz", "popul�rn� hudba a muzik�l", "skladby �esk�ch autor�"]
arrOrder = ["- nez�le�� -", "��nru", "s�dla", "po�tu �len�", "druhu souboru", "roku zalo�en�"]





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
        form['nazev'] = ['N�zev souboru, s�dlo, p��jmen� sbormistra:', False]
        form['druh'] = ['Druh souboru:', arrDruh]
        form['char'] = ['Zvl�tn� charakteristika:', arrChar]
        form['zanr'] = ['��nrov� zam��en�:', arrZanr]
        form['order'] = ['V�sledky �adit podle:', arrOrder]
        
        
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
#         grid1.Add(wx.StaticText(self, -1, 'N�zev souboru, s�dlo, p��jmen� sbormistra:'), 0, style)
#         grid1.Add(form[0])
# 
#         grid1.Add(wx.StaticText(self, -1, 'Druh souboru:'), 0, style)
#         inputDruh = wx.Choice(self, -1, choices = arrDruh)
#         inputDruh.SetSelection(0)
#         grid1.Add(inputDruh)
# 
#         grid1.Add(wx.StaticText(self, -1, 'Zvl�tn� charakteristika:'), 0, style)
#         inputChar = wx.Choice(self, -1, choices = arrChar)
#         inputChar.SetSelection(0)
#         grid1.Add(inputChar)
# 
#         grid1.Add(wx.StaticText(self, -1, '��nrov� zam��en�:'), 0, style)
#         kraje = wx.Choice(self, -1, choices = arrZanr)
#         kraje.SetSelection(0)
#         grid1.Add(kraje)
# 
#         grid1.Add(wx.StaticText(self, -1, 'V�sledky �adit podle:'), 0, style)
#         kraje = wx.Choice(self, -1, choices = arrOrder)
#         kraje.SetSelection(0)
#         grid1.Add(kraje)

        # vbox->button
        butt = wx.Button(self, -1, 'Zobrazit v�sledky')
        vbox.Add(butt, 0, wx.ALIGN_CENTER)
        self.Bind(wx.EVT_BUTTON, self.GetParent().GetParent().UkazVysledky, butt)
        
        self.SetSizer(vbox)
        


class MyPanelVysl(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(layout.getTopSizer(self, "V�sledky"), 0, wx.EXPAND)
        vbox.Add((-1,20))

        butt = wx.Button(self, -1, 'Zm�nit filtr')
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
        StatusBar.SetStatusText("Verze: 0.1, datab�ze: 21.1.2005", 0)
        
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
        frame = MyFrame(None, -1, title="�esk�-sbory.cz")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

if __name__ == '__main__':
    app = MyApp(False) # False => vypisuj chyby p�i startu aplikace
    app.MainLoop()
