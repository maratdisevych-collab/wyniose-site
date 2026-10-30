# -*- coding: utf-8 -*-
"""Polish service and guide pages (wyniose.pl/<slug>/). Built by build.py with src/subpage.html.j2.

Rules for this copy (see CLAUDE.md): only facts the owner confirmed, prices only from prices.py (owner-approved "from" prices),
no reviews, no speed promises, no copied competitor text, no keyword stuffing. Each page answers one real question.
Paragraphs are plain strings (escaped) or Markup when they carry a link written here by hand.
Blocks: str / Markup = paragraph, {'ul': [...]}, {'ol': [[title, text], ...]}, {'note': ...},
{'table': [[row label, value, ...], ...], 'head': [...]}, {'cta': text above the WhatsApp and call buttons}."""
from markupsafe import Markup
from prices import FROM as F, VAN, EXTRA as X, FLOOR_VAN, ZONES, zl

UPDATED = '2026-10-28'
UPDATED2 = '2026-10-30'

def od(n): return 'od ' + zl(n)
def plus(n): return '+' + zl(n)
CENNIK = Markup('Wszystkie ceny i dopłaty: <a href="../cennik/">cennik</a>.')

PHOTOS = {'ul': ['Całe pomieszczenie, z progu.', 'Duże rzeczy z bliska.', 'Klatkę, korytarz lub schody, jeśli są wąskie.',
                 'Im więcej zdjęć, tym dokładniejsza wycena.']}

