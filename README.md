# Soutupörssi
Sovelluksessa käyttäjät voivat etsiä miehistöjä kirkkoveneisiinsä sekä ilmoittautua mukaan muiden käyttäjien luomiin joukkueisiin tulevan kesän Sulkavan Suursoutuihin. Ilmoituksessa näkyvät joukkueen nimi, lähtö, jossa joukkue kilpailee, sekä muut käyttäjät, jotka ovat ilmoittautuneet mukaan. Sovellus huolehtii myös siitä, ettei joukkueen enimmäiskoko ylity eikä yksikään käyttäjä päädy samaan lähtöön kahdessa eri joukkueessa.

Sovellus laaditaan edellisellä periodilla laaditun MVP-verision pohjalta. Tarkoituksena on mahdollistaa tapahtuman kasvu kansainvälisiin mittoihin panosatamalla sovelluksen viimeistelyyn, ulkonäköön ja optiomoimalla sovelluksen rakennetta siten, että se soveltuu suurille käyttäjämäärille.

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä näkee sovellukseen lisätyt joukkueet sekä sarjat joissa ne kilpailevat.
* Käyttäjä pystyy lisäämään joukkueita sekä muokkaamaan ja poistamaan niitä.
* Käyttäjä pystyy etsimään joukkueita nimen ja kuvauksen perusteella.
* Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun (Veneen tyyppi, veneen kunto, tavoiteaika ja tunnelma veneessä).
* Käyttäjä voi ilmoittautua joukkueen miehistöön, mikäli joukkueessa on tilaa eikä käyttäjä ole jo ilmoittautunut samaan sarjaan toisen venekunnan mukana.
* Käyttäjäsivu näyttää, montako joukkuetta käyttäjä kipparoi, listan käyttäjän omista joukkueista sekä ne muut venekunnat, joihin käyttäjä on ilmoittautunut miehistön jäseneksi.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Vaihda tiedostossa config.py oleva kehityksen aikainen salainen.

Voit käynnistää sovelluksen näin:

```
$ flask run
```
