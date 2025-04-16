# AreYouHuman
A library for generating random captcha using emojis. The rendering is done by PIL.

## Installation 
```bash
pip install AreYouHumanLib  
```

> [!WARNING]
> Before using it for the first time, you must download the emoji using the console command `AreYouHuman download` or download and unzip the archive:
**[emojis.zip](https://github.com/krajnow/AreYouHuman/blob/master/emojis.zip)**

## Usage
```python
from AreYouHuman import Captcha  

from AreYouHuman.types import Response

captcha = Captcha()  

response: Response = captcha.generate()  

# Correct answer (5 emojis)  
print(response.emojis_answer)

# Full emoji list (15 items: 10 wrong + 5 correct)  
print(response.emojis_list)  

# CAPTCHA image (BytesIO)  
print(response.image)
```
