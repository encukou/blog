Title: Měnění objektů
Tags: python, mutability
Category: Python


Už víme, [jak v Pythonu fungují proměnné]({filename}2014-01-05-02-cs-promenne-jsou-jmena.md).
(Pokud ne, doporučuju to napřed zjistit,
už jen pro seznámení s mými uměleckými diagramy.)
Teď se pojďme podívat na to, jak se chovají jejich hodnoty – tedy objekty.


<!-- PELICAN_END_SUMMARY -->

Toto je druhý ze série článků o tom, jak funguje Python.
Pokud jsi se dostala přímo sem, koukni na
[Rozcestník]({filename}2014-01-05-01-cs-rozcestnik-python.md)
a trochu se zorientuj.

-------------------------------------------------------------------------------

Řetězce, stejně jako čísla nebo n-tice, jsou neměnitelné *(immutable)*.
To znamená, že se nedá žádným způsobem změnit jejich hodnota.
Chceme-li řetězec „změnit“, musíme vytvořit úplně nový objekt
s novou hodnotou.

    :::python
    retezec = 'abc'
    retezec = retezec.upper()
    retezec = retezec + 'D'
    retezec = retezec[1:]

Tyhle příkazy vytvoří několik „sirotků“,
než do proměnné dostanou správnou hodnotu:

    :::text
    ┌─────────┐     ╔═══════╗
    │ retezec ├─┐ ×→║ 'abc' ║
    └─────────┘ │   ╚═══════╝
                │   ╔═══════╗
                │ ×→║ 'ABC' ║    ╔═════╗
                │   ╚═══════╝    ║ 'D' ║
                │   ╔════════╗   ╚═════╝
                │ ×→║ 'ABCD' ║
                │   ╚════════╝
                │   ╔═══════╗
                └──→║ 'BCD' ║
                    ╚═══════╝

Existují ale i objekty, které měnit lze. Klasický příklad jsou seznamy.

Jak funguje takový seznam?

Když napíšeme

    :::python
    jmeno = 'hynek'
    jmena = ['štěpán', 'vilém']

dostaneme následující situaci:

    :::text
    ┌───────┐          ╔═════════╗
    │ jmeno ├─────────→║ 'hynek' ║
    └───────┘          ╚═════════╝
    ┌───────┐    ╔═════╤═════╗
    │ jmena ├───→║ [0] │ [1] ║
    └───────┘    ╚══╪══╧══╪══╝
                    │     │         ╔═════════╗
                    │     └────────→║ 'vilém' ║
                    │ ╔══════════╗  ╚═════════╝
                    └→║ 'štěpán' ║ 
                      ╚══════════╝ 

Položky seznamu se chovají jako proměnné.
Stejně jako hodnota výrazu `jmeno` je teď `'hynek`',
výraz `jmena[0]` má hodnotu `'štěpán'`.
A stejně tak jako můžeme přiřadit do proměnné `jmeno`,
můžeme přiřadit i do `jmena[0]`:

    :::python
    jmena[0] = jmeno

a dostaneme stejný výsledek, jako by `jmena[0]` byla normální proměnná:

    :::text
    ┌───────┐          ╔═════════╗
    │ jmeno ├─────────→║ 'hynek' ║
    └───────┘       ┌─→╚═════════╝
    ┌───────┐    ╔══╪══╤═════╗
    │ jmena ├───→║ [0] │ [1] ║
    └───────┘    ╚═════╧══╪══╝
                          │         ╔═════════╗
                          └────────→║ 'vilém' ║
                                    ╚═════════╝
                        * poof *

Protože je seznam objekt jako každý jiný,
může mít více jmen — může na něj ukazovat více proměnných.
Po příkazu

    :::python
    slova = jmena

bude situace vypadat takhle:

    :::text
                       ╔═════════╗
                    ┌─→║ 'hynek' ║
                    │  ╚═════════╝
    ┌───────┐    ╔══╪══╤═════╗
    │ jmena ├───→║ [0] │ [1] ║
    └───────┘ ┌─→╚═════╧══╪══╝
    ┌───────┐ │           │         ╔═════════╗
    │ slova ├─┘           └────────→║ 'vilém' ║
    └───────┘                       ╚═════════╝

Seznam teď můžeme měnit pomocí kteréhokoli z těch dvou jmen.

    :::python
    print(jmena)   # → ['hynek', 'vilem']
    slova.append('jarmila')  # na proměnnou `jmena` vůbec nesaháme!
    print(jmena)   # → ['hynek', 'vilem', 'jarmila']

Když si uvědomíme, co se děje uvnitř,
nemůže nás toto chování ničím překvapit.

    :::text
                       ╔═════════╗
                    ┌─→║ 'hynek' ║
                    │  ╚═════════╝
    ┌───────┐    ╔══╪══╤═════╤═════╗   ╔═══════════╗
    │ jmena ├───→║ [0] │ [1] │ [2] ╫──→║ 'jarmila' ║
    └───────┘ ┌─→╚═════╧══╪══╧═════╝   ╚═══════════╝
    ┌───────┐ │           │         ╔═════════╗
    │ slova ├─┘           └────────→║ 'vilém' ║
    └───────┘                       ╚═════════╝

Toto chování je zdrojem častých chyb.
Musíme pořád mít na paměti, že pokud jakýkoli měnitelný objekt
(např. seznam, nebo slovník) poskytneme třeba nějaké funkci jako parametr,
ta funkce nám ho může pod rukama změnit.

Abychom zabránili chybám, je dobré co používat neměnitelné objekty
(řetězce, čísla, n-tice), a psát kód tak,
aby objekty neměnil pokud přímo nemusí.

Ještě připomenu, že pokud máš n-tici,
nelze přiřadit přímo do jejích položek:

    :::python
    ntice = ('abc', 'def')
    ntice[0] = 'ghi'
    # → TypeError: 'tuple' object does not support item assignment

ale dej si pozor na i to,
že objekty které obsahuje se stále měnit dají:

    :::python
    seznam = [1, 2, 3]
    ntice = ('abc', seznam)
    seznam.append(4)
    print(ntice)  # → ('abc', [1, 2, 3, 4])
    ntice[1].append(5)
    print(seznam)  # → [1, 2, 3, 4, 5]

A to je prozatím k měnění objektů všechno.
Příště se můžeš těšit na důkladný rozbor *přiřazování*.

