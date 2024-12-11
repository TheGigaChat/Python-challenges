"""Test."""

import pytest

from football import Player, Team, Match

#Player tests
def test_player_repr():
    player = Player("Ago", player_number=10)
    assert repr(player) == "Ago (10)"


def test_get_player_name():
    player = Player("Ago", player_number=10)
    fun_result = player.get_player_name()

    assert fun_result == "Ago"

#Edge cases
def test_get_player_name_empty_name():
    player = Player(name="", player_number=10)
    result = player.get_player_name()
    assert result == ""

def test_get_player_name_long_name():
    long_name = "A" * 100
    player = Player(name=long_name, player_number=10)
    result = player.get_player_name()
    assert result == long_name


def test_get_player_number():
    player = Player("Ago", player_number=10)
    fun_result = player.get_player_number()

    assert fun_result == 10


def test_get_goals_scored():
    player = Player("Ago", player_number=10)
    fun_result = player.get_goals_scored()
    assert fun_result == 0


def test_get_red_cards():
    player = Player("Ago", player_number=10)
    fun_result = player.get_red_cards()
    assert fun_result == 0


#Team tests
def test_team_repr():
    team = Team("Best team")
    assert repr(team) == "Best team"


def test_team_is_full_false():
    team = Team("Best team")
    team.players = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert team.is_full() == False

def test_team_is_full_true():
    team = Team("Best team")
    team.players = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert team.is_full() == True


def test_team_add_one_player():
    player = Player("Ago", player_number=10)
    team = Team("Best team")

    team.add_player(player)
    assert team.players == [player]

def test_team_add_ten_players():
    added_players_count = 0
    team = Team("Best team")
    expected_result = []
    while added_players_count < 11:
        name = "A" * added_players_count
        player_num = added_players_count

        player = Player(name, player_num)

        team.add_player(player)
        expected_result.append(player)
        added_players_count += 1

    assert team.players == expected_result

def test_team_add_player_returns_true():
    added_players_count = 0
    team = Team("Best team")
    expected_result = []
    fun_result = None
    while added_players_count < 10:
        name = "A" * added_players_count
        player_num = added_players_count

        player = Player(name, player_num)

        fun_result = team.add_player(player)
        expected_result.append(player)
        added_players_count += 1

    assert fun_result == True

def test_team_add_too_many_players_returns_false():
    added_players_count = 0
    team = Team("Best team")
    expected_result = []
    fun_result = None
    while added_players_count < 15:
        name = "A" * added_players_count
        player_num = added_players_count

        player = Player(name, player_num)

        fun_result = team.add_player(player)
        expected_result.append(player)
        added_players_count += 1

    assert fun_result == False


def test_team_remove_player_returns_true():
    player = Player("Ago", player_number=10)
    team = Team("Best team")

    team.add_player(player)
    fun_result = team.remove_player(player)
    assert fun_result == True

def test_team_remove_player_that_not_in_the_team_returns_false():
    player = Player("Ago", player_number=10)
    team = Team("Best team")

    fun_result = team.remove_player(player)
    assert fun_result == False


def test_get_player_by_number():
    player = Player("Ago", player_number=10)
    team = Team("Best team")

    team.add_player(player)
    fun_result = team.get_player_by_number(10)
    assert fun_result == player


def test_get_team_name():
    team = Team("Best team")
    fun_result = team.get_team_name()
    assert fun_result == "Best team"


def test_get_players():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    team = Team("Best team")

    team.add_player(player1)
    team.add_player(player2)
    team.add_player(player3)

    fun_result = team.get_players()
    assert fun_result == [player1, player2, player3]


def test_get_players_sorted_by_score():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    team = Team("Best team")

    player1.score = 3
    player2.score = 6
    player3.score = 1

    team.add_player(player1)
    team.add_player(player2)
    team.add_player(player3)

    fun_result = team.get_players_sorted()
    assert fun_result == [player2, player1, player3]


def test_get_players_sorted_by_red_cards():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    team = Team("Best team")

    player1.score = 1
    player2.score = 1
    player3.score = 1

    player1.red_cards = 1
    player2.red_cards = 0
    player3.red_cards = 2

    team.add_player(player1)
    team.add_player(player2)
    team.add_player(player3)

    fun_result = team.get_players_sorted()
    assert fun_result == [player2, player1, player3]


