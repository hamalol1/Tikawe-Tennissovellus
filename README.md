# tikawe
Tietokannat ja Web ohjelmointi course github repository

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään profiilikuvan.
- Sovelluksessa käyttäjät pystyvät etsimään peliseuraa tennikseen. Ilmoituksessa lukee missä ja milloin pelivuoro on sekä tarvittava pelaajien määrä.
- Käyttäjä pystyy lisäämään ilmoituksia ja muokkaamaan ja poistamaan niitä.
- Käyttäjä näkee sovellukseen lisätyt ilmoitukset.
- Käyttäjä pystyy etsimään ilmoituksia sen perusteella, milloin vuoro on.
- Käyttäjäsivu näyttää, montako ilmoitusta käyttäjä on lähettänyt ja listan ilmoituksista.
- Käyttäjä pystyy valitsemaan esimerkiksi seuraavia luokitteluja:
    Pelipaikka: Kumpula Unisport tai Otaniemi Unisport
    Pelaajan taso: aloittelija, keskitaso tai edistynyt
- Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun (esim. talin tenniskeskus, keskitason pelaaja).
- Käyttäjä pystyy ilmoittautumaan pelivuoroon. Ilmoituksessa näytetään, ketkä käyttäjät ovat ilmoittautuneet.

## Sovelluksen testaaminen paikallisesti

1. Kloonaa repositorio omalle koneellesi ja siirry projektikansioon.
2. Luo salainen avain: Luo projektin juureen tiedosto `config.py` ja lisää sinne seuraava koodirivi istuntojen ja CSRF-suojauksen mahdollistamiseksi:
   `secret_key = "oma_salainen_avaimesi"`
3. Alusta tietokanta: Luo paikallinen tietokantatiedosto ja sen taulut `schema.sql` -tiedoston avulla suorittamalla komentoikkunassa:
   `sqlite3 database.db < schema.sql`
4. Käynnistä sovellus: Varmista, että sinulla on asennettuna Flask. Käynnistä palvelin komennolla:
   `flask run`
5. Testaa: Avaa verkkoselain ja siirry osoitteeseen `http://127.0.0.1:5000`.
