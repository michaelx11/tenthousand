import fnmatch, os, re, sha

fname_r = re.compile('row(\d+)_col(\d+)\.txt')

postalcodes = set(['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY'])

def between(val, low, high):
    return val >= low and val <= high

def find_lettersum(word):
    return sum([ord(c) - ord('A') + 1 for c in word])

def to_base26(word):
    val = 0
    for c in word:
        val += ord(c) - ord('A')
        val *= 26
    return val

def countOccurences(word, letters):
    return sum([c in letters for c in word])

def scrab_val(word):
    scores = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10]
    return sum([scores[ord(c) - ord('A')] for c in word])

def has_double(word):
    for i in xrange(1, len(word)):
        if word[i - 1] == word[i]:
            return True
    return False

def sha_1(word):
  return sha.new(word.lower()).hexdigest().upper()

code_dict = set()
f = open('3166-2.txt')
for line in f:
  code_dict.add(line.strip().upper())

def isoAlpha2(word):
  maxmarked = (len(word) + 4) * [0]
  for i in range(len(word)):
    if word[i:i + 2] in code_dict:
      maxmarked[i + 3] = max(maxmarked[:i + 1]) + 2
  return max(maxmarked)

def isoAlpha2Percent(word):
  maxmarked = (len(word) + 4) * [0]
  for i in range(len(word)):
    if word[i:i + 2] in code_dict:
      maxmarked[i + 3] = max(maxmarked[:i + 1]) + 2
  return 100.0 * max(maxmarked) / len(word)

def postalCodeCount(word):
  maxmarked = (len(word) + 4) * [0]
  for i in range(len(word)):
    if word[i:i + 2] in postalcodes:
      maxmarked[i + 3] = max(maxmarked[:i + 1]) + 2
  return max(maxmarked)

def countNot(word, letters):
  return sum([c not in letters for c in word])

def countMostCommon(word, letters):
  d = {}
  for x in filter(lambda y: y in letters, set(word)):
    if x not in d:
      d[x] = 1
    else:
      d[x] += 1
  return max(d.values() + [0])

def countMostCommonNot(word, letters):
  d = {}
  for x in filter(lambda y: y not in letters, set(word)):
    if x not in d:
      d[x] = 1
    else:
      d[x] += 1
  return max(d.values() + [0])

def canAnagram(word):
    return ''.join(sorted(word)) in sortedStrings

def canAddOneAnagram(word):
  for i in range(65, 65 + 26):
    if ''.join(sorted(word + chr(i))) in sortedStrings:
      return True
  return False

def canAddTwoAnagram(word):
    for i in range(65, 65 + 26):
        for j in range(65, 65 + 26):
            if ''.join(sorted(word + chr(i) + chr(j))) in sortedStrings:
                return True
    return False

def distinctLetters(word, letters):
    return len(set(letter for letter in word if letter in letters))

