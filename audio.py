from gtts import gTTS
import os
import pygame

# set text
text = "未开始开采"

# generate audio
fn = "empty.mp3"
tts = gTTS(text=text, lang='zh')
tts.save(fn)

# play
pygame.mixer.init()
pygame.mixer.music.load(fn)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
