from algorithms.genetic import genMelody, spcross, genPop, mutation
import random
import unittest
from mgen import *
from mgen import transmelody, transevents

def test_genMelody():
    melody = genMelody(5)
    assert len(melody) == 5
    assert all(element in [0,1] for element in melody)


def test_genPop():
    population = genPop(10, 5)
    assert len(population) == 10
    assert all(len(genome) == 5 for genome in population)
    assert all(element in [0,1] for genome in population for element in genome)


def test_spcross():
    g1 = [1,0,1,0,1]
    g2 = [0,1,0,1,0]
    offspring1, offspring2 = spcross(g1, g2)
    assert len(offspring1) == len(offspring2) == len(g1) == len(g2)
    assert offspring1 != g1 and offspring1 != g2
    assert offspring2 != g1 and offspring2 != g2

def test_mutation():
    random.seed(1) 

    genome = [0, 0, 0, 0, 0, 0, 0, 0] 
    num_mutations = 2
    mutation_probability = 0.5

    mutated_genome = mutation(genome, num_mutations, mutation_probability)

    expected_genome = [1, 0, 1, 0, 1, 0, 1, 0] 

    assert mutated_genome == expected_genome, f"Expected {expected_genome} but got {mutated_genome}"


class TestMGen(unittest.TestCase):
    def setUp(self):
        self.genome = [0, 1, 0, 1, 1, 0, 1, 0]
        self.num_bars = 2
        self.num_notes = 4
        self.num_steps = 1
        self.pauses = False
        self.key = "C"
        self.scale = "major"
        self.root = 4
        self.bpm = 128

    def test_bitint(self):
        bits = [1, 0, 1]
        self.assertEqual(bitint(bits), 5)

    def test_transmelody(self):
        melody = transmelody(self.genome, self.num_bars, self.num_notes, self.num_steps, self.pauses, self.key, self.scale, self.root)

    def test_transevents(self): 
        events = transevents(self.genome, self.num_bars, self.num_notes, self.num_steps, self.pauses, self.key, self.scale, self.root, self.bpm)

    def test_savemidi(self):
        filename = "test_midi.mid"
        savemidi(filename, self.genome, self.num_bars, self.num_notes, self.num_steps, self.pauses, self.key, self.scale, self.root, self.bpm)

if __name__ == '__main__':
    unittest.main()
