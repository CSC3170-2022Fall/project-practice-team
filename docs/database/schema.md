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

​	  $\bullet$  password: password of the consumer account

$\vartriangleright$  **publisher**: table contains info of any seller/game publisher

​      $\bullet$  <ins>ID</ins>: primary key, unique indentifier of a game publisher

​      $\bullet$  name: account name of a game publisher

$\vartriangleright$   **developer**: table contains info of any game developer

​      $\bullet$  <ins>ID</ins>: primary key, unique indentifier of a game developer

​      $\bullet$  name: name of a game developer

$\vartriangleright$  **web_section**[not implemented]: table contains info of any section of a webpage, where the selling info of a game will be displayed

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

​      $\bullet$ <ins>status</ins>: status of a barter request, which can either be 'deal'(successful), 'open'(avaliable), 'closed'(no longer avaliable, because 		         game to be sold has been bartered)

$\vartriangleright$  **promote**[not implemented]: table of the way a publisher promotes a game to sell

​      $\bullet$  <ins>pub_id</ins>: ID of the game publisher

​      $\bullet$  <ins>sec_id</ins>: ID of the web section, where the selling advertisment will be displayed

​      $\bullet$  <ins>game_id</ins>: ID of the game to sell

$\vartriangleright$  **develop**: table contains info of the developer(s) of any game, a game may have multiple developer

​      $\bullet$  <ins>dev_id</ins>: ID of the game developer

​      $\bullet$ <ins>game_id</ins>: ID of the game a developer develops

$\vartriangleright$  **prefer**[not implemented]: table of preferences for a consumer, i.e categories of games he/she prefers

​      $\bullet$  <ins>con_id</ins>: ID of the consumer

​      $\bullet$  <ins>cate_id</ins>: ID of the game category

$\vartriangleright$  **game_type**: table of the category a game belongs to, a game may associate with multiple categories

​      $\bullet$  <ins>game_id</ins>: ID of the game

​      $\bullet$  <ins>cate_id</ins>: ID of the category the game belongs to

$\vartriangleright$  **meta**: table tracks the current state of the platform

​      $\bullet$  <ins>stub</ins>: for easy database operation

​      $\bullet$  <ins>con_cnt</ins>: last consumer ID assigned

​      $\bullet$  <ins>pub_cnt</ins>: last publisher ID assigned

​      $\bullet$  <ins>dev_cnt</ins>: Iast developer ID assigned

​      $\bullet$  <ins>cate_cnt</ins>: Iast category ID assigned

​      $\bullet$  <ins>game_cnt</ins>: Iast game ID assigned
