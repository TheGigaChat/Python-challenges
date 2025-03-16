"""Beat the odds."""
import collections
import random
from heapq import nlargest


def read_words(file_path: str) -> dict:
    """
    Read words from file into dictionary.

    Read file and return dictionary
    where keys represent words
    and values represent the count of the given word.

    Each word is on a separate line.
    :param file_path: File to read
    :return: Dictionary of word counts
    """
    with open(file_path, 'r') as file:
        words_list = file.read().splitlines()

    return dict(collections.Counter(words_list))


def guess(sentence: str, guessed_letters: list, word_frequencies: dict) -> str | None:
    """
    Offer the letter which would most probably give the best result.

    The goal of the game is to guess the sentence.
    The sentence is revealed by revealing letters.
    The player guesses a letter, if the letter
    exists in the sentence, all the given letters
    are revealed. The sentence is revealed when all
    the letters are revealed.

    The function should take into account possible
    words from word_dict parameter. The sentence is
    combined using the words from the dictionary and
    spaces between words.

    The sentence parameter represents the sentence
    to be guessed. The value consists of letters,
    spaces ( ) and underscores (_). Space represents
    the space between the words. Underscore indicates
    a letter which has to be guessed. Letter itself
    represents already guessed and revealed letters.

    In addition, the function takes guessed_letters
    parameter which indicates already guessed letters
    which are not in the sentence.

    The best guess is the letter which would have the
    highest probability to reveal letters in the sentence.
    It doesn't matter how many letters will be reveled,
    the function should take into account the probability
    that at least one letter would be revealed.

    Some examples:
    format:
    x)
    correct sentence
    sentence given to the function
    guessed_letters given to the function
    word_dict given to the function

    1)
    hi
    __
    []
    {"hi": 1}

    If the whole sentence is "hi" (one word)
    it is represented as "__".
    If the dictionary consists of only one word "hi",
    then the probability that "h" or "i" would reveal
    at least one letter is 100% for both.

    2)
    hi
    __
    []
    {"hi": 1, "he": 1}
    probabilities:
    h: 100%
    i: 50%
    e: 50%

    3)
    hi
    __
    []
    {"hi": 1, "he": 1, "so": 1}
    probs:
    h: 66%
    i: 33%
    e: 33%
    s: 33%
    o: 33%

    4)
    hi
    __
    []
    {"hi": 1, "he": 3, "so": 1}
    probs:
    h: 80% (4 cases out of 5)
    e: 60% (3 / 5)
    rest 20% (1 / 5)

    5)
    so fun
    __ ___
    {'this': 2, 'is':2, 'he': 3, 'so': 1, 'fun': 1, 'sun': 2, 'far': 1}
    as we have 2 words, we will give probabilities for both words separately:
    n: 0% 75% (3 out of 4): fuN, suN, suN, far
    u: 0% 75% the same
    s: 50% 50% in first word: So, iS, iS, he, he, he.
               second word: Sun, Sun, fun, far
    f: 0% 50%
    h: 50% 0%
    e: 50% 0%
    i: 33% 0%
    a: 0% 25%
    r: 0% 25%
    o: 16% 0%

    6)
    thin is test
    t___ __ t__t
    ['t'] - 't' is already guessed and revealed
    {'term': 3, 'is': 1, 'of': 1, 'that': 4, 'test': 5, 'thin': 2, 'tide': 2}
    as 't' is already revealed and guessed, the words
    in the sentence cannot contain any more 't' letters.
    The first word can be: term, thin, tide (others have another t)
    the hird word can be: that, test
    Percentages:
    e: 71% 0% 55%
    i: 57% 50% 0%
    s: 0% 50% 55%
    f: 0% 50% 0%
    ....

    :param sentence: Sentence to be guessed.
    :param guessed_letters: A list of already guessed letters
    (both revealed and not existing letters).
    :param word_frequencies: A dictionary of words and their counts.
    Use the output from read_words.
    :return: The letter with the best probability.
    """
    if "_" not in sentence or not sentence:  # If no letters are hidden or sentence is empty
        return None

        # Add revealed letters from the sentence to guessed_letters
    for char in sentence:
        if char != " " and char != "_" and char not in guessed_letters:
            guessed_letters.append(char)

        # Split the sentence into words
    words_in_sentence = sentence.split(" ")
    probability_dict = {}

    # Calculate probabilities for each word
    for word in words_in_sentence:
        result = evaluate_word(word, word_frequencies, guessed_letters)
        if result:
            letter, probability = result
            probability_dict[letter] = probability

    if not probability_dict:  # No letters found to guess
        return None

    # Find the letter with the highest probability
    max_probability = max(probability_dict.values())
    for letter, probability in probability_dict.items():
        if probability == max_probability:
            return letter
    return None


