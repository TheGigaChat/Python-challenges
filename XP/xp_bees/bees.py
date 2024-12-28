"""Whether bees meet."""
import copy


def polygon_length(width: int) -> int:
    """Pol len."""
    return 3 * width ** 2 - 3 * width + 1


# find the step_style and diff
def find_step_data(steps_data: str) -> dict:
    """
    Find step data.

    Arithmetical => 1, 2, 3, 4
    3 - 2 = 2 - 1

    Arithmetical Progressive => 1, 2, 4, 7
    7 - 4 != 4 - 2 != 2 - 1
      3        2        1
           1        1  <= const diff

    Geometrical => 1, 2, 4, 8
    4 / 2 = 2 / 1

    Geometrical Progressive => 1, 3, 7, 15
    15 - 7 != 7 - 3 != 3 - 1
       8        4       2
           2        2  <= const division
    """
    steps = list(map(int, steps_data.split(",")))

    first_diff_combination = steps[1] - steps[0]
    sec_diff_combination = steps[2] - steps[1]
    third_diff_combination = steps[3] - steps[2]
    first_diff_diff_combination = sec_diff_combination - first_diff_combination
    sec_diff_diff_combination = third_diff_combination - sec_diff_combination

    step_style_dic = {
        "style": "",
        "diff": None,
        "diff_diff": None,
        "div": None,
        "div_div": None,
        "steps": steps,
        "next_step": steps[0]
    }

    # Arithmetical Case
    if sec_diff_combination == first_diff_combination:
        step_style_dic["style"] = "Arithmetical"
        step_style_dic["diff"] = first_diff_combination
        step_style_dic["diff_diff"] = 0
        return step_style_dic

    # Arithmetical Progressive Case
    else:
        if sec_diff_diff_combination == first_diff_diff_combination:
            step_style_dic["style"] = "Arithmetical Progressive"
            step_style_dic["diff"] = first_diff_combination
            step_style_dic["diff_diff"] = first_diff_diff_combination
            return step_style_dic

    # 0 division check
    if steps[0] != 0 and steps[1] != 0:
        if steps[1] % steps[0] == 0 and steps[2] % steps[1] == 0:  # because we might work only with int numbers  # Might try to test if I have some errors
            first_div_combination = int(steps[1] / steps[0])
            sec_div_combination = int(steps[2] / steps[1])

            # Geometrical
            if sec_div_combination == first_div_combination:
                step_style_dic["style"] = "Geometrical"
                step_style_dic["div"] = first_div_combination
                step_style_dic["div_div"] = 1
                return step_style_dic
        else:
            if sec_diff_combination % first_diff_combination == 0 and third_diff_combination % sec_diff_combination == 0:
                first_div_div_combination = int(sec_diff_combination / first_diff_combination)
                sec_div_div_combination = int(third_diff_combination / sec_diff_combination)

                # Geometrical Progressive Case
                if third_diff_combination != sec_diff_combination != first_diff_combination:  # Check different patterns if I will have some errors
                    if sec_div_div_combination == first_div_div_combination:
                        step_style_dic["style"] = "Geometrical Progressive"
                        step_style_dic["diff"] = first_diff_combination
                        step_style_dic["div_div"] = first_div_div_combination
                        return step_style_dic

    # Unknown case
    raise ValueError("Insufficient data for sequence identification")


def validate_given_steps(steps_style_data_original: dict) -> bool:
    """Validate data."""
    #  First 4 numbers and the 5-th number, if it doesn't match to the formula => raise ValueError.
    steps_style_data = copy.deepcopy(steps_style_data_original)  # make a copy to ensure that we don't change the original data

    for i, step in enumerate(steps_style_data["steps"]):
        next_step = None
        if steps_style_data["style"] == "Arithmetical":
            next_step = step + steps_style_data["diff"]

        elif steps_style_data["style"] == "Arithmetical Progressive":
            next_step = step + steps_style_data["diff"]
            steps_style_data["diff"] += steps_style_data["diff_diff"]

        elif steps_style_data["style"] == "Geometrical":
            next_step = step * steps_style_data["div"]

        elif steps_style_data["style"] == "Geometrical Progressive":
            next_step = step + steps_style_data["diff"]
            steps_style_data["diff"] *= steps_style_data["div_div"]

        # if i is not last and if current step not equal next step => raise ValueError
        if i != len(steps_style_data["steps"]) - 1 and next_step != steps_style_data["steps"][i + 1]:
            raise ValueError("Insufficient data for sequence identification")

    return True


def control_inputs(steps_data: str) -> bool:
    """Control steps input little information and invalid further steps."""
    steps = list(map(int, steps_data.split(",")))
    if len(steps) < 4:
        raise ValueError("Insufficient data for sequence identification")
    step_data = find_step_data(steps_data)
    validate_given_steps(step_data)
    return True


