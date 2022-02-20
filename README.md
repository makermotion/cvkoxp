## Dependencies
- AutoHotKeys (needs to be added to PATH after installation): https://github.com/Lexikos/AutoHotkey_L/releases
- Teserract (needs to be added to PATH after installation): https://github.com/UB-Mannheim/tesseract/wiki 

## Environment
- python3.9
- install requirements.txt (pip)
- In game UI has to be scaled up to 1.3 in Options > Game Option1 menu.
- only works with 1920x1080 res.

## Possible Actions:
- att start
- att stop
- lf start ('light feet' skill needs to be placed 6th place in skill bar)
- lf stop
- wolf start ('Strength of wolf' skill needs to be placed 8th place in skill bar)
- wolf stop
- safety start ('safety' skill needs to be placed 6th place in skill bar)
- safety stop

## More on cvkoxp
cvkoxp is a hobby side project, when I was younger I played Knight Online a lot (not regretting :D). 
lately I saw the game again on twitch and gave it a try. While I was playing, this koxp thing came to my mind 
and I came up with this dirty but working basic script. 

This actually desinged to work for 'Rogue' class in game but because it only selects monsters and presses the keys 
where your skills are located, i guess it could be used also for other classes in the game.

## Demo
![cvkoxp](https://user-images.githubusercontent.com/22776403/154857895-a55d3289-9053-4fdc-9e82-433aed382919.gif) 

watch on youtube: https://www.youtube.com/watch?v=Y17gLpV7eoM

## TODO:
- improve selected monster name recognition: sometimes because of background, agent cant read the selected monster name
- fix spells with long cast times: agent cant wait for spells with long cast times like wolf, so it sometimes wont work while attacking
- a gui?
