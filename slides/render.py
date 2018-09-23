import sys
import subprocess

filename = sys.argv[1]
infile = open(filename, 'r')
outfile = open('out.html', 'w')

cmd = "cat"
cmd = "goat"

for l in infile:
    if l.startswith('diagram:'):
        if len(l.split(' ')) != 2:
            print('bad line {}'.format(l))
        diagram = 'diagrams/{}'.format(l.split(' ')[1].strip())

        result = subprocess.run([cmd, diagram], stdout=subprocess.PIPE, encoding='utf-8')
        if result.returncode == 0:
            count = 0
            outfile.write('.center[\n')
            for o in result.stdout.split('\n'):
            #    print('    ' + o)
                outfile.write(o + '\n')
            outfile.write(']\n')
        else:
            for o in result.stdout:
                print(o, end='')
            outfile.write(l)
    else:
        outfile.write(l)

infile.close()
outfile.close()
