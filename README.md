# Disso-final-year
UWE Dissertation- Music Creation Using Generational Algorithms

Firstly install requirements, system uses pyo which is compatible best with python 3.6, 3.7, 3.8
we have some input parameters to feed the program in order for it to start generating. <br>
1- firstly we have to select the numbr of bars, in music a bar is considered as a segment of a song, it is used as a unit. <br>
2- notes per bar is how many notes are included per bar unit.<br>
3- number of steps is to decide how many notes you would want on top of one another, the output is either a chord or melody depending on steps <br>
4- introduce pauses between notes or not (boolean option) <br>
5-  there are different keys that  you can have the scale in, set on C for default <br>
6- a Scale is a group of notes of a similar frequency and pitch that sound good with one another which is set to major on default since C major is one of the most common scales used. <br>
7- Scale root depends on how high the melody should be. <br>
8- population size is how many melodies (genomes) are initially generated within the population <br>
9- number of mutations is how many notes are to be shifted around and in our case it will switch out the note with another randomly chosen note <br>
10- mutation probability is the probability that a chosen note will be switched out or kept as is, set to 0.5 (50%) on default so it acts as a coin flip to mutate the note or not. <br>
a metranome is added so that it gives the melody created some structure by adding a tick rate.
the midi files store each generation in a decending sort from best rated to worst rated
