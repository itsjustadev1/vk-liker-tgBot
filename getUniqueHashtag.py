import requests
import random
# сначала необходимо сгенерировать случайный хэш
# далее проверить на уникальность


def generateHash():
    s1 = '12342'
    s2 = ['cat', 'dog', 'empty', 'bottle']
    s3 = '25431'

    # hash = random.shuffle(s1) + random.choice(s2) + random.shuffle(s3)
    # print(hash)
    shuffledS1 = s1.split()
    for i, word in enumerate(map(list, shuffledS1)):
        random.shuffle(word)
        shuffledS1[i] = ''.join(word)

    shuffledS2 = random.choice(s2)

    shuffledS3 = s3.split()
    for i, word in enumerate(map(list, shuffledS3)):
        random.shuffle(word)
        shuffledS3[i] = ''.join(word)

    return (shuffledS1[0] + shuffledS2 + shuffledS3[0])
