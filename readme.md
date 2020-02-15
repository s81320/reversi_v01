# pet project: reversi boardgame

Wkipedia explains the rules of [reversi](https://en.wikipedia.org/wiki/Reversi). It is also known as Othello.

![image](https://github.com/s81320/reversi/blob/master/pictures/reversi.png)

players gain to outnumber each other on the board.

## 1 ULM

There are three classes in reversi: Host, Player and Board. Where usually players interact directly with the board by in turn setting their stone on empty positions / spots on the board, in the software version of the game all interaction is mediated by the Host (mediator pattern). The host basically checks that all stones set on the board are in compliance with the rules of reversi. After the setting of a stone the board is updated. 

![image](https://github.com/s81320/reversi/blob/master/pictures/uml-classes.png)

A publish / subscribe pattern would also be fitting for a client-server based version of the game when updating the board. At the moment both players play on one / the same terminal and see the same board.

![image](https://github.com/s81320/reversi/blob/master/pictures/uml-sequence.png)

The last diagram is not completely finished. sorry. It is about a while loop that i turned into a recursion to fit functional programming.

![image](https://github.com/s81320/reversi/blob/master/pictures/uml-flow-control.png)

## 2 metrics
I used sonarcloud
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=s81320_reversi&metric=alert_status)](https://sonarcloud.io/dashboard?id=s81320_reversi)

and codacy
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b420315207b540aca94b6ed3131728dd)](https://app.codacy.com/manual/s81320/reversi?utm_source=github.com&utm_medium=referral&utm_content=s81320/reversi&utm_campaign=Badge_Grade_Dashboard)

pylint gave me valuable hints how to improve the formal code. I had quite a lot to do here: I had all the name conventions wrong (setStone instead of set_stone , camelBacks insted of snake_style). And I had not payed attention to how many blanks arount an assignment or a boolean operation or at the end of a line. Also i had started with indenting by tabs and had to change that to indenting by four blanks. Did that with UNIXs' expand command.

## 3 clean code

see my [wiki of reversi](https://github.com/s81320/reversi/wiki/clean-code)

cheat sheet link at the bottom.

## 4 build management
automated build with github action
![Python application](https://github.com/s81320/reversi/workflows/Python%20application/badge.svg)

This build includes testing with pytest and documentation with pydoc. The created documents are uploaded (from the virtual machine this is executed in) using an artifact upload action. Getting this done in the yml file directly tought me a lot.

## 5 unit tests

unittests are in test06.py to be executed with pytest. This is included in the automated testing in github actions.

## 6 continuous delivery

ci with circle ci:  [![<ORG_NAME>](https://circleci.com/gh/s81320/reversi.svg?style=svg)](https://circleci.com/gh/s81320/workflows/reversi/tree/master)

## 7 ide

i like working with sublime text and doing things in the terminal.

However, intelliJ definitely has its advantages! These are my most used abbreviations in intelliJ:

[keys1](https://github.com/s81320/reversi/blob/master/pictures/intelliJ-1.png) [keys2](https://github.com/s81320/reversi/blob/master/pictures/intelliJ-2.png) and this list was also helpful:
[intelliJ keys](https://resources.jetbrains.com/storage/products/intellij-idea/docs/IntelliJIDEA_ReferenceCard.pdf?_ga=2.136755446.751887257.1581684340-1608094495.1581684340)

## 8 DSL demo example snipplet

see my [wiki of reversi](https://github.com/s81320/reversi/wiki/a-domain-specific-language-for-reversi)

also, the uml diagrams were created applying a dsl, platUML.
## 9 functional programming

see my [wiki of reversi](https://github.com/s81320/reversi/wiki/functional-programming)
