# coding=utf-8
from tatort_fundus import * 


if __name__ == '__main__':
    salzleiche = Episode('Salzleiche')
    print salzleiche.episode_number
    for i in salzleiche.actors:
        print i
    print salzleiche.summary
    print salzleiche.quote
    print salzleiche.drehbuch
    print salzleiche.idee
    print salzleiche.regie
    print salzleiche.sender
    print salzleiche.firma
    print salzleiche.drehzeit
    print salzleiche.drehort
    print salzleiche.bildformat
    print salzleiche.redaktion
    print salzleiche.erstsendung

    ballauf = Ermittler()
    for i in ballauf.folgen('Max Ballauf'):
        print 'Nummer: %s, Name: %s, Datum: %s' % (i[1], i[2], i[3])

    for i in ermittler_uebersicht():
        print i

    for i in naechste_erstsendungen():
        print 'Nummer: %s, Name: %s, Ermittler: %s, Datum: %s, Sender: %s' % (i[0], i[1], i[2], i[3], i[4])

    for i in naechste_wiederholungen():
        print 'Datum: %s, Uhrzeit: %s, Programm: %s, Titel: %s, Ermittler: %s, ProdSender: %s, Nummer: %s' % (i[0], i[1], i[2], i[3], i[4], i[5], i[6])

    for i in tatort_today():
        print 'Datum: %s, Uhrzeit: %s, Programm: %s, Nummer: %s, Titel: %s, Ermittler: %s' % (i[0], i[1], i[2], i[3], i[4], i[5])
