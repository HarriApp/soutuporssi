# Soutupörssi

## Sovelluksen toiminnot

* Sovelluksessa käyttäjät pystyvät etsimään miehistöjä kirkkoveneisiinsä tulevan kesän Sulkavan Suursoutuihin. Ilmoituksessa lukee missä sarjassa ja milloin joukkue kilpailee sekä tarvittava soutajien määrä.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään ilmoituksia ja muokkaamaan ja poistamaan niitä.
* Käyttäjä näkee sovellukseen lisätyt ilmoitukset.
* Käyttäjä pystyy etsimään ilmoituksia sarjan ja soutupäivän perusteella.
* Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun (Esim. veneen tyyppi, veneen kunto ja tavoiteaika).
* Käyttäjä pystyy ilmoittautumaan miehistön jäseneksi. Ilmoituksessa näytetään, ketkä käyttäjät ovat ilmoittautuneet.
* Käyttäjäsivu näyttää, montako ilmoitusta käyttäjä on lähettänyt, listan käyttäjän omista ilmoituksista, sekä muut venekunnat joihin käyttäjä on ilmoitautunut miehistön jäseneksi.

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

Voit käynnistää sovelluksen näin:

```
$ flask run
```
