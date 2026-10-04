# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta:

```text
************* Module app
app.py:179:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
app.py:207:0: C0301: Line too long (133/100) (line-too-long)
app.py:325:0: C0301: Line too long (134/100) (line-too-long)
app.py:413:0: C0301: Line too long (180/100) (line-too-long)
app.py:445:0: C0301: Line too long (149/100) (line-too-long)
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:38:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:44:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:63:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:63:0: R0911: Too many return statements (8/6) (too-many-return-statements)
app.py:63:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:104:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:104:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:128:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:137:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:137:0: R0914: Too many local variables (16/15) (too-many-locals)
app.py:137:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:193:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:210:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:229:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:229:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:251:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:263:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:309:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:328:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:328:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:352:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:362:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:380:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:389:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:389:0: R0914: Too many local variables (20/15) (too-many-locals)
app.py:445:11: R0916: Too many boolean expressions in if statement (6/5) (too-many-boolean-expressions)
app.py:389:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:460:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:465:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module forum
forum.py:9:0: C0301: Line too long (132/100) (line-too-long)
forum.py:33:0: C0301: Line too long (126/100) (line-too-long)
forum.py:1:0: C0114: Missing module docstring (missing-module-docstring)
forum.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:8:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:19:0: R0913: Too many arguments (7/5) (too-many-arguments)
forum.py:19:0: R0917: Too many positional arguments (7/5) (too-many-positional-arguments)
forum.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:39:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:46:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:51:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:55:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:55:0: R0913: Too many arguments (6/5) (too-many-arguments)
forum.py:55:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
forum.py:62:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:66:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:70:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:89:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:115:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:121:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:125:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:38:0: C0301: Line too long (120/100) (line-too-long)
seed.py:43:0: C0301: Line too long (103/100) (line-too-long)
seed.py:45:0: C0301: Line too long (164/100) (line-too-long)
seed.py:46:0: C0301: Line too long (123/100) (line-too-long)
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
seed.py:6:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:6:0: R0914: Too many local variables (18/15) (too-many-locals)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:28:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.38/10 (previous run: 8.35/10, +0.03)
```
Käydään seuraavaksi läpi tarkemmin raportin sisältö ja perustellaan, miksi kyseisiä asioita ei ole korjattu sovelluksessa.

## Docstring-ilmoitukset

Suuri osa raportin ilmoituksista on seuraavan tyyppisiä ilmoituksia:
```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
```

Ilmoitukset tarkoittavat, että moduuleissa ja funktioissa ei ole docstring-kommentteja. Nämä kommentit on jätetty tietoisesti pois, jotta koodi pysyy helposti luettavana.

## Turhat sulkeet (Unnecessary parens)

Raportissa on yksi ilmoitus turhista sulkeista:
```
app.py:179:0: C0325: Unnecessary parens after 'not' keyword (superfluous-parens)
```

Tämä koskee yhtä ehtolausetta `if not (1 <= p_count <= 4) or not (1 <= duration_h <= 10):`. Vaikka Python ei  vaadi sulkeita not-sanan jälkeen, ne on jätetty koodiin tietoisesti. Sulkeiden kanssa ehtolause on  selkeämpi ja luettavampi kehittäjän mielestä.

## Puuttuvat palautusarvot (Inconsistent return statements)
Raportti ilmoittaa useasta kohdasta palautusarvoihin liittyen:
```
app.py:63:0: R1710: Either all return statements in a function should return an expression, or none of them should.
app.py:63:0: R0911: Too many return statements (8/6)
```

Nämä ilmoitukset johtuvat siitä, että koodissa on käytetty Flaskin sisäänrakennettua abort()-funktiota virheiden käsittelyyn. Pylint ei tunnista, että abort() pysäyttää funktion suorituksen kokonaan, ja tulkitsee sen vuoksi palautusarvojen logiikan virheellisesti. Koodi on toimiva ja noudattaa normaaleja Flask käytäntöjä.

## Paikallisten muuttujien ja parametrien määrä (Too many arguments/locals)
Raportissa on huomautuksia funktioista, joille välitetään suuri määrä muuttujia:
```
forum.py:19:0: R0913: Too many arguments (7/5) (too-many-arguments)
app.py:364:0: R0914: Too many local variables (20/15) (too-many-locals)
```

Sovelluksessa käsitellään uuden tennisvuoron ilmoittamista ja muokkaamista varten pitkää HTML-lomaketta (peliaika, paikka, taso, kesto, pelaajien määrä, lisätiedot etc.). Koska nämä tiedot kuuluvat yhteen kokonaisuuteen (yksi pelivuoro), on ne luonnollista pitää yhtenä rakenteena samoissa funktioissa, vaikka muuttujien määrä ylittääkin Pylintin oletusrajan.

## Liian pitkät koodirivit (Line too long)

Muutamalla rivillä ylitetään Pylintin asettama 100 merkin oletusraja:
```
app.py:388:0: C0301: Line too long (180/100) (line-too-long)
forum.py:9:0: C0301: Line too long (132/100) (line-too-long)
```

Nämä ylitykset johtuvat pitkistä SQL-kyselyistä forum.py-tiedostossa sekä pitkistä funktioiden kutsuista reititysten sisällä. Niiden jakaminen useammalle riville luettavuutta, joten ovat jätetty nykyiseen muotoonsa.

## Liian monta ehtolauseketta (Too many boolean expressions)

```
app.py:420:11: R0916: Too many boolean expressions in if statement (6/5)
```

Pylint varoittaa if-lauseesta, jossa tarkistetaan lomakkeen kenttien arvoja kerralla (location, skill_level, p_count, duration_h). Koodin luettavuuden kannalta on selkeämpää ja tehokkaampaa tarkistaa kaikki lomakkeen kenttien sallitut arvot samassa lausekkeessa ja palauttaa tarvittaessa abort(403), kuin tehdä tarkistus useassa erillisessä osassa.

## Testidatan seed.py-skriptin ilmoitukset

Pylint antaa useita ilmoituksia (esim. pitkät rivit C0301, puuttuvat docstringit C0114/C0116 ja liian monta muuttujaa R0914) `seed.py`-tiedostosta. Koska kyseessä on erillinen aputyökalu, joka on tarkoitettu vain suorituskyvyn testaukseen käytettävän datan luontiin, niin sen tyylivirheistä voidaan olla välittämättä.
