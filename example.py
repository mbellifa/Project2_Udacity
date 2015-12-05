from tournament import *
selectTournament(createTournament('test'))
registerPlayer('Harry Potter')
registerPlayer('Hermione Granger')
registerPlayer('Ron Weasley')
pairings = swissPairings()
print(pairings)
# [(101, 'Harry Potter', 102, 'Hermione Granger'),
#  (103, 'Ron Weasley', 104, '!Bye!')]

for pairing in pairings:
    print('{} vs. {}'.format(pairing[1], pairing[3]))

firstPair = pairings[0]
reportMatch(firstPair[0], firstPair[2])  # Report that Harry won
# Harry Potter vs. Hermione Granger
# Ron Weasley vs. !Bye!

print(playerStandings())
# [(101, 'Harry Potter', 1L, 1L),
# (103, 'Ron Weasley', 1L, 1L),
# (102, 'Hermione Granger', 0L, 1L),
# (104, '!Bye!', 0L, 1L)]


pairings = swissPairings()
print(pairings)
# [(101, 'Harry Potter', 103, 'Ron Weasley'),
#  (102, 'Hermione Granger', 104, '!Bye!')]


for pairing in pairings:
    print('{} vs. {}'.format(pairing[1], pairing[3]))

# Harry Potter vs. Ron Weasley
# Hermione Granger vs. !Bye!

firstPair = pairings[0]
reportMatch(firstPair[0], firstPair[2])  # Report that Harry won again
print(playerStandings())

# [(101, 'Harry Potter', 2L, 2L),
# (102, 'Hermione Granger', 1L, 2L),
# (103, 'Ron Weasley', 1L, 2L),
# (104, '!Bye!', 0L, 2L)]


