#  Created by Julia Fisher
#  7/20/11
#  Last modified:  4/18/2015 by Josh Meyer

#  Description:
#  This program takes in a folder, reads systematically through the folder,
#  and produces a text file of information that can be read into R in order to
#  perform a SSANOVA.

#  The folder must be set up in the following manner:
#  The main folder contains separate folders of words.  Each
#  word folder contains some subfolders (plus some other stuff -- random files).
#  One of the subfolders must contain the two vowel tokens from the first
#  repetition of the word.  The other two (or three or more) must contain
#  head-corrected versions of the vowel tokens from repetitions of the word.
#  These will be preceeded by NEW_.

#  Example:
#  Subject15/
#		airgead/
#			airgead1/
#				file1.txt
#				file2.txt
#			airgead2/
#				NEW_file1.txt
#				NEW_file2.txt
#			airgead3/
#				NEW_file1.txt
#				NEW_file2.txt
#		airm/
#			airm1/
#				file1.txt
#				file2.txt
#			airm2/
#				NEW_file1.txt
#				NEW_file2.txt
#			airm3/
#				NEW_file1.txt
#				NEW_file2.txt

import os

def produce_SSANOVA_file(mainDirPath, outFilePath):
    
    wordDirs = os.listdir(mainDirPath)                                          # This opens the main folder.

                                                                                # Create the output file that will be written to 
                                                                                # throughout the script. There is one outputfile per
                                                                                # subject.  It outputs the data in the form needed by
                                                                                # the SSANOVA script.

    outFile = open(outFilePath, 'w')
    outFile.write('word\ttoken\tX\tY\n')                                        # This is the header line of the output file.
    
                                                                                # Now, go through the main folder and find the needed
                                                                                # .traced.txt files and write them appropriately
                                                                                # to the output file.
    for word in wordDirs:                                                       # the label of wordDir is the word itself
                                                                                # AKA, what goes in the 'word' column of output file.
        wordDir = mainDirPath + '/' + word
        if os.path.isdir(wordDir):
            wordRepDirs = os.listdir(wordDir)
            for wordRepDir in wordRepDirs:
                if os.path.isdir(wordDir + '/' + wordRepDir):
                    tokenNum = ''                                               # The tokennum is the number after the word.
                                                                                # So, the folder airgead1
                    i = 0                                                       # would contain all tokens 1 of the two vowels.  
                                                                                # Also, tokenNum is token in the output.
                    while i < len(wordRepDir):
                        if wordRepDir[i].isalpha() == False:                    # path doesn't consist only of alphabetic characters
                            tokenNum = tokenNum + wordRepDir[i]
                            i += 1
                        else:
                            i += 1
                    vowelTokens = os.listdir(wordDir + '/' + wordRepDir)
                    vowels = []                                                 # a list in which to hold V1 and V2
                    NEW = None
                    for fileName in vowelTokens:                                # where fileName is possibly a vowel
                        if 'C1' in fileName or 'C2' in fileName:
                            pass
                        elif 'NEW' in fileName:
                            NEW = 'Yes'
                            vowels.append(wordDir + '/' + wordRepDir + '/' + 
                                          fileName)
                    if vowels == []:                                            # If vowels is empty, then we're in rep. 1.  
                                                                                # Just add the items in it to vowels.  
                        for fileName in vowelTokens:
                            vowels.append(wordDir + '/' + wordRepDir + '/' + 
                                          fileName)

                    if vowels != []:                                            # if the vowel tokens were in fact there,
                                                                                # check which of the two vowel files is the
                                                                                # first (i.e. the lower number)
                        vowela = vowels[0].rsplit('_', 1)[1].split('.')[0]      # These *should* be the frame numbers.
                        vowelb = vowels[1].rsplit('_', 1)[1].split('.')[0]      # This tells us which vowel is the first and 
                                                                                # which is the second.

                        if vowela < vowelb:
                            V1 = vowels[0]
                            V2 = vowels[1]
                        else:
                            V1 = vowels[1]
                            V2 = vowels[0]

                        v1 = open(V1, 'r').readlines()                          # Read through v1
                        for line in v1:
                            data = line.split()
                            if data[0] == '-1':                                 # get rid of -1 lines
                                pass
                            else:
                                if NEW == 'Yes':
                                    one = (str(round(float(data[1]))
                                           ).split('.')[0] + '.00')
                                    two = (str(round(float(data[2]))
                                           ).split('.')[0] + '.00')
                                else:
                                    one = data[1]
                                    two = data[2]
                                outFile.write(wordDir + 'V1\t' + tokenNum + 
                                              '\t' + one + '\t' + two + '\n')

                        v2 = open(V2, 'r').readlines()                          # Now, do the same for v2

                        for line in v2:
                            data = line.split()
                            if data[0] == '-1':
                                pass
                            else:
                                if NEW == 'Yes':
                                    one = (str(round(float(data[1]))
                                           ).split('.')[0] + '.00')
                                    two = (str(round(float(data[2]))
                                           ).split('.')[0] + '.00')
                                else:
                                    one = data[1]
                                    two = data[2]
                                outFile.write(wordDir + 'V2\t' + tokenNum + 
                                              '\t' + one + '\t' + two + '\n')

    outFile.close()


produce_SSANOVA_file('/Users/apiladmin/Desktop/GaelicEpenthesisHC/GaelicS8', 
'/Users/apiladmin/Desktop/GaelicEpenthesisHC/GaelicS8/GaelicS8_SSANOVAfile3.txt')
                                
                                
                            
                        
                        
                        
        

    
