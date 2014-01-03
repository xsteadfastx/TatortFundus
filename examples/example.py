# coding=utf-8
from tatort_fundus import Episode, Ermittler


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

    for i in ballauf.uebersicht:
        print i
