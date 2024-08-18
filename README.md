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

## TODO

Game Model (Peter & Amanda):

- [x] Decide on tools to use
- [ ] Player
  - [ ] Movement
- [ ] Objects/items
- [ ] Map
  - [ ] Interactables (doors, lockers)
  - [ ] Exit
  - [ ] Obstacles
    - [ ] Locked doors
- [ ] Physics & Collision
- [ ] Principle
  - [ ] Health/Stun Bar
- [ ] Line of Sight Visualization
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
