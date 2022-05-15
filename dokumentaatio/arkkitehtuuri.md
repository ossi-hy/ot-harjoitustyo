# Arkkitehtuurikuvaus

## Rakenne

![Pakkauskaavio](./images/PackageDiagram.png)

Pakkaus *UI* sisältää käyttöliittymästä ja kontrolleista vastaavan ja *Game* pelilogiikasta vastaavan koodin.

## Sovelluslogiikka

```mermaid
classDiagram
    class Board {
        +int width
        +int height
        +int visible_height
        +np.ndarray board
    }
    class PiecePool {
        +int next_piece()
    }
    class Piece
    class Renderer {
        +tk.Tk window
        +int width
        +int height
        +draw()
    }
    class InputHandler {
        +process_inputs(int elapsed)
    }

    Board "1" -- "1" Piece
    Board "1" -- "1" PiecePool
    Renderer "*" -- "1" Board
    InputHandler "*" -- "1" Board

```

*Inputhandler* luokka vastaa käyttäjän painalluksien lukemisesta ja kutsuu luokan *Board* metodeja muuttaakseen peliä. Luokkaa *Renderer* kutsutaan *Inputhandler*-luokan jälkeen jolloin se pyytää luokalta *Board* esityksen pelilaudalta piirrettäväksi.

*Board*-luokka käyttää luokkaa *PiecePool* tulevien palojen arpomiseen, sekä luokkaa *Piece*, joka pitää tietoa palan sijainnista ja asennosta.

## Toiminnaillsuudet


Sekvenssikaavio esimerkki palan liikuttamisesta:
```mermaid
sequenceDiagram

participant Renderer
participant main()
participant InputHandler
participant Board
participant Piece

main() ->> InputHandler: process_inputs()
InputHandler ->> Board: move()
Board ->> +Piece: get_shape()
Piece ->> -Board: shape

main() ->> Renderer: draw()
Renderer ->> +Board: get_board_with_piece()
Board ->> +Piece: get_shape()
Piece ->> -Board: shape
Board ->> -Renderer: board

```