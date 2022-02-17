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
  r"/^1*0*(0+(1{3,})?)*1*$/",
  r"/^(?!.*010)(?!.*101)[01]*$/",
  r"/^([01])([01]*\1)?$/",
  r"/\b((\w)(?!\w*\2\w*))*\b/",
  r"/\b((\w)(?!\w*\2\b))+\b/",
  r"//",
  r"/\b([b-df-hj-np-tv-z]*(?=[aeiuo])(\w)(?!\w*\2)){5}\w*\b/",
  r"//",
  r"//",
  r"//"



]
print(regexLines[idx])
#Tommy Williams 7 2023
