from BitHash import * 
from BitVector import * 
import cityhash

class BloomFilter(object):
    # Return the estimated number of bits needed in a Bloom 
    # Filter that will store numKeys keys, using numHashes hash functions, 
    # and that will have a false positive rate of maxFalsePositive 
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        phi = 1 - (maxFalsePositive ** (1/numHashes))
        N = int(numHashes/(1-(phi ** (1/numKeys))))
        return N
    
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        self.__numKeys = numKeys
        self.__numHashes = numHashes
        self.__maxFalsePositive = maxFalsePositive
        self.__vectorSize = self.__bitsNeeded(numKeys, numHashes, maxFalsePositive)
        self.__bitsSet = 0
        self.__arr = BitVector(size = self.__vectorSize)    
        
    # Insert the specified key into the Bloom Filter, always succeeds
    def insert(self, key):
        for i in range(self.__numHashes):
            position = BitHash(key,i+1) % self.__vectorSize
            if not self.__arr[position]:
                self.__arr[position] = 1
                self.__bitsSet += 1
    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the Bloom filter.
    def find(self, key):
        for i in range(self.__numHashes):
            position = BitHash(key,i+1) % self.__vectorSize
            if not self.__arr[position]:
                return False
        return True
            
    # Returns the projected current false positive rate based on the
    # current number of bits actually set in this Bloom Filter. 
    def falsePositiveRate(self):
        phi = (1 - (self.__numHashes/self.__vectorSize)) ** self.__numKeys
        P = (1-phi) ** self.__numHashes
        return P 
       
    # Returns the current number of bits set in this Bloom Filter
    def numBitsSet(self):
        return self.__bitsSet
    
    # Returns the length of this Bloom Filter
    def __len__(self):
        return self.__vectorSize
       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    bloomFilter = BloomFilter (numKeys, numHashes, maxFalse)
    
    fin = open("wordlist.txt")
    words = [ ]
    for line in fin:
        words.append(line)
    fin.close()
    
    # Insert first numKeys words from the text file
    for i in range(numKeys):
        bloomFilter.insert(words[i])    

    # Print out what the projected false positive rate should be based on the 
    # number of bits that actually ended up being set in the Bloom Filter
    print(bloomFilter.falsePositiveRate() * 100)

    # Check how many words from the same first numKeys words are missing from 
    # the Bloom filter, which should be 0 --> checking for false negatives
    missingCount = 0
    for i in range(numKeys):
        if not bloomFilter.find(words[i]):
            missingCount += 1
    print(missingCount)

    # Check how many words from the next numKeys words from the text file are 
    # supposedly in the Bloom filter --> checking for false postivies
    falseCount = 0
    for i in range(numKeys,numKeys*2,1):
        if bloomFilter.find(words[i]):
            falseCount +=1
    # Using those false positives, print the real false positive rate
    print((falseCount/100000)*100)

    
if __name__ == '__main__':
    __main()       

