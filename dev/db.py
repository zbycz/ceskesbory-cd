# -*- coding: utf8 -*-

from sqlite3 import dbapi2 as sqlite
import os.path
import locale


arr = {
'kraje': [u'- nezáleží -'],
'krajeId': [-1],
'druh': [u'- nezáleží -'],
'druhId': [-1],
'char': [u'- nezáleží -'],
'charId': [-1],
'zanr': [u'- nezáleží -'],
'zanrId': [-1],
}

locale.setlocale(locale.LC_ALL,'')

arrOrder = [u"- nezáleží -", u"žánru", u"sídla", u"počtu členů", u"druhu souboru", u"roku založení"]

connection = sqlite.connect('ucps.db')
def ceskycompare(a, b):
  return locale.strcoll(unicode(a, 'utf-8').encode("cp1250"), unicode(b, 'utf-8').encode("cp1250"));
connection.create_collation("cesky", ceskycompare);
connection.row_factory = sqlite.Row
cursor = connection.cursor()




def close():
    connection.commit()
    cursor.close()


def getDate():
    return u"01/2009";
    cursor.execute("SELECT MAX(aktualizace) FROM katalog")
    s = cursor.fetchone()[0]
    return u"%s/%s" % (int(s[5:7]), s[0:4])



def _fill(name):
    for row in cursor:
        arr[name].append(row[1])
        arr[name+'Id'].append(row[0])
    

def fillLists():
    cursor.execute("SELECT id,nazev FROM kraje")
    _fill('kraje')
    
    cursor.execute("SELECT ID,druh FROM druhy")
    _fill('druh')
    
    cursor.execute("SELECT ID,charakteristika FROM dopl_char")
    _fill('char')
    
    cursor.execute("SELECT ID,zanr FROM zanr")
    _fill('zanr')
    

def getVysledky(userdata):
    
    sql = "SELECT * FROM katalog "
    sql+= "WHERE (status_CID*1=88 OR status_CID*1>1 AND status_CID*1 < 11 AND status_CID*1!=4) "
    
    if userdata['nazev']:
        sql += '''
        AND (nazev LIKE '%$chci_hledat%'
        OR sbm_prijmeni LIKE '%$chci_hledat%' 
        OR sbm1_prijmeni LIKE '%$chci_hledat%' 
        OR sbm2_prijmeni LIKE '%$chci_hledat%' 
        OR sbm3_prijmeni LIKE '%$chci_hledat%' 
        OR sidlo LIKE '%$chci_hledat%' 
        OR sbor_ID LIKE '%$chci_hledat%' 
        OR zrizovatel_nazev LIKE '%$chci_hledat%') 
        '''.replace("$chci_hledat", userdata['nazev'].replace("'","''"))
    
    if userdata['kraje'] != -1:
        sql += 'AND kraj_CID="%s" ' % userdata['kraje']
    
    if userdata['druh'] != -1:
        sql += 'AND druh_CID="%s" ' % userdata['druh']
    
    if userdata['char'] != -1:
        sql += 'AND dopl_char_CID="%s" ' % userdata['char']
    
    if userdata['zanr'] != -1:
        sql += 'AND zanr_CID="%s" ' % userdata['zanr']
    
    sql += ' ORDER BY %s' % userdata['orderby'];
    
    cursor.execute(sql);
    data = []
    i = 0
    for row in cursor:
        i+=1
        data.append(getRowHtml(row))
    
    data2 = []
    data2.append(u"<table width='100%'><tr>")
    if i:
        data2.append(u"<td>Vyhledávání nalezlo %s výsled%s." % (i, (u"ků","ek","ky","ky","ky",u"ků")[i*(i<=5) + 5*(i>5)]) )
        data2.append(u"<td align='right'>řazení %s / %s / %s" % \
         ((u"<a href='order-nazev collate cesky'>název</a>", u"název")[userdata['orderby']=='nazev collate cesky'], \
          (u"<a href='order-sidlo_obec collate cesky'>sídlo</a>", u"sídlo")[userdata['orderby']=='sidlo_obec collate cesky'], \
          (u"<a href='order-celkem DESC'>počet členů</a>", u"počet členů")[userdata['orderby']=='celkem DESC']))
    else:
        data2.append(u"<td>Nebyly nalezeny žádné výsledky, prosím, upravte požadavky.")
    data2.append(u"</table>")
    data2.extend(data)
    
    return u''.join(data2)



