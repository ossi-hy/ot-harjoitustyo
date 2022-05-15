# Ohjelmistotekniikka, harjoitustyö

## Dokumentaatio

[Kayttöohje](./dokumentaatio/kayttoohje.md)

[Vaatimusmäärittely](./dokumentaatio/vaatimusmaarittely.md)

[Arkkitehtuuri](./dokumentaatio/arkkitehtuuri.md)

[Testausdokumentti](./dokumentaatio/testaus.md)

[Tuntikirjanpito](./dokumentaatio/tuntikirjanpito.md)

[Changelog](./dokumentaatio/changelog.md)


## Asennus

[Uusin release](https://github.com/ossi-hy/ot-harjoitustyo/releases/tag/loppupalautus)

Asenna riippuvuudet
```bash
$ poetry install [--no-dev]
```

Käynnistä sovellus
```bash
$ poetry run invoke start
```

## Testaus
Aja testit
```bash
$ poetry run invoke test
```

Muodosta koodikattavuus
```bash
$ poetry run invoke coverage-report
```
Kattavuus löytyy kansiosta *htmlcov*. Sen näkee avaamalla tiedoston `index.html`.

## Muut
Aja pylint
```bash
$ poetry run invoke lint
```

