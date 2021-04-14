import string
import re

import xml.etree.ElementTree as et
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Patent:
    def __init__(self, patent_id):
        self.patentNumber = patent_id
        self.__process_xml()
		#Extract epitope information
        self.__extract_epitope_info()
        
    def __process_xml(self):
        tree = et.parse(self.patentNumber + '.xml')
        root = tree.getroot()
        logger.info("in __process_xml")
        self.patentName = root.find('.//invention-title').text
        self.patentDate = root.find('.//publication-reference').find('.//date').text
        self.inventors = [el.find('.//first-name').text + ' ' + 
                            el.find('.//last-name').text
                            for el in root.findall('.//inventor')]
        self.abstract = ' '.join([' '.join(el.itertext()) 
                            for el in root.findall('.//abstract')])
        self.description = ' '.join([' '.join(el.itertext()) 
                            for el in root.findall('.//description')])
        self.claims = [' '.join(el.itertext()) 
                            for el in root.findall('.//claim')]
        self.patentAssignees = [el.find('.//orgname').text 
                            for el in root.findall('.//assignee')]
        #self.applicants = [el.find('.//orgname').text
                                #for el in root.findall('.//us-applicant')]
        self.examiners = root.find('.//primary-examiner').find('.//first-name').text + ' ' + root.find('.//primary-examiner').find('.//last-name').text
        self.claimsCount = len(self.claims)
        self.appNumber = root.find('.//application-reference').find('.//doc-number').text
        self.appDate = root.find('.//application-reference').find('.//date').text

    #Extract epitope information
    def __extract_epitope_info(self):
        #US9574011
        bindingString = r'''([^.]*?antibody(.*)binds(.*)residues[^.]*\.)'''
        #US8829165
        #bindingString1 = r'''([^.]*?antibody binds to at least one of the following residues[^.]*\.)'''
        #US8859741
        #bindingString2 = r'''([^.]*?antibody binds an epitope on(.*)comprising at least one of residues[^.]*\.)'''
        #US8563698
        #bindingString3 = r'''([^.]*?antibody binds to at least one residue within the sequence set forth by residues[^.]*\.)'''
        #US10023654
        bindingString4 = r'''([^.]*?antibody(.*)binds(.*)residue[^.]*\.)'''
        
        #Regex
        bindingPattern = [re.compile(p) for p in [bindingString, bindingString4]]

        #claimedResidues array of dictionaries
        self.claimedResidues = []
        keysForSequences = ["seqNoId", "values"]
        keysForValues = ["num", "code"]
        
        lines = iter(self.claims)
        
        #Claimed as string
        for claimed in lines:
        
			#Find the required sentence with epitope info
			sentenceToEvaluate = ''
			for regex in bindingPattern:
				if re.findall(regex, claimed):
					sentenceToEvaluate = re.findall(regex, claimed)
			
			#If pattern not found - return
			if not sentenceToEvaluate:
				next(lines, None)
				continue
			
			sequencesDict = dict.fromkeys(keysForSequences)
			sentenceToEvaluate = ','.join(str(v) for v in sentenceToEvaluate)
			
			#Extract Seq ID
			extractedSeqID = ''.join(sentenceToEvaluate)
			if re.search(r'\bresidues\b', extractedSeqID):
				extractedSeqID = extractedSeqID.split("SEQ ID NO:")[1].split(".")[0].strip()
				extractedSeqID = extractedSeqID.split(",")[0].strip()
			else:
				extractedSeqID = extractedSeqID.split("(SEQ ID NO:")[1].split(").")[0].strip()

			listings = extractedSeqID.split()
			for l in listings:
				if l.isdigit():
					sequencesDict["seqNoId"] = l
			
			sequencesDict["values"] = []
			
			#Extract string with residues info
			extractedString = ''.join(sentenceToEvaluate)
			if re.search(r'\bresidues\b', extractedString):
				extractedString = extractedString.split("residues")[1].split("SEQ ID")[0]
			else:
				extractedString = extractedString.split("residue")[1].split("SEQ ID")[0]
			words = extractedString.split()
			for i in words:
				i = i.replace(',','')
				#if punctuation
				if i in string.punctuation:
					i = i.replace(':','')
				#if range of sequences
				elif i.find("-") != -1:
					rangeList = i.split("-")
					for n in range(int(rangeList[0]), int(rangeList[-1]) + 1):
						valuesDict = dict.fromkeys(keysForValues)
						valuesDict["num"] = int(n)
						sequencesDict["values"].append(valuesDict)
				#if mix of letters and digits
				elif (i.isalpha() == False) and (i.isdigit() == False) and (len(i) < 5 ):
					i = i[1:]
					valuesDict = dict.fromkeys(keysForValues)
					valuesDict["num"] = int(i)
					sequencesDict["values"].append(valuesDict)
				#if digital
				elif i.isdigit():
					valuesDict = dict.fromkeys(keysForValues)
					valuesDict["num"] = int(i)
					sequencesDict["values"].append(valuesDict)
			self.claimedResidues.append(sequencesDict)
