#myomr
=====

An [Optical Mark Recognizer Software](https://en.wikipedia.org/wiki/Optical_mark_recognition "OMR") made by me using OpenCV and Python.

This software has two parts: a GUI configurer and a CLI OMR.

## Requirements:
* Python 2.7.x
* OpenCV 2.4.x
* Numpy
* PIL and ImageTk
* Tix 

## License:
* [GPL V2](LICENSE)

Preprocessing
-----

You might preprocessing the image to ensure that there is not problems with the sheet image alignment. 

First you might use scripts to ensure the image alignment. Enter the _/omr/src/cropped_ folder and use the *align.py* script as follow:

> python align.py x1 y1 x2 y2 regex

Where *x1* and *y1* is the beginning of the rightest superior mark, *x2* and *y2* is the beginning of the rightest inferior mark and *regex* is a regular expression refering the image files. All the result files will have a *rot_* prefix.

After you might crop the image with the _/omr/src/cropped/crop.py_ script as follow:

> python crop.py x1 y1 x2 y2 regex

Where *x1* and *y1* is the beginning of the rightest superior mark, *x2* and *y2* is the beginning of the rightest inferior mark and *regex* is a regular expression refering the image files. All the result files will have a *crop_* prefix.

GUI configurer tool
-----

Open the configurer tool (folder _/configurer/src/_) using the command line:

> python configurer.py

##Open a background image

Before you start creating a configuration file, now called *application*, it is necessary to define a background image to the canvas. This is necessary for the user to have idea how to define each field. The keyboard shortcut for the command to open the background image is *Ctrl + i* or from the *File* menu, *Open background Image*.

##Creating a new application

When a new *application* is created, all fields already set are deleted and remains only the background image. The keyboard shortcut for the new application command is *Ctrl + n* or from the *File* menu, *New*.

##Save

 O atalho de teclado para salvar uma aplicação é Ctrl+s ou no menu Arquivo, Salvar Aplicação.
Applications are saved to disk with the extension .csv (Comma Separated Values) compatible with the OMR. The *application* contains all configured fields. The keyboard shortcut to save an application is *Ctrl + s* or from the *File* menu, *Save*.

##Abrindo aplicação salva em disco

As aplicações são salvas no disco com a extensão de arquivo .csv (Comma Separated Values  - Valores separados por vírgula). Quando da abertura do arquivo de aplicação, os campos configurados são mostrados na tela na ordem como foram criados. Uma aplicação só pode ser aberta se houver uma imagem de fundo configurada. Se houver algum campo configurado anteriormente, ele será apagado e somente os campos do arquivo de aplicação aparecerão. O atalho de teclado para o comando de abrir aplicação é Ctrl+a ou no menu Arquivo, Abrir Aplicação.

##Criando novo campo

Para criar um novo campo para a correção, selecione o menu Campo, Novo, clique com o botão esquerdo do mouse por cima da imagem de fundo, selecionando o início do campo. Aparecerá um diálogo para configuração do campo. Nesse diálogo coloque a quantidade de células do campo (1 até 10), a direção do campo (horizontal ou vertical), o tipo do campo (caractere ou numeral), se o campo faz parte do identificador da folha de respostas, as dimensões de cada célula do campo em pixels e o espaçamento entre cada célula. Caso deseje desistir do processo, basta clicar no botão Cancelar. Para salvar o campo, clique em Ok. Após a seleção do campo será atualizada para as dimensões especificadas. Ao campo será atribuído um identificador que ficará próximo do campo.

##Movendo campo

Para selecionar um campo e movê-lo, utilize o botão central do mouse ou selecione o menu Campo, Mover e utilize o botão esquerdo. Clique sobre a linha limítrofe do campo, ela mudará pra a cor vermelha, indicando que foi selecionado. Após a seleção, pode-se  mantenha o botão central pressionado e mova o campo para outra área, ao soltar a operação estará finalizada.

##Apagando campo

Selecione o campo utilizando o botão central do mouse ou selecione o menu Campo, Mover e utilize o botão esquerdo. Depois de selecionado, apague o campo usando a tecla Delete.

##Alterando campo

Selecione o campo utilizando o clique com botão direito do mouse. A linha limítrofe do campo mudará para a cor azul, indicando que o campo foi selecionado. Altere as informações do campo da mesma forma que na operação de criação do campo. Caso deseje desistir do processo, basta clicar no botão Cancelar. Para salvar o campo, clique em Ok.
