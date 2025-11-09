# Project Requirements

## Description

Create a web application with no backend using Vite and React. It will display a phrase to type with an on screen keyboard that reflects the user's input

### Requiremenets

1. When a user presses a key that key gets pressed on the on screen keyboard
2. When a key is unpressed it shows it unpressed on the on screen keyboard
3. The next key that is required to be pressed will be outlined in red
4. The next letter that needs to be typed will be underlined
5. When the correct key is typed the letter will turn black and the underline will go to the next key and the red highlight will go to the next key on the on screen keyboard
6. if the next letter is capitalized the red highlight will go to the shift key, until its pressed then it will go to the letter
7. when you press the shift key the one screen keyboard will change to reflect the shift options
8. If you press the wrong key the keyboard animation will still happen, but you will not advance to the next letter
9. When you finish typing out the phrase, it will go to a new phrase

### Other Notes

* Use keydown/keyup events in jsx
* Use useMemo to memorize the keyboard layout 
* Use useRef to make the keyboard keys not be re rendered, even if the value changes