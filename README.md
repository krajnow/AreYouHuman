# AreYouHuman
**Emoji-based CAPTCHA verification library**  

## Installation  
```bash  
pip install AreYouHumanLib  
```

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

```
Response Object

Attribute	Description
----------------------------------------------
emojis_answer	5 correct emojis (list)
emojis_list	15 emojis (10 wrong + 5 correct)
image		Image bytes (BytesIO)
```
