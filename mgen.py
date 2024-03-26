import click
from datetime import datetime
from typing import List, Dict 
from midiutil import MIDIFile
from pyo import * 

from algorithms.genetic import genMelody, Genome, selectparents, spcross, mutation 

bpn = 4
keys = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"] 
scales = ["major", "minorM", "dorian", "phrygian", "lydian", "mixolydian", "majorBlues", "minorBlues"]


#calculating the integer value from a list of 0s & 1s 
def bitint(bits: List[int]) -> int:
    return int(sum([bit*pow(2, index) for index, bit in enumerate(bits)]))
 

def transmelody(genome: Genome, num_bars: int, num_notes: int, num_steps: int,
                     pauses: int, key: str, scale: str, root: int) -> Dict[str, list]:
    #iterate each note then ith section of bits till i+1 and add them to a list, making a list of lists
    notes = [genome[i * bpn:i * bpn + bpn] for i in range(num_bars * num_notes)]

    #default length per note in pyo is 4 ticks, ex 8 notes per bar = note length 0.5
    note_length = 4 / float(num_notes)

    #pyo scale which has a key, scale, and first = first key
    scl = EventScale(root=key, scale=scale, first=root)

    #melody object includes notes, velocity per note (loudness), beat (length)
    melody = {
        "notes": [],
        "velocity": [],
        "beat": []
    }

    #goes through list of lists, generates an int for each bit quadrantS, 3 bits used for ptch and one used for if pause / !pause 
    for note in notes:
        integer = bitint(note)

        #if !pause then notes remapped in the 3 bit range
        if not pauses:
            #modulo for 2^ bits per note -1
            integer = int(integer % pow(2, bpn - 1))

        #if pauses included  
        if integer >= pow(2, bpn - 1):
            melody["notes"] += [0]

            #pass velocity 0 note for muted note 
            melody["velocity"] += [0]
            melody["beat"] += [note_length]
        else:

            #if the previous and next note are of the same tone then extend previous rather than add a new one 
            if len(melody["notes"]) > 0 and melody["notes"][-1] == integer:
                melody["beat"][-1] += note_length
            else:
                melody["notes"] += [integer]
                melody["velocity"] += [127]
                melody["beat"] += [note_length]

    
    #to generate chords we add a number of steps on top of the root note   
    steps = []
    for step in range(num_steps):
        steps.append([scl[(note+step*2) % len(scl)] for note in melody["notes"]])


    #new notes added on top of the other notes, new melody replaces old melody
    melody["notes"] = steps
    return melody

#in order to add to events we translate the genome to a melody using its pramaters
def transevents(genome: Genome, num_bars: int, num_notes: int, num_steps: int, 
                     pauses: bool, key: str, scale: str, root: int, bpm: int) -> [Events]:
    melody = transmelody(genome, num_bars, num_notes, num_steps, pauses, key, scale, root)

    return [
        Events(
        #pyo objects to make it readable when sent to pyo server        
            midinote=EventSeq(step, occurrences=1),#pitch 
            midivel=EventSeq(melody["velocity"], occurrences=1),
            beat=EventSeq(melody["beat"], occurrences=1),
            attack=0.001, #length of note
            decay=0.05, #how fast the sound decays
            sustain=0.5, #how long to sustain before start of decay
            release=0.005, #how long it lasts before virtual key press is released  
            bpm=bpm
        ) for step in melody["notes"]
    ]


def fitness(genome: Genome, s: Server, num_bars: int, num_notes: int, num_steps: int,
            pauses: bool, key: str, scale: str, root: int, bpm: int) -> int:
    
    #metronome chosen is played as base of audio
    m = metronome(bpm)

    #genome turned into events, sent to pyo server that then generates the melody
    events = transevents(genome, num_bars, num_notes, num_steps, pauses, key, scale, root, bpm)
    for e in events:

        #starts playing melody 
        e.play()
    s.start()

    #rating is the user input
    rating = input("Rating (0-5)")

    
    for e in events:

        #after ending force pause
        e.stop()
    s.stop()
    time.sleep(1)

    try:
        rating = int(rating)

    #if cant parse input then error
    except ValueError:
        rating = 0

    #fitness value is returned as input by user
    return rating


#copied from the pyo documentation, introduces a ticking noise to give a referance for the speed of melody
def metronome(bpm: int):
    met = Metro(time=1 / (bpm / 60.0)).play()
    t = CosTable([(0, 0), (50, 1), (200, .3), (500, 0)])
    amp = TrigEnv(met, table=t, dur=.25, mul=1)
    freq = Iter(met, choice=[660, 440, 440, 440])
    return Sine(freq=freq, mul=amp).mix(2).out()


#to save the genome in midi, pass all parameters
def savemidi(filename: str, genome: Genome, num_bars: int, num_notes: int, num_steps: int,
                        pauses: bool, key: str, scale: str, root: int, bpm: int):
    
    #melody object
    melody = transmelody(genome, num_bars, num_notes, num_steps, pauses, key, scale, root)

    if len(melody["notes"][0]) != len(melody["beat"]) or len(melody["notes"][0]) != len(melody["velocity"]):
        raise ValueError

    #midifile class for generating midi save
    mf = MIDIFile(1)

    #give it one track, one channel, starting time  
    track = 0
    channel = 0

    time = 0.0

    #give it a track and a bpm
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, bpm)

    #iterate over all velocities and checks if not pause
    for i, vel in enumerate(melody["velocity"]):
        if vel > 0:

            #add all the notes for one melody step at time value
            for step in melody["notes"]:
                mf.addNote(track, channel, step[i], time, melody["beat"][i], vel)

        #time increased in melody beats
        time += melody["beat"][i]

    #folder created 
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    #file saved midi generated 
    with open(filename, "wb") as f:
        mf.writeFile(f)

