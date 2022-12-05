[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9422637&assignment_repo_type=AssignmentRepo)
# CSC3170 Course Project

## Project Overall Description

This is our implementation for the course project of CSC3170, 2022 Fall, CUHK(SZ). For details of the project, you can refer to [project-description.md](project-description.md). In this project, we will utilize what we learned in the lectures and tutorials in the course, and implement either one of the following major job:

<!-- Please fill in "x" to replace the blank space between "[]" to tick the todo item; it's ticked on the first one by default. -->

- [x] **Application with Database System(s)**
- [ ] **Implementation of a Database System**

## Team Members

Our team consists of the following members, listed in the table below (the team leader is shown in the first row, and is marked with 🚩 behind his/her name):

<!-- change the info below to be the real case -->

| Student ID | Student Name | GitHub Account (in Email) |
| ---------- | ------------ | ------------------------- |
| 120090326  | 房子皓 🚩      | fzh0424@outlook.com        |
| 120090234  | 王森         | 120090234@link.cuhk.edu.cn|
| 120090320  | 尹无非       | 120090320@link.cuhk.edu.cn|
| 120090225  | 郑家豪         | 120090225@link.cuhk.edu.cn  |
| 120090188 | 李子涵         | noah_822@163.com|
| 119010423  | 章辰舸        | 1418457284@qq.com         |
## Project Specification

After thorough discussion, our team made the choice and the specification information is listed below:

- Our option choice is: **Option 2**
- Our branch choice is: **Branch 1**
- The difficulty level is: **Normal**

As for Option 2, our topic background specification can be found in [background-specification.md](background-specification.md).



#### TODO List

$\bullet$ Frontend

- [ ] TODO
- [ ] TODO
- [ ] TODO
- [ ] TODO

$\bullet$ Backend

- [x] scrap data
- [ ] create database
- [ ] sql python api
- [ ] url routing



## Project Abstract

### Overview

In this project, we hope to implement an advanced game distribution platform, where both the consumer, or say the player, and the saler, or say the game publisher can get involved.

As a player, you can either purchase a game like you normally do on any game platform or barter for a game. Bartering is a new concept we try to introduce to our platform. One possible scenario where you may want to barter for a game is you would like to exchange a game, which you no longer want to play, for another game you interested in with somebody else.  Players can put the game to exchange and their wishlist on the platform, and then wait for others to make the deal.

As a publisher, you can upload the game to sell and make purchases with the platform to determine where the sale info will be displayed on the webpage.

In this project, we hope to incorporate as many aspects of database as possible, ranging from normal operations: select, insert, delete to more advanced topics: privilege granting, concurrency, etc. We really try to come up with a real world application instead of a toy model.



### Database Schema

$\vartriangleright$   **game**: table contains info of any game

​      $\bullet$  <ins>ID</ins>: primary key, unique indentifier of a game

​      $\bullet$  name: name of the game

​      $\bullet$  price: price of a game in US dollar

​      $\bullet$  pub_id: ID of the game publisher 

​      $\bullet$  release_date: date when a game is offcially distributed, in format "DD MM YYYY"

$\vartriangleright$  **consumer**: table contains info of any consumer/player

​      $\bullet$  <ins>ID</ins>: primary key, unique indentifier of a consumer

​      $\bullet$  name: account name of a consumer

$\vartriangleright$  **publisher**: table contains info of any seller/game publisher

​      $\bullet$  <ins>ID</ins>: primary key, unique indentifier of a game publisher

​      $\bullet$  name: account name of a game publisher

$\vartriangleright$   **developer**: table contains info of any game developer

​      $\bullet$  <ins>ID</ins>: primary key, unique indentifier of a game developer

​      $\bullet$  name: name of a game developer

$\vartriangleright$  **web_section**: table contains info of any section of a webpage, where the selling info of a game will be displayed

​      $\bullet$  <ins>ID</ins>: primary key, unique indentifier of a website section

​      $\bullet$  position: where the section locates on the webpage

​      $\bullet$  price: price of a section in US dollar

$\vartriangleright$  **category**: table contains info of any category a game might belong to

​      $\bullet$  <ins>ID</ins>: primary key, unique indentifier of a category

​      $\bullet$  name: name of a category, like PVP, MOBA

$\vartriangleright$  **purchase**: table of any purchase of game a consumer ever made

​      $\bullet$  <ins>con_id</ins>: ID of the cosumer who made the purchase

​      $\bullet$ <ins>game_id</ins>: ID of the game the consumer purchased

​      $\bullet$ date: date the purchase was made, in format "DD MM YYYY"

$\vartriangleright$  **rate**: table of rating record of a consumer

​      $\bullet$  <ins>con_id</ins>: ID of the consumer who rates the game

​      $\bullet$ <ins>game_id</ins>: ID of the game rated

​      $\bullet$ score: rating score, ranging from 0 to 5

$\vartriangleright$  **barter**: table of game bartering records

​      $\bullet$  <ins>con_id</ins>: ID of the consumer who wants to barter

​      $\bullet$ <ins>sell_id</ins>: ID of the game the consumer hopes to sell

​      $\bullet$ <ins>wish_id</ins>: ID of the game the consumer hopes to exchange for

$\vartriangleright$  **promote**: table of the way a publisher promotes a game to sell

​      $\bullet$  <ins>pub_id</ins>: ID of the game publisher

​      $\bullet$  <ins>sec_id</ins>: ID of the web section, where the selling advertisment will be displayed

​      $\bullet$  <ins>game_id</ins>: ID of the game to sell

$\vartriangleright$  **develop**: table contains info of the developer(s) of any game, a game may have multiple developer

​      $\bullet$  <ins>dev_id</ins>: ID of the game developer

​      $\bullet$ <ins>game_id</ins>: ID of the game a developer develops

$\vartriangleright$  **prefer**: table of preferences for a consumer, i.e categories of games he/she prefers

​      $\bullet$  <ins>con_id</ins>: ID of the consumer

​      $\bullet$  <ins>cate_id</ins>: ID of the game category

$\vartriangleright$  **game_type**: table of the category a game belongs to, a game may associate with multiple categories

​      $\bullet$  <ins>game_id</ins>: ID of the game

​      $\bullet$  <ins>cate_id</ins>: ID of the category the game belongs to



### ER Diagram

<img src="./pics/ER_diagram.png" alt="ER_diagram" style="zoom: 50%;" />

### Application Workflow

<img src="./pics/workflow.png" alt="workflow" style="zoom: 50%;" />











- [ ] 
