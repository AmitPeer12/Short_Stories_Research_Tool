# Map bitmasks returned by Meni Adler's tagger into readable tags.
# Yoav Goldberg 2008
from collections import defaultdict
import codecs, sys

MASKS = {
    'PREFIX':     0x756, # ^ 0x4,     # 0x756 ^ DEF
    'POS':        0x1F0000,           # bits 17-21
    'GENDER':     0x0000000000600000, # bits 22-23
    'NUMBER':     0x7000000,          # bits 25-27
    'PERSON':     0x38000000,         # bits 28-30
    'STATUS':     0x00000000c0000000, # bits 31-32
    'TENSE':      0xE00000000,        # bits 34-36
    'SUFFIX':     0x0000fdb000000000, # bits 37-38, 40-41, 43-48
    'SUFF_FUNC':  0x0000003000000000, # bits 37-38
    'SUFF_GEN':   0x0000018000000000, # bits 40-41

    'SUFF_NUM':   0x1c0000000000,     # bits 43-45
    'SUFF_PERS':  0xE00000000000,     # bits 46-48
    'CONT':       0x1000000000000,    # bits 49
    'POLARITY':   0x6000000000000,    # bits 50-51
    'BINYAN':     0x0038000000000000, # bits 52-54 base form BINYAN
    'CONJ_TYPE':  0x00c0000000000000, # bits 55-56 base form conjunction type
    'PRON_TYPE':  0x0700000000000000, # bits 57-59 base form pronoun type
    'NUM_TYPE':   0x0000000000007000, # bits 13-15 @NEW

    'INTERROGATIVE_TYPE': 0x0001004000000020, # bits 6,39,49 @NEW
    'QUANTIFIER_TYPE'   : 0x0000000100800000, # bits 24,33 @NEW
    }

POS = {
    'ADJECTIVE':         0x0000000000010000,
    'ADVERB':            0x0000000000020000,
    'CONJUNCTION':       0x0000000000030000,
    'AT_PREP':           0x0000000000040000, # NOT IN MILA
    'NEGATION':          0x0000000000050000,
    'NOUN':              0x0000000000060000,
    'NUMERAL':           0x0000000000070000,
    'PREPOSITION':       0x00000000000080000,
    'PRONOUN':           0x0000000000090000,
    'PROPERNAME':        0x00000000000a0000,
    #'PARTICLE':          0x00000000000b0000, # NOT USED
    #'AUXVERB':           0x00000000000c0000, # NOT USED
    'VERB':              0x00000000000d0000,
    'PUNCTUATION':       0x00000000000e0000,
    'INTERROGATIVE':     0x00000000000f0000,
    'INTERJECTION':      0x0000000000100000,
    'UNKNOWN':           0x0000000000110000,
    'QUANTIFIER':        0x0000000000120000,
    'EXISTENTIAL':       0x0000000000130000,
    'MODAL':             0x0000000000140000,
    'PREFIX':            0x0000000000150000,
    'URL':               0x0000000000160000,
    'FOREIGN':           0x0000000000170000,
    'JUNK':              0x0000000000180000,
    #'IMPERSONAL':        0x0000000000190000, # NOT USED
    'PARTICIPLE':        0x00000000001a0000,
    'COPULA':            0x00000000001b0000,
    'NUMEXP':            0x00000000001c0000,
    'TITULA':            0x00000000001d0000,
    'SHEL_PREP':         0x00000000001e0000, # NOT IN MILA
    }

GENDER={
    'M':  0x0000000000200000,
    'F':0x0000000000400000,
    'MF':0x0000000000600000,
    }
NUMBER={
    'S':0x0000000001000000,
    'P':0x0000000002000000,
    'D':0x0000000003000000,
    'DP':0x0000000004000000,
    'SP':0x0000000005000000,
    }
PERSON={
    '1':0x0000000008000000,
    '2':0x0000000010000000,
    '3':0x0000000018000000,
    'A':0x0000000020000000,
    }
STATUS={
    'ABS':0x0000000040000000,
    'CONST':0x0000000080000000,
    }
TENSE={
    'PAST':0x0000000200000000,
    'ALLTIME': 0x0000000400000000,  # @NEW
    'BEINONI':0x0000000600000000,
    'FUTURE':0x0000000800000000,
    'IMPERATIVE':0x0000000a00000000,
    'TOINFINITIVE':0x0000000c00000000,
    'BAREINFINITIVE':0x0000000e00000000,
    }
