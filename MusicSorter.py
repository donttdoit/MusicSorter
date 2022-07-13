import os
import mutagen.id3
from mutagen.easyid3 import EasyID3

path = 'MusicFolder'
countForFolder = 3

musicFiles = next(os.walk(path), (None, None, []))[2]
musicDirs = next(os.walk(path), (None, [], None))[1]

# Подсчет количества песен по авторам и сохранение в словарь
artistCount_dict = {}
for song in musicFiles:
    songInfo = song.split('-')
    songArtist = songInfo[0].strip().title()
    if songArtist not in artistCount_dict:
        artistCount_dict.setdefault(songArtist, 1)
    else:
        artistCount_dict[songArtist] += 1

for dir in musicDirs:
    curMusicFiles = next(os.walk(os.path.join(path, dir)), (None, None, []))[2]
    countDir = len(os.listdir(os.path.join(path, dir)))
    if dir not in artistCount_dict:
        artistCount_dict.setdefault(dir, countDir)
    else:
        artistCount_dict[dir] += countDir


# Создание папок под песни
for key, value in artistCount_dict.items():
    if artistCount_dict[key] >= countForFolder and not os.path.isdir(os.path.join(path, key)):
        os.mkdir(os.path.join(path, key))

if not os.path.isdir(os.path.join(path, 'Другое')):
    os.mkdir(os.path.join(path, 'Другое'))


# Сортировка и сохранение песен
for song in musicFiles:
    print('# Обработка ', song, end='')
    songInfo = song.split('-', maxsplit=1)
    songArtist = songInfo[0].strip().title()
    songName = songInfo[1].strip()[:-4].capitalize()

    curMusicFile = os.path.join(path, song)

    try:
        tags = EasyID3(curMusicFile)
    except mutagen.id3.ID3NoHeaderError:
        tags = mutagen.File(curMusicFile, easy=True)
        tags.add_tags()

    tags['artist'] = songArtist
    tags['title'] = songName
    tags.save()

    print('  -->  Ок')
    if artistCount_dict[songArtist] >= countForFolder:
        os.rename(curMusicFile, os.path.join(path, songArtist + '/' + songArtist + ' - ' + songName + '.mp3'))
    else:
        os.rename(curMusicFile, os.path.join(path, 'Другое' + '/' + songArtist + ' - ' + songName + '.mp3'))


