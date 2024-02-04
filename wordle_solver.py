import pandas as pd
import numpy as np
import math

# main function
def main():
    word_list = read_in_data('./wordle_answers.txt')
    prev_word = ''
    prev_hint = ''
    prev_word_subset = word_list
    for i in ['first', 'second', 'third', 'fourth', 'fifth', 'sixth']:
        prev_word, prev_hint, prev_word_subset = wordle_guess(prev_word, prev_hint, prev_word_subset, i)

# takes in previous word guessed, hint, and remaining words to produce optimal guesses
def wordle_guess(prev_word, prev_hint, prev_word_list, guess_num):
    # find remaining possible words
    cur_word_subset = prev_word_list
    if guess_num != 'first':
        cur_word_subset = get_words_matching_pattern(prev_word, prev_word_list, prev_hint)

    # calculate information gained from guessing each word
    word_information_dict = {}
    i = 1
    for word in cur_word_subset:
        print('Calculating optimal', guess_num, 'guess...', '{:.2f}'.format(i / cur_word_subset.shape[0] * 100), '%', end='\r')
        word_information_dict[word] = calculate_information(word, cur_word_subset)
        i += 1
    print()

    # display the top guesses
    print('The top guesses are:')
    i = 0
    for k, _ in sorted(word_information_dict.items(), key=lambda x: x[1], reverse=True):
        if i >= 10:
            break
        print(k + '   ', end='')
        if i == 4:
            print()
        i += 1
    print()

    # have user type in what word they guessed
    cur_word = input('Enter you ' + guess_num + ' guess (if you guessed correctly, press ENTER): ')
    if cur_word == '':
        print()
        print('Congrats on winning!')
        quit()

    # have user type in what hint they received
    cur_hint = input('Enter the colors of the squares (g for green, y for yellow, b for gray): ')

    # if it's their last guess and they did not win, display the remaining words it could have been
    if guess_num == 'sixth':
        print('Unfortunately you did not win')
        cur_word_subset = get_words_matching_pattern(cur_word, cur_word_subset, cur_hint)
        word_information_dict = {}
        i = 1
        for word in cur_word_subset:
            print('Finding remaining words...', '{:.2f}'.format(i / cur_word_subset.shape[0] * 100), '%', end='\r')
            word_information_dict[word] = calculate_information(word, cur_word_subset)
            i += 1
        print()
        print('Here are the remaining words it could have been:')
        i = 0
        for k, v in sorted(word_information_dict.items(), key=lambda x: x[1], reverse=True):
            print(k + '   ', end='')
            if i != 0 and i % 4 == 0:
                print()
            i += 1
    print()

    return cur_word, cur_hint, cur_word_subset

# calculates the information gained by guessing a particular word
def calculate_information(guess_word, word_list):
    count = 0
    hint_pattern_counts = {}
    for answer_word in word_list:
        pattern = get_pattern(guess_word, answer_word)
        count += 1
        if pattern in hint_pattern_counts:
            hint_pattern_counts[pattern] = hint_pattern_counts[pattern] + 1
        else:
            hint_pattern_counts[pattern] = 1

    information = 0
    for val in hint_pattern_counts.values():
        prob = val / count
        information += prob * math.log2(1 / prob)
    
    #print(guess_word, information)
    return information

# gets the hint pattern for guess_word, assuming answer_word is the answer
def get_pattern(guess_word, answer_word):
    pattern = '-----'
    # find greens
    for index in range(5):
        if guess_word[index] == answer_word[index]:
            pattern = pattern[:index] + 'g' + pattern[index + 1:]
            #pattern[index] = 'g' # green
    answer_word_subset = get_word_subset_from_pattern(answer_word, pattern)
    # find grays
    for index in range(5):
        if pattern[index] != '-':
            continue
        char_index = answer_word_subset.find(guess_word[index])
        if char_index >= 0:
            pattern = pattern[:index] + 'y' + pattern[index + 1:]
            #pattern[index] = 'y' # yellow
        else:
            pattern = pattern[:index] + 'b' + pattern[index + 1:]
            #pattern[index] = 'b' # gray (black)
            answer_word_subset = answer_word_subset[:char_index] + answer_word_subset[char_index + 1:]
    return pattern

# gets the characters in word corresponding to the '-' in the pattern
# word: stern
# pattern: g--g-
# returns: ten
def get_word_subset_from_pattern(word, pattern):
    output = ''
    for index, c in enumerate(pattern):
        if c == '-':
            output += word[index]
    return output

# search through a list of words that are possible answers given a word and the hint for it
def get_words_matching_pattern(word, word_list, pattern):
    possible_words = []
    # iterate through words in the list
    for w in word_list:
        is_match = True
        unused_chars = ''
        for i in range(5):
            if pattern[i] == 'g': # green
                if word[i] != w[i]:
                    is_match = False
                    break
            elif pattern[i] == 'b': # gray (black)
                if word[i] in w:
                    is_match = False
                    break
                unused_chars += w[i]
            elif pattern[i] == 'y': # yellow
                if word[i] == w[i]:
                    is_match = False
                    break
                unused_chars += w[i]
        
        if not is_match:
            continue

        for i in range(5):
            if pattern[i] == 'y': # yellow
                char_index = unused_chars.find(word[i])
                if char_index < 0:
                    is_match = False
                    break
                else:
                    unused_chars = unused_chars[:char_index] + unused_chars[char_index + 1:]

        if is_match:
            possible_words.append(w)
    return np.array(possible_words, dtype=np.str_)

# read in words from a file
# one word per line
def read_in_data(filename):
    # read in data
    data = pd.read_csv(
        filepath_or_buffer=filename,
        header=None,
        dtype=np.str_,
    )
    data = data.to_numpy()
    data = np.squeeze(data)
    return data

if __name__ == '__main__':
    main()
