Title: Jak funguje Python
Tags: python, rozcestník
Category: Python

Znáte to.
Studentka vám položí otázku, a abyste na ni mohli pořádně odpovědět,
je potřeba trochu osvětlit základy.
Mně se to stalo s proměnnými v Pythonu.

No a tak píšu.  
Píšu na téma *Všechno o proměnných, hodnotách a jménech v Pythonu.*  
Píšu už druhý den.

<!-- PELICAN_END_SUMMARY -->

Přišel čas to trošku rozdělit.
Tady je moje osnova; až (a jestli) to dopíšu, tak z toho udělám odkazy.

* [Proměnné jsou jména]({filename}2014-01-05-02-cs-promenne-jsou-jmena.md)
* [Měnění objektů]({filename}2014-01-05-03-cs-meneni-objektu.md)
* Přiřazování
* Jmenné prostory
* Identity a hodnoty <!-- udělat odkaz v poznámce pod čarou v "Proměnné jsou jména" -->

Články budou používat diakritiku v řetězcích.
V Pythonu 3 s tím není žádný problém, ale používáš-li Python 2,
napiš na začátek každého pythoního souboru tyto řádky:

    :::python
    # Encoding: UTF-8
    from __future__ import unicode_literals

Jinak by všechny ukázky kódu měly fungovat v Pythonu 2.7 i 3.3,
pokud není jinak uvedeno.


Pokud uvidíš nějakou chybu, ozvi se mi na [mail],
nebo rovnou založ [issue] či [pull request][github].


[mail]: mailto:encukou@gmail.com
[github]: https://github.com/encukou/blog
[issue]: https://github.com/encukou/blog/issues/new
