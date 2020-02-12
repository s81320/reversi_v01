# pet project: reversi boardgame

## 1 ULM
## 2 metrics
I used sonarcloud
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=s81320_reversi&metric=alert_status)](https://sonarcloud.io/dashboard?id=s81320_reversi)

and codacy
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b420315207b540aca94b6ed3131728dd)](https://app.codacy.com/manual/s81320/reversi?utm_source=github.com&utm_medium=referral&utm_content=s81320/reversi&utm_campaign=Badge_Grade_Dashboard)

I worked with pylint to get hints for how to improve the code. I had quite a lot to do here: I had all the name conventions wrong (setStone instead of set_stone , camelBacks insted of snake_style). And I had not payed attention to how many blanks arount an assignment or a boolean operation or at the end of a line. Also i had started with indenting by tabs and had to change that to indenting by four blanks. Did that with UNIXs' expand command.
## 3 clean code
  * intuitive names that need no further documentation:

There are two players, each one has a number. Each player has to know their own number and also their opponents number.
The corresponding getter functions are get_my_number and get_other_player_number. 
On second thoughts: Getting the opponents number is performing a calculation (starting with the players own number) and not getting a property of the object. Maybe it is not a getter after all??
  * write short functions:

Before a stone can be set on the board, the host has to check if this is feasible and complies with the rules of the game:
The spot / position has to be empty it has to be next to a stone of the opponent and it has to enclose stones of the opponent.
Obviously being next to a stone of the opponent is required to enclose stones of the opponent. In the beginning when the focus was on getting the logic right, I was glad to get it right and running stepwise. Now that it works the required condition does not have to be checked separately.

  * single exit points for functions:

In the check_enclose_opponent() I disagree with pylint about dead code.
~~~~
take06.py:189:8: W0612: Unused variable 'dir_enclose_opponent' (unused-variable)
take06.py:215:8: R1705: Unnecessary "else" after "return" (no-else-return)
~~~~
There is an if statement, and in the then case a return statement. The code pylint thinks is unused is after this statement. I checked (print to scree) that the variable dir_enclose_opponent (a list of directions in which stones of the opponent are enclosed) is used.
Since this should not happen to begin with I should refactor the code...

## 4 build management
automated build with github action
![Python application](https://github.com/s81320/reversi/workflows/Python%20application/badge.svg)

to do: gradle, generate docs, call tests
## 5 unit tests
## 6 continuous delivery
show pipepines in circle ci , travis ci
## 7 ide
## 8 DSL demo example snipplet
## 9 functional programming
