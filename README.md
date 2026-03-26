# Disso-final-year
UWE Dissertation- Music Creation Using Generational Algorithms

🎵 Genetic Algorithm for Music Generation
A Final‑Year Dissertation Project by Wissam Salhab
This project implements a Genetic Algorithm (GA) to generate musical melodies using pyo for real‑time audio synthesis and MIDIUtil for exporting evolved melodies as MIDI files.
It is a human‑in‑the‑loop evolutionary system, where the user listens to melodies and provides fitness ratings that guide the evolution of new musical ideas.
The system combines evolutionary computation, digital signal processing, music theory, and interactive evaluation to explore how computational methods can generate creative musical output.

📌 Table of Contents
- Overview
- Key Features
- System Architecture
- Genetic Algorithm Design
- Melody Encoding
- Audio Synthesis Pipeline
- MIDI Export
- Command Line Interface
- Project Structure
- Installation
- Running the System
- Testing
- Future Improvements

🎼 Overview
This project explores how genetic algorithms can be used to generate short musical melodies.
Each melody is represented as a binary genome, which is translated into musical notes, played through pyo, and evaluated by the user.
The system evolves melodies over generations using:
- Selection
- Crossover
- Mutation
- Elitism
The user listens to the best melodies each generation and decides whether to continue evolving or stop.

✨ Key Features
🎵 Real‑Time Audio Playback
Melodies are synthesized using pyo and played directly to the user.
🧬 Genetic Algorithm Engine
Includes:
- Random population generation
- Weighted parent selection
- Single‑point crossover
- Bit‑flip mutation
- Elitism
- Fitness‑limit stopping conditions
🎹 Melody Translation
Binary genomes are mapped to:
- Notes
- Pauses
- Durations
- Chords (via multi‑step harmonization)
- Scales and keys
🎼 MIDI Export
Every generation is saved as a folder of .mid files for use in DAWs like Ableton or FL Studio.
🖥️ CLI Interface
Built with click, allowing users to configure:
- Bars
- Notes per bar
- Scale & key
- Chord steps
- Mutation settings
- Population size
🧪 Unit Tests
Includes tests for:
- Melody generation
- Population generation
- Crossover
- Mutation
- Melody translation
- MIDI export

🏗️ System Architecture
/project
│── algorithms/
│   └── genetic.py        # Core GA implementation
│
│── mgen.py               # Music generation engine + CLI
│── tests.py              # Unit tests
│── requirements.txt      # Dependencies
│── README.md             # This file



🧬 Genetic Algorithm Design
The GA is implemented in genetic.py and includes:
Genome Representation
A melody is encoded as a list of bits:
[0,1,0,1,1,0,1,0, ...]


Every 4 bits represent one musical event:
- 3 bits → pitch
- 1 bit → pause flag
Population Initialization
genPop(size, genome_length)


Selection
Weighted selection based on fitness:
- Higher‑fitness genomes appear more often in the selection pool.
Crossover
Single‑point crossover:
offspring_a, offspring_b = spcross(g1, g2)


Mutation
Bit‑flip mutation with configurable probability:
mutation(genome, num_mutations, probability)


Elitism
Top 2 genomes are always preserved.

🎵 Melody Encoding
The function transmelody() converts a genome into a structured melody:
- Splits genome into 4‑bit chunks
- Converts bits → integer → pitch
- Applies scale & key using EventScale
- Handles pauses
- Merges repeated notes into longer durations
- Generates chords using num_steps
Output format:
{
  "notes": [...],
  "velocity": [...],
  "beat": [...]
}



🔊 Audio Synthesis Pipeline
The function transevents() converts the melody into pyo Events:
- midinote → pitch
- midivel → velocity
- beat → duration
- ADSR envelope
- BPM
A metronome is added for rhythmic reference.
The user listens to each melody and provides a rating (0–5), which becomes the fitness score.

🎼 MIDI Export
savemidi() converts the melody into a .mid file:
- Creates directories automatically
- Writes notes, durations, velocities
- Supports chords
- Saves each generation’s population
Example output structure:
/1708972345/
    /0/
        major-C-0.mid
        major-C-1.mid
        ...



🖥️ Command Line Interface
The CLI prompts the user for all musical and GA parameters:
Number of bars:
Notes per bar:
Number of steps:
Would you like to add pauses?
Select your key:
Select your scale:
Scale Root:
How many melodies per generation?
Number of mutations:
Mutation probability:


Then the system evolves melodies interactively.

📁 Project Structure
algorithms/
│── genetic.py
mgen.py
tests.py
requirements.txt
README.md



📦 Installation
1. Install dependencies
pip install -r requirements.txt


2. Install pyo (may require system packages)
Refer to:
https://ajaxsoundstudio.com/software/pyo/

▶️ Running the System
Start the CLI:
python mgen.py


Follow the prompts to configure your musical parameters.
The system will:
- Generate a population
- Play each melody for rating
- Evolve new melodies
- Play the best two
- Save MIDI files
- Ask whether to continue

🧪 Testing
Run all tests:
python tests.py


Tests cover:
- Genome generation
- Population generation
- Crossover
- Mutation
- Melody translation
- Event generation
- MIDI export

🚀 Future Improvements
- Add automated fitness evaluation (e.g., rule‑based or ML‑based)
- Add GUI for easier interaction
- Add visualization of melodies
- Add support for multiple instruments
- Add multi‑objective fitness (e.g., rhythmic variety + pitch contour)
- Add real‑time parameter tweaking

🎤 Final Notes
This project demonstrates:
- Strong understanding of genetic algorithms
- Practical application of music theory
- Real‑time audio synthesis using pyo
- Interactive evolutionary computation
- Clean modular software design
- Full testing suite
- MIDI export for real‑world use

