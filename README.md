# Ohjelmistotekniikka, harjoitustyö

## Dokumentaatio

[Vaatimusmäärittely](https://github.com/ossi-hy/ot-harjoitustyo/blob/master/dokumentaatio/vaatimusmaarittely.md)

[Arkkitehtuuri](https://github.com/ossi-hy/ot-harjoitustyo/blob/master/dokumentaatio/arkkitehtuuri.md)

[Tuntikirjanpito](https://github.com/ossi-hy/ot-harjoitustyo/blob/master/dokumentaatio/tuntikirjanpito.md)

[Changelog](https://github.com/ossi-hy/ot-harjoitustyo/blob/master/dokumentaatio/changelog.md)


## Asennus

[Uusin release](https://github.com/ossi-hy/ot-harjoitustyo/releases/tag/viikko6)

Asenna riippuvuudet
```bash
$ poetry install [--no-dev]
```

Käynnistä sovellus
```bash
$ poetry run invoke start
```

Asetukset sijaitsevat tiedostossa `config\settings.ini`.
Eri asetusten selitykset [täällä](https://github.com/ossi-hy/ot-harjoitustyo/blob/master/config/README.md).

## Testaus
Aja testit
```bash
$ poetry run invoke test
```

Muodosta koodikattavuus
```bash
$ poetry run invoke coverage-report
```
Kattavuus luodaan kansioon *htmlcov*

## Muut
Aja pylint
```bash
$ poetry run invoke lint
```

