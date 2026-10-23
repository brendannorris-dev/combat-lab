# Project Roadmap

## Phase 1: Foundations
- [x] Initialize repo, README, .gitignore
- [x] Define Fighter data model - both enemy & player character can stem from this
- [x] Write basic damage formula (i.e. calculate_damage())

## Phase 2: Single Combat Engine
- [ ] Implement some element of turn order (higher speed acts first)
- [ ] Build the engine to simulate the entire fight until either fighter dies
- [ ] Verify single combat

## Phase 3: Expand Single Fight to Monte Carlo Runner
- [ ] Implement a loop to run the simulation x times
- [ ] Once loop is successfully running x fights, aggregate win rates, time to kill, remaining HP, etc.
- [ ] Organize and clean the output for the terminal

## Phase 4: Exporting and Summarizing Data
- [ ] Export raw results
- [ ] Summarize and analyze the results

## Phase 5: Increase Depth to Fight
- [ ] Examine alternate methods to make combat more interesting & add depth
  - [ ] Critical Rate?
  - [ ] Split out weapon stats from armor stats?

## Phase 6: Architecture & Data
- [ ] File separation, organize code into appropriate models
- [ ] Move character/weapon stats to JSON inputs
- [ ] Unit Tests

## Phase 7: Polish
- [ ] Write and update the README
- [ ] Cleanup code