def _select(name, val):
    #for i in arr[name+'Id']:
    #    if arr[name+'Id'][i] == val:
    #        break
    try:
        i = arr[name+'Id'].index(val)
    except ValueError:
        print val;
        print name
        print arr[name]
        exit()
    
    if arr[name][i] == u"bez omezení":
        return u"bez žánrového omezení"
    
    return arr[name][i]
    

def getRowHtml(row):        
    if not row["druh_CID"]:
        return u'';
    
    if row["status_CID"] in ('88', '2', '5'):
        if row["status_CID"]=='88' or row["status_CID"]=='5':
           txt = u"<br>Podrobné údaje nebyly na přání souboru zveřejněny."
        elif row["status_CID"]=='2':
           txt = u"<br>Sbor neposkytl informace o své činnosti."
        else:
           txt = u""
        
        return u'''
            <p>&nbsp;<font color=#666666 size="+1">%s</font>
            <table width=100%%>
            <tr><td><font color=#666666><b>%s</b>%s</font><td align=right><font color=#666666><b>%s</b></font>
            </table>
        ''' % (row['nazev'], row['sidlo_obec'], txt, _select('druh', row['druh_CID']))

    
    
    #levý sloupec + nazev
    txt = u'<p>&nbsp;<a href="id-%s"><font size="+1">%s</font></a>' % (row['id'], row["nazev"])
    txt += u'<table width="100%"><tr><td>'
    ##obec
    txt += u'<b>%s</b>' % row["sidlo_obec"]
    ##kraj - PRAHU nezobrazujeme
    if row["kraj_CID"] != 1:
        txt += u' (%s)' % _select('kraje',row["kraj_CID"])
    ##umělec
    txt += u"<br>umělecký vedoucí: <b>%s</b>" % (row["sbm_jmeno"]+" "+row["sbm_prijmeni"])
    ##autorizace udaju
    if row["status_CID"]==3:
        txt += u"<br><font color='#666'>Zde uvedené informace nebyly sborem autorizovány.</font>"

    
    #pravý sloupec
    txt += u"<td align='right'><b>%s</b><br>" % _select('druh', row['druh_CID'])
    ##dopl char
    if row["dopl_char_CID"] in arr['char']:
        txt += u" (%s)" % _select('char',row["dopl_char_CID"])
    ##rok zal
      #if row["rok_zal"]:
      #    txt += u" | založen v roce %s" % row["rok_zal"]
    ##pocet clenu
    if row["celkem"]:
        txt += u'%s členů' % row["celkem"]
    
    # fotka, tabulka
     #if os.path.exists(os.path.join("images","sbory_%s.jpg" % row["id"])):
     #   txt += u"<br><font color='#666'>fotografie souboru k dispozici</font>"
    txt += "</table>";

    return txt
   
    


