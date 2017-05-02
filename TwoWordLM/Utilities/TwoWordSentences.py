'''
Created on 2017/04/10

@author: rondelion
'''
import sys
import random
import os

if __name__ == '__main__':
    if len(sys.argv)<3:
        print "Usage: TwoWordSentences.py outfile size"
        quit()
    outfile = open(sys.argv[1], 'w')
    for i in range(0, int(sys.argv[2])):
        subject = random.choice(['Tu', 'Luca', 'Io', 'Mario'])
        verb = random.choice(['gira', 'veni', 'vade'])
        sentence = subject + " " + verb # + "."
        print >> outfile, sentence
    outfile.close()
