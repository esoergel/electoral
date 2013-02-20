a="""
I plan to rewrite this as part of a web app so I can actually get some
real data and analyze it.  As part of that, I'll store each run-off
result and then run the orderings based on that info rather than
re-calculating each run-off.


Main Principles:
 1. Vote in a way that fairly represents voters' views.
 2. Interpret that information to choose a candidate who best
    represents the voters' views.
Guidelines:
There should be no incentive for (or possibility of) strategic voting.
Best way to represent voters' views is to rank candidates by preference.
"""
others = a.split() # seems like a decent way to get random candidates

"""Each ballot will be represented as an ordered list of candidates"""
candidates = ["George Washington", "John Adams", "Thomas Jefferson",
    "James Madison", "James Monroe", "John Quincy Adams"]

import random, math


def make_ballot(n=False, ballot=False):
    """makes a list of candidates at random."""
    if not (n or ballot):
        n = random.randint(2,5)
        ballot = []

    candidate = random.choice(candidates)
    if candidate not in ballot:
        ballot.append(candidate)

    if len(ballot) >= n:
        return ballot
    else:
        return make_ballot(n, ballot)

def rand_cand(ballot):
    """Selects a random candidate
    One out of every 10 times votes write-in."""
    if random.random() <= 0.1:
        choice =  random.choice(others)
    else:
        choice = random.choice(candidates)
    if choice not in ballot:
        return choice
    else:
        return rand_cand(ballot)


def permute(in_ballot, v=10):
    """introduces variation to ballot.  
    v controls level of variation"""
    ballot = in_ballot[:]

    # remove or add random candidate sometimes
    if random.random() < (0.04*v):
        ballot.remove(random.choice(ballot))
    if random.random() < (0.06*v):
        ballot.append(rand_cand(ballot))


    # permute
    length = len(ballot)
    if length == 0:
        return ballot

    for i in range(v): # idk, how much should I permute?
        if random.random() < 0.1:
            i=random.randrange(length)
            j=random.randrange(length)
            if i != j:
                ballot[i], ballot[j] = ballot[j], ballot[i]
    return ballot


def make_parties(n=5):
    """Produces n 'ideologies' which will be cloned and
    randomly modified to create electorate"""
    parties = []
    for i in range(n):
        ballot = make_ballot()
        parties.append(ballot)
    return parties


def populate(ideology, n, v=10):
    "return n ballots based on a provided ideology"
    ballots = []
    while n>0:
        n-=1
        ballots.append(permute(ideology, v))
    return ballots


def make_electorate(p=3, branch_max=800, verbose=False):
    electorate = []
    parties = make_parties(p)
    show = ""
    for party in parties:
        voters = 0
        show += str(party)
        division = random.randint(2,5) #how many splits
        branches = populate(party, division)
        show += "has %d divisions" % division
        for branch in branches:
            size = random.randint(1,branch_max)
            voters += size
            v = random.randint(2, 20)
            people = populate(branch, size, v)
            show += "\n   %s has %d people and %d variance" % (str(branch), size, v)
            electorate += people
        show += "\n%d total people in this party\n" % voters
    show += "\nThere are a total of %d voters" % len(electorate)
    if verbose:
        print show
    return electorate


import operator

def deprecated_get_candidates(electorate, percent=0.01, verbose=False):
    """"returns a hash table of candidates who were on
    at least 'percent' percent of the ballots, and the
    number of people who voted for them"""
    candidates = {}
    voters = len(electorate)
    for voter in electorate:
        for candidate in voter:
            candidates[candidate] = candidates.get(candidate, 0) + 1

    too_low = 0
    for candidate, votes in candidates.items():
        if votes/float(voters) < percent:
            too_low += 1
            candidates.pop(candidate)
    if verbose:
        print "%d candidates were on fewer than %.1f percent of the ballots" \
            % (too_low, percent*100)
        c = sorted(candidates.iteritems(), key=operator.itemgetter(1))
        for candidate, votes in c:
            print "%s was on %d ballots" % (candidate, votes)
        print ''
    return candidates

