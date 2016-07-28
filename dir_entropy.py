import os
import sys
import math
import random
import operator
import stat

FAILURE = -1
 
class BufferedEntropy:
  def __init__(self):
    self.n = [0]*256
    self.H = 0.0
    self.totalStreamLength = 0

  def addToStream(self, buf):
    if len(buf) == 0:
      return
  
    self.totalStreamLength += len(buf)
    #COUNT THE OCCURANCE OF EACH SYMBOL
    for i in buf:
      self.n[ord(i)] += 1

  def calcEntropy(self):
    # SUMMATION OF P_i*Log2(P_i) FOR EACH SYMBOL THAT HAS AN OCCURANCE
    for x in xrange(256):
      prob = float(self.n[x])/self.totalStreamLength
      if self.n[x] != 0:
        self.H += -( prob * math.log(prob, 2) )

  def getEntropy(self):
    return self.H


def main():
  BUFSIZE = 4096

  if len(sys.argv) != 2:
    sys.stderr.write("python %s <dir>\n" % sys.argv[0])
    sys.exit(-1)

  rootdir = sys.argv[1]

  countTotalFiles = 0
  countFilesProcessed = 0
  entropyTotal = 0.0

  for root, subFolders, files in os.walk(rootdir):
    for file in files:

      try:
        path = os.path.join(root,file)

        file_stats = os.lstat(path)
        mode = file_stats.st_mode
			
        if stat.S_ISREG(mode):

          fp = open(path, "rb")

          be = BufferedEntropy()
          buf = fp.read(BUFSIZE)
          if len(buf) != 0:
            while len(buf) > 0:
              be.addToStream(buf)
              buf = fp.read(BUFSIZE)
      
            be.calcEntropy()
            e = be.getEntropy()          

            entropyTotal += e

          fp.close() 

          countFilesProcessed += 1

      except IOError as e:
        sys.stderr.write("I/O error({0}): {1}\n".format(e.errno, e.strerror))
        
      countTotalFiles += 1

  print "countTotalFiles\tcountFilesProcessed\tavg_entropy_bpb"
  print "{0}\t{1}\t{2}".format(countTotalFiles, countFilesProcessed, float(entropyTotal) / float(countFilesProcessed))

if __name__ == "__main__":
  main()
  