def calculate_next_step(curr_step: int, steps_style_data_original: dict) -> dict:
    """Calc next step."""
    steps_style_data = copy.deepcopy(steps_style_data_original)  # make a copy to ensure that we don't change the original data

    next_step = None
    if steps_style_data["style"] == "Arithmetical":
        next_step = curr_step + steps_style_data["diff"]

    elif steps_style_data["style"] == "Arithmetical Progressive":
        next_step = curr_step + steps_style_data["diff"]
        steps_style_data["diff"] += steps_style_data["diff_diff"]

    elif steps_style_data["style"] == "Geometrical":
        next_step = curr_step * steps_style_data["div"]

    elif steps_style_data["style"] == "Geometrical Progressive":
        next_step = curr_step + steps_style_data["diff"]
        steps_style_data["diff"] *= steps_style_data["div_div"]

    steps_style_data["next_step"] = next_step
    return steps_style_data


def change_steps_for_second_bee(steps: str) -> str:
    """Change steps."""
    steps = list(map(int, steps.split(",")))
    actual_steps = list(map(lambda pos: 62 - pos, steps))

    actual_steps_str = ""
    for i, pos in enumerate(actual_steps):
        if i == len(actual_steps) - 1:
            actual_steps_str += str(pos)
        else:
            actual_steps_str += str(pos) + ","

    return actual_steps_str


# create bees
class Bee:
    """Bee."""

    def __init__(self, honeyhopper_data: str, pollenpaddle_data: str, choice: str, hexagon_width: int):
        """Init."""
        if choice == "upper":
            self.steps = honeyhopper_data
        elif choice == "down":
            self.steps = pollenpaddle_data

        self.step_data = find_step_data(self.steps)
        self.hexagon_length = polygon_length(hexagon_width)
        self.curr_step = self.step_data["next_step"]
        self.next_st = None

        self.steps_history = {}

    def next_step(self) -> int:
        """Change the pattern for the geometrical progression."""
        self.curr_step = self.step_data["next_step"]

        step_style = self.step_data["style"]
        if step_style == "Geometrical":
            self.step_data = calculate_next_step(self.curr_step, self.step_data)
            next_st = self.step_data["next_step"]

            if next_st % self.hexagon_length != 0:
                next_st = next_st % self.hexagon_length

            self.next_st = next_st
            self.step_data["next_step"] = self.next_st
            return self.next_st
        else:

            # for all other step styles the pattern is the same
            curr_step_projection = self.curr_step - 1

            self.step_data = calculate_next_step(curr_step_projection, self.step_data)  # next step data
            next_step_projection = self.step_data["next_step"]

            next_step_projection_in_range_of_hexagon = next_step_projection % self.hexagon_length  # bee in range of the hexagon
            self.next_st = next_step_projection_in_range_of_hexagon + 1

            self.step_data["next_step"] = self.next_st
            return self.next_st

    def add_steps_to_history(self) -> bool:
        """Add to the history."""
        pair = (self.curr_step, self.next_st)
        if pair not in self.steps_history:
            self.steps_history[pair] = True
            return True
        else:
            return False


def do_bees_meet(honeycomb_width: int, honeyhopper_data: str, pollenpaddle_data: str) -> bool:  # valid raise ValueError(insufficient data)
    """
    Return whether bees meet.

    Steps plan:
    find the polygon length
    find the step_style and diff
    create bees
    valid data, first 4 numbers and the 5-th number, if it doesn't match to the formula => raise ValueError
    start bees steps
    store the history about bees steps
    find bees collision => bool
    """
    if honeycomb_width > 49:
        return True
    # change the pollenpaddle_data to actual positions
    pollenpaddle_data = change_steps_for_second_bee(pollenpaddle_data)

    # control given data steps
    control_inputs(honeyhopper_data)
    control_inputs(pollenpaddle_data)

    bee1 = Bee(honeyhopper_data, pollenpaddle_data, "upper", honeycomb_width)
    bee2 = Bee(honeyhopper_data, pollenpaddle_data, "down", honeycomb_width)

    # find bees collision => bool
    for i in range(10000):
        if bee1.curr_step == bee2.curr_step:
            return True

        bee1.next_step()
        bee2.next_step()

        # # store the history about bees steps
        # if bee1.add_steps_to_history() or bee2.add_steps_to_history():
        #     print(bee1.curr_step)
        #     print(bee2.curr_step)
        # else:
        #     return False
        print(bee1.curr_step)
        print(bee2.curr_step)
    else:
        return False


if __name__ == '__main__':
    print(polygon_length(1))  # 1
    print(polygon_length(4))  # 37
    print(polygon_length(-1))  # 7
    print(polygon_length(0))  # 1
    print()
    print(find_step_data("1,1,1,1"))  # 0,0,0,0 might be?? I think can't
    print(find_step_data("1,2,3,4"))
    print(find_step_data("5,11,17,23"))
    print(find_step_data("16,15,14,13"))
    print()
    print(find_step_data("1,2,4,7"))
    print(find_step_data("5,9,17,29"))
    print()
    print(find_step_data("1,2,4,8"))
    print(find_step_data("2,6,18,54"))
    print(find_step_data("2,4,8,16"))
    print()
    print(find_step_data("1,3,7,15"))
    print(find_step_data("5,9,17,33"))
    print(find_step_data("16,12,4,-12"))
    print()
    print(change_steps_for_second_bee("1,2,4,8"))  # 61,60,58,54
    print()
    # print(do_bees_meet(5, "2,6,18,54", "2,6,18,54"))
    print(-1 % 61)
    # print(do_bees_meet(50, "3,4,5,6,7", "1,2,4,8,16"))
