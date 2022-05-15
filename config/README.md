# Asetukset

## Peliasetukset
- DAS (int): automaattisen liikkumisen alkamisen viive millisekunneissa
- ARR (int): automaattisen liikkumisen toiston viive millisekunneissa
- shadow (bool): maassa näkyvä varjo, joka näyttää mihin pala putoaa
- lines (int): tyhjennettävien rivien määrä pelin läpäisyksi

## Grafiikkasetukset
- width (int): peli-ikkunan leveys
- height (int): peli-ikkunan korkeus

## Kontrollit
Näihin tulee haluttu näppäin tekstinä englanniksi
- move-left: tetrominon liikutus yksi ruutu vasemmalle
- move-right: tetrominon liikutus yksi ruutu oikealle
- rotate-cw: kierrä tetrominoa 90 astetta myötäpäivään
- rotate-ccw: kierrä tetrominoa 90 astetta vastapäivään
- rotate-180: kierrä tetrominoa 180 astetta
- drop: tiputa tetromino maahan
- hold: vaihda pelattava pala seuraavaksi tulevaan, tai "kädessä" olevaan (näkyy oikealla ylhäällä) 
- reset: aloita peli alusta