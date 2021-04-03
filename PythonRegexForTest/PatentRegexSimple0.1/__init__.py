import sys
import json
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
        self.bindingPattern = re.compile(self.bindingString)
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
        self.sentenceToEvaluate = re.findall(self.bindingPattern, self.data)
        return self.sentenceToEvaluate

    # Preprocess the required string
    def extractWords(self):
        self.extractedString = ''.join(self.sentenceToEvaluate).split("residues:")[1].split("SEQ ID")[0]
        self.words = self.extractedString.split()
        return self.words

    # Fill the dictionary
    def fillEpitopeDict(self):
        for i in self.words:
            i = i.replace(',', '')
            if (i.isalpha() == False) and (i.isdigit() == False):
                i = i[1:]
                self.epitopeDictionary["residuesPositionsMarked"].append(i)

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
