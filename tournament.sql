-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


create table tournaments (
        id serial primary key,
        name text
);

create table participants (
        tournament integer references tournaments (id),
        id serial primary key,
        name text
);

create table matches (
        tournament integer references tournaments (id),
        id serial primary key,
        player1 integer references participants (id),
        player2 integer references participants (id),
        winner integer references participants (id)
);
-- This view returns all participants in all tournaments and their current wins and total games
create view wins_totals as SELECT
        id, name, tournament,
        (SELECT
            count(id) as wins
         FROM matches
         WHERE tournament = participants.tournament AND winner = participants.id) as wins,
        (SELECT
            count(id) as wins
         FROM matches
         WHERE tournament = participants.tournament AND
             (player1 = participants.id OR player2 = participants.id)) as total

    FROM participants
    ORDER BY wins DESC;
