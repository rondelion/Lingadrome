'''
Created on 2016/12/06

@author: rondelion
'''

import sys

def sum(list):
    s = 0
    for x in list:
        s = s + x
    return s

if __name__ == '__main__':
    if len(sys.argv)!=8:
        print "Usage: Evaluator.py rlog.txt output.txt wsize step type mode choice"
        quit()
    argvs = sys.argv
    try:
        rlog = open(argvs[1])
    except:
        print "Error opening ", argvs[1]
    outp = open(argvs[2], 'w')
    wsize = int(argvs[3])
    step = int(argvs[4])
    if wsize <= 1:
        print "Wsize must be larger than 0."
        quit()
    if step <= 1:
        print "Step must not be negative."
        quit()
    if step < wsize:
        print "Wsize must be equal to or smaller than step."
        quit()
    type = argvs[5]
    mode = argvs[6]
    choice = argvs[7]
    print >> outp, "# wsize=", wsize, ", step=", step, ", type=", type, ", mode=", mode, ", choice=", choice
    cnt  = 0
    list = [0] * wsize
    next = step
    for line in rlog:
        buf = line.strip().split('\t')
        reward = int(buf[4])
        iter = int(buf[0])
        if iter >= next:
            avr = 0
            if cnt > 0:
                if cnt < wsize:
                    avr = float(sum(list)) / float(cnt)
                else:
                    avr = float(sum(list)) / float(wsize)
            print >> outp, "%d\t%f" % (next, avr)
            next = next + step
        if type == buf[1]:
            if mode == "*" or mode == buf[2]:
                if choice == "*" or choice == buf[3]:
                    list[cnt % wsize] = reward
                    cnt = cnt + 1