def get_candidates(electorate, max=5, verbose=False):
    """"returns a hash table of the top 'max' candidates,
    and the number of people who voted for them"""
    candidates = {}
    voters = len(electorate)
    for voter in electorate:
        for candidate in voter:
            candidates[candidate] = candidates.get(candidate, 0) + 1

    valid_candidates = {}
    too_low = len(candidates) - max
    c = sorted(candidates.iteritems(), key=operator.itemgetter(1))
    for candidate, votes in c[-max:]:
        valid_candidates[candidate] = votes

    if verbose:
        print "%d candidates were cut off." % too_low
        votes = c[-(max+1)][1]
        print "they were on %d or fewer of %d ballots (%.1f percent)"\
            % (votes, voters, (100*votes/float(voters)))
        c = sorted(valid_candidates.iteritems(), key=operator.itemgetter(1))
        for candidate, votes in c:
            print "%s was on %d ballots" % (candidate, votes)
        print ''
    return valid_candidates

def orderings(candidates):
    "returns every possible ordering of candidates"
    if type(candidates) == dict:
        candidates = candidates.keys()
    if len(candidates) == 1:
        return [candidates]

    races = []
    for candidate in candidates:
        others = candidates[:]
        others.remove(candidate)
        for ordering in orderings(others):
            # print type(candidate), type(ordering)
            race = [candidate] + ordering
            races.append(race)
    return races

def runoff(electorate, c1, c2, verbose=False):
    votes = {}
    abstained = 0
    for ballot in electorate:
        vote = check_ballot(ballot, c1, c2)
        if vote:
            votes[vote] = votes.get(vote, 0) + 1
        else:
            abstained += 1
    c = sorted(votes.iteritems(), key=operator.itemgetter(1))
    if verbose:
        if c[0][1] == c[1][1]:
            print "Draw between %s and %s" % (c1, c2)
        else:
            winner, loser = c[1][0], c[0][0]
            win, los = c[1][1], c[0][1]
            print "%s beat %s with %.1f percent of the vote (%d vs %d, with %d abstaining)"\
                % (winner, loser, (100*float(win)/(win+los)), win, los, abstained)
    return c[1][0]


def check_ballot(ballot, c1, c2):
    for candidate in ballot:
        if candidate == c1:
            return c1
        elif candidate == c2:
            return c2
        return False 

def run_ordering(electorate, candidates, verbose=False):
    "returns winning candidate"
    if len(candidates) == 1:
        return candidates[0]
    elif len(candidates) == 0:
        print "****0 candidates in a split??!??********"
    split = len(candidates)/2
    a = run_ordering(electorate, candidates[:split], verbose)
    b = run_ordering(electorate, candidates[split:], verbose)
    return runoff(electorate, a, b, verbose)

def go(candidates=4, once=False, verbose=False):
    e = make_electorate(3,800, verbose)
    c = get_candidates(e, candidates, verbose)
    if verbose:
        print "%d candidates met the threshold" % len(c)
        num_races = math.factorial(len(c))
        print "there are %d possible races" % num_races
    o = orderings(c)
    # if len(o) != num_races:
    #     print "problem counting number of orderings"

    if once:
        print "\nRunning this ordering:", o[0]
        w = run_ordering(e, o[0], True)
        print '\nOverall winner of this ordering is %s' % w
    else:
        wins = {}
        for ordering in o:
            w = run_ordering(e, ordering, verbose)
            wins[w] = wins.get(w, 0) + 1
        if len(wins) != 1:
            print "\nOrdering mattered!!"
            for cand, ws  in wins.items():
                print "%s won %d times" % (cand, ws)
        for cand, ws in wins.items():
            return "%s won %d times" % (cand, ws)

go(6, 1, 1)

# for i in range(100):
#     print i, go(5)


"""
a beats b
b beats c
c beats a
Is that possible?
"""
