# -*- coding: cp1250 -*-

import layout, wx
import  wx.lib.scrolledpanel as wxscrolled
import  wx.lib.fancytext as wxfancytext

arrKraje = ["- nez�le�� -", "Hlavn� m�sto Praha", "St�edo�esk� kraj", "Jiho�esk� kraj", "Plze�sk� kraj", "Karlovarsk� kraj", "�steck� kraj", "Libereck� kraj", "Kr�lov�hradeck� kraj", "Pardubick� kraj", "Kraj Vyso�ina", "Jihomoravsk� kraj", "Olomouck� kraj", "Moravskoslezsk� kraj", "Zl�nsk� kraj"]
arrDruh = ["- nez�le�� -", "mu�sk� sbor", "�ensk� sbor", "sm�en� sbor", "d�tsk� sbor", "d�v�� sbor", "chlapeck� sbor", "vok�ln� noneto", "vok�ln� okteto", "vok�ln� septeto", "vok�ln� sexteto", "vok�ln� kvinteto", "vok�ln� kvarteto", "vok�ln� trio"]
arrChar = ["- nez�le�� -", "sborov� �kola", "sokolsk� sbor", "sbor z�kladn� �koly", "gymnazi�ln� sbor", "akademick� sbor", "chr�mov� sbor", "sbor z�kladn� um�leck� �koly", "st�edo�kolsk� sbor", "sbor z�kladn� a z�kladn� um�leck� �koly", "sbor mate�sk� �koly", "m�stsk� sbor", "skautsk� sbor", "projektov� sbor", "�koln� sbor", "folklorn� soubor"]
arrZanr = ["- nez�le�� -", "bez omezen�", "duchovn� hudba", "chor�l, liturgick� hudba", "star� hudba (v�etn� barokn�)", "hudba klasicismu a romantismu", "soudob� v�n� hudba", "folkl�r a �pravy lidov�ch p�sn�", "jazz", "popul�rn� hudba a muzik�l", "skladby �esk�ch autor�"]
arrOrder = ["- nez�le�� -", "��nru", "s�dla", "po�tu �len�", "druhu souboru", "roku zalo�en�"]

                


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
        form['nazev'] = ['N�zev souboru, s�dlo, p��jmen� sbormistra:', False]
        form['druh'] = ['Druh souboru:', arrDruh]
        form['char'] = ['Zvl�tn� charakteristika:', arrChar]
        form['zanr'] = ['��nrov� zam��en�:', arrZanr]
        form['order'] = ['V�sledky �adit podle:', arrOrder]
        
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
        data = []
        data.append(["Beru�ky", "Klatovy | d�tsk� sbor ", "| sbor z�kladn� �koly | zalo�en v roce 2001", "60 �len�", "um�leck� vedouc�: Dana Martinkov�"])

        #vytvo�� panel
        self.PnlVysl = wx.Panel(self)
        self.PnlVysl.Hide()
        
        #sizer a obr�zek
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(layout.getTopSizer(self.PnlVysl, "V�sledky vyhled�v�n�"), 0, wx.EXPAND)

        #tla��tko 
        butt = wx.Button(self.PnlVysl, -1, 'Zm�nit filtr')
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
        wx.Frame.__init__(self, None, -1, "�esk�-sbory.cz", (10, 10), (650, 400))
        self.CenterOnScreen()
        self.SetBackgroundColour((255,255,255))
        self.SetIcon(wx.Icon('icon.gif', wx.BITMAP_TYPE_GIF))
        
        
        self.StatusBar = self.CreateStatusBar(1)
        self.StatusBar.SetStatusText("Verze: 0.1, datab�ze: 21.1.2005", 0)
        
        self.Spltr = UcpsSpltr(self)
        self.Refresh()

class UcpsApp(wx.App):
    def OnInit(self):
        self.frame = UcpsFrame()
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

if __name__ == '__main__':
    app = UcpsApp(False) # False => vypisuj chyby p�i startu aplikace
    app.MainLoop()