def evaluate_word(word, word_frequencies, guessed_letters):
    """Evaluate possible guesses for a single word."""
    if "_" not in word:  # If the word is fully revealed
        return None

    # Filter words by length matching the current word
    possible_words = {wd: count for wd, count in word_frequencies.items() if len(wd) == len(word)}

    # Exclude words containing guessed letters not in the current word
    for guessed_letter in guessed_letters:
        if guessed_letter not in word:
            possible_words = {wd: count for wd, count in possible_words.items() if guessed_letter not in wd}

    # Check pattern matches between possible words and the current word
    filtered_words = {}
    for wd, count in possible_words.items():
        matches_pattern = all(
            word[i] == "_" or word[i] == wd[i] for i in range(len(word))
        )
        if matches_pattern:
            filtered_words[wd] = count

    # Calculate the probability of each letter revealing the word
    total_counts = sum(filtered_words.values())
    return select_best_letter(filtered_words, guessed_letters, total_counts)


def select_best_letter(filtered_words, guessed_letters, total_counts):
    """Select the best letter to guess based on probabilities."""
    letter_counts = {}
    for word, count in filtered_words.items():
        unique_letters = set(word)  # Only unique letters in the word
        for letter in unique_letters:
            if letter not in letter_counts:
                letter_counts[letter] = 0
            letter_counts[letter] += count

    # Sort letters by their probabilities (descending order)
    sorted_letter_counts = dict(sorted(letter_counts.items(), key=lambda x: -x[1]))
    for letter, count in sorted_letter_counts.items():
        if letter not in guessed_letters:  # Exclude already guessed letters
            return letter, (count / total_counts)
    return None


def the_game(filename, word_count):
    """Play the game."""
    d = read_words(filename)
    c = collections.Counter(d)
    correct_sentence = " ".join([x for _, x in nlargest(word_count, ((random.random(), x) for x in c.elements()))])
    sentence = "".join([x if x == ' ' else '_' for x in correct_sentence])
    guessed_letters = []
    print("Correct sentence: " + correct_sentence)
    print(sentence)
    cnt = 0
    while True:
        guessed_letter = guess(sentence, guessed_letters, d)
        if guessed_letter is None or guessed_letter in guessed_letters:
            print("Nothing to guess any more, breaking.")
            break
        print('guessed:' + guessed_letter)
        guessed_letters.append(guessed_letter)
        sentence = "".join([c if c == guessed_letter else sentence[i] for i, c in enumerate(correct_sentence)])
        print("Sentence: " + sentence)
        cnt += 1
        if '_' not in sentence:
            print("Congrats! Number of guesses:" + str(cnt))
            break

if __name__ == '__main__':
    sentence = "__"
    guessed_letters = []
    word_frequencies = {"hi": 1}
    print(guess(sentence, guessed_letters, word_frequencies))

    sentence = "__"
    guessed_letters = []
    word_frequencies = {"hi": 1, "he": 1}
    print(guess(sentence, guessed_letters, word_frequencies))

    sentence = "__"
    guessed_letters = []
    word_frequencies = {"hi": 1, "he": 1, "so": 1}
    print(guess(sentence, guessed_letters, word_frequencies))

    sentence = "__"
    guessed_letters = []
    word_frequencies = {"hi": 1, "he": 3, "so": 1}
    print(guess(sentence, guessed_letters, word_frequencies))

    sentence = "__ ___"
    guessed_letters = []
    word_frequencies = {'this': 2, 'is': 2, 'he': 3, 'so': 1, 'fun': 1, 'sun': 2, 'far': 1}
    print(guess(sentence, guessed_letters, word_frequencies))

    sentence = "t___ __ t__t"
    guessed_letters = ['t']
    word_frequencies = {'term': 3, 'is': 1, 'of': 1, 'that': 4, 'test': 5, 'thin': 2, 'tide': 2}
    print(guess(sentence, guessed_letters, word_frequencies))
    
