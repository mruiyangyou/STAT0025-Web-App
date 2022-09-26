# University College London STAT0025 Opreational Research Assiatance App

This repository consists of two parts. The first part is the introduction of how the web calculation app works. The second part is how you can run the code on your own ide to see the details of the calcultion and it requires you know a bit about **Python**.

## STAT0025-Web-App

 The web incorporates most type of questions in STAT0025 syllabus, ranging from **graphic solution, simplex algothirsm visualization, bigM visualization and markov dynamic programming**.  For rest of the question like dynamic programming and two phase visualization, it is still under development. As I know, many students are unfamillar with operational research. 

This website aims to help students understand the process of calculation and save them much time as iit is 100% consitent with syllabus and easy and concise to use. The return error like **"can't solve" or "there are no solutions"** are still under development. At this point, if the website doesn't return answer . You can take it as can not be solved. 

Most of questions aims to solve maxmize question, if the problem is minimize. Simply type your  coefficient of cost function into
$$
-1 \times coefficent of cost function
$$

* Minimize: [3, 8] =  Minimize: [-3,-8]

Most input is Python list. if you don't understand list, simply understand it as **Matrix** . Make sure if you type any non numeric character, remember to add "".

Everyone can access the page through: **[STAT0025-Web](https://stat0025-help-app.herokuapp.com)**

Url: **https://stat0025-help-app.herokuapp.com**

### Home Page

You can access github page, markdown files and contact me in the homepage. There is a navbar on Top of the page which you can acess to all calculation tools. 

### BigM

The input should looks like this:

![BigM Input](Introimage/bigM.png)

### Graphic Solution

Input:

![GraphicSolution](Introimage/graphicSol.png)

### Simplex

Simplex page is really similar to BigM without the last character line.

### Markov Dynamic Programming

input:

![Markov Dynamic Programming](Introimage/markov.png)

More advanced adversion is still under developemt. This calculation only accepts from each state it can move to all the next state in next phase.

## Python code

If you know a bit python, you can run all the calculation in your own terminal. I will show how you can type your own input and then run that in terminal. All the relevant package are in the **requirements.txt** file in the web directory.

The directory looks like this. Take example as GraphicSolution.

* GraphicSolution/

​						input.py

​						GraphicSolution.py

​						utils.py

Each category cosists of one input file while cotaina a input class object and a calculation file. All you nedd to do is type your input in the input file and run the calculation file. It will also give you the format of question like you constraints and objective functions.

### Graphic Solution

Run the following line in the terminal/bash

` python3 GraphicSolution.py`

### Simplex visual

`python3 SimplexVisual.py`

### BigM visual

`python3 bigm.py`

### Markov dynamic Programming

`python3 StochasticOptimize.py`

### Output format

![Output](Introimage/output.png)

## Notice

The whole project are stlll under developnment and I will update as soon as possible. Thank you for using and hope this help your operational research learning!!! Feel free to contanct me thorough **m.ruiyangyou2@gmail.com** or fork the repository. 





