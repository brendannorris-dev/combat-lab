# Project Roadmap

## Phase 1: Foundations
- [x] Initialize repo, README, .gitignore
- [x] Define Fighter data model - both enemy & player character can stem from this
- [x] Write basic damage formula (i.e. calculate_damage())

## Phase 2: Single Combat Engine
- [x] Implement some element of turn order (higher speed acts first) -> Iterated on this and created an active time system with turn meter 
- [x] Build the engine to simulate the entire fight until either fighter dies
- [x] Verify single combat
- [x] Stretch: Include a verbose mode to play out a single fight descriptively (for demoing purposes)

## Phase 3: Increase Depth to Fight
- [ ] Examine alternate methods to make combat more interesting & add depth
  - [x] Critical Rate?
  - [ ] Evasion Rate?
  - [x] Damage Variance?
  - [ ] Blocking?

## Phase 4: Expand Single Fight to Monte Carlo Runner
- [ ] Implement a loop to run the simulation x times
- [ ] Once loop is successfully running x fights, aggregate win rates, time to kill, remaining HP, etc.
- [ ] Organize and clean the output for the terminal
- [ ] Create a way to output the round results to CSV

## Phase 5: Exporting and Summarizing Data
- [ ] Export raw results
- [ ] Summarize and analyze the results

## Phase 6: Further Depth
- [ ] Look into splitting out stats into a base class and adding on weapons as independent objects?

## Phase 7: Architecture & Data
- [ ] File separation, organize code into appropriate models
- [ ] Move character/weapon stats to JSON inputs
- [ ] Unit Tests

## Phase 8: Polish
- [ ] Write and update the README
- [ ] Cleanup code