PAGES = [
    dict(
        slug='oproznianie-piwnic-strychow-garazy', kind='service', updated=UPDATED2,
        title='Opróżnianie piwnic, strychów i garaży Wrocław | Wyniosę',
        desc='Opróżniamy piwnice, komórki lokatorskie, strychy i garaże we Wrocławiu i okolicy do 70 km. Piwnica od ' + zl(F['cellar']) + ', wycena ze zdjęć za darmo.',
        crumb='Piwnice, strychy i garaże', service_type='Opróżnianie piwnic, strychów i garaży',
        plate='−1', eyebrow='Piwnice, komórki, strychy, garaże',
        h1a='Opróżnianie piwnic, strychów i garaży', h1b='we Wrocławiu',
        lead='Wynosimy rzeczy z piwnic, komórek lokatorskich, strychów i garaży, ładujemy je do naszego busa i wywozimy do PSZOK albo do recyklingu.',
        facts=['Własny bus', 'Rozkręcamy meble', 'Do 70 km od Wrocławia', 'Kontakt w czterech językach'],
        sections=[
            dict(h='Co najczęściej wynosimy', body=[
                {'ul': ['Stare meble, regały, szafki i półki.', 'Rowery, wózki, sanki, narty.',
                        'Kartony, słoiki, książki i stare gazety.', 'Stare AGD: pralki, lodówki i inne duże sprzęty.',
                        'Narzędzia, deski, meble ogrodowe, dywany i materace.']},
                'Farby, chemię, gruz i opony bierzemy tylko po wcześniejszym uzgodnieniu. Azbestu, odpadów medycznych, butli gazowych i gaśnic nie zabieramy.',
            ]),
            dict(h='Piwnica w kamienicy, w bloku albo pod domem', body=[
                'W kamienicach piwnice mają często niskie stropy i ciasne przejścia. W blokach dochodzą długie korytarze komórek i drzwi, przez które szafa nie przejdzie w całości. Dlatego meble rozkręcamy na miejscu, a przy dużych rzeczach w razie potrzeby zabezpieczamy narożniki i poręcze.',
                'Nie musisz niczego wcześniej pakować ani wynosić. Wystarczy, że powiesz, co ma zostać.',
            ]),
            dict(h='Strych i garaż', body=[
                'Ze strychu najtrudniej się schodzi: strome schody, właz, wąski korytarz. W garażu zwykle jest po prostu dużo rzeczy, bo trafia tam wszystko, co nie zmieściło się w mieszkaniu. Wszystko wynosimy i ładujemy do busa, a potem segregujemy i oddajemy do PSZOK albo do recyklingu.',
            ]),
            dict(h='Ile kosztuje opróżnienie piwnicy?', body=[
                {'table': [['Piwnica lub komórka lokatorska', od(F['cellar'])], ['Garaż', od(F['garage'])], ['Pojedyncza rzecz, np. rower albo szafka', od(F['item'])]], 'head': ['Co', 'Cena']},
                'Dwie piwnice o tej samej powierzchni mogą się bardzo różnić ilością rzeczy. Na cenę wpływa to, ile jest do wyniesienia, czy trzeba rozkręcać meble, jak daleko jest do busa i jakie są schody. Strych wychodzi zwykle trochę drożej, bo zejście jest trudniejsze.',
                'Wstępną cenę podajemy po zdjęciach. Ostateczną potwierdzamy na miejscu, zanim zaczniemy. Jakie zdjęcia wysłać:',
                PHOTOS, CENNIK,
            ]),
            dict(h='Pojedyncze rzeczy', body=[
                'Wywieziemy też pojedyncze rzeczy, na przykład stary rower, szafkę albo materac. Zabieramy je przy okazji innych zleceń w okolicy, termin ustalamy razem.',
                {'cta': 'Wyślij zdjęcia piwnicy, garażu albo strychu.'},
            ]),
        ],
        faq=[
            ['Czy muszę być na miejscu?', 'Nie. Przy wycenie ustalimy, jak dostać się do piwnicy i przekazać klucze, a po pracy wyślemy zdjęcia.'],
            ['Piwnica jest w kamienicy bez windy. Dacie radę?', 'Tak. Schody i odległość do busa uwzględniamy w wycenie.'],
            ['Czy przy okazji opróżnicie też mieszkanie?', 'Tak. Piwnica, strych, garaż i mieszkanie mogą być jednym zleceniem. Napisz to w wiadomości.'],
            ['Posprzątacie po opróżnieniu?', 'Tak, na życzenie, jako usługę dodatkową.'],
            ['Przyjedziecie obejrzeć przed wyceną?', 'Tak, za darmo, jeśli zdjęcia nie wystarczą.'],
        ],
        related=['wywoz-mebli-wroclaw', 'oproznianie-mieszkania-po-zmarlym', 'dla-firm', 'obszar-dzialania'],
    ),
    dict(
        slug='oproznianie-mieszkania-po-zmarlym', kind='service', updated=UPDATED2,
        title='Opróżnianie mieszkania po zmarłym Wrocław | Wyniosę',
        desc='Opróżniamy mieszkania po bliskich we Wrocławiu i okolicy. Dokumenty, zdjęcia i pamiątki odkładamy dla rodziny. Możesz to zlecić, nawet jeśli mieszkasz daleko.',
        crumb='Mieszkania po bliskich', service_type='Opróżnianie mieszkania po zmarłym',
        plate='', eyebrow='Mieszkania po bliskich',
        h1a='Opróżnianie mieszkania po bliskiej osobie', h1b='we Wrocławiu',
        lead='Gdy trzeba opróżnić mieszkanie po zmarłym członku rodziny, odkładamy dla bliskich dokumenty, zdjęcia i pamiątki, a meble i resztę rzeczy wynosimy i wywozimy. Możesz nam to zlecić także wtedy, gdy mieszkasz daleko od Wrocławia.',
        facts=['Nie musisz być na miejscu', 'Dokumenty i pamiątki odkładamy', 'Zdjęcia po robocie', 'Kontakt w czterech językach'],
        sections=[
            dict(h='Jak to wygląda krok po kroku', body=[
                {'ol': [['Zdjęcia albo oględziny.', 'Piszesz lub dzwonisz. Zdjęcia może wysłać ktokolwiek, kto ma dostęp do mieszkania. Jeśli zdjęcia nie wystarczą, przyjedziemy obejrzeć mieszkanie za darmo.'],
                        ['Ustalenia.', 'Mówisz, co ma zostać: konkretne meble, jeden pokój, rzeczy dla rodziny. Ustalamy cenę, termin i sposób przekazania kluczy.'],
                        ['Opróżnienie.', 'Pakujemy, rozkręcamy, znosimy i ładujemy do naszego busa. Dokumenty, zdjęcia, listy i pamiątki, które znajdziemy, odkładamy osobno.'],
                        ['Zdjęcia po robocie.', 'Wysyłamy zdjęcia pustego mieszkania. Rzeczy odłożone dla rodziny zostawiamy tam, gdzie się umówimy.']]},
            ]),
            dict(h='Co odkładamy dla rodziny', body=[
                'Dokumenty, zdjęcia, listy i pamiątki, które znajdziemy podczas pracy, odkładamy osobno, zamiast wyrzucać.',
                'Mimo to radzimy, żeby przed naszym przyjazdem rodzina zabrała to, o czym wie i co jest dla niej ważne: biżuterię, gotówkę, ważne dokumenty, telefony i komputery z danymi.',
            ]),
            dict(h='Gdy rodzina mieszka daleko', body=[
                'Często mieszkanie we Wrocławiu zostaje po kimś, a najbliżsi mieszkają w innym mieście albo za granicą. Nie musisz przyjeżdżać. Sposób przekazania kluczy ustalimy przy wycenie, kontakt prowadzimy przez WhatsApp albo telefon, a po pracy wysyłamy zdjęcia pustego mieszkania.',
                'Rozmawiamy po polsku, ukraińsku, rosyjsku i angielsku. Pisz w języku, w którym Ci wygodnie.',
            ]),
            dict(h='Przed sprzedażą, oddaniem kluczy albo remontem', body=[
                'Mieszkanie trzeba zwykle opróżnić przed sprzedażą, przed oddaniem lokalu właścicielowi lub zarządcy albo przed remontem. Opróżniamy całe mieszkanie albo tylko wskazane pokoje, razem z piwnicą i komórką. Sprzątanie po opróżnieniu robimy na życzenie, jako usługę dodatkową.',
                {'note': 'Zanim zlecisz opróżnienie, upewnij się, że możesz dysponować mieszkaniem i rzeczami, na przykład jako spadkobierca albo w porozumieniu z pozostałymi spadkobiercami lub zarządcą.'},
            ]),
            dict(h='Ile to kosztuje', body=[
                {'table': [['Kawalerka', od(F['studio'])], ['Mieszkanie dwupokojowe', od(F['flat'])], ['Mieszkanie trzypokojowe', od(F['flat3'])], ['Dom', od(F['house'])]], 'head': ['Co', 'Cena']},
                'Cena zależy od ilości rzeczy, piętra, windy i tego, czy trzeba rozkręcać meble. Wstępną cenę podajemy po zdjęciach, ostateczną potwierdzamy na miejscu, zanim zaczniemy. Wycena jest za darmo.',
                'Płacisz gotówką, BLIK-iem albo przelewem. Wystawiamy fakturę bez VAT.', CENNIK,
            ]),
        ],
        faq=[
            ['Czy ktoś z rodziny musi być na miejscu?', 'Nie. Przy wycenie ustalimy, jak przekazać klucze, a po pracy wyślemy zdjęcia pustego mieszkania.'],
            ['Czy możecie opróżnić tylko część mieszkania?', 'Tak. Wskaż, co zostaje, a co wynosimy. Wyniesiemy nawet pojedyncze rzeczy.'],
            ['Co się dzieje z meblami i rzeczami?', 'Segregujemy je i oddajemy do PSZOK albo do recyklingu.'],
            ['Zabierzecie też rzeczy z piwnicy i komórki?', 'Tak, mogą być częścią tego samego zlecenia.'],
            ['Przyjedziecie obejrzeć mieszkanie przed wyceną?', 'Tak, za darmo, jeśli zdjęcia nie wystarczą.'],
        ],
        related=['oproznianie-piwnic-strychow-garazy', 'wywoz-mebli-wroclaw', 'obszar-dzialania', 'jak-pozbyc-sie-starych-mebli-wroclaw'],
    ),
    dict(
        slug='wywoz-mebli-wroclaw', kind='service', updated=UPDATED2,
        title='Wywóz starych mebli i AGD Wrocław | Wyniosę',
        desc='Wynosimy i wywozimy stare meble i AGD we Wrocławiu: szafy, meblościanki, wersalki, pralki, lodówki. Rozkręcamy, znosimy z każdego piętra. Jeden mebel od 270 zł.',
        crumb='Wywóz mebli i AGD', service_type='Wywóz starych mebli i AGD',
        plate='IV', eyebrow='Meble i AGD z każdego piętra',
        h1a='Wywóz starych mebli', h1b='i AGD we Wrocławiu',
        lead='Wywozimy stare meble i AGD z mieszkań, piwnic i biur. Meble, które nie przechodzą przez drzwi albo klatkę, rozkręcamy na miejscu, a lodówki i pralki znosimy z każdego piętra.',
        facts=['Także pojedyncze meble', 'Rozkręcamy meble', 'Każde piętro, także bez windy', 'Do 70 km od Wrocławia'],
        sections=[
            dict(h='Co wywozimy', body=[
                {'ul': ['Szafy, meblościanki, komody, regały.', 'Wersalki, kanapy, fotele, łóżka i materace.',
                        'Stoły, krzesła, biurka.', 'Pralki, lodówki i inne duże AGD.', 'Dywany, kartony i drobne wyposażenie.']},
            ]),
            dict(h='Rozkręcamy i znosimy', body=[
                'Co nie przejdzie przez drzwi albo zakręt klatki, rozkręcamy na miejscu. Schodzimy z każdego piętra, także bez windy. Piętro i brak windy uwzględniamy w wycenie od razu. Przy dużych meblach w razie potrzeby zabezpieczamy narożniki i poręcze.',
            ]),
            dict(h='Jeden mebel też wywieziemy', body=[
                'Wywieziemy też pojedynczy mebel, na przykład kanapę, szafę albo lodówkę. Pojedyncze rzeczy zabieramy przy okazji innych zleceń w okolicy, termin ustalamy razem. Jeśli zależy Ci na konkretnym dniu, przyjedziemy osobno.',
                {'table': [['Fotel, materac, szafka', od(F['item'])], ['Lodówka, pralka, kuchenka', od(F['appliance'])], ['Kanapa, łóżko, szafa w całości, stół', od(F['furniture'])],
                           ['Szafa do rozkręcenia', od(320)], ['Meblościanka lub narożnik do rozkręcenia', od(460)], ['Każdy kolejny mebel z tego samego adresu', plus(X['next_item'])],
                           ['Osobny przyjazd w dniu, który wybierzesz', od(F['solo'])], ['Piętro bez windy', plus(X['floor_item']) + ' za piętro']], 'head': ['Co', 'Cena']},
                Markup('Jeśli masz samochód, jedną kanapę możesz bezpłatnie oddać w PSZOK albo wystawić do osiedlowego kontenera na gabaryty. Jak to zrobić, opisaliśmy w poradniku <a href="../jak-pozbyc-sie-starych-mebli-wroclaw/">Jak pozbyć się starych mebli we Wrocławiu</a>.'),
            ]),
            dict(h='Dokąd trafiają meble', body=[
                'Meble, elektroodpady, papier i resztę segregujemy, a potem oddajemy do PSZOK albo do recyklingu. Niczego nie zostawiamy przy śmietniku, bo za gabaryty wystawione poza terminem odbioru grozi mandat.',
            ]),
            dict(h='Ile kosztuje wywóz mebli', body=[
                'Ceny w tabeli powyżej to ceny minimalne. Ostateczna cena zależy od ilości mebli, piętra, windy i tego, czy trzeba je rozkręcać. Wstępną cenę podajemy po zdjęciach, a ostateczną potwierdzamy na miejscu, przed rozpoczęciem pracy. Wycena jest bezpłatna. Jakie zdjęcia wysłać:',
                PHOTOS, CENNIK, {'cta': 'Wyślij zdjęcia mebli, a podamy cenę.'},
            ]),
        ],
        faq=[
            ['Wywieziecie jedną kanapę?', f'Tak, od {zl(F["furniture"])}. Zabieramy ją przy okazji innych zleceń w okolicy albo osobnym przyjazdem w wybranym dniu, od {zl(F["solo"])}.'],
            ['Rozkręcacie meble na miejscu?', 'Tak, jeśli nie przechodzą przez drzwi albo klatkę.'],
            ['Zabieracie lodówki i pralki?', 'Tak. Duże AGD wynosimy i oddajemy osobno, jako elektroodpady.'],
            ['Czy muszę być na miejscu?', 'Nie. Przy wycenie ustalimy, jak przekazać klucze, a po pracy wyślemy zdjęcia pustego miejsca.'],
            ['Wystawiacie fakturę?', 'Tak, fakturę bez VAT. Płacisz gotówką, BLIK-iem albo przelewem.'],
        ],
        related=['jak-pozbyc-sie-starych-mebli-wroclaw', 'oproznianie-piwnic-strychow-garazy', 'oproznianie-mieszkania-po-zmarlym', 'dla-firm'],
    ),
    dict(
        slug='dla-firm', kind='service', updated=UPDATED2,
        title='Opróżnianie biur i lokali Wrocław, dla firm | Wyniosę',
        desc='Opróżniamy biura, lokale usługowe i mieszkania na wynajem we Wrocławiu i do 70 km. Pracujemy dla właścicieli, zarządców i wspólnot. Faktura bez VAT.',
        crumb='Dla firm i zarządców', service_type='Opróżnianie biur i lokali',
        plate='', eyebrow='Dla firm i zarządców',
        h1a='Opróżnianie biur i lokali', h1b='we Wrocławiu',
        lead='Opróżniamy biura po przeprowadzce, lokale po najemcach i mieszkania na wynajem między lokatorami. Wynosimy meble i wyposażenie, wywozimy je i oddajemy pusty lokal. Wystawiamy fakturę bez VAT.',
        facts=['Faktura bez VAT', 'Kilka adresów w jednej wycenie', 'Zdjęcia po robocie', 'Do 70 km od Wrocławia'],
        sections=[
            dict(h='Dla kogo pracujemy', body=[
                {'ol': [['Biura.', 'Biurka, krzesła, regały i szafy na dokumenty, także z kilku pięter.'],
                        ['Lokale usługowe.', 'Wyposażenie po zakończonej działalności albo przed nowym najemcą.'],
                        ['Właściciele mieszkań na wynajem.', 'Rzeczy zostawione przez najemców i stare meble przed remontem.'],
                        ['Zarządcy nieruchomości i wspólnoty.', 'Kilka lokali, piwnic albo komórek naraz, w jednym zleceniu.']]},
            ]),
            dict(h='Kilka lokali naraz', body=[
                'Jeśli lokali jest kilka, wpisz w wiadomości wszystkie adresy. Wycenimy wszystko razem i ustalimy termin, który pasuje do Twojego harmonogramu.',
            ]),
            dict(h='Bez Twojej obecności', body=[
                'Nie musisz przyjeżdżać na miejsce. Dostęp i przekazanie kluczy ustalimy przy wycenie, a po pracy wyślemy zdjęcia pustego lokalu. Możesz je od razu przekazać właścicielowi, najemcy albo zarządowi.',
            ]),
            dict(h='Rozliczenie', body=[
                'Wstępną cenę podajemy po zdjęciach, a ostateczną potwierdzamy na miejscu, przed rozpoczęciem pracy. Wystawiamy fakturę bez VAT. Płatność przelewem, BLIK-iem albo gotówką.',
                f'Pół busa wyposażenia biura kosztuje od {zl(F["office"])}. Odpadów z działalności firm PSZOK nie przyjmuje, więc oddajemy je do uprawnionego punktu odbioru, a ten koszt jest już w cenie.', CENNIK,
            ]),
            dict(h='Czego nie zabieramy', body=[
                'Azbestu, odpadów medycznych, butli gazowych i gaśnic. Farby, chemię, gruz i opony bierzemy tylko po wcześniejszym uzgodnieniu.',
            ]),
        ],
        faq=[
            ['Wystawiacie fakturę?', 'Tak, fakturę bez VAT.'],
            ['Możecie opróżnić kilka lokali naraz?', 'Tak. Dopisz adresy w wiadomości, wycenimy wszystko razem.'],
            ['Przyjedziecie obejrzeć lokal?', 'Tak, za darmo, jeśli zdjęcia nie wystarczą.'],
            ['Pracujecie poza Wrocławiem?', 'Tak, do około 70 km od miasta.'],
            ['Czy ktoś musi nas wpuścić?', 'Nie zawsze. Dostęp i przekazanie kluczy ustalimy przy wycenie.'],
        ],
        related=['oproznianie-piwnic-strychow-garazy', 'wywoz-mebli-wroclaw', 'obszar-dzialania', 'oproznianie-mieszkania-po-zmarlym'],
    ),
    dict(
        slug='obszar-dzialania', kind='area', updated=UPDATED2,
        title='Wrocław i okolice do 70 km: obszar działania | Wyniosę',
        desc='Opróżniamy mieszkania, piwnice i biura w całym Wrocławiu i w miejscowościach do około 70 km od miasta: Oława, Siechnice, Kąty Wrocławskie, Trzebnica, Oleśnica.',
        crumb='Obszar działania', service_type='Opróżnianie mieszkań i wywóz rzeczy',
        plate='70 km', eyebrow='Obszar działania',
        h1a='Wrocław i okolice', h1b='do 70 km',
        lead='Dojeżdżamy własnym busem do każdego osiedla we Wrocławiu i do miejscowości w promieniu około 70 km od miasta.',
        facts=['Własny bus', 'Wycena po zdjęciach', 'Darmowe oględziny, gdy zdjęcia nie wystarczą'],
        sections=[
            dict(h='Wrocław: każde osiedle', body=[
                'Pracujemy w całym mieście, w kamienicach, blokach i domach. Na przykład:',
                {'ul': ['Stare Miasto, Szczepin, Przedmieście Świdnickie', 'Nadodrze, Ołbin, Plac Grunwaldzki, Biskupin, Sępolno, Zalesie',
                        'Krzyki, Gaj, Borek, Huby, Tarnogaj, Brochów, Jagodno, Ołtaszyn, Partynice, Klecina',
                        'Grabiszyn, Muchobór, Nowy Dwór, Kozanów, Gądów Mały, Popowice, Pilczyce, Leśnica, Maślice',
                        'Psie Pole, Karłowice, Różanka, Zakrzów']},
            ]),
            dict(h='Okolice Wrocławia', body=[
                'Dojeżdżamy do miejscowości wokół Wrocławia, między innymi:',
                {'ul': ['Siechnice, Oława, Jelcz-Laskowice, Czernica', 'Długołęka, Oleśnica, Wisznia Mała, Trzebnica, Oborniki Śląskie',
                        'Brzeg Dolny, Miękinia, Środa Śląska, Kąty Wrocławskie, Smolec', 'Kobierzyce, Żórawina, Sobótka, Strzelin']},
                'Jeśli Twojej miejscowości tu nie ma, a leży do około 70 km od Wrocławia, napisz do nas.',
            ]),
            dict(h='W mieście i pod miastem', body=[
                'We Wrocławiu to zwykle mieszkania w kamienicach i blokach: wysokie piętra, wąskie klatki, nie zawsze winda. Pod Wrocławiem częściej całe domy, razem z garażem, strychem, piwnicą i komórką na podwórku. Piętro, windę i dostęp uwzględniamy w wycenie od razu.',
            ]),
            dict(h='Jak zamówić poza Wrocławiem', body=[
                'Tak samo jak w mieście. Wyślij zdjęcia i dopisz miejscowość. Wstępną cenę podajemy po zdjęciach, ostateczną potwierdzamy na miejscu, zanim zaczniemy. Jeśli zdjęcia nie wystarczą, przyjedziemy obejrzeć miejsce za darmo.',
                'Do ceny dochodzi dopłata za dojazd, liczona od granicy Wrocławia:',
                {'table': [[f'do {km} km', plus(p)] for km, p in ZONES], 'head': ['Odległość od granicy Wrocławia', 'Dopłata']},
            ]),
            dict(h='Co robimy na miejscu', body=[
                Markup('Opróżniamy mieszkania i domy, <a href="../oproznianie-piwnic-strychow-garazy/">piwnice, strychy i garaże</a>, '
                       '<a href="../dla-firm/">biura i lokale</a>, <a href="../oproznianie-mieszkania-po-zmarlym/">mieszkania po bliskich</a>. '
                       'Wywozimy <a href="../wywoz-mebli-wroclaw/">stare meble i AGD</a> i <a href="../wywoz-gratow-wroclaw/">graty</a>, także pojedyncze rzeczy.'),
            ]),
        ],
        faq=[
            ['Opróżniacie domy jednorodzinne pod Wrocławiem?', 'Tak, razem z garażem, strychem i piwnicą.'],
            ['Czy muszę być na miejscu?', 'Nie. Przy wycenie ustalimy, jak przekazać klucze, a po pracy wyślemy zdjęcia.'],
        ],
        related=['oproznianie-piwnic-strychow-garazy', 'wywoz-mebli-wroclaw', 'oproznianie-mieszkania-po-zmarlym', 'dla-firm'],
    ),
    dict(
        slug='jak-pozbyc-sie-starych-mebli-wroclaw', kind='article', updated=UPDATED2, published=UPDATED,
        title='Jak pozbyć się starych mebli we Wrocławiu | Wyniosę',
        desc='Kontener na gabaryty, PSZOK, oddanie albo firma. Jak legalnie pozbyć się starej kanapy, szafy czy lodówki we Wrocławiu i kiedy który sposób ma sens.',
        crumb='Poradnik: stare meble', service_type='',
        plate='', eyebrow='Poradnik',
        h1a='Jak pozbyć się starych mebli', h1b='we Wrocławiu',
        lead='We Wrocławiu stare meble i sprzęt można legalnie oddać na cztery sposoby. Kontener na gabaryty, PSZOK i oddanie komuś, kto rzecz odbierze, są dla mieszkańców bezpłatne. Czwarty sposób to płatny wywóz przez firmę.',
        facts=[],
        sections=[
            dict(h='1. Kontener na gabaryty na osiedlu', body=[
                Markup('Odbiór odpadów wielkogabarytowych od mieszkańców jest w ramach opłaty za śmieci. Według <a href="https://ekosystem.wroc.pl/segregacja-odpadow/odpady-wielkogabarytowe/" target="_blank" rel="noopener">Ekosystemu</a> w zabudowie wielorodzinnej odbywa się co najmniej raz w miesiącu, a w jednorodzinnej co najmniej raz na dwa miesiące. Na osiedlach ustawiane są kontenery, zwykle na kilka dni.'),
                Markup('Terminy i miejsca sprawdzisz w harmonogramie na stronie <a href="https://gabaryty.ekosystem.wroc.pl/" target="_blank" rel="noopener">gabaryty.ekosystem.wroc.pl</a>. Zarządca budynku, spółdzielnia albo wspólnota może też poprosić o dodatkowy kontener.'),
                'W ścisłym centrum, czyli na Starym Mieście, Nadodrzu, Ołbinie, Placu Grunwaldzkim i Przedmieściu Świdnickim, zamiast kontenerów działa zbiórka objazdowa z własnym harmonogramem.',
                'Do gabarytów pasują meble, materace, dywany, rowery i meble ogrodowe. Nie wrzuca się tam gruzu, elektroodpadów (lodówek, pralek, telewizorów), opon ani odpadów niebezpiecznych.',
            ]),
            dict(h='2. PSZOK: zawozisz sam', body=[
                'Do Punktów Selektywnego Zbierania Odpadów Komunalnych mieszkańcy mogą za darmo przywieźć m.in. odpady wielkogabarytowe, elektroodpady, opony, farby i niewielkie ilości gruzu z remontu. Obsługa nie rozładowuje samochodu: transport, wnoszenie i rozładunek są po Twojej stronie.',
                {'ul': ['ul. Kazimierza Michalczyka 9', 'ul. Szwajcarska 15', 'ul. Legnicka 51–53', 'ul. Janowska 51']},
                Markup('Godziny otwarcia zmieniają się sezonowo, a punkty bywają czasowo zamknięte. Przed wyjazdem sprawdź aktualne informacje na <a href="https://ekosystem.wroc.pl/segregacja-odpadow/pszok/" target="_blank" rel="noopener">stronie Ekosystemu</a>.'),
            ]),
            dict(h='3. Oddaj albo sprzedaj', body=[
                'Mebel w dobrym stanie może się komuś przydać. Wystaw go w lokalnym serwisie ogłoszeniowym albo w osiedlowej grupie. Często znajdzie się ktoś, kto przyjedzie i zabierze go sam.',
                'Stara lodówka czy pralka to elektroodpad. Kupując nowy sprzęt, możesz oddać stary tego samego rodzaju w sklepie: sprzedawca ma obowiązek przyjąć go bezpłatnie.',
            ]),
            dict(h='4. Firma: kiedy to ma sens', body=[
                'Firma przydaje się wtedy, gdy rzeczy jest dużo albo samo wyniesienie jest problemem:',
                {'ul': ['opróżniasz całe mieszkanie, piwnicę, strych albo garaż;', 'mieszkasz wysoko, bez windy, a meble trzeba rozkręcić;',
                        'nie masz samochodu, którym zawieziesz rzeczy do PSZOK;', 'goni Cię termin: sprzedaż mieszkania, oddanie kluczy, nowy najemca;',
                        'mieszkanie jest po bliskiej osobie, a rodzina mieszka daleko.']},
                Markup(f'W takich sytuacjach możesz zlecić to nam. Wyniesiemy, rozkręcimy i wywieziemy wszystko, także pojedynczy mebel. Jedną kanapę wywozimy od {zl(F["furniture"])}. Jeśli masz auto, PSZOK (sposób 2) nic nie kosztuje. Szczegóły: <a href="../wywoz-mebli-wroclaw/">wywóz mebli i AGD</a> i <a href="../cennik/">cennik</a>.'),
            ]),
            dict(h='Czego nie robić', body=[
                'Nie zostawiaj mebli przy śmietniku poza terminem odbioru ani w lesie. Wystawianie gabarytów w miejscu, które nie jest do tego przeznaczone, jest niezgodne z przepisami i grozi mandatem.',
            ]),
        ],
        faq=[
            ['Czy odbiór gabarytów we Wrocławiu jest płatny?', 'Dla mieszkańców nie. Odbiór z osiedlowych kontenerów jest w ramach opłaty za śmieci, a PSZOK przyjmuje odpady od mieszkańców bezpłatnie.'],
            ['Gdzie oddać starą lodówkę albo pralkę?', 'To elektroodpad, więc nie do kontenera na gabaryty. Oddaj ją w PSZOK albo w sklepie przy zakupie nowego sprzętu tego samego rodzaju.'],
            ['Co zrobić, gdy kontener na gabaryty jest pełny?', Markup('Według <a href="https://www.wroclaw.pl/zielony-wroclaw/gabaryty-sprawa-wielkiej-wagi-gdzie-kiedy-i-jak-mozemy-je-wyrzucic-zasady" target="_blank" rel="noopener">informacji miasta</a> można to zgłosić firmie podanej na kontenerze albo Ekosystemowi. Rzeczy, które się nie zmieściły, można postawić obok pełnego kontenera.')],
            ['Czy wywieziecie jedną szafę?', f'Tak, od {zl(F["furniture"])}, a szafę do rozkręcenia od {zl(320)}. Bezpłatnie możesz ją oddać do kontenera na gabaryty albo w PSZOK.'],
        ],
        related=['wywoz-mebli-wroclaw', 'oproznianie-piwnic-strychow-garazy', 'oproznianie-mieszkania-po-zmarlym', 'obszar-dzialania'],
    ),
    dict(
        slug='wywoz-gratow-wroclaw', kind='service', updated=UPDATED2,
        title='Wywóz gratów i rzeczy Wrocław, od 190 zł | Wyniosę',
        desc='Wywozimy graty, stare rzeczy i odpady wielkogabarytowe we Wrocławiu i do 70 km, także pojedyncze rzeczy. Znosimy z każdego piętra i wozimy do PSZOK.',
        crumb='Wywóz gratów', service_type='Wywóz gratów i rzeczy',
        plate='', eyebrow='Wrocław i okolice do 70 km',
        h1a='Wywóz gratów i rzeczy', h1b='we Wrocławiu',
        lead='Zabieramy stare meble, kartony, rowery, materace i wszystko inne, co zalega w mieszkaniu, na balkonie albo w piwnicy. Znosimy z każdego piętra, ładujemy do busa i wieziemy do PSZOK albo do recyklingu.',
        facts=['Pojedyncze rzeczy od ' + zl(F['item']), 'Każde piętro', 'Do 70 km od Wrocławia'],
        sections=[
            dict(h='Co zabieramy', body=[
                {'ul': ['Meble: kanapy, szafy, łóżka, stoły, krzesła, fotele.', 'AGD i RTV: lodówki, pralki, kuchenki, telewizory.',
                        'Materace, dywany i wykładziny.', 'Kartony, książki, ubrania, zabawki, słoiki.',
                        'Rowery, wózki, sprzęt sportowy, meble ogrodowe.', 'Opony, deski, drzwi i gruz w workach, po wcześniejszym uzgodnieniu.']},
                'Nie zabieramy azbestu, odpadów medycznych, butli gazowych, gaśnic ani chemii bez etykiet. Azbestu, odpadów medycznych, butli i gaśnic nie przyjmuje też PSZOK.',
            ]),
            dict(h='Jak to działa', body=[
                {'ol': [['Zdjęcia.', 'Wysyłasz zdjęcia na WhatsApp albo dzwonisz. Jeśli zdjęcia nie wystarczą, przyjedziemy obejrzeć za darmo.'],
                        ['Cena i termin.', 'Mówimy, ile to kosztuje i kiedy możemy przyjechać. Cenę potwierdzamy, zanim zaczniemy.'],
                        ['Wynosimy.', 'Znosimy z każdego piętra, rozkręcamy, co trzeba, ładujemy do busa.'],
                        ['Oddajemy.', 'Segregujemy i oddajemy wszystko do PSZOK albo do recyklingu.']]},
            ]),
            dict(h='Ile kosztuje wywóz gratów', body=[
                {'table': [['Pojedyncza rzecz: fotel, materac, szafka, dywan', od(F['item'])], ['Lodówka, pralka, kuchenka', od(F['appliance'])],
                           ['Duży mebel: kanapa, szafa, łóżko', od(F['furniture'])], ['Pokój, ok. 4 m³ rzeczy', od(F['room'])],
                           ['Pół busa, ok. 8 m³', od(1050)], ['Kawalerka', od(F['studio'])]], 'head': ['Co', 'Cena']},
                'To ceny minimalne we Wrocławiu, gdy rzeczy są gotowe do wyniesienia i jest winda albo parter. Dopłaty doliczamy za piętro bez windy, rozkręcanie mebli, pakowanie drobnych rzeczy i dojazd poza Wrocław.',
                CENNIK,
            ]),
            dict(h='Sam do PSZOK czy z nami?', body=[
                'Mieszkańcy Wrocławia oddają odpady w PSZOK bez opłat. Trzeba je tylko samemu wynieść, przewieźć własnym autem i rozładować do właściwych kontenerów, w godzinach otwarcia punktu. Jeśli masz samochód i czas, tak wyjdzie najtaniej.',
                Markup('Jeśli nie, zrobimy to za Ciebie, a rzeczy i tak trafią do PSZOK albo do recyklingu. Adresy, godziny i zasady punktów: <a href="../pszok-wroclaw/">PSZOK we Wrocławiu</a>.'),
                {'cta': 'Wyślij zdjęcia gratów, a podamy cenę.'},
            ]),
        ],
        faq=[
            ['Wywieziecie jedną rzecz?', f'Tak, od {zl(F["item"])}. Pojedyncze rzeczy zabieramy przy okazji innych zleceń w okolicy, termin ustalamy razem. Osobny przyjazd w dniu, który wybierzesz, kosztuje od {zl(F["solo"])}.'],
            ['Czy muszę wszystko spakować?', f'Nie. Drobne rzeczy możemy spakować za Ciebie, za dopłatą {zl(X["pack_m3"])} za m³. Wystarczy, że powiesz, co ma zostać.'],
            ['Zabierzecie gruz po remoncie?', f'Niewielkie ilości w workach, po uzgodnieniu: do 10 worków od {zl(X["rubble_10"])}. Przy więcej niż tonie gruzu taniej wyjdzie kontener.'],
            ['Czy muszę być na miejscu?', 'Nie. Przy wycenie ustalimy, jak przekazać klucze, a po pracy wyślemy zdjęcia pustego miejsca.'],
            ['Jak można zapłacić?', 'Gotówką, BLIK-iem albo przelewem. Wystawiamy fakturę bez VAT.'],
        ],
        related=['cennik', 'wywoz-mebli-wroclaw', 'pszok-wroclaw', 'oproznianie-piwnic-strychow-garazy'],
    ),
    dict(
        slug='cennik', kind='service', updated=UPDATED2,
        title='Cennik wywozu gratów, mebli i AGD Wrocław | Wyniosę',
        desc='Ceny wywozu we Wrocławiu: pojedyncze rzeczy od 190 zł, pokój od 700 zł, kawalerka od 1600 zł. Dopłaty za piętro, demontaż i dojazd. Faktura bez VAT.',
        crumb='Cennik', service_type='Wywóz gratów, mebli i AGD',
        plate='zł', eyebrow='Ceny minimalne, faktura bez VAT',
        h1a='Cennik wywozu', h1b='we Wrocławiu',
        lead='Podajemy ceny minimalne we Wrocławiu, gdy rzeczy są gotowe do wyniesienia i jest winda albo parter. Dokładną cenę podamy po zdjęciach i potwierdzimy przed rozpoczęciem pracy. Możesz zapłacić gotówką, BLIK-iem albo przelewem, wystawiamy fakturę bez VAT.',
        facts=['Faktura bez VAT', 'Gotówka, BLIK, przelew', 'Wycena ze zdjęć za darmo'],
        sections=[
            dict(h='Pojedyncze rzeczy', body=[
                'Pojedyncze rzeczy zabieramy przy okazji innych zleceń w okolicy, termin ustalamy razem. Jeśli zależy Ci na konkretnym dniu, przyjedziemy osobno.',
                {'table': [['Fotel, materac, szafka, dywan', od(F['item'])], ['Lodówka, pralka, kuchenka', od(F['appliance'])],
                           ['Kanapa, łóżko, szafa w całości, stół', od(F['furniture'])], ['Szafa do rozkręcenia', od(320)],
                           ['Meblościanka lub narożnik do rozkręcenia', od(460)], ['Każda kolejna rzecz z tego samego adresu', plus(X['next_item'])],
                           ['Osobny przyjazd w dniu, który wybierzesz', od(F['solo'])]], 'head': ['Co', 'Cena']},
            ]),
            dict(h='Większe ilości', body=[
                'Przy większej ilości liczymy, ile miejsca rzeczy zajmą w naszym busie. Bus ma około 16 m³ i zabiera do 1,2 tony, więc ciężkie rzeczy, na przykład książki, mogą wymagać drugiego kursu.',
                {'table': [[name, od(p)] for name, p in VAN] + [['Drugi kurs, gdy rzeczy nie zmieszczą się za pierwszym razem', plus(X['second_trip'])]], 'head': ['Ilość', 'Cena']},
            ]),
            dict(h='Mieszkania, domy, piwnice', body=[
                'Orientacyjne ceny za typową ilość rzeczy. Dokładną cenę policzymy po zdjęciach.',
                {'table': [['Pokój', od(F['room'])], ['Piwnica lub komórka lokatorska', od(F['cellar'])], ['Garaż lub strych', od(F['garage'])],
                           ['Kawalerka', od(F['studio'])], ['Mieszkanie dwupokojowe', od(F['flat'])], ['Mieszkanie trzypokojowe', od(F['flat3'])],
                           ['Dom', od(F['house'])], ['Biuro lub lokal, pół busa', od(F['office'])]], 'head': ['Co', 'Cena']},
                'Biura i lokale są droższe, bo odpadów z działalności firm PSZOK nie przyjmuje. Oddajemy je do uprawnionego punktu odbioru, a ten koszt jest w cenie.',
            ]),
            dict(h='Dopłaty', body=[
                {'table': [['Piętro bez windy, pojedyncza rzecz', plus(X['floor_item']) + ' za piętro']] + [[f'Piętro bez windy, {n}', plus(p) + ' za piętro'] for n, p in FLOOR_VAN] +
                          [['Rozkręcenie dużego mebla', plus(X['dismantle']) + ' za sztukę'], ['Pakowanie drobnych rzeczy przez nas', plus(X['pack_m3']) + ' za m³'],
                           ['Wieczór, niedziela albo święto', '+' + str(X['evening_pct']) + '%']], 'head': ['Za co', 'Dopłata']},
            ]),
            dict(h='Dojazd poza Wrocław', body=[
                'Pracujemy do około 70 km od Wrocławia. Dopłatę liczymy od granicy miasta.',
                {'table': [[f'do {km} km', plus(p)] for km, p in ZONES], 'head': ['Odległość od granicy Wrocławia', 'Dopłata']},
            ]),
            dict(h='Gruz i praca na godziny', body=[
                {'table': [['Gruz w workach do 25 kg, do 10 worków', od(X['rubble_10'])], ['Każdy kolejny worek', plus(X['rubble_bag'])],
                           ['Ekipa dwóch osób z busem, pierwsza godzina', zl(X['hour_first'])], ['Każda kolejna godzina', zl(X['hour_next'])]], 'head': ['Co', 'Cena']},
                'Przy więcej niż tonie gruzu taniej wyjdzie kontener. Godzinowo liczymy prace, w których trudno z góry ocenić ilość rzeczy.',
            ]),
            dict(h='Od czego zależy cena', body=[
                {'ul': ['Ile rzeczy jest do wyniesienia.', 'Piętro i to, czy jest winda.', 'Czy meble trzeba rozkręcić.',
                        'Jak daleko jest od drzwi do busa.', 'Czy to rzeczy z mieszkania, czy z firmy.']},
                'Wstępną cenę podajemy po zdjęciach, ostateczną potwierdzamy na miejscu, zanim zaczniemy. Wycena jest za darmo.',
                {'cta': 'Wyślij zdjęcia, a podamy cenę.'},
            ]),
        ],
        faq=[
            ['Czy wycena jest płatna?', 'Nie. Wycena po zdjęciach i oględziny na miejscu są za darmo.'],
            ['Kiedy poznam ostateczną cenę?', 'Na miejscu, zanim zaczniemy pracę. Im dokładniejsze zdjęcia i opis, tym dokładniejsza wycena wstępna.'],
            ['Wystawiacie fakturę?', 'Tak, fakturę bez VAT.'],
            ['Dlaczego dla firm drożej?', 'Odpadów z działalności firm PSZOK nie przyjmuje, więc oddajemy je do uprawnionego punktu odbioru. Ten koszt jest w cenie.'],
        ],
        related=['wywoz-gratow-wroclaw', 'wywoz-mebli-wroclaw', 'oproznianie-mieszkan-wroclaw', 'obszar-dzialania'],
    ),
    dict(
        slug='oproznianie-mieszkan-wroclaw', kind='service', updated=UPDATED2,
        title='Opróżnianie mieszkań Wrocław, kawalerka od 1600 zł | Wyniosę',
        desc='Opróżniamy mieszkania i domy we Wrocławiu i do 70 km: rozkręcamy meble, znosimy z każdego piętra, wozimy do PSZOK. Kawalerka od 1600 zł, wycena za darmo.',
        crumb='Opróżnianie mieszkań', service_type='Opróżnianie mieszkań i domów',
        plate='IV', eyebrow='Mieszkania i domy, Wrocław i okolice',
        h1a='Opróżnianie mieszkań', h1b='we Wrocławiu',
        lead='Opróżniamy całe mieszkania albo wybrane pokoje, razem z piwnicą i komórką lokatorską. Rozkręcamy meble, znosimy wszystko z każdego piętra i wywozimy do PSZOK albo do recyklingu.',
        facts=['Kawalerka od ' + zl(F['studio']), 'Rozkręcamy meble', 'Każde piętro', 'Nie musisz być na miejscu'],
        sections=[
            dict(h='Kiedy opróżnia się mieszkanie', body=[
                {'ul': ['Przed sprzedażą albo wynajmem.', 'Po najemcach, którzy zostawili meble i rzeczy.', 'Przed remontem.',
                        'Przy przeprowadzce, gdy stare meble nie jadą z Tobą.']},
                Markup('Jeśli to mieszkanie po bliskiej osobie, dokumenty i pamiątki odkładamy dla rodziny. Więcej: <a href="../oproznianie-mieszkania-po-zmarlym/">mieszkania po bliskich</a>.'),
            ]),
            dict(h='Jak pracujemy', body=[
                {'ol': [['Wycena.', 'Po zdjęciach na WhatsApp albo po darmowych oględzinach, jeśli zdjęcia nie wystarczą.'],
                        ['Ustalenia.', 'Mówisz, co zostaje, a co wynosimy. Ustalamy cenę, termin i klucze.'],
                        ['Opróżnienie.', 'Rozkręcamy meble, znosimy z każdego piętra, ładujemy do busa.'],
                        ['Wywóz.', 'Segregujemy i oddajemy wszystko do PSZOK lub do recyklingu.']]},
                'Sprzątanie po opróżnieniu robimy na życzenie, jako usługę dodatkową.',
            ]),
            dict(h='Ile kosztuje opróżnienie mieszkania', body=[
                {'table': [['Pokój', od(F['room'])], ['Kawalerka', od(F['studio'])], ['Mieszkanie dwupokojowe', od(F['flat'])],
                           ['Mieszkanie trzypokojowe', od(F['flat3'])], ['Dom', od(F['house'])], ['Piwnica lub komórka', od(F['cellar'])]], 'head': ['Co', 'Cena']},
                'To ceny minimalne dla typowej ilości rzeczy, z windą albo na parterze. Dopłaty doliczamy za piętro bez windy, demontaż, pakowanie drobnych rzeczy i dojazd poza Wrocław.',
                CENNIK,
            ]),
            dict(h='Dlaczego czasem dwa kursy', body=[
                'Nasz bus zabiera do 1,2 tony. W mieszkaniu dwupokojowym meble, książki i naczynia ważą zwykle więcej, więc jedziemy dwa razy. W cenach od dla mieszkań drugi kurs jest już uwzględniony.',
            ]),
            dict(h='Gdy nie możesz być na miejscu', body=[
                'Nie musisz przyjeżdżać. Sposób przekazania kluczy ustalimy przy wycenie, kontakt prowadzimy przez WhatsApp albo telefon, a po pracy wysyłamy zdjęcia pustego mieszkania. Rozmawiamy po polsku, ukraińsku, rosyjsku i angielsku.',
                {'cta': 'Wyślij zdjęcia mieszkania, a podamy cenę.'},
            ]),
        ],
        faq=[
            ['Czy opróżnicie tylko część mieszkania?', 'Tak. Wskaż, co zostaje, a co wynosimy. Wyniesiemy nawet pojedyncze rzeczy.'],
            ['Co z rzeczami, które chcę zachować?', 'Wskaż je przed pracą, zostawimy je na miejscu.'],
            ['Zabierzecie też rzeczy z piwnicy i komórki?', 'Tak, mogą być częścią tego samego zlecenia.'],
            ['Posprzątacie po opróżnieniu?', 'Tak, na życzenie, jako usługę dodatkową.'],
            ['Wystawiacie fakturę?', 'Tak, fakturę bez VAT. Płacisz gotówką, BLIK-iem albo przelewem.'],
        ],
        related=['oproznianie-mieszkania-po-zmarlym', 'cennik', 'oproznianie-piwnic-strychow-garazy', 'wywoz-mebli-wroclaw'],
    ),
    dict(
        slug='pszok-wroclaw', kind='article', updated=UPDATED2, published=UPDATED2,
        title='PSZOK Wrocław: adresy, godziny i co przyjmuje | Wyniosę',
        desc='PSZOK we Wrocławiu: adresy punktów, godziny, co można oddać za darmo i czego nie. A gdy nie masz auta albo siły, wywieziemy rzeczy za Ciebie, od 190 zł.',
        crumb='PSZOK we Wrocławiu', service_type='',
        plate='', eyebrow='Poradnik, stan na 30.10.2026',
        h1a='PSZOK we Wrocławiu', h1b='adresy, godziny, zasady',
        lead='PSZOK, czyli Punkt Selektywnego Zbierania Odpadów Komunalnych, przyjmuje od mieszkańców Wrocławia odpady bez opłat. Trzeba je tylko samemu przywieźć i rozładować.',
        facts=[],
        sections=[
            dict(h='Adresy i godziny', body=[
                {'ul': ['ul. Kazimierza Michalczyka 9 (Szczepin): poniedziałek–piątek 8:00–19:00, sobota 8:00–16:00.',
                        'ul. Szwajcarska 15 (Muchobór Mały): poniedziałek–piątek 8:00–19:00, sobota 8:00–16:00.',
                        'ul. Legnicka 51–53: poniedziałek–piątek 7:30–15:30.', 'ul. Janowska 51: czasowo zamknięty.']},
                Markup('Godziny podajemy według strony Ekosystemu z 29.10.2026. Zimą punkty bywają czynne krócej, w niedziele i święta są zamknięte. Przed wyjazdem sprawdź <a href="https://ekosystem.wroc.pl/segregacja-odpadow/pszok/" target="_blank" rel="noopener">aktualne informacje Ekosystemu</a>.'),
            ]),
            dict(h='Co można oddać', body=[
                {'ul': ['Meble i inne odpady wielkogabarytowe.', 'Elektroodpady: lodówki, pralki, telewizory i drobny sprzęt.',
                        'Opony od samochodów osobowych.', 'Farby, kleje, oleje, baterie i akumulatory.',
                        'Przeterminowane leki, termometry rtęciowe, świetlówki.', 'Drewno, metal, plastik, papier i tekstylia.',
                        'Odpady zielone.', 'Niewielkie ilości gruzu z remontu.']},
            ]),
            dict(h='Czego PSZOK nie przyjmuje', body=[
                {'ul': ['Odpadów z działalności firm, na przykład z biura albo warsztatu.', 'Azbestu.', 'Odpadów medycznych i weterynaryjnych.',
                        'Gaśnic i butli gazowych.', 'Części samochodowych, na przykład zderzaków i silników.', 'Odpadów w ilościach hurtowych.']},
            ]),
            dict(h='Zasady na miejscu', body=[
                {'ul': ['Odpady muszą pochodzić z gospodarstwa domowego.', 'Obsługa nie rozładowuje auta, tylko wskazuje właściwy kontener.',
                        'Gruz i odpady zielone trzeba wysypać z worków, a worki wrzucić do osobnego kontenera.',
                        'Przed wyjazdem warto sprawdzić, czy potrzebny kontener jest dostępny.']},
            ]),
            dict(h='Gdy PSZOK nie wystarczy', body=[
                'Do PSZOK trzeba dojechać własnym autem i samemu wszystko rozładować. Jeśli mieszkasz wysoko bez windy, nie masz samochodu albo rzeczy jest dużo, możesz zlecić to nam. Wyniesiemy rzeczy, w razie potrzeby rozkręcimy meble i sami zawieziemy wszystko do PSZOK albo do recyklingu.',
                {'table': [['Pojedyncza rzecz', od(F['item'])], ['Kanapa, szafa, łóżko', od(F['furniture'])], ['Lodówka, pralka', od(F['appliance'])],
                           ['Pokój', od(F['room'])], ['Piwnica lub komórka', od(F['cellar'])]], 'head': ['Co', 'Cena']},
                CENNIK, {'cta': 'Nie masz jak dowieźć rzeczy do PSZOK? Napisz albo zadzwoń.'},
            ]),
        ],
        faq=[
            ['Czy PSZOK we Wrocławiu jest płatny?', 'Dla mieszkańców Wrocławia nie. Odpady z gospodarstw domowych przyjmuje bez opłat.'],
            ['Czy w PSZOK pomogą rozładować auto?', 'Nie. Obsługa wskazuje kontener, a rozładunek jest po Twojej stronie.'],
            ['Czy przyjmą odpady z biura albo warsztatu?', 'Nie. PSZOK przyjmuje tylko odpady komunalne z gospodarstw domowych.'],
            ['Co zrobić z jedną kanapą, jeśli nie mam auta?', Markup(f'Możesz wystawić ją do osiedlowego kontenera na gabaryty w terminie z <a href="https://gabaryty.ekosystem.wroc.pl/" target="_blank" rel="noopener">harmonogramu Ekosystemu</a> albo poprosić kogoś z autem o zawiezienie jej do PSZOK. Możemy też ją wynieść i wywieźć, od {zl(F["furniture"])}.')],
        ],
        related=['wywoz-gratow-wroclaw', 'cennik', 'jak-pozbyc-sie-starych-mebli-wroclaw', 'wywoz-mebli-wroclaw'],
    ),
]

BY_SLUG = {p['slug']: p for p in PAGES}

# Short labels for links between pages, the footer and the home page cards
LINK_LABEL = {
    'oproznianie-piwnic-strychow-garazy': 'Piwnice, strychy i garaże',
    'oproznianie-mieszkania-po-zmarlym': 'Mieszkania po bliskich',
    'wywoz-mebli-wroclaw': 'Wywóz mebli i AGD',
    'dla-firm': 'Dla firm i zarządców',
    'obszar-dzialania': 'Obszar działania',
    'jak-pozbyc-sie-starych-mebli-wroclaw': 'Poradnik: stare meble',
    'wywoz-gratow-wroclaw': 'Wywóz gratów',
    'cennik': 'Cennik',
    'oproznianie-mieszkan-wroclaw': 'Opróżnianie mieszkań',
    'pszok-wroclaw': 'PSZOK we Wrocławiu',
}
