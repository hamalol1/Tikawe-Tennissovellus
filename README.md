# tikawe
Tietokannat ja Web ohjelmointi kurssin repo.

Tennisvuoron ilmoitus sovellus, josta löytyy seuraavat ominaisuudet:
- Sovelluksessa käyttäjä pystyy etsimään peliseuraa tennikseen. 
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy luoda, muokkaa ja poistaa pelivuorohakuilmoituksia:
   - Ilmoituksessa kerrotaan missä ja milloin pelivuoro on, tarvittavien pelaajien määrä, haluttu pelaajien taitotaso, pelivuoron kesto, ilmoituksen tekijä, ilmoittautuneet ja mahdolliset lisätiedot.
- Käyttäjä pystyy valitsemaan ilmoituksessa seuraavia luokitteluja:
    - Pelipaikka: Kimpisen massatenniskentät tai Huhtiniemen sisähalli.
    - Pelaajan taso: aloittelija, keskitaso tai edistynyt.
    - Haluttu aika: kalenterivalikko missä voi valita vain tulevaisuuden aikoja tasatunnittain.
    - Pelivuoron kesto: tunneittain 1h - 10h.
    - Pelaajien määrä: 1 - 4 pelaajaa. 
- Käyttäjä näkee etusivulla kaikki sovellukseen lisätyt ilmoitukset.
- Käyttäjä pystyy etsimään ilmoituksia sen perusteella, milloin, missä ja montaka pelaajaa tarvitaan.
- Profiilisivu näyttää, montako ilmoitusta käyttäjä on lähettänyt ja listan omista ilmoituksista.
- Pofiilisivuun käyttäjä voi lisätä oman profiilikuvan.
- Käyttäjä pystyy ilmoittautumaan pelivuoroon ja perumaan ilmoittautumisen.

## Sovelluksen testaaminen paikallisesti

1. Kloonaa repositorio omalle koneellesi ja siirry projektikansioon.
2. Asenna Flask: Varmista, että koneellasi on Python asennettuna. Asenna Flask suorittamalla komentoikkunassa komento:
   `pip install Flask`
3. Alusta tietokanta: Luo paikallinen tietokantatiedosto ja sen taulut `schema.sql` -tiedoston avulla suorittamalla komentoikkunassa:
   `sqlite3 database.db < schema.sql`
4. äynnistä sovellus: Käynnistä paikallinen palvelin komennolla:
   `flask run`
5. Testaa: Avaa verkkoselain ja siirry osoitteeseen `http://127.0.0.1:5000`.
