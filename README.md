# Projet Reversi

## Description

Cette archive contient les fichiers DisplayBoard.py, humanPlayer.py, localGame.py, mylocalGame.py,
 myPlayer.py, myPlayerv0.py, PlayerInterface.py, RandomPlayer.py, Reversi.py et enfin ce readme.

DisplayBoard permet l'affichage d'une interface, et est nécessaire pour la bonne exécution de 
localGame et mylocalGame. On peut changer la taille de la fenêtre pygame, en changeant simplement la 
valeur de la variable sizegame en cas de besoin. Lors du jeu, les cases repassées en jaune sont les 
cases où un coup est possible.

humanPLayer contient les classes humanPlayer et clickerPlayer. Cela permet à un joueur humain de 
jouer, respectivement avec des entrées et avec la souris (sur l'interface pour la souris).

localGame lance une partie où notre I.A. joue contre elle-même (les noirs commencent).

mylocalGame est une version "custom" de localGame avec des options et differents mode de jeux:
	- dans un premier lieu une option pour entrer les joueurs, dans l'ordre de son choix (le 
	   premier entré sera les blancs, le deuxième sera les noirs). Chaque joueur est associé à 
	   une lettre:
		- "r"  pour un joueur aléatoire
		- "i"  pour notre intelligence artificielle
		- "i2" pour une version antérieure à notre intelligence artificielle
		- "h"  pour un joueur humain jouant au clavier avec des entrées. En jouant au 
			clavier, on entre les coordonées du coup désiré, et, s'il est autorisé, il 
			est joué. Lors du jeu, on peut aussi entrer "a" pour un coup aléatoire et 
			"ia" ou juste taper sur la touche entrée pour que l'IA réfléchisse à sa 
			place. Enfin, on peut quitter la partie en entrant "q".
		- "z"  pour un joueur utilisant la souris. Dans la fenêtre pygame, en cliquant sur 
			une case valide avec un clic gauche, on peut y placer sa pièce. Avec un clic 
			droit, l'I.A. réflechit à sa place, et avec un clic sur la molette, on 
			quitte la partie.
	- ensuite il est demandé un nombre de coups aléatoire à jouer, cela permet d'obtenir des 
	   parties différentes en cas de besoin. (bien évidemment, on peut entrer zéro!)

myPlayer est le fichier où est stockée notre intelligence artificielle. Elle est indépendante de 
notre localGame, dans le sens où elle peut s'adapter à n'importe lequel du moment qu'elle est 
appelée correctement.

myPlayerv0 est une version antérieure de notre intelligence artificielle.

PlayerInterface contient les fonctions de notre I.A. à appeler depuis un autre fichier.

RandomPlayer contient le joueur aléatoire.

Reversi contient la globailité du jeu.


## Stratégie


Pour ce qui est de la stratégie, nous avons utilisé une version itérative de l'approche alphabeta, 
explorant l'arbre des possiblités profondeur après profondeur, s'arrêtant en fonction du temps qui 
lui reste. Il s'agit donc d'un pari, car chaque coup ayant un temps limite élévé, on estime qu'il 
peut prendre entre le-dit temps limite et 14% du temps limite. 
14 est un chiffre trouvé à force de tatonner, afin de s'arrêter ni trop tôt ni trop tard.

Tout au long de la partie, on espère voir au minimum en profondeur 3, et en profondeur 4 ou plus si 
possible.

En fin de partie, on part jusqu'à la fin de l'arbre sur beaucoup de coup à l'avance, mais avec une 
heuristique beaucoup plus simple, afin de pouvoir remporter plus ou moins à coup sur la partie.
On note que cela marche beaucoup moins sur un IA qui utilise des probabilités de victoire en fin de 
partie au lieu d'un alphabeta simple.

Pour notre heuristique, nous avons fait simplement fait en sorte qu'elle évalue un plateau, de cette 
manière:

-les coins ont un poids très élevé
-les sous coins (autour des coins) ont un poids négatif, puis nul une fois que leur coin est pris
-les sous sous coins (autour des sous coins) ont un poids élevé, surtout au bords
-les bords ont un poids assez élevé
-les sous bords ont un poids négatif, mais qui reste modéré
-les cases centrales ont un poids faible

Nous avons ajouté quelque chose de plus pour les coins : étant donné que l'on cherche à ce que notre 
IA veuille une position solide sur les coins et les bords, nous ajoutons beaucoup de poids pour un 
coin étendu, et le score augmente drastiquement si deux coins sont reliés.

Pour l'heuristique de fin de partie, c'est une heuristique simple retournant une valeur élevée 
positive, ou négative s'il y a un gagnant, ou une valeur nulle autrement. Si les valeurs sont 
élevées, c'est afin que si l'IA a l'occasion de gagner en cours de partie, elle le fasse.

Nous n'avons pas joué sur la mobilité. Une IA utilisant l'iterativité peut voir plus loin si elle a 
peu de mobilité, et de manière générale, avoir beaucoup de mobilité est aussi un avantage. Etant 
donné le temps limite sur une partie, nous avons préféré économiser du temps plutôt que de faire des 
calculs sur la mobilité.

## Installation
### Clone
Clone this repository to your local machine 
```shell
$ git clone https://github.com/Exjp/AI_Othello
```
### Setup
Check the version of Python 3 that is installed in the system by typing: 
```shell
$ sudo apt-get -y upgrade
$ python3 -V
```
To manage software packages for Python and download pygame, let’s install pip
```shell
$ sudo apt-get install -y python3-pip
```
Download pygame
```shell
$ pip3 install pygame
```


## Auteurs

**Pourtier Jacques**
- Github: [@Exjp](https://github.com/Exjp)

	**Antri Sofian**
- Github: [@Kronenby](https://github.com/Kronenby)

- [MIT license](https://github.com/Exjp/AI_Othello/blob/master/LICENSE)<br/>
- Copyright © 2019 [Exjp](https://github.com/Exjp)