Title: Proměnné jsou jména
Tags: python, proměnné
Category: Python

Jak v Pythonu fungují proměnné?
Už asi víš, že se přiřazují pomocí rovnítka,
a že se pak dají používat ve výrazech.
Pojďme se na ně podívat trochu podrobněji.

<!-- PELICAN_END_SUMMARY -->

Toto je první ze série článků o tom, jak funguje Python.
Pokud jsi se dostala přímo sem, koukni na
[Rozcestník]({filename}2014-01-05-01-cs-rozcestnik-python.md)
a trochu se zorientuj.

-------------------------------------------------------------------------------

Na rozdíl od jazyků jako C, kde proměnná je vyhrazené místo v paměti,
Proměnné v Pythonu jsou *jména*, nebo řekněme *ukazatele*.

Abych to vysvětlil, pojďme se krok po kroku podívat,
co přesně dělá tohle jednoduché přiřazení:

    :::python
    jazyk = 'python'

Nejdřív se vyhodnotí výraz za rovnítkem.
Výsledek vyhodnocení výrazu je vždycky nějaký *objekt*;
v našem případě řetězec 'python'.
Ukážeme si ho takhle:

    :::text
                    ╔══════════╗
                    ║ 'python' ║
                    ╚══════════╝

Teď, když má hodnotu výrazu, podívá se Python na jméno před rovnítkem,
a zařídí, aby na tu hodnotu „ukazovalo“.

    :::text
    ┌───────┐       ╔══════════╗
    │ jazyk ├──────→║ 'python' ║
    └───────┘       ╚══════════╝

Voilà! Hodnota proměnné `jazyk` je odteď `'python'`.

Pojďme si přiřadit další proměnnou:

    :::python
    rec = 'češ' + 'tina'

Opět se vyhodnotí výraz, vezmou se řetězce `'češ'` a `'tina'`, sečtou se,
a na výslednou hodnotu začne ukazovat proměnná `rec`:

    :::text
    ┌───────┐       ╔══════════╗
    │ jazyk ├──────→║ 'python' ║
    └───────┘       ╚══════════╝
    ┌─────┐         ╔═══════════╗
    │ rec ├────────→║ 'čeština' ║
    └─────┘         ╚═══════════╝

Že to není zas tak složité?

Teď zkusíme jednu proměnnou „přiřadit“ do druhé:

    :::python
    jazyk = rec

Opět se nejdřív vyhodnotí výraz za rovnítkem.
Výsledek bude objekt, který je v proměnné `rec`.
A proměnná `jazyk` začne jednoduše ukazovat na tento objekt:

    :::text
    ┌───────┐       ╔══════════╗
    │ jazyk ├───┐ ×→║ 'python' ║
    └───────┘   │   ╚══════════╝
    ┌─────┐     └──→╔═══════════╗
    │ rec ├────────→║ 'čeština' ║
    └─────┘         ╚═══════════╝

Tady je důvod, proč říkám že proměnné v Pythonu jsou *jména*.
Jeden objekt může mít několik jmen, ale pořád je to ten samý objekt.

Řetězec `'python'` teď žádné jméno nemá. Nedá se k němu nijak
dostat[^interned-strings], a tudíž s ním dál nemůžeme nijak pracovat.
Jediné co můžeme dělat je vytvořit nový objekt se stejnou hodnotou.
Takovéhle sirotky Python časem smaže, aby nezabíraly paměť počítače:

    :::text
    ┌───────┐
    │ jazyk ├───┐      * poof *
    └───────┘   │
    ┌─────┐     └──→╔═══════════╗
    │ rec ├────────→║ 'čeština' ║
    └─────┘         ╚═══════════╝

Teď, když víme jak fungují proměnné, se můžeme podívat na zoubek
jejich hodnotám, tedy objektům.
Další článek v sérii nám poví
o [Měnění objektů]({filename}2014-01-05-03-cs-meneni-objektu.md).


-------------------------------------------------------------------------------

## Zdroje a další materiály

* [Python Tutor](http://pythontutor.com/) umí názorně zobrazovat, jak proměnné fungují
* Ned Batchelder: [Facts and myths about Python names and values ](http://nedbatchelder.com/text/names.html)
* David Gooder: [Code Like a Pythonista: Idiomatic Python — Python has Names](http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html#python-has-names)


[^interned-strings]: Tohle je zjednodušení; řetězce co se vyskytují přímo v kódu
jsou (v CPythonu) součástí modulu, takže se k nim nějak dostat dá,
a budou “žít” dál.
Podrobněji to plánuju rozeberat v článku *identity a hodnoty*.