def getDetail(id):
    cursor.execute("SELECT * FROM katalog WHERE id=? LIMIT 1", (id,)); 
    row = cursor.fetchone()
    
    if row['status_CID'] == 88:
        return u'''
            <h1>%s</h1>
            <h3>%s</h3>
            <p>Pěvecký sbor  si nepřeje zobrazení svých údajů ve veřejném katalogu.
        ''' % (row['nazev'], row['sidlo'])
    
    txt = u''
    
    txt += u'<table width="100%">'
    txt += u'<tr><td><h1>%s <font size=-2>' % row['nazev']
    txt += (u'| ', u'<br>')[len(row['nazev']) > 30]
    txt += row['sidlo_obec']
    ####txt += (u'<br>', u'')[len(row['nazev']) > 30]
    if row["kraj_CID"] != 1:
        txt += u' <font size=-2>(%s)</font>' % _select('kraje',row["kraj_CID"])

    txt += u'</font></h1>'
    
    if row['adresa_zverejnit']:
        txt += u'<br><b>%s, %s, %s %s</b>' %  (row['adresa_osloveni'], row['adresa_ulice'], row['adresa_psc'], row['adresa_obec'])

    # ---------------------------  www a email
    tmp = []
    if row['email']:
        tmp.append(u"<a href='mailto:%s'>%s</a>" % (row['email'],row['email']))
    www = (row['www'], u"")[row['www'] == "http://"] ## když je http, tak False
    if www:
        tmp.append(u"<a href='%s'>%s</a>" % (www,www))
    tmp.append(u"<a href='http://www.ucps.cz/portal/cz/02-01-detail.php?id=%d'>online profil</a>"%id)
    txt += u'<br>' + u' ~ '.join(tmp)
    
    # --------------------------- status
    if row['status_CID'] == 3:
        txt += u"<p><font color='#666'>Zde uvedené informace dosud nebyly sborem autorizovány.</font>"
    
    # --------------------------- logo
    imgpath = os.path.join("images", str(id)+"-logo.jpg")
    if os.path.exists(imgpath):
        txt += u"<td align=right><img src='%s'>" % imgpath
    txt += u'</table>'
    
    
    # -------------------------------- obecné informace    
    txt += u'<table width="100%" cellspacing=0>'
    txt += u"<tr bgcolor='#eeeeee'><td><b>%s</b> " % _select('druh',row['druh_CID'])
    
    if row['rok_zal'] and row['druh_CID'] > 6:
        txt += u"založené v roce %s" % row['rok_zal'];
    elif row['rok_zal']:
        txt += u"založený v roce %s" % row['rok_zal'];
    
    if row["dopl_char_CID"] in arr['charId']:
        txt += u"<br><b>%s</b>" % _select('char', row['dopl_char_CID'])
    txt += u"<br><b>%s</b>" % _select('zanr', row['zanr_CID'])
    
    txt += u"<p><small>umělecký vedoucí:</small><br> <b>%s</b>" % _sbormistr(row)
    
    # ------------------------------------ sbormistři
    if row['sbm1_prijmeni']:
        txt += u"<p><small>další sbormistři:</small>"

    for i in range(1,3):
        if row['sbm%s_prijmeni'%i]:
            txt += u"<br>%s" % _sbormistr(row, "sbm%s"%i)
    
    if row['umpor_prijmeni']:
        txt += u"<p><small>umělecký poradce:</small><br>%s" % _sbormistr(row, "umpor")
    
    
    # ----------------------------------- členové sboru a INFO
    txt += u"<p><small>členové sboru:</small><br>"

    cl_m = row['muzi']+row['chlapci']+row['mladici']
    cl_w = row['zeny']+row['divky']+row['slecny']
    if cl_w:
        txt += u"%s zpěvač%s" % (cl_w, ("ek","ka","ky","ky","ky","ek")[cl_w*(cl_w<=5) + 5*(cl_w>5)] )
    
    if cl_w and cl_m:
        txt += u" a "
        
    if cl_m:
        txt += u"%s zpěvá%s" % (cl_m, (u"ků","k","ci","ci","ci",u"ků")[cl_m*(cl_m<=5) + 5*(cl_m>5)] )
    
    if row["vek_prumer"]:
        txt += u"<br>průměrný věk <b>%s let</b>" % row["vek_prumer"]
    
    if row["frekvence_zkousek"]:
        txt += u"<br>sbor zkouší <b>%s</b>× týdně" % row["frekvence_zkousek"]    
    
    if row["soustredeni"]:
        txt += u"<br>sbor absolvuje <b>%s</b> soustředění ročně" % row["soustredeni"]    
    
    if row["poznamka_verejna"]:
        txt += u"<p>Poznámka:<br>%s" % row["poznamka_verejna"]
    

    # --------------------------------   obrázky
    txt += u"<td align=right width=266px>"
    for i in (1,2):    
        imgpath = os.path.join("images", "%s-%s.jpg" % (id,i))
        if os.path.exists(imgpath):
            txt += u"<img src='%s'>" % imgpath
    
    #----------------------------------   zobrazení šedého rámečku
    zobraz = False
    for k in ('festivaly', 'disko', 'kmenovy_repertoar', 'premiery', 'venovane_skladby', 'zahranicni_projekty'):
        if row[k] and row[k] != u" ":
            zobraz = True
    
    if zobraz:
        txt += u"<tr><td> <td> <tr><td colspan=2 bgcolor='#eeeeee'>"
        
        if row['festivaly'] and row['festivaly'] != u" ":
            txt += u"<p><b>Účast a ocenění na soutěžích a festivalech</b><br>%s</b>" % \
            row['festivaly'].replace(u"\n",u"</b><br>").replace(u"#", u"</b> » <b>")
        
        if row['disko'] and row['disko'] != u" ":
            txt += u"<p><b>Diskografie a rozhlasové nahrávky</b><br>%s" % \
            row['disko'].replace(u"\n",u"<br>")
        
        if row['kmenovy_repertoar'] and row['kmenovy_repertoar'] != u" ":
            txt += u"<p><b>Příklady kmenového repertoáru</b><br>%s</b>" % \
            row['kmenovy_repertoar'].replace(u"\n",u"</b><br>").replace(u"#", u"</b> » <b>")
        
        if row['premiery'] and row['premiery'] != u" ":
            txt += u"<p><b>Premiéry významných českých děl</b><br>%s" % \
            row['premiery'].replace(u"\n",u"<br>")
        
        if row['venovane_skladby'] and row['venovane_skladby'] != u" ":
            txt += u"<p><b>Skladby věnované sboru</b><br>%s" % \
            row['venovane_skladby'].replace(u"\n",u"<br>")
        
        if row['zahranicni_projekty'] and row['zahranicni_projekty'] != u" ":
            txt += u"<p><b>Uskutečněné zahraniční projekty</b><br>%s" % \
            row['zahranicni_projekty'].replace(u"\n",u"<br>")
        
    
    txt += u"<p align='right'><i><small>Záznam byl založen %s a naposledy aktualizován %s.</small></i>" % (_datum(row['zalozeni_profilu']), _datum(row['aktualizace']))
    txt += u"</table>"
        
    return txt
    
    

