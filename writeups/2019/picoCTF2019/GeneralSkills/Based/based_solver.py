from pwn import *

s = remote('2019shell1.picoctf.com', 20836)

for i in range(3):
    # get encoded word
    text = s.recv().decode()
    start_index = text.find('the ') + 3
    end_index = text.find('as ')
    encoded_word = text[start_index:end_index]
    encoded_word_split = encoded_word.split()
    print(encoded_word_split)

    # construct answer
    answer = ''
    if i == 0:
        for encoded_char in encoded_word_split:
            answer += chr(int(encoded_char, 2))
    elif i == 1:
        for encoded_char in encoded_word_split:
            answer += chr(int(encoded_char, 8))
    elif i == 2:
        j = 0
        encoded_word = encoded_word_split[0]
        while j < len(encoded_word):
            answer += chr(int(encoded_word[j:j+2], 16))
            j += 2
    
    print('[*] answer : %s' % answer)
    s.sendline(answer)
    
    # print flag
    if i == 2:
        print(s.recv())