POLARITY={
    'POSITIVE':0x0002000000000000,
    'NEGATIVE':0x0004000000000000,
    }
BINYAN={
    'PAAL'    :0x0008000000000000,
    'NIFAL'   :0x0010000000000000,
    'HIFIL'   :0x0018000000000000,
    'HUFAL'   :0x0020000000000000,
    'PIEL'    :0x0028000000000000,
    'PUAL'    :0x0030000000000000,
    'HITPAEL' :0x0038000000000000,
    }

CONJ_TYPE={
    'COORD': 0x0040000000000000,
    'SUB':   0x0080000000000000,
    'REL':   0x00c0000000000000
    }
PRON_TYPE={
    'PERS': 0x0100000000000000, # PERSONAL
    'DEM':  0x0200000000000000, # DEMONSTRATIVE
    'IMP':  0x0300000000000000, # IMPERSONAL
    'REF':  0x0400000000000000, # REFLEXIVE @@@@
    #'INT':  0x0300000000000000, # INTERROGATIVE
    #'REL':  0x0400000000000000, # RELATIVIZER
    }
NUM_TYPE={
    'ORDINAL' : 0x1000,
    'CARDINAL': 0x2000,
    'FRACTIONAL': 0x3000,
    'LITERAL': 0x4000,
    'GIMATRIA': 0x5000,
    }
INTEROGATIVE_TYPE={
    'PRONOUN' : 0x20,
    'PROADVERB' : 0x0000004000000000,
    'PRODET'    : 0x0000004000000020,
    'YESNO'     : 0x0001000000000000,
    }
QUANTIFIER_TYPE={
    'AMOUNT'    : 0x0000000000800000,
    'PARTITIVE' : 0x0000000100000000,
    'DETERMINER': 0x0000000100800000,
    }

FEATURES = {}
for f in [GENDER,NUMBER,PERSON,STATUS,TENSE,POLARITY,BINYAN,CONJ_TYPE,PRON_TYPE]:
    FEATURES.update(f)



SUFFIX={
    'POSSESSIVE':0x0000001000000000,
    'ACC-NOM':0x0000002000000000,    # This is the nominative
    'PRONOMINAL':0x0000003000000000,  # for ADVERBS and PREPS
    }
SHORTSUFFIX={
    'POSSESSIVE':'S_PP',
    'PRONOMINAL': 'S_PRN',  # for ADVERBS and PREPS
    'ACC-NOM': 'S_ANP',    # This is the nominative
    '': None # NO suffix
    }
SUFF_GEN={
    'M':0x0000008000000000,
    'F':0x0000010000000000,
    'MF':0x0000018000000000,
    }
SUFF_NUM={
    'S':0x0000040000000000,
    'P':0x0000080000000000,
    'D':0x00000c0000000000,
    'DP':0x0000100000000000,
    'SP':0x0000140000000000,
    }
SUFF_PERS={
    '1':0x0000200000000000,
    '2':0x0000400000000000,
    '3':0x0000600000000000,
    'A':0x0000800000000000,
    }

SFEATURES = {}
for f in SUFF_PERS, SUFF_NUM, SUFF_GEN:
    SFEATURES.update(f)

PREFIX={
    'CONJ':0x0000000000000002, 
    'DEF':0x0000000000000004,  # used as a feature..
    'INTERROGATIVE':0x0000000000000010,
    'PREPOSITION':0x0000000000000040,
    'REL-SUBCONJ':0x00000000000000100,
    'TEMP-SUBCONJ':0x00000000000000200,
    'TENSEINV':0x0000000000000020,
    'ADVERB':0x00000000000000400,
    'PREPOSITION2':0x0000000000000080, #??
    }

#### map long POS name to short encoding
SHORTPOS = {
    'ADJECTIVE':         'JJ',
    'ADVERB':            'RB',
    'CONJUNCTION':       'CC',
    'AT_PREP':           'AT',
    'NEGATION':          'NEG',
    'NOUN':              'NN',
    'NUMERAL':           'CD',
    'PREPOSITION':       'IN',
    'PRONOUN':           'PRP',
    'PROPERNAME':        'NNP',
    'VERB':              'VB',
    'PUNCTUATION':       'PUNC',
    'INTERROGATIVE':     'QW',
    'INTERJECTION':      'INTJ',
    'UNKNOWN':           'UNK',
    'QUANTIFIER':        'DT',
    'EXISTENTIAL':       'EX',
    'MODAL':             'MD',
    'PREFIX':            'P',
    'URL':               'URL',
    'FOREIGN':           'FW',
    'JUNK':              'JNK',
    'PARTICIPLE':        'BN',
    'COPULA':            'COP',
    'NUMEXP':            'NCD',
    'TITULA':            'TTL',
    'SHEL_PREP':         'POS',
    'PARTICLE':          'PRT',
    '' : '',
    }

