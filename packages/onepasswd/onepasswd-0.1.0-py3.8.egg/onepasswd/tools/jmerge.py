import json
import os
import sys
import colored
import time
import shutil
from onepasswd import ltlog

log = ltlog.getLogger('onepasswd.tools.jmerge')

def merge(fa, fb):
    log.debug(fa + ' ' + fb)
    shutil.copyfile(fa, fa + '.' + str(time.time()) + '.bck')
    ja, jb = {}, {}
    with open(fa, "r") as fpa:
        ja = json.load(fpa)
    with open(fb, "r") as fpb:
        jb = json.load(fpb)

    for keya, vala in ja.items():
        if keya not in jb:
            pass
        elif jb[keya] != vala:
            at = float(vala['time'])
            bt = float(jb[keya]['time'])
            if at < bt:
                print("%s [-] {%s: %s} %s" 
                    % (colored.fg('red'), 
                        keya, json.dumps(vala),
                        colored.attr('reset')))
                print("%s [+] {%s: %s} %s" 
                    % (colored.fg('green'), 
                        keya, json.dumps(jb[keya]),
                        colored.attr('reset')))
                ja[keya] = jb[keya]
            
    for keyb, valb in jb.items():
        if keyb not in ja:
            print("%s [+] {%s: %s} %s" 
                  % (colored.fg('green'), 
                     keyb, json.dumps(valb),
                     colored.attr('reset')))
            ja[keyb] = valb
    with open(fa, "w") as fpa:
        json.dump(ja, fpa)


def main():
    assert len(sys.argv) == 3
    merge(*sys.argv[1:])

if __name__ == "__main__":
    main()
