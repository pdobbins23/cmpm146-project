# After Hours

By Scott, Leonardo, Amanda, Peter

## Project Setup Instructions

Open your terminal, and navigate to the project directory.

Then, initialize a virtual environment:

`python3 -m venv ./`

Then, source the virtual environment for your shell:

**macOS & Linux:**
`source bin/activate`

**Windows:**
`.\Scripts\activate.bat`

Finally, install pygame:

`pip install pygame`

Now, you should be able to run the game with:

**NOTE:** `python` and not `python3` for this command, as we are using the virtual environment version.

`python src/main.py` 

## Level Editing

Levels are made using [LDtk](https://ldtk.io/).

To edit the main level, open LDtk and import the file `assets/level.json`.

From there, you will be able to edit the level used by the game.

To add new tile textures to be used in the game, you can edit `assets/tileset.png`.

## TODO

Game Model (Peter & Amanda):

- [x] Decide on tools to use
- [ ] Player
  - [x] Movement
  - [ ] Picking up items
- [ ] Objects/items
- [ ] Map
  - [x] Tilemap
  - [ ] Interactables (doors, lockers)
  - [ ] Exit
  - [ ] Obstacles
    - [ ] Locked doors
- [ ] Physics & Collision
- [ ] Principle
  - [ ] Health/Stun Bar
- [ ] Line of Sight Visualization
- [ ] Level design
- [ ] Art (TBD)
- [ ] Sounds (TBD)

Behavior Trees (Scott & Leonardo):

- [ ] Roam
  - [ ] Invesigate sounds
  - [ ] Prioritize following sight over sound
  - [ ] Wander to points of interest
- [ ] Patrol
  - [ ] Invesigate sounds
  - [ ] Search last seen player locations
  - [ ] Search lockers near last location of player
  - [ ] Prioritize sight over sound
- [ ] Chase
  - [ ] Pursue player until collision or lost sight (~5sec)
