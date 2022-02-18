import sys; args=sys.argv[1:]

###
#TASKS:
#Q60: Match all binary strings that do not contain the forbidden substring 010.  (14)
#Q61: Match all binary strings containing neither 101 nor 010 as substrings.  (20)
#Q62: Match on all non-empty binary strings with the same number of 01 substrings as 10 substrings.  (14)
#Q63: Match all words whose final letter is not to be found elsewhere in the word.  (21)  
#Q64: Match all words that have at least two pairs of doubled letters (two pairs of distinct letters or four of the same letter are both OK).  (43)
#Q65: Match all words that have no duplicate letter, except for one, which occurs at least 3 times.  (42)
#Q66: Match all words where each of the five vowels occurs exactly once.  (39)
#Q67: Match all binary strings that have an odd number of 0s and an even number of 1s.  (22)
#Q68: Match all binary integer strings that are divisible by 3.  (19)
#Q69: Match all binary integer strings that are not divisible by 3.  (19)
###

idx = int(args[0])-60
regexLines = [
  r"/^(0(?!10)|1)*$/",
  r"/^(0(?=10)|1(?=01))*$/",
  r"/^([01])([01]*\1)?$/",
  r"/\b((\w)(?!\w*\2\b))+\b/i",
  r"/\b\w*((\w)(?=\w*\2))\w*((\1\w*){3,}|(?!\2)(\w)(?=\w*\5)\w*)\b/i",
  r"/\b((\w)(?!\w*\2))*((\w)(?=(\w*\4\w*\4)))(\4|(\w)(?!\w*\7))*\b/i",
  r"/\b([^aeiuo\s]*(?=[aeiuo])(\w)(?!\w*\2)){5}\w*\b/",
  r"/^(?=0*(10*10*)*0*$)(?=1*01*(01*01*)*1*$)[01]*$/",
  r"/^1(01*0)*1(0|(1(01*0)*1))*$|^0$/",
  r"/^1(10*1|01*0)*(01*)?$/"



]
print(regexLines[idx])
#Tommy Williams 7 2023
