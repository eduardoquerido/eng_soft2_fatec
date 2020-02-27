# Engenharia de Software II 

## Nome Projeto: <nome_do_projeto>

### Groupo:

    - Cleber Silva
    - Eduardo Querido
    - João Cruz
    - José Francisco
    - Willian Couto

## Orientações para os devs

Como rodar a aplicação? 

1. Criar um ambiente virtual:

    > $ pip3 install virtualenv

    > $ mkvirtualenv <nome_do_ambiente_virtual> Ex: mkvirtualenv gsw_project

2. Navegar até a pasta do ambiente virtual, no caso "$ cd gsw_project/bin/", nesta pasta ativar o virtualenv com o comando "activate"

3. Com o ambiente virtual criado, entrar na pasta de destino da aplicação que você queira deixá-lo e fazer o clone da aplicação que está no github.

    > $ git clone git@github.com:eduardoquerido/eng_soft2_fatec.git 

4. Com o ambiente virtual ativado, instalar os requirements do projeto

    > $ pip install -r requirement.txt (no caso, o projeto terá mais de um requirement, por tanto, provavelmente mudando para dev.txt que irá puxar de um base.txt e um production.txt que também puxará do base)

#### Obs: Posteriormente será criado uma imagem Docker para facilitar os passos anteriores

5. Feito isso, teste a aplicação com:

    > $ python3 manage.py runserver --settings gsw_project.settings.local_dev