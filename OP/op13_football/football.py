"""Football OP."""


class Team:
    """Football Team class."""

    def __init__(self, name: str, attack: int, defense: int):
        """
        Initialize Team object. Team should have score count, which is initially 0.

        :param name: team's name.
        :param attack: team's attack value.
        :param defense: team's defence value.
        """""
        self.name = name
        self.attack = attack
        self.defense = defense
        self.score = 0

    def train(self) -> None:
        """
        Train the team.

        +1 to defense
        +1 to attack
        :return: None.
        """
        self.attack += 1
        self.defense += 1

    def get_score(self) -> int:
        """
        Return team's score.

        :return: score.
        """
        return self.score

    def set_score(self, score: int):
        """
        Set score.

        :param score: score value.

        :return: None.
        """
        self.score = score

    def get_attack(self) -> int:
        """
        Return attack value.

        :return: attack value.
        """
        return self.attack

    def get_defence(self) -> int:
        """
        Return defence value.

        :return: defence value.
        """
        return self.defense

    def get_name(self) -> str:
        """
        Get team's name.

        :return: team's name.
        """
        return self.name

    def __repr__(self):
        """Format the string of the team as: '[name]'."""
        return f"{self.name}"


class League:
    """Football League class."""

    def __init__(self, name: str, teams: list):
        """
        Initialize League object.

        :param name: league name.
        :param teams: list of teams in league.
        """
        self.name = name
        self.teams = teams
        self.scoreboard = {team: team.get_score() for team in teams}

    def add_team(self, team: Team) -> None:
        """
        Add team to league.

        A league can contain a maximum of 10 teams.
        If team gets added then it must also show up on the scoreboard.

        :param team: Team object.
        """
        if team not in self.teams and len(self.teams) < 10:
            self.teams.append(team)
            self.scoreboard[team] = team.get_score()

    def remove_team(self, team_name: str) -> None:
        """
        Remove team from league by name.

        Team should also be removed from scoreboard.

        :param team_name: Name of team to remove from league.
        """
        teams_to_remove = [team for team in self.teams if team.get_name() == team_name]
        for team in teams_to_remove:
            self.teams.remove(team)
            del self.scoreboard[team]

    def play_games(self) -> None:
        """
        Each team should play against other team once.

        Create Game object and get the winner.
        Winner gets +1 point to league scoreboard.
        :return: None.
        """
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                # Create a Game object for the match
                game = Game(self.teams[i], self.teams[j])

                winner = game.play()

                if winner:
                    self.scoreboard[winner] += 1

    def get_first_place(self) -> Team:
        """
        Get first place in the league.

        :return: team on the first place in scoreboard.
        """
        return max(self.scoreboard, key=self.scoreboard.get)

    def get_last_place(self) -> Team:
        """
        Get last place in the league.

        :return: team on the last place in scoreboard.
        """
        return min(self.scoreboard, key=self.scoreboard.get)

    def clear_scoreboard(self):
        """
        Clear scoreboard (for the new season).

        :return: None.
        """
        self.scoreboard = {team: 0 for team in self.teams}

    def get_name(self) -> str:
        """Return league name."""
        return self.name

    def get_teams(self) -> list:
        """Get all teams in league."""
        return self.teams

    def get_scoreboard(self) -> dict:
        """Return league scoreboard."""
        return self.scoreboard

    def __repr__(self):
        """Format the string of the league as: '[name]'."""
        return f"{self.name}"


class Game:
    """Football Game class."""

    def __init__(self, team1: Team, team2: Team):
        """
        Initialize Game object.

        :param team1: first team in the game.
        :param team2: second team in the game.
        """
        self.team1 = team1
        self.team2 = team2

    def play(self) -> object:
        """Play the game."""
        team1_points = 0
        team2_points = 0

        # Compare attack values
        if self.team1.attack > self.team2.attack:
            team1_points += 1
        elif self.team1.attack < self.team2.attack:
            team2_points += 1

        # Compare defense values
        if self.team1.defense > self.team2.defense:
            team1_points += 1
        elif self.team1.defense < self.team2.defense:
            team2_points += 1

        # If points are tied, compare total (attack + defense)
        if team1_points == team2_points:
            team1_total = self.team1.attack + self.team1.defense
            team2_total = self.team2.attack + self.team2.defense

            if team1_total > team2_total:
                return self.team1
            elif team2_total > team1_total:
                return self.team2

            # If still tied, sort alphabetically by team name
            return min(self.team1, self.team2, key=lambda team: team.name)

        # Return the team with more points
        return self.team1 if team1_points > team2_points else self.team2

    def __repr__(self):
        """Format the string of the game as: '[team1] vs. [team2]'."""
        return f"{self.team1} vs. {self.team2}"

# Example of the next and yeild properties
# def count_up_to(n):
#     i = 1
#     while i <= n:
#         yield i
#         i += 1
#
# gen = count_up_to(3)
# print(next(gen))  # Output: 1
# print(next(gen))  # Output: 2
# print(next(gen))  # Output: 3
# # Raises StopIteration if called again

# First match with the next function
# numbers = [10, 20, 30, 40]
#
# # Find the first number greater than 25
# result = next((x for x in numbers if x > 25), "No match")
# print(result)  # Output: 30
#
# # If no match is found
# result = next((x for x in numbers if x > 50), "No match")
# print(result)  # Output: No match

# def generate_primes():
#     primes = []
#     candidate = 2
#     while True:
#         for p in primes:
#             if candidate % p != 0:
#                 primes.append(candidate)
#                 yield candidate
#         candidate += 1
#
# prime_gen = generate_primes()
# print(next(prime_gen))  # Output: 2
# print(next(prime_gen))  # Output: 3
# print(next(prime_gen))  # Output: 5
