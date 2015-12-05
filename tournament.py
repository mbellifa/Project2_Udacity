#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

"""
There is bound to be a better way to do this but I wanted to make as few
changes to the existing API as possible while adding multiple tournaments.

I think given total freedom to design the code for this I would have all of
these functions as methods of a tournament object, which would also allow you
to have multiple tournaments.
"""

_activeTournament = None


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def createTournament(name):
    """Creates a new tournament, and returns its id"""
    con = connect()
    cursor = con.cursor()
    # I found the RETURNING id syntax here: http://stackoverflow.com/a/5247723

    cursor.execute('INSERT INTO tournaments (name) VALUES (%s) RETURNING id',
                   (name,))
    con.commit()
    return cursor.fetchone()[0]


def selectTournament(id):
    """Selects an id as the active tournament, this tournament will be
    the one manipulated by the other commands"""
    global _activeTournament
    con = connect()
    cursor = con.cursor()
    cursor.execute('SELECT id FROM tournaments WHERE id = %s', (id,))
    if cursor.rowcount == 0:
        raise ValueError("Non-existant Tournament ID")
    _activeTournament = id


def deleteMatches():
    """Remove all the match records from the database."""
    global _activeTournament
    con = connect()
    cur = con.cursor()
    cur.execute('DELETE FROM matches WHERE tournament = %s',
                (_activeTournament,))
    con.commit()


def deletePlayers():
    """Remove all the player records from the database."""
    global _activeTournament
    con = connect()
    cur = con.cursor()
    cur.execute('DELETE FROM participants WHERE tournament = %s',
                (_activeTournament,))
    con.commit()


def countPlayers():
    """Returns the number of players currently registered."""
    global _activeTournament
    con = connect()
    cur = con.cursor()
    cur.execute('SELECT count(id) FROM participants WHERE tournament = %s',
                (_activeTournament,))
    return cur.fetchone()[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    global _activeTournament
    con = connect()
    cursor = con.cursor()
    # I found the RETURNING id syntax here: http://stackoverflow.com/a/5247723

    cursor.execute("""
        INSERT INTO participants (tournament,name) VALUES (%s,%s) RETURNING id
    """,
                   (_activeTournament, name))
    con.commit()
    return cursor.fetchone()[0]


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    global _activeTournament
    con = connect()
    cur = con.cursor()
    cur.execute("""
    SELECT
        id, name, wins, total
    FROM wins_totals
    WHERE tournament = %s
    """, (_activeTournament,))

    ret = []
    for row in cur:
        ret.append(row)
    return ret


def reportMatch(winner, loser, draw=False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      draw:   specifies if the match was a draw, defaults to false
    """
    global _activeTournament
    con = connect()
    cursor = con.cursor()
    # I found the RETURNING id syntax here: http://stackoverflow.com/a/5247723
    winnerID = winner
    if draw:
        winnerID = 'NULL'
    cursor.execute("""
    INSERT INTO matches
        (tournament, player1, player2, winner)
     VALUES
        (%s, %s, %s, %s)
    RETURNING id
    """, (_activeTournament, winner, loser, winnerID))
    con.commit()
    return cursor.fetchone()[0]


def getByeId():
    """Returns the id of the Bye player if there is one, or None otherwise"""
    global _activeTournament
    con = connect()
    cursor = con.cursor()
    cursor.execute("""
        SELECT id FROM participants WHERE name = '!Bye!' AND tournament = %s
    """, (_activeTournament,))
    for row in cursor:
        return row[0]
    return None


def havePlayed(player1, player2):
    """Returns True if the given players have played a match so far."""
    global _activeTournament
    con = connect()
    cursor = con.cursor()
    cursor.execute("""
    SELECT id FROM matches WHERE ((player1 = %s AND player2 = %s) OR
    (player1 = %s AND player2 = %s)) LIMIT 1
    """, (player1, player2, player2, player1))
    for row in cursor:
        return True
    return False


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    ret = []
    byeId = getByeId()
    if countPlayers() % 2 == 1:
        if byeId is not None:
            raise ValueError("Asked to create two Bye accounts")
        byeId = registerPlayer('!Bye!')  # This is our special "Bye" player
    standings = playerStandings()
    while len(standings) > 0:
        player1 = standings.pop(0)
        player2 = None
        for i, player in enumerate(standings):
            if not havePlayed(player1[0], player[0]):
                player2 = standings.pop(i)
                break
        if player2 is None:
            raise ValueError("Can't find non-duplicate match")
        ret.append((player1[0], player1[1], player2[0], player2[1]))
        # If either player is the Bye then we can immediately report a victor
        if player1[0] == byeId:
            reportMatch(player2[0], byeId)
        elif player2[0] == byeId:
            reportMatch(player1[0], byeId)
    return ret





