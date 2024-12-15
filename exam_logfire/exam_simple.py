import logfire
from dotenv import load_dotenv
from datetime import date

load_dotenv()


logfire.configure()  
logfire.info('Hello, {name}!', name='world')

with logfire.span('Asking the user their {question}', question='age'):
    user_input = input('How old are you [YYYY-mm-dd]? ')
    dob = date.fromisoformat(user_input)
    logfire.debug('{dob=} {age=!r}', dob=dob, age=date.today() - dob)
