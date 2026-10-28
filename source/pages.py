# -*- coding: utf-8 -*-
"""Polish service and guide pages (wyniose.pl/<slug>/). Built by build.py with src/subpage.html.j2.

Rules for this copy (see CLAUDE.md): only facts the owner confirmed on the home page, no prices, no reviews,
no speed promises, no copied competitor text, no keyword stuffing. Each page answers one real question.
Paragraphs are plain strings (escaped) or Markup when they carry a link written here by hand.
Blocks: str / Markup = paragraph, {'ul': [...]}, {'ol': [[title, text], ...]}, {'note': ...}."""
from markupsafe import Markup

UPDATED = '2026-10-28'

PHOTOS = {'ul': ['Całe pomieszczenie, z progu.', 'Duże rzeczy z bliska.', 'Klatkę, korytarz lub schody, jeśli są wąskie.',
                 'Im więcej zdjęć, tym dokładniejsza wycena.']}

PAGES = [
    dict(
        slug='oproznianie-piwnic-strychow-garazy', kind='service', updated=UPDATED,
        title='Opróżnianie piwnic, strychów i garaży Wrocław | Wyniosę',
        desc='Opróżniamy piwnice, komórki lokatorskie, strychy i garaże we Wrocławiu i do 70 km. Wynosimy, rozkręcamy, wywozimy. Wycena po zdjęciach za darmo.',
        crumb='Piwnice, strychy i garaże', service_type='Opróżnianie piwnic, strychów i garaży',
        plate='−1', eyebrow='Piwnice · komórki · strychy · garaże',
        h1a='Opróżnianie piwnic, strychów i garaży', h1b='we Wrocławiu',
        lead='Wąskie schody, słabe światło i rzeczy sprzed lat. Wynosimy wszystko z piwnicy, komórki, strychu albo garażu, ładujemy do naszego busa i wywozimy. Zostaje puste miejsce.',
        facts=['Własny bus', 'Rozkręcamy meble', 'Do 70 km od Wrocławia', 'PL · UA · RU · EN'],
        sections=[
            dict(h='Co najczęściej wynosimy', body=[
                {'ul': ['Stare meble, regały, szafki i półki.', 'Rowery, wózki, sanki, narty.',
                        'Kartony, słoiki, książki i stare gazety.', 'Stare AGD: pralki, lodówki i inne duże sprzęty.',
                        'Narzędzia, deski, meble ogrodowe, dywany i materace.']},
                'Farby, chemię, gruz i opony bierzemy tylko po wcześniejszym uzgodnieniu. Azbestu i odpadów medycznych nie zabieramy.',
            ]),
            dict(h='Piwnica w kamienicy, w bloku albo pod domem', body=[
                'W kamienicach piwnice mają często niskie stropy i ciasne przejścia. W blokach dochodzą długie korytarze komórek i drzwi, przez które szafa nie przejdzie w całości. Dlatego meble rozkręcamy na miejscu, a przy dużych rzeczach w razie potrzeby zabezpieczamy narożniki i poręcze.',
                'Nie musisz niczego wcześniej pakować ani wynosić. Wystarczy, że powiesz, co ma zostać.',
            ]),
            dict(h='Strych i garaż', body=[
                'Na strychu trudne jest zwykle zejście: strome schody, właz, wąski korytarz. W garażu problemem jest ilość, bo przez lata trafia tam wszystko, co nie zmieściło się w mieszkaniu. W obu przypadkach pracujemy tak samo: wynosimy, ładujemy do busa, segregujemy i oddajemy do PSZOK lub do recyklingu.',
            ]),
            dict(h='Ile kosztuje opróżnienie piwnicy?', body=[
                'Nie mamy cennika z góry. Dwie piwnice o tej samej powierzchni mogą się bardzo różnić ilością rzeczy. Na cenę wpływa to, ile jest do wyniesienia, czy trzeba rozkręcać meble, jak daleko jest do busa i jakie są schody.',
                'Wstępną cenę podajemy po zdjęciach. Ostateczną potwierdzamy na miejscu, zanim zaczniemy. Jakie zdjęcia wysłać:',
                PHOTOS,
            ]),
            dict(h='Minimalne zlecenie', body=[
                'Przyjeżdżamy, gdy rzeczy jest mniej więcej pół pokoju. Jeśli nie wiesz, czy Twoja piwnica albo komórka się kwalifikuje, wyślij zdjęcia. Powiemy wprost.',
            ]),
        ],
        faq=[
            ['Czy muszę być na miejscu?', 'Nie. Dostęp i klucze ustalamy przy wycenie, a po robocie wysyłamy zdjęcia pustego miejsca.'],
            ['Piwnica jest w kamienicy bez windy. To problem?', 'Nie. Schodzimy i wchodzimy po każdych schodach. Piętro i dostęp uwzględniamy w wycenie od razu.'],
            ['Czy przy okazji opróżnicie też mieszkanie?', 'Tak. Piwnica, strych, garaż i mieszkanie mogą być jednym zleceniem. Napisz to w wiadomości.'],
            ['Posprzątacie po opróżnieniu?', 'Tak, na życzenie, jako usługę dodatkową.'],
            ['Przyjedziecie obejrzeć przed wyceną?', 'Tak, za darmo, jeśli zdjęcia nie wystarczą.'],
        ],
        related=['wywoz-mebli-wroclaw', 'oproznianie-mieszkania-po-zmarlym', 'dla-firm', 'obszar-dzialania'],
    ),
    dict(
        slug='oproznianie-mieszkania-po-zmarlym', kind='service', updated=UPDATED,
        title='Opróżnianie mieszkania po zmarłym Wrocław | Wyniosę',
        desc='Opróżniamy mieszkania po bliskich we Wrocławiu i okolicach. Bez pośpiechu i z szacunkiem. Dokumenty i pamiątki odkładamy dla rodziny. Nie musisz być na miejscu.',
        crumb='Mieszkania po bliskich', service_type='Opróżnianie mieszkania po zmarłym',
        plate='', eyebrow='Mieszkania po bliskich',
        h1a='Opróżnianie mieszkania po bliskiej osobie', h1b='we Wrocławiu',
        lead='Opróżnienie mieszkania po kimś bliskim to coś więcej niż wywóz mebli. Pracujemy bez pośpiechu, dokumenty i pamiątki odkładamy dla rodziny, a resztę wynosimy i wywozimy. Możesz nam to zlecić także wtedy, gdy mieszkasz daleko od Wrocławia.',
        facts=['Nie musisz być na miejscu', 'Dokumenty i pamiątki odkładamy', 'Zdjęcia po robocie', 'PL · UA · RU · EN'],
        sections=[
            dict(h='Jak to wygląda krok po kroku', body=[
                {'ol': [['Zdjęcia albo oględziny.', 'Piszesz lub dzwonisz. Zdjęcia może wysłać ktokolwiek, kto ma dostęp do mieszkania. Jeśli zdjęcia nie wystarczą, przyjedziemy obejrzeć mieszkanie za darmo.'],
                        ['Ustalenia.', 'Mówisz, co ma zostać: konkretne meble, jeden pokój, rzeczy dla rodziny. Ustalamy cenę, termin i sposób przekazania kluczy.'],
                        ['Opróżnienie.', 'Pakujemy, rozkręcamy, znosimy i ładujemy do naszego busa. Dokumenty, zdjęcia, listy i pamiątki, które znajdziemy, odkładamy osobno.'],
                        ['Zdjęcia po robocie.', 'Wysyłamy zdjęcia pustego mieszkania. Rzeczy odłożone dla rodziny zostawiamy tam, gdzie się umówimy.']]},
            ]),
            dict(h='Co odkładamy dla rodziny', body=[
                'Dokumenty, zdjęcia, listy i pamiątki, które znajdziemy podczas pracy, odkładamy osobno, zamiast wyrzucać.',
                'Mimo to radzimy, żeby przed naszym przyjazdem rodzina zabrała to, o czym wie i co jest dla niej ważne: biżuterię, gotówkę, ważne dokumenty, telefony i komputery z danymi. Łatwiej zabrać coś wcześniej, niż później szukać.',
            ]),
            dict(h='Gdy rodzina mieszka daleko', body=[
                'Często mieszkanie we Wrocławiu zostaje po kimś, a najbliżsi mieszkają w innym mieście albo za granicą. Nie musisz przyjeżdżać. Klucze ustalamy przy wycenie, kontakt prowadzimy przez WhatsApp albo telefon, a po robocie wysyłamy zdjęcia pustego mieszkania.',
                'Rozmawiamy po polsku, ukraińsku, rosyjsku i angielsku. Pisz w języku, w którym Ci wygodnie.',
            ]),
            dict(h='Przed sprzedażą, oddaniem kluczy albo remontem', body=[
                'Mieszkanie trzeba zwykle opróżnić przed sprzedażą, przed oddaniem lokalu właścicielowi lub zarządcy albo przed remontem. Opróżniamy całe mieszkanie albo tylko wskazane pokoje, razem z piwnicą i komórką. Sprzątanie po opróżnieniu robimy na życzenie, jako usługę dodatkową.',
                {'note': 'Warto pamiętać: zanim zlecisz opróżnienie, upewnij się, że możesz dysponować mieszkaniem i rzeczami, na przykład jako spadkobierca albo w porozumieniu z pozostałymi spadkobiercami lub zarządcą.'},
            ]),
            dict(h='Ile to kosztuje', body=[
                'Cena zależy od ilości rzeczy, piętra, windy i tego, czy trzeba rozkręcać meble. Wstępną cenę podajemy po zdjęciach, ostateczną potwierdzamy na miejscu, zanim zaczniemy. Wycena jest za darmo.',
                'Płacisz gotówką, BLIK-iem albo przelewem. Wystawiamy fakturę bez VAT.',
            ]),
        ],
        faq=[
            ['Czy ktoś z rodziny musi być na miejscu?', 'Nie. Klucze ustalamy przy wycenie, a po robocie wysyłamy zdjęcia pustego mieszkania.'],
            ['Czy możecie opróżnić tylko część mieszkania?', 'Tak. Wskaż, co zostaje, a co wynosimy. Minimum to mniej więcej pół pokoju rzeczy.'],
            ['Co się dzieje z meblami i rzeczami?', 'Segregujemy je i oddajemy do PSZOK lub do recyklingu. Nic nie zostaje pod śmietnikiem.'],
            ['Zabierzecie też rzeczy z piwnicy i komórki?', 'Tak, mogą być częścią tego samego zlecenia.'],
            ['Przyjedziecie obejrzeć mieszkanie przed wyceną?', 'Tak, za darmo, jeśli zdjęcia nie wystarczą.'],
        ],
        related=['oproznianie-piwnic-strychow-garazy', 'wywoz-mebli-wroclaw', 'obszar-dzialania', 'jak-pozbyc-sie-starych-mebli-wroclaw'],
    ),
    dict(
        slug='wywoz-mebli-wroclaw', kind='service', updated=UPDATED,
        title='Wywóz starych mebli i AGD Wrocław | Wyniosę',
        desc='Wynosimy i wywozimy stare meble i AGD we Wrocławiu: szafy, meblościanki, wersalki, pralki, lodówki. Rozkręcamy, znosimy z każdego piętra. Od pół pokoju rzeczy.',
        crumb='Wywóz mebli i AGD', service_type='Wywóz starych mebli i AGD',
        plate='IV', eyebrow='Meble i AGD · z każdego piętra',
        h1a='Wywóz starych mebli', h1b='i AGD we Wrocławiu',
        lead='Szafa, której nikt nie zniesie z czwartego piętra. Meblościanka, która nie przejdzie przez drzwi. Rozkręcamy, znosimy, ładujemy do busa i wywozimy, razem z resztą rzeczy z mieszkania, piwnicy albo biura.',
        facts=['Własny bus', 'Rozkręcamy meble', 'Każde piętro, także bez windy', 'Do 70 km od Wrocławia'],
        sections=[
            dict(h='Co wywozimy', body=[
                {'ul': ['Szafy, meblościanki, komody, regały.', 'Wersalki, kanapy, fotele, łóżka i materace.',
                        'Stoły, krzesła, biurka.', 'Pralki, lodówki i inne duże AGD.', 'Dywany, kartony i drobne wyposażenie.']},
            ]),
            dict(h='Rozkręcamy i znosimy', body=[
                'Co nie przejdzie przez drzwi albo zakręt klatki, rozkręcamy na miejscu. Schodzimy z każdego piętra, także bez windy. Piętro i brak windy uwzględniamy w wycenie od razu. Przy dużych meblach w razie potrzeby zabezpieczamy narożniki i poręcze.',
            ]),
            dict(h='Od jakiej ilości przyjeżdżamy', body=[
                'Meble wywozimy przy opróżnianiu: od mniej więcej pół pokoju rzeczy w górę. Pojedynczego mebla, na przykład jednej kanapy albo jednej szafy, nie wywozimy.',
                Markup('Przy jednej kanapie najtaniej skorzystać z miejskiego odbioru gabarytów albo z PSZOK. Jak to zrobić we Wrocławiu, opisaliśmy w poradniku <a href="../jak-pozbyc-sie-starych-mebli-wroclaw/">Jak pozbyć się starych mebli we Wrocławiu</a>.'),
            ]),
            dict(h='Dokąd trafiają meble', body=[
                'Nie pod wiatę i nie do lasu. Meble, elektroodpady, papier i resztę segregujemy, a potem oddajemy do PSZOK lub do recyklingu. Za gabaryty zostawione przy śmietniku grozi mandat. U nas to nie Twój problem.',
            ]),
            dict(h='Ile kosztuje wywóz mebli', body=[
                'Cena zależy od ilości mebli i rzeczy, piętra, windy i demontażu. Nie mamy cennika z góry: wstępną cenę podajemy po zdjęciach, ostateczną potwierdzamy na miejscu, zanim zaczniemy. Wycena jest za darmo. Jakie zdjęcia wysłać:',
                PHOTOS,
            ]),
        ],
        faq=[
            ['Wywieziecie jedną kanapę?', 'Nie, pojedynczych mebli nie wywozimy. Minimum to mniej więcej pół pokoju rzeczy. Jedną kanapę najtaniej oddać w miejskim odbiorze gabarytów albo w PSZOK.'],
            ['Rozkręcacie meble na miejscu?', 'Tak, jeśli nie przechodzą przez drzwi albo klatkę.'],
            ['Zabieracie lodówki i pralki?', 'Tak. Duże AGD wynosimy i oddajemy osobno, jako elektroodpady.'],
            ['Czy muszę być na miejscu?', 'Nie. Klucze ustalamy przy wycenie, a po robocie wysyłamy zdjęcia pustego miejsca.'],
            ['Wystawiacie fakturę?', 'Tak, fakturę bez VAT. Płacisz gotówką, BLIK-iem albo przelewem.'],
        ],
        related=['jak-pozbyc-sie-starych-mebli-wroclaw', 'oproznianie-piwnic-strychow-garazy', 'oproznianie-mieszkania-po-zmarlym', 'dla-firm'],
    ),
    dict(
        slug='dla-firm', kind='service', updated=UPDATED,
        title='Opróżnianie biur i lokali Wrocław, dla firm | Wyniosę',
        desc='Opróżniamy biura, lokale usługowe i mieszkania na wynajem we Wrocławiu i do 70 km. Dla właścicieli, zarządców i wspólnot. Jedna wycena, faktura bez VAT.',
        crumb='Dla firm i zarządców', service_type='Opróżnianie biur i lokali',
        plate='', eyebrow='Dla firm i zarządców',
        h1a='Opróżnianie biur i lokali', h1b='we Wrocławiu',
        lead='Biuro po przeprowadzce, lokal po najemcy, mieszkanie na wynajem między lokatorami. Wynosimy meble i wyposażenie, wywozimy i zostawiamy pusty lokal. Jedna wycena, jeden termin, faktura bez VAT.',
        facts=['Faktura bez VAT', 'Kilka lokali, jedna wycena', 'Zdjęcia po robocie', 'Do 70 km od Wrocławia'],
        sections=[
            dict(h='Dla kogo pracujemy', body=[
                {'ol': [['Biura.', 'Biurka, krzesła, regały, szafy na dokumenty. Jedna wycena za cały lokal.'],
                        ['Lokale usługowe.', 'Wyposażenie po zakończonej działalności albo przed nowym najemcą.'],
                        ['Właściciele mieszkań na wynajem.', 'Rzeczy zostawione przez najemców i stare meble przed remontem.'],
                        ['Zarządcy nieruchomości i wspólnoty.', 'Kilka lokali, piwnic albo komórek naraz, w jednym zleceniu.']]},
            ]),
            dict(h='Kilka lokali, jedno zlecenie', body=[
                'Jeśli lokali jest kilka, wpisz w wiadomości wszystkie adresy. Wycenimy wszystko razem i ustalimy termin, który pasuje do Twojego harmonogramu.',
            ]),
            dict(h='Bez Twojej obecności', body=[
                'Nie musisz przyjeżdżać na miejsce. Dostęp i klucze ustalamy przy wycenie, a po robocie wysyłamy zdjęcia pustego lokalu. Możesz je od razu przekazać właścicielowi, najemcy albo zarządowi.',
            ]),
            dict(h='Rozliczenie', body=[
                'Cenę uzgadniamy przed rozpoczęciem pracy: wstępną po zdjęciach, ostateczną na miejscu, zanim zaczniemy. Wystawiamy fakturę bez VAT. Płatność przelewem, BLIK-iem albo gotówką.',
            ]),
            dict(h='Czego nie zabieramy', body=[
                'Azbestu i odpadów medycznych. Farby, chemię, gruz i opony bierzemy tylko po wcześniejszym uzgodnieniu.',
            ]),
        ],
        faq=[
            ['Wystawiacie fakturę?', 'Tak, fakturę bez VAT.'],
            ['Możecie opróżnić kilka lokali naraz?', 'Tak. Dopisz adresy w wiadomości, wycenimy wszystko razem.'],
            ['Przyjedziecie obejrzeć lokal?', 'Tak, za darmo, jeśli zdjęcia nie wystarczą.'],
            ['Pracujecie poza Wrocławiem?', 'Tak, do około 70 km od miasta.'],
            ['Czy ktoś musi nas wpuścić?', 'Nie zawsze. Dostęp i klucze ustalamy przy wycenie.'],
        ],
        related=['oproznianie-piwnic-strychow-garazy', 'wywoz-mebli-wroclaw', 'obszar-dzialania', 'oproznianie-mieszkania-po-zmarlym'],
    ),
    dict(
        slug='obszar-dzialania', kind='area', updated=UPDATED,
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
            ]),
            dict(h='Co robimy na miejscu', body=[
                Markup('Opróżniamy mieszkania i domy, <a href="../oproznianie-piwnic-strychow-garazy/">piwnice, strychy i garaże</a>, '
                       '<a href="../dla-firm/">biura i lokale</a>, <a href="../oproznianie-mieszkania-po-zmarlym/">mieszkania po bliskich</a>. '
                       'Wywozimy <a href="../wywoz-mebli-wroclaw/">stare meble i AGD</a>. Minimum to mniej więcej pół pokoju rzeczy.'),
            ]),
        ],
        faq=[
            ['Opróżniacie domy jednorodzinne pod Wrocławiem?', 'Tak, razem z garażem, strychem i piwnicą.'],
            ['Czy muszę być na miejscu?', 'Nie. Klucze ustalamy przy wycenie, a po robocie wysyłamy zdjęcia.'],
        ],
        related=['oproznianie-piwnic-strychow-garazy', 'wywoz-mebli-wroclaw', 'oproznianie-mieszkania-po-zmarlym', 'dla-firm'],
    ),
    dict(
        slug='jak-pozbyc-sie-starych-mebli-wroclaw', kind='article', updated=UPDATED, published=UPDATED,
        title='Jak pozbyć się starych mebli we Wrocławiu | Wyniosę',
        desc='Kontener na gabaryty, PSZOK, oddanie albo firma. Jak legalnie pozbyć się starej kanapy, szafy czy lodówki we Wrocławiu i kiedy który sposób ma sens.',
        crumb='Poradnik: stare meble', service_type='',
        plate='', eyebrow='Poradnik',
        h1a='Jak pozbyć się starych mebli', h1b='we Wrocławiu',
        lead='Stara kanapa, szafa po babci, lodówka, która już nie chłodzi. We Wrocławiu są cztery legalne sposoby, żeby się ich pozbyć. Trzy z nich są dla mieszkańców darmowe.',
        facts=[],
        sections=[
            dict(h='1. Kontener na gabaryty na osiedlu', body=[
                'Odbiór odpadów wielkogabarytowych od mieszkańców jest w ramach opłaty za śmieci. Według Ekosystemu w zabudowie wielorodzinnej odbywa się co najmniej raz w miesiącu, a w jednorodzinnej co najmniej raz na dwa miesiące. Na osiedlach ustawiane są kontenery, zwykle na kilka dni.',
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
                Markup('Wtedy wynosimy, rozkręcamy, ładujemy i wywozimy, od mniej więcej pół pokoju rzeczy w górę. Pojedynczego mebla nie wywozimy, więc przy jednej kanapie lepiej skorzystać ze sposobu 1 albo 2. Więcej: <a href="../wywoz-mebli-wroclaw/">wywóz mebli i AGD</a>.'),
            ]),
            dict(h='Czego nie robić', body=[
                'Nie zostawiaj mebli przy śmietniku poza terminem odbioru ani w lesie. Wystawianie gabarytów w miejscu, które nie jest do tego przeznaczone, jest niezgodne z przepisami i grozi mandatem.',
            ]),
        ],
        faq=[
            ['Czy odbiór gabarytów we Wrocławiu jest płatny?', 'Dla mieszkańców nie. Odbiór z osiedlowych kontenerów jest w ramach opłaty za śmieci, a PSZOK przyjmuje odpady od mieszkańców bezpłatnie.'],
            ['Gdzie oddać starą lodówkę albo pralkę?', 'To elektroodpad, więc nie do kontenera na gabaryty. Oddaj ją w PSZOK albo w sklepie przy zakupie nowego sprzętu tego samego rodzaju.'],
            ['Co zrobić, gdy kontener na gabaryty jest pełny?', 'Według informacji miasta można to zgłosić firmie podanej na kontenerze albo Ekosystemowi. Rzeczy, które się nie zmieściły, można postawić obok pełnego kontenera.'],
            ['Czy wywieziecie jedną szafę?', 'Nie. Przyjeżdżamy od mniej więcej pół pokoju rzeczy. Przy jednej szafie lepszy będzie kontener na gabaryty albo PSZOK.'],
        ],
        sources=[['Ekosystem: odpady wielkogabarytowe', 'https://ekosystem.wroc.pl/segregacja-odpadow/odpady-wielkogabarytowe/'],
                 ['Ekosystem: PSZOK', 'https://ekosystem.wroc.pl/segregacja-odpadow/pszok/'],
                 ['Harmonogram odbioru gabarytów', 'https://gabaryty.ekosystem.wroc.pl/'],
                 ['wroclaw.pl: Gabaryty. Gdzie, kiedy i jak możemy je wyrzucić', 'https://www.wroclaw.pl/zielony-wroclaw/gabaryty-sprawa-wielkiej-wagi-gdzie-kiedy-i-jak-mozemy-je-wyrzucic-zasady']],
        related=['wywoz-mebli-wroclaw', 'oproznianie-piwnic-strychow-garazy', 'oproznianie-mieszkania-po-zmarlym', 'obszar-dzialania'],
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
}
