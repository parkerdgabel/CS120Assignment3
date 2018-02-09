"""
    File: rhymes.py
    Author: Parker Gabel
    Purpose: Match a given word to all its possible rhymes.
    Course Number: CS120

"""


def init():
    """Reads the input file and makes the database.
    Parameters: None
    Returns: A dictionary the maps a word to its pronunciations.
    Pre-condition: Program is running.
    Post-condition: A build database for pronuciations."""
    pfile = open(input())
    return _build_pronuciation_db(pfile)


def _build_pronuciation_db(pfile):
    """Builds the pronuciations database.
    Parameters: pfile is an open File object.
    Returns: A dictionary that maps an uppercase word to a list of lists that contain its phonememe.
    Pre-condition: pfile is an open File object.
    Post-condition: A built database for the pronuciations."""
    pfile = pfile.readlines()
    p_dict = {}
    for line in pfile:
        line = line.strip().split()
        if line[0] not in p_dict:
            p_dict[line[0]] = []
        p_dict[line[0]].append(line[1::])
    return p_dict


def match_rhymes(pronuciation_db, pronuciations):
    """Returns all the words that are perfect rhymes for all pronuciations.
    Parameters: pronuciation_db is the database
                pronuciations is the list that contains all pronuciations.
    Returns:    A list of words that are perfect rhymes(Hopefully)
    Pre-conditions: pronuciation_db is a dictionary and pronuciations is a list
    Post-conditions: Returns a list of rhymes."""
    rhymes = []
    for elem in pronuciations:
        stress = _find_stress(elem)
        if stress is None:
            continue
        words = set(_match_stress(pronuciation_db, stress))
        syllables = _build_syllables(elem, stress)
        for word in words:
            val = pronuciation_db[word]
            for pronunciation in val:
                pro_stress = _find_stress(pronunciation)
                if pro_stress is None:
                    continue
                pro_syllables = _build_syllables(pronunciation, pro_stress)
                if syllables.index(stress) - 1 < 0:
                    # This acts as a dummy value to allow for the case when the word starts with a stress.
                    syllables.insert(0, "_")
                    syllable_index = 1
                else:
                    syllable_index = syllables.index(stress)
                if pro_syllables.index(pro_stress) - 1 < 0:
                    # Same reason as the other.  This code is ugly but it seems like it works.
                    pro_syllables.insert(0, "_")
                    pro_syllable_index = 1
                else:
                    pro_syllable_index = pro_syllables.index(pro_stress)
                if syllables[syllable_index - 1] != pro_syllables[pro_syllable_index - 1]:
                    sub_syllables = syllables[syllables.index(stress)::]
                    sub_pro_syllables = pro_syllables[pro_syllables.index(pro_stress)::]
                    if len(sub_syllables) != len(sub_pro_syllables):
                        continue
                    count = 0
                    for i in range(len(sub_syllables)):
                        if sub_syllables[i] == sub_pro_syllables[i]:
                            count += 1
                    if count == len(sub_syllables):
                        rhymes.append(word)

    return rhymes


def _build_syllables(elem, stress):
    """Builds the relevant syllables for a perfect rhyme.
    Parameters: elem is a list of phonemes.
                stress is a phoneme.
    Returns: list of phonemes.
    Pre-condition: elem is a list and stress is a string.
    Post-condition: returns a list of strings."""
    index = elem.index(stress)
    if index == 0:
        syllables = elem
    else:
        syllables = elem[index - 1::]
    return syllables


def _match_stress(pronuciation_db, stress):
    """Matches a stress to all words with that stress in the database.
    Parameters: pronuciation_db is the pronuciation database
                stress is the stressed phoneme.
    Returns: list of words.
    Pre-conditions: pronuciations_db is a dictionary that maps words to their pronuciations.
                    stress is a string.
    Post_conditions: returns a list of strings."""
    words = []
    for key, val in pronuciation_db.items():
        for elem in val:
            for phoneme in elem:
                if phoneme == stress:
                    words.append(key)
    return words


def _find_stress(pronunciation):
    """Finds the stressed phoneme in the pronuciation.
    Parameters: pronuciation is a list of phonemes.
    Returns: phoneme or None.
    Pre-conditions: pronunciation is a list of strings.
    Post-conditions: returns either a string or none."""
    for elem in pronunciation:
        if "1" in elem:
            return elem


def main():
    """Matches an input word to all its perfect rhymes.
    Parameters: Good vibes.
    Returns: A good grade on this assignment.
    Pre-conditions: You need a rhyme for a sick rap/poem and have a computer.
    Post-conditions: You are ready to write some slick rhymes."""
    pronuciation_db = init()
    word = input().upper()
    if word not in pronuciation_db:
        return
    pronunciations = pronuciation_db[word]
    rhymes = match_rhymes(pronuciation_db, pronunciations)
    for elem in rhymes:
        print(elem)


main()
