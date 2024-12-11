"""Among us."""


class Crewmate:
    """Crewmate."""

    def __init__(self, color: str, role: str, tasks: int = 10):
        """
        Initialize crewmate class.

        :param color: The color of the player Works as ID.
        :param role: The role of the player One of the following ["Crewmate", "Sheriff", "Guardian Angel", "Altruist"].
        :param tasks: The number of tasks that crewmate should complete to crewmate's team wins.
        """
        self.color = color.capitalize()  # ID

        role = role.lower()
        if role == "sheriff":
            self.role = "Sheriff"
        elif role == "guardian angel":
            self.role = "Guardian Angel"
        elif role == "altruist":
            self.role = "Altruist"
        else:
            self.role = "Crewmate"

        self.tasks = tasks  # int
        self.protected = False

    def __repr__(self):
        """
        Represent player.

        Format the string of the player as:
        [color], role: [role], tasks left: [tasks]

        :return: The string representation of the player.
        """
        return f"{self.color}, role: {self.role}, tasks left: {self.tasks}."

    def complete_task(self):
        """Complete a task."""
        if self.tasks > 0:
            self.tasks -= 1


class Impostor:
    """Impostor."""

    def __init__(self, color: str):
        """
        Initialize impostor class.

        :param color: The color of the player Works as ID.
        """
        self.color = color.capitalize()  # ID
        self.kills = 0

    def __repr__(self):
        """
        Represent player.

        Format the string of the player as:
        Impostor [color], kills: [kills]

        :return: The string representation of the player.
        """
        return f"Impostor {self.color}, kills: {self.kills}."