def _sbormistr(row, sbm="sbm"):
    txt = u'';
    if row[sbm+'_predni_titul']:
        txt += row[sbm+'_predni_titul'] + ' ';
    txt += row[sbm+'_jmeno'] + ' ' + row[sbm+'_prijmeni']
    if row[sbm+'_zadni_titul']:
        txt += ', ' + row[sbm+'_zadni_titul'] 
    return txt


def _datum(s):
    return u"%s.%s.%s %s" % (int(s[8:10]), int(s[5:7]), s[0:4], s[11:])

if __name__ == '__main__':
    #cursor.execute("SELECT name FROM SQLITE_MASTER")
    #print cursor.fetchall()
#     cursor.execute("SELECT id,dopl_char_CID FROM katalog")
#     for row in cursor:
#         if row['dopl_char_CID'] != int(row['dopl_char_CID']):
#             print row['id']
#     exit()





    cursor.execute("SELECT kmenovy_repertoar FROM katalog WHERE id=168 LIMIT 1"); 
    print cursor.fetchone()    
    fillLists()
    data=getDetail(168)
    #data=getVysledky({'char': -1, 'druh': 6, 'zanr': -1, 'kraje': -1, 'nazev': u''})
    
    import wx,layout
    app=wx.App()
    frm = wx.Frame(None, -1, u"Test", (10, 10), (650, 400))
    html = layout.HtmlWin(frm, -1)
    html.SetPage(data)
    frm.Show()
    app.MainLoop()

#cursor.execute("SELECT * FROM SQLITE_MASTER")
# cursor.execute("SELECT status_CID*1 FROM katalog LIMIT 100")
# for r in cursor:
#     print r
#     
# exit()









