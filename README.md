Project 2: Tournament Application
=================================

tournament.py contains the actual definitions to use and tournament_test.py
contains the test suite.

## Prerequisites

This application requires Python 3 and psycopg installed, as well as a local
postgres installation with a database named 'tournament' the definitions for 
this database are located in 'tournament.sql'.

## Function Defintiions

The tournament library provides the following definitions.

### createTournament

`createTournament(name)` creates a tournament with a given name in the
database. It returns an id which can be used by `selectTournament(id)`

```createTournament('Test') # 1```

### selectTournament

`selectTournament(id)` specifies the active tournament id that all of the
following functions will operate on. This allows for multiple tournaments to
be managed at once.

```
id = createTournament('Blah') # 2
selectTournament(id) # All future calls will modify tournament #2
```

### deleteMatches

`deleteMatches()` removes all matches from the currently selected tournament.

### deletePlayers

`deletePlayers()` removes all players from the currently selected tournament.

### countPlayers

`countPlayers()` returns a count of players in the currently selected
tournament.

### registerPlayer

`registerPlayer(name)` registers a new player in the currently selected
tournament and returns their unique id.

### playerStandings

`playerStandings()` returns a list of tuples sorted by standing (wins). Each
tuple is in the following format (id, name, wins, total_games)

### reportMatch

`reportMatch(winner, loser, draw=False)` reports that a match has completed
where winner has won and loser has lost, unless draw is specified as True.

### swissPairings

`swissPairings()` returns the next set of match ups based on the current
standing of the players. If the number of players is odd then a player will
be given a bye. Matches are guaranteed to not repeat. It returns a list of
tuples in the following form (id1, name1, id2, name2).

## Example

This is also in example.py.

```
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




```

