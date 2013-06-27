import xapian
import string

MAX_PROB_TERM_LENGTH = 64

def p_alnum(c):
    return (c in string.ascii_letters or c in string.digits)

def p_notalnum(c):
    return not p_alnum(c)

def p_notplusminus(c):
    return c != '+' and c != '-'

def find_p(string, start, predicate):
    while start<len(string) and not predicate(string[start]):
        start += 1
    return start

database = xapian.WritableDatabase('test/', xapian.DB_CREATE_OR_OPEN)
stemmer = xapian.Stem("english")

#para = '''this is a testing'''
para = 'this is a test'
doc = xapian.Document()
doc.set_data(para)
pos = 0
i = 0
while i < len(para):
    i = find_p(para, i, p_alnum)
    j = find_p(para, i, p_notalnum)
    k = find_p(para, j, p_notplusminus)
    if k == len(para) or not p_alnum(para[k]):
        j = k
    if (j - i) <= MAX_PROB_TERM_LENGTH and j > i:
        #term = stemmer.stem_word(string.lower(para[i:j]))
        term = stemmer(string.lower(para[i:j]))
        doc.add_posting(term, pos)
        pos += 1
    i = j
database.add_document(doc)
