import sys
import json
import string
import re

# Extract epitope residues
class EpitopeExtractRegex:

    # Init the class
    def __init__(self, antigen, patentID, patentJson):
        self.antigen = antigen
        self.patentID = patentID
        self.patentJson = patentJson
        self.keyList = ["antigen", "patentID", "residuesPositionsMarked"]
        self.epitopeDictionary = dict.fromkeys(self.keyList)
        self.epitopeDictionary["antigen"] = antigen
        self.epitopeDictionary["patentID"] = patentID
        self.epitopeDictionary["residuesPositionsMarked"] = []
        self.bindingString = r'''([^.]*?An isolated monoclonal antibody, wherein, when bound to PCSK9, the monoclonal antibody binds to at least one of the following residues:[^.]*\.)'''
        self.bindingString1 = r'''([^.]*?An isolated monoclonal antibody that binds to PCSK9, wherein the isolated monoclonal antibody binds an epitope on PCSK9 comprising[^.]*\.)'''
        self.bindingString2 = r'''([^.]*?antibody to human PCSK9, wherein the antibody recognises an epitope on human PCSK9 comprising amino acid residues[^.]*\.)'''
        self.bindingPattern = [re.compile(p) for p in [self.bindingString, self.bindingString1, self.bindingString2]]
        self.outputJson = ''.join(("extracted", patentID, ".json"))

    # Load patent from json
    def loadJson(self):
        try:
            self.jsonfile = open(self.patentJson)
        except OSError:
            print("Could not open/read file:", self.patentJson)
            sys.exit()
        with self.jsonfile:
            self.data = self.jsonfile.read().replace('\n', '')
            return self.data

    # Find the relevant sentence
    def findRelevantSentence(self):
        for regex in self.bindingPattern:
            if re.findall(regex, self.data):
                self.sentenceToEvaluate = re.findall(regex, self.data)
        return self.sentenceToEvaluate

    # Preprocess the required string
    def extractWords(self):
        self.extractedString = ''.join(self.sentenceToEvaluate).split("residues")[1].split("SEQ ID")[0]
        self.extractedString = self.extractedString.replace('PCSK9', '')
        self.words = self.extractedString.split()
        return self.words

    # Fill the dictionary
    def fillEpitopeDict(self):
        for i in self.words:
            i = i.replace(',', '')
            # if punctuation
            if i in string.punctuation:
                i = i.replace(':', '')
            # if range of sequences
            elif i.find("-") != -1:
                rangeList = i.split("-")
                for n in range(int(rangeList[0]), int(rangeList[-1]) + 1):
                    self.epitopeDictionary["residuesPositionsMarked"].append(int(n))
            # if mix of letters and digits
            elif (i.isalpha() == False) and (i.isdigit() == False):
                i = i[1:]
                self.epitopeDictionary["residuesPositionsMarked"].append(int(i))
            # if digital
            elif i.isdigit():
                self.epitopeDictionary["residuesPositionsMarked"].append(int(i))


    # Write epitope dictionary to json file
    def epitopeDictToJson(self):
        with open(self.outputJson, 'w') as outputJson:
            json.dump(self.epitopeDictionary, outputJson)

if __name__ == '__main__':
    evaluatedPatent = EpitopeExtractRegex(sys.argv[1], sys.argv[2], sys.argv[3])
    evaluatedPatent.loadJson()
    evaluatedPatent.findRelevantSentence()
    evaluatedPatent.extractWords()
    evaluatedPatent.extractWords()
    evaluatedPatent.fillEpitopeDict()
    evaluatedPatent.epitopeDictToJson()
