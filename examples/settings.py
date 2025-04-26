from AreYouHuman import Captcha
from AreYouHuman.types import Settings
from AreYouHuman.types import Response


captcha = Captcha()  # The standard settings will be created.

settings = Settings(
    gradient=((100, 200, 255), (200, 162, 200)),
    sizes=(400, 300),
    emojis_dir="emojis"
)
captcha = Captcha(settings=settings)  # Setting user settings.

captcha.settings.keyboard.refresh.active = True  # Default value.
captcha.settings.keyboard.confirm.active = False  # The button will be removed from the keyboard.

captcha.settings.keyboard.refresh.text = "Button 1"
captcha.settings.keyboard.confirm.text = "Button 2"  # Rename the button text.


response: Response = captcha.generate()  # Generating a captcha and getting a Response object.
print(response.emojis_answer)  # List of correct answers. (emojis)
print(response.emojis_list)  # The list of 15 emojis for keyboard generation includes 5 emojis from correct answers.
print(response.emojis_user)  # Emojis selected by the user using the keyboard.

response.get_keyboard(user_id=...)  # Generating a keyboard with 15 emojis and function buttons.
response.get_image()  # Get the BufferedInputFile of the captcha image.
response.checking_similarity()  # Checking the match of emojis_answer and emojis_user. True/False