#here is where i used click to prompt the CL to ask you for the parameters you would like to use
@click.command()
@click.option("--num-bars", default=6, prompt='Number of bars:', type=int)
@click.option("--num-notes", default=6, prompt='Notes per bar:', type=int)
@click.option("--num-steps", default=1, prompt='Number of steps:', type=int)
@click.option("--pauses", default=True, prompt='Would you like to add pauses?', type=bool)
@click.option("--key", default="C", prompt='Select your key:', type=click.Choice(keys, case_sensitive=False))
@click.option("--scale", default="major", prompt='Select your scale:', type=click.Choice(scales, case_sensitive=False))
@click.option("--root", default=4, prompt='Scale Root:', type=int)
@click.option("--population-size", default=8, prompt='mow many melodies per generation would you like:', type=int)
@click.option("--num-mutations", default=2, prompt='Number of mutations:', type=int)
@click.option("--mutation-probability", default=0.5, prompt='Mutations probability (0-1):', type=float)

#bpm is kept at default since users with no advanced knowledge of music would not know what to set it as
@click.option("--bpm", default=128, type=int)

#after passing parameters they are injected by this main function
def main(num_bars: int, num_notes: int, num_steps: int, pauses: bool, key: str, scale: str, root: int,
         population_size: int, num_mutations: int, mutation_probability: float, bpm: int):

    #the folder to store the midi files, name is timestamped in order for you to keep track of what take it was
    folder = str(int(datetime.now().timestamp()))

    #create a random set of genomes (melodies) of length bars*notes*bits ex: 2 bars and 8 notes in each bar and 4 bits as default = 64 
    population = [genMelody(num_bars * num_notes * bpn) for _ in range(population_size)]

    #starting pyo server, further explainied in 6.1 startup 
    s = Server().boot()

    #initialise population   
    popnum = 0

    #after first iteration is done, if user chooses n to continue, running is set to false and program ends
    running = True
    while running:

        #shuffle genomes generated so that no order of generation is in place 
        random.shuffle(population) 

        #to evaluate fitness, genome is passed to function and a tuple of genome and corresponding fitness is created
        fpop = [(genome, fitness(genome, s, num_bars, num_notes, num_steps, pauses, key, scale, root, bpm)) for genome in population]

        #sorting by best to worst by checking e (genome entry) and its corresponding fitness
        sorted_fpop = sorted(fpop, key=lambda e: e[1], reverse=True)

        #take the entry of sorted genome list 
        population = [e[0] for e in sorted_fpop]

        #take the first 2 elements of the population and add them into the next generation (elitism) 
        newgen = population[0:2]

        #selection of entries: if pop = 5, 5/2 =2.5 whole number = 2   2-1 = 1 so we do it for entry 0 & 1  
        for j in range(int(len(population) / 2) - 1):

            #this function goes into the population_fitness list 
            def fitness_lookup(genome):
                for e in fpop:

                    #searching for entry with the genome it wants
                    if e[0] == genome:

                        #once found returns the fitness value of that genome 
                        return e[1]
                return 0

            #selects 2 parents (pair) depending on the fitness_lookup function
            parents = selectparents(population, fitness_lookup)

            #crossover occuring
            offspring_a, offspring_b = spcross(parents[0], parents[1])
            offspring_a = mutation(offspring_a, num=num_mutations, probability=mutation_probability)
            offspring_b = mutation(offspring_b, num=num_mutations, probability=mutation_probability)

            #added to generation, new genomes is from elitism and crossover & mutation 
            newgen += [offspring_a, offspring_b]

        print(f"population {popnum} done")

        #this function takes the first genome of the population and it parameters
        events = transevents(population[0], num_bars, num_notes, num_steps, pauses, key, scale, root, bpm)

        #genome turned into events, sent to pyo server that then generates the melody
        for e in events:
            e.play()
        s.start()
        input("The best melody generated ♫") 

        #server ends playing melody once finished
        s.stop()
        for e in events:
            e.stop()

        #pause the program for 1.5 seconds after 
        time.sleep(1)

        #repeat to play second best tune
        events = transevents(population[1], num_bars, num_notes, num_steps, pauses, key, scale, root, bpm) 
        for e in events:
            e.play()
        s.start()
        input("The second best melody ♪")
        s.stop()
        for e in events:
            e.stop()

        time.sleep(1)

        print("saving the generated population…")

        #save function that takes the following parameters including index of population
        for i, genome in enumerate(population):
            savemidi(f"{folder}/{popnum}/{scale}-{key}-{i}.mid", genome, num_bars, num_notes, num_steps, pauses, key, scale, root, bpm)
        print("midi file has been saved") 

        #loops 'while running' again if user does not enter n 
        running = input("continue? [y/n]") != "n"
        population = newgen
        popnum += 1


if __name__ == '__main__':
    main()
    
