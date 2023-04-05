############################################################
# CMPSC442: Homework 5
############################################################

student_name = "Trisha Mandal"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import math
import os
import collections


############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    lst = []
    path = open(email_path, encoding="utf8")

    with path as file:
        mess = email.message_from_file(file)

    iterstatement = email.iterators.body_line_iterator(mess)

    for l in iterstatement:
        lst = lst + l.split()

    path.close()
    return lst


def log_probs(email_paths, smoothing):
    loadedtokens, probs = [], {}

    for path in email_paths:
        for l in load_tokens(path):
            loadedtokens += [l]

    numofwords = collections.defaultdict(int)

    for l in loadedtokens:
        numofwords[l] = numofwords[l] + 1

    denominator2 = (len(loadedtokens) + smoothing * (len(numofwords.keys()) + 1))
    probs['<UNK>'] = math.log(smoothing / denominator2)

    for k in numofwords.keys():
        numerator = numofwords[k] + smoothing
        denominator = len(loadedtokens) + smoothing * (len(numofwords.keys()) + 1)
        probs[k] = math.log(numerator / denominator)

    return probs


class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):

        spaml = []
        haml = []
        sfiles = os.listdir(spam_dir)
        hfiles = os.listdir(ham_dir)
        for f in sfiles:
            spaml.append(spam_dir + '/' + f)
        for f in hfiles:
            haml.append(ham_dir + '/' + f)
        self.spamlogs = log_probs(spaml, smoothing)
        self.hamlogs = log_probs(haml, smoothing)
        lenspam = len(spaml)
        lenham = len(haml)
        self.spamprobs = math.log(lenspam / (lenspam + lenham))
        self.hamprobs = math.log(lenham / (lenspam + lenham))

    def is_spam(self, email_path):
        words = {}
        hprobs, sprobs = self.hamprobs, self.spamprobs
        hlogs, slogs = self.hamlogs, self.spamlogs
        gettokens = load_tokens(email_path)

        for w in gettokens:
            if w not in words:
                words[w] = 1
            else:
                words[w] = words[w] + 1

        for w in words.keys():
            if w in hlogs and w not in slogs:
                hprobs = hprobs + hlogs[w]
            else:
                hprobs = hprobs + hlogs["<UNK>"]

        for w in words.keys():
            if w in slogs and w not in hlogs:
                sprobs = sprobs + slogs[w]
            else:
                sprobs = sprobs + slogs["<UNK>"]

        return hprobs < sprobs

    def most_indicative_spam(self, n):
        indicativespam, sol = {}, []
        ckeys = self.hamlogs.keys()
        skeys = self.spamlogs.items()

        for key, v in skeys:
            if key in ckeys:
                exponentspam = math.exp(self.spamlogs[key])
                exponentham = math.exp(self.hamlogs[key])
                p1 = self.spamlogs[key]
                p2 = math.log(exponentspam + exponentham)
                indicativespam[key] = p1 - p2

        dictitems = indicativespam.items()
        sorteditems = sorted(dictitems, key=lambda x: x[1], reverse=True)

        for key, value in sorteditems:
            sol.append(key)
            t = len(sol)
            if t == n:
                return sol
        return sol

    def most_indicative_ham(self, n):
        indicativeham, sol = {}, []
        ckeys = self.hamlogs.items()
        skeys = self.spamlogs.keys()

        for key, v in ckeys:
            if key in skeys:
                exponentspam = math.exp(self.spamlogs[key])
                exponentham = math.exp(self.hamlogs[key])
                p1 = self.hamlogs[key]
                p2 = math.log(exponentspam + exponentham)
                indicativeham[key] = p1 - p2

        dictitems = indicativeham.items()
        sorteditems = sorted(dictitems, key=lambda x: x[1], reverse=True)

        for key, value in sorteditems:
            sol.append(key)
            t = len(sol)
            if t == n:
                return sol
        return sol


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
Took me 12 hours to do this project.
"""

feedback_question_2 = """
It's a totally new kind of project that uses different python libraries. 
It was a little difficult to start.
"""

feedback_question_3 = """
I like the idea of the spam filter. It is pretty cool. 
"""
