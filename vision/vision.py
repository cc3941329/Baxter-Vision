# -*- coding: utf-8 -*-
import cv2

from letterrecognizer.interface import ILetterRecognizer
from letterrecognizer.naive_bayes import NaiveBayes
from tools.maps import ClassMap

"""
Module for cube detecting and letter recognize
"""

# for draw ru letter as en letter
ru_to_en = {
    u'а': 'a', u'б': 'b', u'в': 'v', u'г': 'g',
    u'д': 'd', u'е': 'e', u'ё': 'yo', u'ж': 'zh',
    u'з': 'z', u'и': 'i', u'й': 'Ji', 'uк': 'k',
    u'л': 'l', u'м': 'm', u'н': 'n', u'о': 'o',
    u'п': 'p', u'р': 'r', u'с': 's', u'т': 't',
    u'у': 'u', u'ф': 'f', u'х': 'kh', u'ц': 'ts',
    u'ч': 'ch', u'ш': 'sh', u'щ': 'shch', u'ъ': 'tv znak',
    u'ь': 'mg znak', u'э': 'iE', u'ю': 'Yu', u'я': 'Ya'
}

classmap = ClassMap('config/class_letter.txt')
cascade = None
letter_recognizer = None


def init(config):
    global cascade, letter_recognizer

    cascade = cv2.CascadeClassifier()
    if not cascade.load(config):
        raise Exception("Cascade not load")

    # FIXME: hard code path!
    ILetterRecognizer.setup_letters('assets/letters/training_set/marked.list')
    letter_recognizer = NaiveBayes('b.out')

i = 0

def run(frame):

    global cascade, letter_recognizer,i
    frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame2 = cv2.equalizeHist(frame2)
    cv2.imshow('test', frame2)

    image = frame.copy()
    cubes = cascade.detectMultiScale(image)

    letters = list()
    for x, y, w, h in cubes:
        start = x, y
        end = x + w, y + h
        color = 255, 255, 255

        cutted_cube = frame[x: x + w, y: y + h]

        if i < 100:
            cv2.imwrite(str(i) + '.jpg', cutted_cube)
            i+=1


        if cutted_cube.size:
            class_ = letter_recognizer.letter(cutted_cube)[0]
            letter = classmap.get_letter(class_)
            letter = ru_to_en.get(letter)
            font, scale = cv2.FONT_HERSHEY_SIMPLEX, 1
            cv2.putText(image, letter, start, font, scale, color)
            letters.append(letter)

        cv2.rectangle(image, start, end, color, 2)

    if len(cubes) > 0:
        found = " ".join(map(str, letters))
        print "Found %d rectangle(s)" % len(cubes), "r",  found

    cv2.imshow("Cascade", image)