__PREF_PRECEDENCE = {#{{{
    'CONJ' : 0,
    'REL-SUBCONJ' : 1,
    'TEMP-SUBCONJ' : 1,
    'PREPOSITION' : 2,
    'ADVERB' : 3,
    'TENSEINV' : 5, #@VERIFY...
    'DEF': 4,
    }
#}}}

def order_prefixes(prefs):#{{{
    prefs = [x for x in prefs if x]
    prefs = sorted(prefs, key=lambda p:__PREF_PRECEDENCE[p])
    return prefs
#}}}



def revdict(d):
    res = dict(((v,k) for (k,v) in d.items()))
    return res

SHORT_TO_LONG_POS = revdict(SHORTPOS)
SHORT_TO_LONG_SUF = revdict(SHORTSUFFIX)

def _bminvlookup(mask,table,bm):
    bm = bm & MASKS[mask]
    res = []
    for k,v in table.items():
        if v == bm: res.append(k)
    res.sort()
    #if mask=='SUFFIX' and res: print "can't find",res
    #if mask=='SUFFIX' and bm and not res: print "bm: %x" % bm
    return " ".join(res)

def bm_is_definite(bm): return bm & MASKS['PREFIX'] == 0x04
def bm_get_pos(bm): return _bminvlookup('POS',POS,bm)
def bm_get_gender(bm): return _bminvlookup('GENDER',GENDER,bm)
def bm_get_number(bm): return _bminvlookup('NUMBER',NUMBER,bm)
def bm_get_person(bm): return _bminvlookup('PERSON',PERSON,bm)
def bm_get_status(bm): return _bminvlookup('STATUS',STATUS,bm)
def bm_get_tense(bm): return _bminvlookup('TENSE',TENSE,bm)
def bm_get_polarity(bm): return _bminvlookup('POLARITY',POLARITY,bm)

def bm_get_prntype(bm): return _bminvlookup('PRON_TYPE',PRON_TYPE ,bm)
def bm_get_cnjtype(bm): return _bminvlookup('CONJ_TYPE',CONJ_TYPE,bm)
def bm_get_numtype(bm): return _bminvlookup('NUM_TYPE',NUM_TYPE,bm)
def bm_get_inttype(bm): return _bminvlookup('INTERROGATIVE_TYPE',INTEROGATIVE_TYPE,bm)
def bm_get_qnttype(bm): return _bminvlookup('QUANTIFIER_TYPE',QUANTIFIER_TYPE,bm)
def bm_get_binyan(bm): return _bminvlookup('BINYAN',BINYAN,bm)
#def bm_get_prefixes(bm): return _bminvlookup('PREFIX',PREFIX,bm)
def bm_get_suff_func(bm): return _bminvlookup('SUFF_FUNC',SUFFIX,bm)
def bm_get_suff_gen(bm): return _bminvlookup('SUFF_GEN',SUFF_GEN,bm)
def bm_get_suff_num(bm): return _bminvlookup('SUFF_NUM',SUFF_NUM,bm)
def bm_get_suff_pers(bm): return _bminvlookup('SUFF_PERS',SUFF_PERS,bm)

def bm_get_definite(bm): 
    if bm_is_definite(bm): return "H"
    return ""

def bm_get_prefixes(bm):
    bm = bm & MASKS['PREFIX']
    res = []
    for k,v in PREFIX.items():
        if v & bm: res.append(k)
    #res.sort()
    #if mask=='SUFFIX' and res: print "can't find",res
    #if mask=='SUFFIX' and bm and not res: print "bm: %x" % bm
    return " ".join(res)

def decode_morph_tag(bm):
    prefs = bm_get_prefixes(bm)
    base  = bm_get_pos(bm)
    mods = [f(bm) for f in [bm_get_gender,
                            bm_get_number,
                            bm_get_person,
                            bm_get_status,
                            bm_get_tense,
                            bm_get_polarity,
                            bm_get_binyan]]
    mods.insert(0, prefs)
    mods.insert(1, base)
    mods.append(bm_get_suff_func(bm))
    return mods