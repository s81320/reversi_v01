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

see my [wiki of reversi](https://github.com/s81320/reversi/wiki/clean-code)

cheat sheet link at the bottom.

## 4 build management
automated build with github action
![Python application](https://github.com/s81320/reversi/workflows/Python%20application/badge.svg)

This build includes testing with pytest and documentation with pydoc. The created documents are uploaded (from the virtual machine this is executed in) using an artifact upload action. Getting this done in the yml file directly tought me a lot.

## 5 unit tests

testing is done in a testfile to be executed with pytest.

## 6 continuous delivery

ci with circle ci:  [![<ORG_NAME>](https://circleci.com/gh/s81320/reversi.svg?style=svg)](https://circleci.com/gh/s81320/workflows/reversi/tree/master)

## 7 ide

i still like to work with sublime text and do things in the terminal.

Hower, intelliJ definitely has its advantages! These are my most used abbreviations in intelliJ:

[keys1](https://github.com/s81320/reversi/blob/master/pictures/intelliJ-1.png) [keys2](https://github.com/s81320/reversi/blob/master/pictures/intelliJ-2.png) and this list was also helpful:
[intelliJ keys](https://resources.jetbrains.com/storage/products/intellij-idea/docs/IntelliJIDEA_ReferenceCard.pdf?_ga=2.136755446.751887257.1581684340-1608094495.1581684340)

## 8 DSL demo example snipplet

see my [wiki of reversi](https://github.com/s81320/reversi/wiki/a-domain-specific-language-for-reversi)
## 9 functional programming

see my [wiki of reversi](https://github.com/s81320/reversi/wiki/functional-programming)
