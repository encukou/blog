[Glutexo píše](http://glutexo.livejournal.com/137926.html):

> Narazil jsem na drsné a vytůněné Sudoku: Podobá se klasickému killer sudoku:
> V začátku neznáme žádná čísla, pouze máme ohraničené spojité oblasti, u
> kterých vždy víme součet čísel v nich, a také víme, že kromě řádků, sloupců
> a čtverců se ani v těchto ohraničených oblastech číslice neopakují.
> 
> Řešení takového sudoku však nejspíše není unikátní (nakrmil jsem jím řešítko,
> které jsem si našel), ale výsledek nebyl takový, jaký jsem chtěl: Chtěl jsem
> jiné možné řešení, ne libovolné. A nejspíše právě proto je zadání obohaceno
> ještě o informace o některých dvojicích sousedících políček, že na jedné
> straně je číslo větší než to na druhé.
>
> Zajímalo mě, zda na to lze jít metodou hrubé síly, tedy projít si všech 9^81
> kombinací a porovnat je proti zadání. Nešlo: Za deset minut běhu program
> prokombinoval jen třikrát prvních osm pozic. Takže než by prošel všechny,
> uplynula by přibližně věčnost. Takže na to budeme muset jít jinak. Jak?
>
> Pár možností mě napadá: Např. zjistit si pro každou ohraničenou oblast
> všechny možné kombinace čísel v rozsahu 1-9, které dají při daném počtu polí
> daný součet a následně do oblastí dosazovat tato čísla ve všech možných
> kombinacích. Pak už by stačilo jen pro každé vyplnění plochy jen zvalidovat,
> zda platí základní pricipy sudoku a zda platí ona pravidla o tom, které ze
> sousedních polí má obsahovat větší číslo. Ale nedostanu se tím opět do
> astronomické množství kombinací a tak času? Uvidíme, ale jindy.
>
> Nebo máte někdo nějaký nápad, nebo dokonce víte a jste ochotni mi řešení
> představit a vysvětlit? Rád se přiučím.
>
> A pokud by někoho zajímalo zadání, tak se jedná o kešku Loki's mystery
> (GCZE5N).

Napsal jsem program, který to vyluští za <s>11 vteřin</s>, v pomalém Pythonu bez
velkých optimalizací, jen s rozumným algoritmem.
Zkusím tu docela detailně popsat jak na to. Třeba to nebude nudné.
Kdyby něco naopak nebylo k pochopení, prosím čtenáře, aby se ozval.

.* *Upřesnění: celý graf to projde za 3 minuty, 11 vteřin bylo jen štěstí.*

Na podobné úlohy platí různé techniky prohledávání stavového prostoru.
Zrovna tady si vystačíš s relativně jednoduchými, takže se to bude dobře
vysvětlovat.

Než začneme se stavovým prostorem, musíme vědět co je to stav.
Pro sudoku si stav můžeme definovat jako 9x9 pole, kde v každém políčku
budou číslice, které tam teoreticky můžou nakonec vyjít.
V počátečním stavu budou všechna políčka obsahovat všech 9 možných čislic:

    ╔═══════╤═══════╤═══════╦═══════╤═══════╤═══════╦═══════╤═══════╤═══════╗
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 > 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 1
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟── ∨ ──┼───────┼── ∧ ──╫───────┼───────┼── ∨ ──╫───────┼───────┼───────╢
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 2
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟── ∧ ──┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 < 4 5 6 < 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 < 4 5 6 │ 4 5 6 > 4 5 6 ║ 3
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╠═══════╪═══════╪═══════╬═══════╪═══════╪══ ∨ ══╬═══════╪═══════╪═══════╣
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 < 4 5 6 │ 4 5 6 < 4 5 6 │ 4 5 6 │ 4 5 6 > 4 5 6 │ 4 5 6 > 4 5 6 ║ 4
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟── ∨ ──┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 > 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 5
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟───────┼───────┼───────╫───────┼───────┼── ∨ ──╫───────┼───────┼───────╢
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 < 4 5 6 │ 4 5 6 ║ 4 5 6 > 4 5 6 < 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 6
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╠═══════╪═══════╪═══════╬═══════╪═══════╪══ ∧ ══╬══ ∧ ══╪══ ∨ ══╪══ ∧ ══╣
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 < 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 7
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟───────┼───────┼───────╫───────┼───────┼───────╫───────┼── ∧ ──┼───────╢
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 > 4 5 6 │ 4 5 6 < 4 5 6 │ 4 5 6 │ 4 5 6 > 4 5 6 │ 4 5 6 │ 4 5 6 ║ 8
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟── ∧ ──┼── ∧ ──┼───────╫───────┼───────┼── ∧ ──╫───────┼───────┼── ∧ ──╢
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 9
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╚═══════╧═══════╧═══════╩═══════╧═══════╧═══════╩═══════╧═══════╧═══════╝
        A       B       C       D       E       F       G       H       I

No a abychom se dostali dál, budeme z tohohle stavu některá čísla odebírat.
Třeba, pro začátek, hrubou silou: vygenerujeme devět stavů, které jsou stejné
jako tenhle původní, jen v políčku A1 mají každý vybranou jednu číslici.
Třetí z nich by vypadal takhle:


    ╔═══════╤═══════╤═══════╦═══════╤═══════╤═══════╦═══════╤═══════╤═══════╗
    ║     3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║       │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 > 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 1
    ║       │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟── ∨ ──┼───────┼── ∧ ──╫───────┼───────┼── ∨ ──╫───────┼───────┼───────╢
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 2
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟── ∧ ──┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 < 4 5 6 < 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 < 4 5 6 │ 4 5 6 > 4 5 6 ║ 3
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╠═══════╪═══════╪═══════╬═══════╪═══════╪══ ∨ ══╬═══════╪═══════╪═══════╣
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 < 4 5 6 │ 4 5 6 < 4 5 6 │ 4 5 6 │ 4 5 6 > 4 5 6 │ 4 5 6 > 4 5 6 ║ 4
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟── ∨ ──┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 > 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 5
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟───────┼───────┼───────╫───────┼───────┼── ∨ ──╫───────┼───────┼───────╢
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 < 4 5 6 │ 4 5 6 ║ 4 5 6 > 4 5 6 < 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 6
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╠═══════╪═══════╪═══════╬═══════╪═══════╪══ ∧ ══╬══ ∧ ══╪══ ∨ ══╪══ ∧ ══╣
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 < 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 7
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟───────┼───────┼───────╫───────┼───────┼───────╫───────┼── ∧ ──┼───────╢
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 > 4 5 6 │ 4 5 6 < 4 5 6 │ 4 5 6 │ 4 5 6 > 4 5 6 │ 4 5 6 │ 4 5 6 ║ 8
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟── ∧ ──┼── ∧ ──┼───────╫───────┼───────┼── ∧ ──╫───────┼───────┼── ∧ ──╢
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 9
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╚═══════╧═══════╧═══════╩═══════╧═══════╧═══════╩═══════╧═══════╧═══════╝
        A       B       C       D       E       F       G       H       I

Nu a z tohohle stavu se jde "dostat" do dalších devíti stavů, každého s jedinou
číslicí v políčku B1.

Jeden z těchto nových stavů (B1==3) nebude odpovídat
pravidlům. Navíc všechny další stavy, které z něj můžeme dostat odebíráním
možností, budou taky špatně. Takže tenhle stav můžeme vyloučit.

A tímhle způsobem dostaneme obrovitánský graf stavů.
Graf vytvořený takhle hrubou silou bude až moc velký na to, aby se dal rozumně
pozkoumat, ale důležité je, že obsahuje všechny stavy odpovídající pravidlům.
(Vlastně je pro nás důležité jen to, že určitě obsahuje *řešení* (pokud nějaké
existuje), ale vzhledem k tomu že řešení neznáme, všechny "správné" stavy budou
muset stačit.)

Zbývá jen nějak zajistit, abychom nemuseli procházet ten graf celý, ale
zkusili v něm hledat rozumné cesty a zkratky, které nás k cíli dovedou co
nejrychleji. Tedy, použít něco lepšího než hroubou sílu.

(Jen podotknu že ten graf nemusí být nutně stromem; do jednoho stavu se může
dát dostat několika různými cestami.)

Základní schéma algoritmu na prohledávání stavového prostoru je následující
(s komentáři tam, kde Pythonová syntax není naprosto pruhledná):

    open = [initial_state]  # `[v]` je seznam s jedním prvkem, `v`
    closed = set()  # prázdná množina

    while open:  # dokud je něco v open
        current = take_one(open)
        if is_goal(current):
            return current
        closed.add(current)
        for next in generate_next_states(current):
            if next not in closed and is_valid(next):
                open.append(next)

Algoritmus nemá k dispozici celý graf (to by se těžko vešlo do paměti!),
ale "tvoří" si ho pomocí funkce `generate_next_states`, která prostě vrátí
seznam stavů, do kterých se z daného stavu dá dostat.

Množina `open` obsahuje všechny stavy které chceme ještě prozkoumat, neboli
"hranici" zatím prozkoumané části grafu. Množina `closed` obsahuje stavy, které
jsme už viděli; těmi se nemá cenu zabývat, pokud na ně narazíme znovu.

Tož to by byl učebnicový algoritmus.
Teď teoreticky všechno závisí jen na tom, jak chytře navrhneme funkce
`take_one()` a `generate_next_states()`.
Dám několik tipů, které jsem použil já.

Přímo v `generate_next_states` je dobré vyhazovat čísla, která neodpovídají
pravidlům. Já jsem dal tuhle logiku přímo do konstruktoru třídy Stav, takže
můj první stav vypadá ve skutečnosti takhle:

    ╔═══════╤═══════╤═══════╦═══════╤═══════╤═══════╦═══════╤═══════╤═══════╗
    ║   2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │     3 │   2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 > 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 1
    ║ 7 8 9 │ 7 8 9 │ 7 8   ║ 7 8 9 │ 7 8 9 │ 7 8   ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟── ∨ ──┼───────┼── ∧ ──╫───────┼───────┼── ∨ ──╫───────┼───────┼───────╢
    ║ 1 2 3 │ 1 2 3 │   2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 2
    ║       │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7     ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟── ∧ ──┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢
    ║   2 3 │     3 │       ║ 1 2 3 │ 1 2 3 │     3 ║       │   2 3 │ 1 2 3 ║
    ║ 4 5 6 < 4 5 6 < 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 < 4 5 6 │ 4 5 6 > 4 5 6 ║ 3
    ║ 7     │ 7 8   │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8   ║ 7 8 9 │ 7 8 9 │ 7 8   ║
    ╠═══════╪═══════╪═══════╬═══════╪═══════╪══ ∨ ══╬═══════╪═══════╪═══════╣
    ║     3 │       │ 1 2 3 ║   2 3 │ 1 2 3 │   2 3 ║ 1 2 3 │   2 3 │ 1 2 3 ║
    ║ 4 5 6 < 4 5 6 │ 4 5 6 < 4 5 6 │ 4 5 6 │ 4 5 6 > 4 5 6 │ 4 5 6 > 4 5 6 ║ 4
    ║ 7 8   │ 7 8 9 │ 7 8   ║ 7 8 9 │ 7 8 9 │ 7     ║       │ 7 8 9 │ 7 8   ║
    ╟── ∨ ──┼───────┼───────╫───────┼───────┼───────╫───────┼───────┼───────╢
    ║   2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │     3 ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║
    ║ 4 5 6 > 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 5
    ║ 7     │       │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╟───────┼───────┼───────╫───────┼───────┼── ∨ ──╫───────┼───────┼───────╢
    ║ 1 2 3 │   2 3 │ 1 2 3 ║   2 3 │ 1 2 3 │   2 3 ║ 1 2 3 │   2 3 │ 1 2 3 ║
    ║ 4 5 6 < 4 5 6 │ 4 5 6 ║ 4 5 6 > 4 5 6 < 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 6
    ║ 7 8   │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7     │ 7 8   ║ 7 8   │ 7 8 9 │ 7 8   ║
    ╠═══════╪═══════╪═══════╬═══════╪═══════╪══ ∧ ══╬══ ∧ ══╪══ ∨ ══╪══ ∧ ══╣
    ║ 1 2 3 │ 1 2 3 │ 1 2 3 ║ 1 2 3 │   2 3 │     3 ║   2 3 │ 1 2 3 │   2 3 ║
    ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 < 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 7
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8   │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8   │ 7 8 9 ║
    ╟───────┼───────┼───────╫───────┼───────┼───────╫───────┼── ∧ ──┼───────╢
    ║   2 3 │ 1 2 3 │ 1 2 3 ║   2 3 │ 1 2 3 │   2 3 ║ 1 2 3 │   2 3 │ 1 2 3 ║
    ║ 4 5 6 > 4 5 6 │ 4 5 6 < 4 5 6 │ 4 5 6 │ 4 5 6 > 4 5 6 │ 4 5 6 │ 4 5 6 ║ 8
    ║ 7 8   │ 7     │ 7 8   ║ 7 8 9 │ 7 8 9 │ 7 8   ║ 7     │ 7 8 9 │ 7 8   ║
    ╟── ∧ ──┼── ∧ ──┼───────╫───────┼───────┼── ∧ ──╫───────┼───────┼── ∧ ──╢
    ║     3 │   2 3 │ 1 2 3 ║ 1 2 3 │ 1 2 3 │     3 ║ 1 2 3 │ 1 2 3 │   2 3 ║
    ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 4 5 6 │ 4 5 6 │ 4 5 6 ║ 9
    ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║ 7 8 9 │ 7 8 9 │ 7 8 9 ║
    ╚═══════╧═══════╧═══════╩═══════╧═══════╧═══════╩═══════╧═══════╧═══════╝
        A       B       C       D       E       F       G       H       I

Moje implementace tu dělá několik věcí:

- vyhazuje čísla podle zadaných nerovností (pokud má jedno číslo
být větší než druhé, které může být 3-8, tak bude určitě 4 nebo víc).
- vyhazuje čísla z řádků, sloupců, čtverců a oblastí, pokud v jiném políčku
  je už dané číslo vybrané
- vyhazuje čísla, která nemůžou dát daný součet pro oblast
- ještě by mohla vybrat číslo, pokud se v řádku/sloupci/čtverci jen jedno
  políčko kde je to číslo možné, ale našel jsem řešení než jsem tohle stihl
  napsat, tak jsem se na to vykašlal.

Tím, že tohle dělám co nejdřív, se vyhýbám spoustě zbytečných stavů. Vzhledem k
tomu, že každý stav nejen potřebuje nějaký ten procesorový čas a paměť, ale
navíc se pak množí jak králík v Austrálii, je dobré takhle normalizovat co
nejagresivněji.

Další místo, kde je možné algoritmus potunit, je výběr políčka, ve kterém se
budou generované stavy lišit.
Já vždycky vyberu políčko s nejnižším počtem možností (kromě 1, samozřejmě).
Tím docílím toho, že každý stav má co nejmenší počet "potomků", takže graf
neroste tak rychle.
Je samozřejmě možné zvolit úplně jinou strategii. Fungovalo by třeba udělat
potomky dva: jednoho s první možností v daném políčku, a druhého s možnostmi
ostatními. Dokonce není nutné generovat stavy lišící se jen v jednom políčku.
Jen je důležité, aby existovala cesta ke každému validnímu stavu (nebo teda
aspoň k tomu cílovému).

Tohle tunění tvaruje prozkoumávanou oblast grafu, je tak širší nebo hlubší,
rozvětvenější nebo kompaktnější.
Nějaké velké optimalizování je silně závislé na problému,
a je to leckdy spíš umění než exaktní věda.
Naštěstí na tohle sudoku nic moc složitého potřeba není.

No a snad poslední kritické místo v algoritmu je funkce `take_one`, která vyjme
a vrátí další stav, kterým se bude program zabývat.
Může například zvolit vždycky nejstarší prvek ze seznamu (v tom případě jde o
hledání "do šířky", které se vyplatí třeba pokud víme že cíl není v grafu
příliš hluboko), nebo naopak nejnovější (hledání do hloubky).
Taky jde jednotlivým stavům přiřadit skóre, a vždycky vybrat ten stav, který
nejvíc vypadá že povede ke správnému řešení.
Vyrobit na tohle dobrou hodnotící funkci je celkem kumšt; já to tady zkusil,
ale nakonec jsem zjistil že je to rychlejší bez ní.

(Na takové hodnotící funkci jsou pak založené algoritmy jako A*, které nejen že
ve stavovém prostoru najdou cíl, ale vrátí opotimální cíl a optimální cestu k
němu. Typické použití: AI ve hrách.)


A na závěr jeden tip: je dobré investovat nějaký čas do funkcí na zobrazení
stavů nebo toho, jak si algoritmus vede (např. velikosti množin `open` a
`closed`; cesta grafem k právě prohledávanému stavu, atd.).
Možná není potřeba to přehánět jako já (ty ASCII-arty výše jsou v mém programu
navíc obarvené podle oblastí se součtem), ale cokoli pomůže pochopit to, co se
vevnitř děje, hodně pomáhá.

Tož přeji hezké programování, snad tenhle výlev trochu pomůže.
