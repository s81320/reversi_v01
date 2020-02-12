# pet project: reversi boardgame

## 1 ULM
## 2 metrics
I used sonarcloud
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=s81320_reversi&metric=alert_status)](https://sonarcloud.io/dashboard?id=s81320_reversi)

and codacy
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b420315207b540aca94b6ed3131728dd)](https://app.codacy.com/manual/s81320/reversi?utm_source=github.com&utm_medium=referral&utm_content=s81320/reversi&utm_campaign=Badge_Grade_Dashboard)

I think it is kind of unfair / time consuming that codacy grades my quality down if I don't do the markdown in this readme in git flavour. Not enough spaces in the bullet list -> get code quality B ??

### pylint

I worked with pylint to get hints for how to improve the code. I had quite a lot to do here: I had all the name conventions wrong (setStone instead of set_stone , camelBacks insted of snake_style). And I had not payed attention to how many blanks arount an assignment or a boolean operation or at the end of a line. Also i had started with indenting by tabs and had to change that to indenting by four blanks. Did that with UNIXs' expand command.

## 3 clean code

see my Wiki [wiki of reversi](./wiki/clean-code)


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
