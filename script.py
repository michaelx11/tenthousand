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

def count(word, letters):
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
  maxmarked = (len(word) + 2) * [0]
  for i in range(len(word)):
    if word[i:i + 2] in code_dict:
      maxmarked[i + 3] = max(maxmarked[:i + 1]) + 2
  return max(maxmarked)

def isoAlpha2Percent(word):
  maxmarked = (len(word) + 2) * [0]
  for i in range(len(word)):
    if word[i:i + 2] in code_dict:
      maxmarked[i + 3] = max(maxmarked[:i + 1]) + 2
  return 100.0 * max(maxmarked) / len(word)

def postalCodeCount(word):
  maxmarked = (len(word) + 2) * [0]
  for i in range(len(word)):
    if word[i:i + 2] in postalcodes:
      maxmarked[i + 3] = max(maxmarked[:i + 1]) + 2
  return 1.0 * max(maxmarked) / len(word)

instructions = {
'Contains: $word':
lambda word, args: args[0] in word,

'Ends with: $word':
lambda word, args: word[-len(args[0]):] == args[0],

'Sum of letters (A=1, B=2, etc): between $val and $val (inclusive)':
lambda word, args: between(find_lettersum(word), args[0], args[1]),

'Sum of letters (A=1, B=2, etc): $val':
lambda word, args: find_lettersum(word) == args[0],

'Vowels: between $val% and $val% (inclusive)':
lambda word, args: between(100.0 * count(word, 'AEIOU') / len(word), args[0], args[1]),

'Base Scrabble score: $val points':
lambda word, args: scrab_val(word) == args[0],

'Sum of letters (A=1, B=2, etc) is divisible by $val: $bool':
lambda word, args: find_lettersum(word) % args[0] == args[1],

'Most common vowel(s) each account(s) for: between $val% and $val% (inclusive) of the letters':
lambda word, args: between(100.0 * max([count(word, c) for c in 'AEIOU']) / len(word), args[0], args[1]),

'Letters located in the middle row on a QWERTY keyboard: between $val% and $val% (inclusive) of the letters':
lambda word, args: between(100.0 * count(word, 'ASDFGHJKL') / len(word), args[0], args[1]),

'Letters located in the bottom row on a QWERTY keyboard: $val':
lambda word, args: count(word, 'ZXCVBNM') == args[0],

'Word interpreted as a base 26 number (A=0, B=1, etc) is divisible by $val: $bool':
lambda word, args: (to_base26(word) % args[0] == 0) == args[1],

'Starts with a vowel: $bool':
lambda word, args: (word[0] in 'AEIOU') == args[0],

'Vowels: $val':
lambda word, args: count(word, 'AEIOU') == args[0],

'Vowels: between $val and $val (inclusive) of the letters':
lambda word, args: between(count(word, 'AEIOU'), args[0], args[1]),

'Contains at least one doubled letter: $bool':
lambda word, args: has_double == args[0],

'Word interpreted as a base 26 number (A=0, B=1, etc) is representable as an unsigned 32-bit integer: $bool':
lambda word, args: (to_base26(word) < (2 ** 32)) == args[0],

'Has property QAKAREIBI: $bool':
lambda word, args: True,  # TODO

'SHA-1 hash of lowercased word, expressed in hexadecimal, starts with: $word':
lambda word, args: (sha_1(word)[:2] == args[0]),

'If you marked nonoverlapping officially-assigned ISO 3166-1 alpha-2 country codes, you could mark at most: $val letters':
lambda word, args: (isoAlpha2(word) <= args[0]),

'If you marked nonoverlapping officially-assigned ISO 3166-1 alpha-2 country codes, you could mark at most: between $val% and $val% (inclusive) of the letters':
lambda word, args: (args[0] <= isoAlpha2Percent(word) and isoAlpha2Percent(word) <= args[1]),

'If you marked nonoverlapping US state postal abbreviations, you could mark at most: $val letters':
lambda word, args: (postalCodeCount(word) <= args[0]),
}

filters = {}
for instruct in instructions:
    args = re.findall('(\$[a-z]+)', instruct)
    s = instruct
    s = s.replace('(', '\(')
    s = s.replace(')', '\)')
    s = s.replace('$word', '([A-Z]+)')
    s = s.replace('$val', '([0-9\.]+)')
    s = s.replace('$bool', '([A-Z]+)')
    filters[re.compile(s)] = (args, instructions[instruct])

def find_filter(instruct):
    for filt in filters:
        args, func = filters[filt]
        match = filt.search(instruct)
        if match != None and len(match.groups()) == len(args):
            groups = list(match.groups())
            for i, arg in enumerate(args):
                if arg == '$word':
                    pass
                elif arg == '$val':
                    groups[i] = float(groups[i])
                elif arg == '$bool':
                    groups[i] = (groups[i] == 'YES')
            print filt.pattern
            return groups, func

words = set()
for line in open('words.txt'):
    words.add(line.strip().upper())
for line in open('dircontents', 'r'):
    os.chdir(line.strip())
    os.system('pwd')
    filename = line.strip()
    for filename in os.listdir('.'):
        if filename == 'words.txt' or 'DS_Store' in filename or 'sw' in filename:
            continue

        match = fname_r.search(filename)
        row, col = match.group(1), match.group(2)

        print filename
        valid_words = list(words)
        for line in open(filename).readlines():
            result = find_filter(line)
            if not result:
                print 'Error: not found', line
                exit(1)
            groups, func = result
            valid_words = filter(lambda x: func(x, groups), valid_words)
        print valid_words
    os.chdir('..')