class Spaceship:
    """Spaceship."""

    def __init__(self):
        """Initialize spaceship class."""
        self.crewmate_list = []
        self.impostor_list = []
        self.dead_players = []

    def get_spaceship_colors(self):
        """
        Get colors of all players on the spaceship.

        :return: list.
        """
        return list(map(lambda mate: mate.color, self.crewmate_list)) + list(map(lambda imp: imp.color, self.impostor_list))  # all colors on the ship

    def get_crewmates_colors(self):
        """
        Get colors of all crewmates on the spaceship.

        :return: list.
        """
        return list(map(lambda mate: mate.color, self.crewmate_list))

    def get_impostors_colors(self):
        """
        Get colors of all impostors on the spaceship.

        :return: list.
        """
        return list(map(lambda imp: imp.color, self.impostor_list))

    def get_protected_players(self):
        """
        Get all protected players.

        :return: list.
        """
        return list(filter(lambda mate: mate.protected, self.crewmate_list))

    def get_crewmate_list(self):
        """
        Get the list of all crewmates on the ship.

        :return: list.
        """
        return self.crewmate_list

    def get_impostor_list(self):
        """
        Get the list of all impostors on the ship.

        :return: list.
        """
        return self.impostor_list

    def get_dead_players(self):
        """
        Get the list of all dead players on the ship.

        :return: list.
        """
        return self.dead_players

    def add_crewmate(self, crewmate: Crewmate):  # Type check, Color check
        """
        Add a new crewmate on the ship.

        Check: crewmate type and color.
        """
        if isinstance(crewmate, Crewmate):
            if crewmate.color not in self.get_spaceship_colors():
                self.crewmate_list.append(crewmate)

    def add_impostor(self, impostor: Impostor):  # Type check, 3max, Color check
        """
        Add a new impostor on the ship.

        Check: impostor type, 3 max amount and color.
        """
        if isinstance(impostor, Impostor) and len(self.impostor_list) < 3:
            if impostor.color not in self.get_spaceship_colors():
                self.impostor_list.append(impostor)

    def kill_impostor(self, sheriff: Crewmate, color: str):  # capitalise color, Role check, sheriff on the ship, impostor has color check,
        """
        Kill the impostor on the ship.

        Check: capitalise the color, check a role of the sheriff, sheriff on the ship, color in impostor's list.
        """
        color = color.capitalize()
        if sheriff.role == "Sheriff" and sheriff in self.crewmate_list:
            if color in self.get_impostors_colors():
                # impostor dead
                killed_impostor = list(filter(lambda imp: imp.color == color, self.impostor_list))[0]
                self.impostor_list.remove(killed_impostor)
                self.dead_players.append(killed_impostor)
            else:
                # sheriff dead
                self.crewmate_list.remove(sheriff)
                self.dead_players.append(sheriff)

    def revive_crewmate(self, altruist: Crewmate, dead_crewmate: Crewmate):  # Role check, Altruist on the ship check, type Crewmate check, player is dead check
        """
        Revive a crewmate on the ship by sacrificing the altruist's life.

        Check: a role of the altruist, altruist on the ship, dead crewmate type, player is dead.
        """
        if altruist.role == "Altruist" and altruist in self.crewmate_list:
            if isinstance(dead_crewmate, Crewmate) and dead_crewmate in self.dead_players:
                self.dead_players.remove(dead_crewmate)
                self.dead_players.append(altruist)

                self.crewmate_list.remove(altruist)
                self.crewmate_list.append(dead_crewmate)

    def protect_crewmate(self, guardian_angel: Crewmate, crewmate_to_protect: Crewmate):   # Role check, angel is dead check, type Crewmate check, player is alive, protected only one player check
        """
        Protect a crewmate from being killed by an impostor.

        Conditions:
        - The guardian_angel's role must be "Guardian Angel".
        - The guardian_angel must be dead.
        - crewmate_to_protect must be a valid Crewmate and alive.
        - Only one crewmate can be protected at a time.

        :param guardian_angel: The crewmate with the "Guardian Angel" role.
        :param crewmate_to_protect: The crewmate to be protected.
        """
        if guardian_angel.role == "Guardian Angel" and guardian_angel in self.dead_players:
            if isinstance(crewmate_to_protect, Crewmate):
                if crewmate_to_protect in self.crewmate_list and self.get_protected_players() == []:
                    crewmate_to_protect.protected = True

    def kill_crewmate(self, impostor: Impostor, color: str):  # color capitalise, impostor type check, impostor on the ship check, color is a crewmate check, Protection check,
        """
        Kill a crewmate specified by their color.

        Conditions:
        - The impostor must be of type Impostor and on the ship.
        - The color must belong to a crewmate on the ship.
        - If the targeted crewmate is protected, they lose protection instead of being killed.

        :param impostor: The impostor attempting to kill a crewmate.
        :param color: The color of the crewmate to be killed (case-insensitive).
        """
        color = color.capitalize()
        if isinstance(impostor, Impostor) and impostor in self.impostor_list:
            if color in self.get_crewmates_colors():
                targeted_crewmate_list = list(filter(lambda mate: mate.color == color, self.crewmate_list))
                if len(targeted_crewmate_list):
                    targeted_crewmate = targeted_crewmate_list[0]
                    if targeted_crewmate.protected:
                        targeted_crewmate.protected = False
                    else:
                        # kill the crewmate
                        self.crewmate_list.remove(targeted_crewmate)
                        self.dead_players.append(targeted_crewmate)

                        impostor.kills += 1

    def sort_crewmates_by_tasks(self) -> list:
        """
        Sort all crewmates on the ship by the number of tasks they have completed.

        :return: A list of crewmates sorted by tasks completed in ascending order.
        """
        return sorted(self.crewmate_list, key=lambda mate: mate.tasks)

    def sort_impostors_by_kills(self) -> list:
        """
        Sort all impostors on the ship by the number of kills they have made.

        :return: A list of impostors sorted by kills in descending order.
        """
        return sorted(self.impostor_list, key=lambda imp: imp.kills, reverse=True)

    def get_regular_crewmates(self):
        """
        Get all regular crewmates (those with the role "Crewmate") currently on the ship.

        :return: A list of regular crewmates.
        """
        return list(filter(lambda mate: mate.role == "Crewmate", self.crewmate_list))

    def get_role_of_player(self, color: str):  # capitalise color, check color in the game
        """
        Get the role of a player based on their color.

        Conditions:
        - The color must belong to a player currently in the game.

        :param color: The color of the player (case-insensitive).
        :return: The role of the player ("Crewmate", specific crewmate role, or "Impostor").
        """
        color = color.capitalize()
        if color in self.get_spaceship_colors():
            # find color among crewmates
            if color in self.get_crewmates_colors():
                # find a role of the player
                expected_player_role = [mate.role for mate in self.crewmate_list if mate.color == color][0]
                return expected_player_role
            else:
                return "Impostor"

    def get_crewmate_with_most_tasks_done(self):  # crewmates on the ship check
        """
        Get the crewmate with the most tasks completed on the ship.

        Condition:
        - There must be at least one crewmate on the ship.

        :return: The crewmate with the most tasks completed.
        """
        if len(self.crewmate_list):
            return self.sort_crewmates_by_tasks()[0]

    def get_impostor_with_most_kills(self):  # impostors on the ship check
        """
        Get the impostor with the most kills on the ship.

        Condition:
        - There must be at least one impostor on the ship.

        :return: The impostor with the most kills.
        """
        if len(self.impostor_list):
            return self.sort_impostors_by_kills()[0]


