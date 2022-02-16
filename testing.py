


l = 3
occurences = [{"diatermi":0, "forceps":0,"head":0,"scalpel":0,"needle driver":0, "retractor":0, "hl tube":0, "saw":0} for x in range(l)]
print(occurences)
occurences[1]["scalpel"] +=1
print(occurences)

print(min(0,-1))

import subprocess 

s = "afff,befff"
print(s.split(","))