instructions = {
'Contains: $word':
lambda word, args: args[0] in word,

'Starts with: $word':
lambda word, args: word.startswith(args[0]),

'Ends with: $word':
lambda word, args: word.endswith(args[0]),

'Length: between $val and $val (inclusive) letters':
lambda word, args: between(len(word), args[0], args[1]),

'Sum of letters (A=1, B=2, etc): between $val and $val (inclusive)':
lambda word, args: between(find_lettersum(word), args[0], args[1]),

'Sum of letters (A=1, B=2, etc): $val':
lambda word, args: find_lettersum(word) == args[0],

'Vowels: between $val% and $val% (inclusive)':
lambda word, args: between(100.0 * countOccurences(word, 'AEIOU') / len(word), args[0], args[1]),

'Vowels: between $val and $val (inclusive)':
lambda word, args: between(countOccurences(word, 'AEIOU'), args[0], args[1]),

'Base Scrabble score: $val points':
lambda word, args: scrab_val(word) == args[0],

'Base Scrabble score: between $val and $val (inclusive) points':
lambda word, args: between(scrab_val(word), args[0], args[1]),

'Sum of letters (A=1, B=2, etc) is divisible by $val: $bool':
lambda word, args: find_lettersum(word) % args[0] == args[1],

'Most common vowel(s) each account(s) for: between $val% and $val% (inclusive) of the letters':
lambda word, args: between(100.0 * max([countOccurences(word, c) for c in 'AEIOU']) / len(word), args[0], args[1]),

'Letters located in the middle row on a QWERTY keyboard: between $val% and $val% (inclusive) of the letters':
lambda word, args: between(100.0 * countOccurences(word, 'ASDFGHJKL') / len(word), args[0], args[1]),

'Letters located in the bottom row on a QWERTY keyboard: $val':
lambda word, args: countOccurences(word, 'ZXCVBNM') == args[0],

'Letters located in the top row on a QWERTY keyboard: $val':
lambda word, args: countOccurences(word, 'QWERTYUIOP') == args[0],

'Letters located in the top row on a QWERTY keyboard: between $val and $val (inclusive)':
lambda word, args: between(countOccurences(word, 'QWERTYUIOP'), args[0], args[1]),

'Letters located in the top row on a QWERTY keyboard: exactly $val% of the letters':
lambda word, args: 100.0 * countOccurences(word, 'QWERTYUIOP') / len(word) == args[0],

'Letters located in the top row on a QWERTY keyboard: between $val% and $val% (inclusive) of the letters':
lambda word, args: between(100.0 * countOccurences(word, 'QWERTYUIOP') / len(word), args[0], args[1]),

'Word interpreted as a base 26 number (A=0, B=1, etc) is divisible by $val: $bool':
lambda word, args: (to_base26(word) % args[0] == 0) == args[1],

'Starts with a vowel: $bool':
lambda word, args: (word[0] in 'AEIOU') == args[0],

'Vowels: $val':
lambda word, args: countOccurences(word, 'AEIOU') == args[0],

'Vowels: between $val and $val (inclusive) of the letters':
lambda word, args: between(countOccurences(word, 'AEIOU'), args[0], args[1]),

'Contains at least one doubled letter: $bool':
lambda word, args: has_double == args[0],

'Word interpreted as a base 26 number (A=0, B=1, etc) is representable as an unsigned 32-bit integer: $bool':
lambda word, args: (to_base26(word) < (2 ** 32)) == args[0],

'Word interpreted as a base 26 number (A=0, B=1, etc) is exactly representable in IEEE 754 single-precision floating point format: $bool':
lambda word, args: (to_base26(word) < (2 ** 53)) == args[0],

'SHA-1 hash of lowercased word, expressed in hexadecimal, starts with: $string':
lambda word, args: (sha_1(word).startswith(args[0])),

'SHA-1 hash of lowercased word, expressed in hexadecimal, contains: $string':
lambda word, args: (args[0] in sha_1(word)),

'SHA-1 hash of lowercased word, expressed in hexadecimal, ends with: $string':
lambda word, args: (sha_1(word).endswith(args[0])),

'If you marked nonoverlapping officially-assigned ISO 3166-1 alpha-2 country codes, you could mark at most: $val letters':
lambda word, args: (isoAlpha2(word) <= args[0]),

'If you marked nonoverlapping officially-assigned ISO 3166-1 alpha-2 country codes, you could mark at most: between $val% and $val% (inclusive) of the letters':
lambda word, args: (args[0] <= isoAlpha2Percent(word) and isoAlpha2Percent(word) <= args[1]),

'If you marked nonoverlapping US state postal abbreviations, you could mark at most: $val letters':
lambda word, args: (postalCodeCount(word) <= args[0]),

'Most common consonant(s) each account(s) for: between $val% and $val% (inclusive) of the letters':
lambda word, args: between(100.0 * countMostCommonNot(word, 'AEIOU') / len(word), args[0], args[1]),

'Most common consonant(s) each appear(s): $val times':
lambda word, args: countMostCommonNot(word, 'AEIOU') == args[0],

'Most common letter(s) each account(s) for: between $val% and $val% (inclusive) of the letters':
lambda word, args: between(100.0 * countMostCommonNot(word, '') / len(word), args[0], args[1]),

'Has at least one anagram that is also in the word list: $bool':
lambda word, args: canAnagram(word) == args[0],

'Can be combined with one additional letter to produce an anagram of something in the word list: $bool':
lambda word, args: canAddOneAnagram(word) == args[0],

'Can be combined with two additional letters to produce an anagram of something in the word list: $bool':
lambda word, args: True,  # TODO

'Length: $val':
lambda word, args: len(word),

'Distinct letters: $val':
lambda word, arg: distinctLetters(word, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ') == args[0],

'Distinct vowels: $val':
lambda word, arg: distinctLetters(word, 'AEIOU') == args[0],

'Distinct consonants: $val':
lambda word, args: distinctLetters(word, 'BCDFGHJKLMNPQRSTVWXYZ') == args[0],

'If you marked nonoverlapping occurrences of words in the word list that are 3 or fewer letters long, you could mark at most: between $val% and $val% (inclusive) of the letters':
lambda word, args: True,  # TODO

'If you marked nonoverlapping occurrences of words in the word list that are 3 or fewer letters long, you could mark at most: $val letters':
lambda word, args: True,  # TODO

'If you marked nonoverlapping chemical element symbols (atomic number 112 or below), you could mark at most: between $val% and $val% (inclusive) of the letters':
lambda word, args: True,  # TODO

'If you marked nonoverlapping officially-assigned ISO 3166-1 alpha-2 country codes, you could mark at most: between $val and $val (inclusive) letters':
lambda word, args: True,  # TODO

'Has property $word: $bool':
lambda word, args: True,  # TODO

'This is NOT a word with property $word.':
lambda word, args: True,  # TODO

'This is a word with property $word.':
lambda word, args: True,  # TODO

'This word is associated with the concept $word.':
lambda word, args: True,  # TODO

}

# Stores the filters, where the keys are compiled regex, and values are (args, func(word, args)->bool).
filters = {}
for instruct in instructions:
    args = re.findall('(\$[a-z]+)', instruct)
    s = instruct
    s = s.replace('(', '\(')
    s = s.replace(')', '\)')
    s = s.replace('$word', '([A-Z]+)')
    s = s.replace('$val', '([0-9\.]+)')
    s = s.replace('$bool', '([A-Z]+)')
    s = s.replace('$string', '([\w]+)')
    filters[re.compile(s)] = (args, instructions[instruct])

def find_filter(instruct):
    for filt in filters:
        args, func = filters[filt]
        match = filt.search(instruct)
        if match != None and len(match.groups()) == len(args):
            groups = list(match.groups())
            for i, arg in enumerate(args):
                if arg == '$word' or arg == '$string':
                    pass
                elif arg == '$val':
                    groups[i] = float(groups[i])
                elif arg == '$bool':
                    groups[i] = (groups[i] == 'YES')
            #print filt.pattern
            return groups, func

words = set()

for line in open('pyramid/words.txt'):
    words.add(line.strip().upper())

sortedStrings = set(map(lambda x: ''.join(sorted(x)), words))

for filename in os.listdir('pyramid'):
    if filename in ('examples', 'words.txt'):
        continue
    row_path = 'pyramid/%s' % filename
    for filename in os.listdir(row_path):
        match = fname_r.search(filename)
        row, col = match.group(1), match.group(2)
        file_path = '%s/%s' % (row_path, filename)

        # Narrow down the valid words.
        valid_words = list(words)
        for line in open(file_path).readlines():
            if line[-1] != '\n':
                raise
            if not line.strip():
                # blank line
                continue
            result = find_filter(line)
            if not result:
                print 'Error: not found', line
                exit(1)
            groups, func = result
            print line
            valid_words = filter(lambda x: func(x, groups), valid_words)
            print len(valid_words)
        print valid_words
        break