if __name__ == "__main__":
    # Example test setup
    ship = Spaceship()
    altruist = Crewmate("Alice", role="altruist")
    dead_player = Crewmate("Bob", role="Cre")
    ship.crewmate_list = [altruist]
    ship.dead_players = [dead_player]

    # Revive the dead player
    ship.revive_crewmate(altruist, dead_player)
    print([mate.color for mate in ship.crewmate_list])  # ['Bob']
    print([mate.color for mate in ship.dead_players])  # ['Alice']
    # print("Spaceship.")
    #
    # spaceship = Spaceship()
    # print(spaceship.get_protected_players())  # -> []
    # print(spaceship.get_dead_players())  # -> []
    # print()
    #
    # print("Let's add some crewmates.")
    # red = Crewmate("Red", "Crewmate")
    # white = Crewmate("White", "Impostor")
    # yellow = Crewmate("Yellow", "Guardian Angel", tasks=5)
    # green = Crewmate("green", "Altruist")
    # blue = Crewmate("BLUE", "Sheriff", tasks=0)
    #
    # print(red)  # -> Red, role: Crewmate, tasks left: 10.
    # print(white)  # -> White, role: Crewmate, tasks left: 10.
    # print(yellow)  # -> Yellow, role: Guardian Angel, tasks left: 5.
    # print(blue)  # -> Blue, role: Sheriff, tasks left: 0.
    # print()
    #
    # print("Let's make Yellow complete a task.")
    # yellow.complete_task()
    # print(yellow)  # ->  Yellow, role: Guardian Angel, tasks left: 4.
    # print()
    #
    # print("Adding crewmates to Spaceship:")
    # spaceship.add_crewmate(red)
    # spaceship.add_crewmate(white)
    # spaceship.add_crewmate(yellow)
    # spaceship.add_crewmate(green)
    # print(spaceship.get_crewmate_list())  # -> [Red, role: Crewmate, tasks left: 10., White, role: Crewmate, tasks left: 10., Yellow, role: Guardian Angel, tasks left: 4., Green, role: Altruist, tasks left: 10.]
    #
    # spaceship.add_impostor(blue)  # Blue cannot be an Impostor.
    # print(spaceship.get_impostor_list())  # -> []
    # spaceship.add_crewmate(blue)
    # print()
    #
    # print("Now let's add impostors.")
    # orange = Impostor("orANge")
    # black = Impostor("black")
    # purple = Impostor("Purple")
    # spaceship.add_impostor(orange)
    # spaceship.add_impostor(black)
    #
    # spaceship.add_impostor(Impostor("Blue"))  # Blue player already exists in Spaceship.
    # spaceship.add_impostor(purple)
    # spaceship.add_impostor(Impostor("Pink"))  # No more than three impostors can be on Spaceship.
    # print(spaceship.get_impostor_list())  # -> [Impostor Orange, kills: 0., Impostor Black, kills: 0., Impostor Purple, kills: 0.]
    # print()
    #
    # print("The game has begun! Orange goes for the kill.")
    # spaceship.kill_crewmate(orange, "yellow")
    # print(orange)  # -> Impostor Orange, kills: 1.
    # spaceship.kill_crewmate(black, "purple")  # You can't kill another Impostor, silly!
    # print(spaceship.get_dead_players())  # -> [Yellow, role: Guardian Angel, tasks left: 4.]
    # print()
    #
    # print("Kill an impostor.")
    # print(spaceship.get_impostor_list())
    # spaceship.kill_impostor(blue, "black")
    # print(spaceship.get_impostor_list())

    # print("Yellow is a Guardian angel, and can protect their allies when dead.")
    # spaceship.protect_crewmate(yellow, green)
    # print(green.protected)  # -> True
    # spaceship.kill_crewmate(orange, "green")
    # print(green in spaceship.dead_players)  # -> False
    # print(green.protected)  # -> False
    # print()
    #
    # print("Green revives their ally.")
    # spaceship.kill_crewmate(purple, "RED")
    # print(red in spaceship.dead_players)  # -> True
    # spaceship.revive_crewmate(green, red)
    # print(red in spaceship.dead_players)  # -> False
    # print(green in spaceship.dead_players)  # -> True
    # print()
    #
    # print("Let's check if the sorting and filtering works correctly.")
    #
    # red.complete_task()
    # print(spaceship.get_role_of_player("Blue"))  # -> Sheriff
    # spaceship.kill_crewmate(purple, "blue")
    # print(spaceship.sort_crewmates_by_tasks())  # -> [Red, role: Crewmate, tasks left: 9., White, role: Crewmate, tasks left: 10.]
    # print(spaceship.sort_impostors_by_kills())  # -> [Impostor Purple, kills: 2., Impostor Orange, kills: 1., Impostor Black, kills: 0.]
    # print(spaceship.get_regular_crewmates())  # -> [White, role: Crewmate, tasks left: 10., Red, role: Crewmate, tasks left: 9.]
    #
    # print(spaceship.get_crewmate_with_most_tasks_done())
    # print(spaceship.get_impostor_with_most_kills())
