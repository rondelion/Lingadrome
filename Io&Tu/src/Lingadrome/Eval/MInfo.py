'''
Created on 2016/12/08

@author: rondelion

MInfo.py
=====

This program calculate mutual information among data in Learner Log
of Io&Tu experiments.

'''

import sys
import math

def check_condition(features, cond_f, cond_v):
    if cond_f != '':
        for feature in features:
            kv = feature.split(':')
            if len(kv) == 2 and kv[0] == cond_f and kv[1] == cond_v:
                return True
        return False
    else:
        return True

if __name__ == '__main__':
    if len(sys.argv)<5:
        print "Usage: MInfo.py file start feat1 feat2 [feat:value]"
        quit()
    argvs = sys.argv
    llog = open(argvs[1])
    start = int(argvs[2])
    feat1 = argvs[3]
    feat2 = argvs[4]
    cond_f = ''
    cond_v = ''
    if len(sys.argv)>5:
        print "Constraint:", argvs[5]
        if ':' in argvs[5]:
            fv = argvs[5].split(':')
            cond_f = fv[0]
            cond_v = fv[1]
    cnt = 0
    feat1v = {}  # feature1 value counter
    feat2v = {}  # feature2 value counter
    featCn = {}  # feature 1 and 2 conjunction counter
    for line in llog:
        cnt += 1
        if cnt >= start:
            features = line.strip().split(',')
            if not check_condition(features, cond_f, cond_v):
                continue
            val1 = ''
            val2 = ''
            for feature in features:
                kv = feature.split(':')
                if len(kv)==2:
                    if kv[0] == feat1:
                        val1 = kv[1]
                    if kv[0] == feat2:
                        val2 = kv[1]
            if val1!= '' and val2!='':
                if feat1v.has_key(val1):
                    feat1v[val1] += 1
                else:
                    feat1v[val1] = 1
                if feat2v.has_key(val2):
                    feat2v[val2] += 1
                else:
                    feat2v[val2] = 1
                cnj = str(val1) + ':' + str(val2)
                if featCn.has_key(cnj):
                    featCn[cnj] += 1
                else:
                    featCn[cnj] = 1
    if cnt > start:
        total = cnt - start
        print str(cnt) + "(cnt) - " + str(start) + "(start) = " + str(total) + "(total)"
        tot = 0
        for k1 in feat1v:
            tot = tot + feat1v[k1]
        mi = 0.0
        for k1 in feat1v:
            for k2 in feat2v:
                cnj = str(k1) + ":" + str(k2)
                pCn = 0.0
                ppp = 0.0
                itm = 0.0
                if featCn.has_key(cnj):
                    pCn = float(featCn[cnj]) / float(tot)
                    # p(x,y) / (p(x) * p(y))
                    ppp = float(featCn[cnj] * tot)  / float(feat1v[k1] * feat2v[k2])
                    itm = pCn * math.log(ppp, 2.0)
                mi += itm
        print "Mutual Information between " + feat1 + " and " + feat2 + " is " + str(mi) + "."
    else:
        print "Line number " + str(cnt) + " is not larger than " + str(start) + "!"