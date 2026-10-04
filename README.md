# tikawe
Tietokannat ja Web ohjelmointi kurssin repo.

Tennisvuoron ilmoitus sovellus, josta löytyy seuraavat ominaisuudet:
- Sovelluksessa käyttäjä pystyy etsimään peliseuraa tennikseen.
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy luoda, muokkaa ja poistaa pelivuorohakuilmoituksia:
   - Ilmoituksessa kerrotaan missä ja milloin pelivuoro on, tarvittavien pelaajien määrä, haluttu pelaajien taitotaso, pelivuoron kesto, ilmoituksen tekijä, ilmoittautuneet ja mahdolliset lisätiedot.
   - Muokkauksessa kaikkia syötettyjä arvoja ilmoituksessa voi muokata.
- Käyttäjä pystyy valitsemaan ilmoituksessa seuraavia luokitteluja:
    - Pelipaikka: Kimpisen massatenniskentät tai Huhtiniemen sisähalli.
    - Pelaajan taso: aloittelija, keskitaso tai edistynyt.
    - Haluttu aika: kalenterivalikko missä voi valita vain tulevaisuuden aikoja tasatunnittain.
    - Pelivuoron kesto: tunneittain 1h - 10h.
    - Pelaajien määrä: 1 - 4 pelaajaa.
- Käyttäjä näkee etusivulla kaikki sovellukseen lisätyt ilmoitukset.
- Käyttäjä pystyy etsimään ilmoituksia sen perusteella, milloin, missä ja montako pelaajaa tarvitaan.
- Profiilisivu näyttää, montako ilmoitusta käyttäjä on lähettänyt ja listan omista ilmoituksista.
- Profiilisivuun käyttäjä voi lisätä oman profiilikuvan.
- Käyttäjä pystyy ilmoittautumaan pelivuoroon ja perumaan ilmoittautumisen.

## Sovelluksen testaaminen paikallisesti

1. Kloonaa repo omalle koneellesi ja siirry projektikansioon.
2. Asenna Flask: Varmista, että koneellasi on Python asennettuna. Asenna Flask suorittamalla komento:
   `pip install Flask`
3. Alusta tietokanta: Luo paikallinen tietokantatiedosto ja sen taulut `schema.sql` -tiedoston avulla suorittamalla komento:
   `sqlite3 database.db < schema.sql`
4. Käynnistä sovellus paikallisessa palvelimessa komennolla:
   `flask run`
5. Testaa: Avaa verkkoselain ja siirry osoitteeseen `http://127.0.0.1:5000`.

## Testaus suurella datan määrällä

Sovellusta testattiin suurella datan määrällä. `seed.py` avulla luotiin tietokantaan seuraava määrä dataa:
- 1 000 käyttäjää
- 100 000 pelivuoroa
- 100 000 viestiä (ilmoituksen lisätiedot)

**Mittauskohteet ja vasteajat:**
- Etusivun lataus (avoimet pelivuorot ja sivutus): 0.02 sekuntia.
- Yksittäisen ilmoituksen avaaminen: 0.01 sekuntia.
- Hakutoiminto (esim. kaikki tietyn pelipaikan haku ja sivutus): 0.04 sekuntia.
- Profiilisivun lataus (käyttäjän omat ilmoitukset ja sivutus): 0.04 sekuntia.

**Huomioita:**
Tietokannassa on käytössä indeksi `CREATE INDEX idx_thread_messages ON messages (thread_id)`, joka nopeuttaa tietokantahakuja. Tulosten perusteella sovellus skaalautuu erinomaisesti suuriin data määriin.

Testidatan voi ajaa komennolla `python seed.py`.
Ajan mittauksen saa päälle poistamalla kommentit `app.py`-tiedoston alusta olevista funktioista `before_request()` ja `after_request()`.

