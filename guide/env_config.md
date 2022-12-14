#### Environment Configuration Guide

$\bullet$ Make sure you have installed conda

To check whether conda installed or not

```
$ conda --version
```

if not, you can refer to https://conda.io/projects/conda/en/latest/user-guide/install/index.html, which helps intall conda only

or, you can install anaconda https://docs.anaconda.com/anaconda/install/, which has conda coming with it 



$\bullet$ After completing conda installation, create a new enviroment and download the necessary dependencies, do

You need to pull the git repo first to get the "requirements.txt" file for this project

```
cd to the repo folder in your computer
$ conda create -n csc3170 --file requirements.txt
$ conda activate csc3170
```



$\bullet$ Whenever you try to run the project code, you need to switch to the "csc3170" environment

If you try to run the codes in command line, do
(Windows users could use anaconda prompt with priviledged rights)
```
$ conda activate csc3170
```

In VSC, you can achieve this by selecting python interpreter, do

Shift+Command+p (for Win, Shift+Control+p) $\rightarrow$ Type "Python: Select Interpreter" $\rightarrow$ Select "csc3170"