#Match tests


def test_match_player_scored_true():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    player4 = Player("Brum", player_number=13)

    team1 = Team("Best team")
    team2 = Team("Dump team")

    match = Match(team1, team2)

    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)
    team2.add_player(player4)

    fun_result = match.player_scored(team1, player1)
    assert fun_result == True

def test_match_player_scored_false():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    player4 = Player("Brum", player_number=13)

    team1 = Team("Best team")
    team2 = Team("Dump team")

    match = Match(team1, team2)

    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)
    team2.add_player(player4)

    fun_result = match.player_scored(team2, player1)
    assert fun_result == False


def test_match_give_red_card_true():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    player4 = Player("Brum", player_number=13)

    team1 = Team("Best team")
    team2 = Team("Dump team")

    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)
    team2.add_player(player4)

    match = Match(team1, team2)

    fun_result = match.give_red_card(player1)
    assert fun_result == True

def test_match_give_red_card_false():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    player4 = Player("Brum", player_number=13)

    team1 = Team("Best team")
    team2 = Team("Dump team")

    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)

    match = Match(team1, team2)

    fun_result = match.give_red_card(player4)
    assert fun_result == False


def test_get_score():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)

    team1 = Team("Best team")
    team2 = Team("Dump team")

    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)

    team1.team_score = 100
    match = Match(team1, team2)

    fun_result = match.get_score(team1)
    assert fun_result == 100


def test_match_get_winner():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    player4 = Player("Brum", player_number=13)

    team1 = Team("Best team")
    team2 = Team("Dump team")

    team1.team_score = 2
    team2.team_score = 20

    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)
    team2.add_player(player4)

    match = Match(team1, team2)

    fun_result = match.get_winner()
    assert fun_result == team2

    team1.team_score = 20
    team2.team_score = 2
    fun_result = match.get_winner()

    assert fun_result == team1

def test_match_get_winner_none():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    player4 = Player("Brum", player_number=13)

    team1 = Team("Best team")
    team2 = Team("Dump team")

    team1.team_score = 2
    team2.team_score = 2

    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)
    team2.add_player(player4)

    match = Match(team1, team2)

    fun_result = match.get_winner()
    assert fun_result is None


def test_get_top_goal_scorer():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    player4 = Player("Brum", player_number=13)

    team1 = Team("Best team")
    team2 = Team("Dump team")

    player1.score = 10

    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)
    team2.add_player(player4)

    match = Match(team1, team2)

    fun_result = match.get_top_goalscorer()
    assert fun_result == player1

    player2.score = 100
    match = Match(team1, team2)

    fun_result = match.get_top_goalscorer()
    assert fun_result == player2


def test_has_red_card_true():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    player4 = Player("Brum", player_number=13)

    team1 = Team("Best team")
    team2 = Team("Dump team")

    player1.red_cards = 1

    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)
    team2.add_player(player4)

    match = Match(team1, team2)

    fun_result = match.has_red_card(player1)
    assert fun_result == True

def test_has_red_card_false():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    player4 = Player("Brum", player_number=13)

    team1 = Team("Best team")
    team2 = Team("Dump team")

    player1.red_cards = 0

    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)
    team2.add_player(player4)

    match = Match(team1, team2)

    fun_result = match.has_red_card(player1)
    assert fun_result == False


def test_get_red_carded_players():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    player4 = Player("Brum", player_number=13)

    team1 = Team("Best team")
    team2 = Team("Dump team")

    player1.red_cards = 1
    player2.red_cards = 1

    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)
    team2.add_player(player4)

    match = Match(team1, team2)

    fun_result = match.get_red_carded_players()
    assert fun_result == [player1, player2]

def test_get_red_carded_players_empty():
    player1 = Player("Ago", player_number=10)
    player2 = Player("Bus", player_number=12)
    player3 = Player("Car", player_number=11)
    player4 = Player("Brum", player_number=13)

    team1 = Team("Best team")
    team2 = Team("Dump team")

    team1.add_player(player1)
    team1.add_player(player2)
    team2.add_player(player3)
    team2.add_player(player4)

    match = Match(team1, team2)

    fun_result = match.get_red_carded_players()
    assert fun_result == []