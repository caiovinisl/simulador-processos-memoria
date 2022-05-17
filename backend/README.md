1- Vc precisa ao menos rodar esses 2 comandos:

    docker build -t so_backend_image . builds the image[dont forget the dot]
    docker run -d --name so_backend_container -p 8000:8000 so_backend_image run the Container

2- Instalar as extensõe no vscode (remote container)

3- Leia essa página https://davidefiocco.github.io/debugging-containers-with-vs-code/#preparing-to-debug-in-the-container
    obs: Não deixe de cliquer no link que direciona para um video-gif (no tópico Preparing to debug in the containerPermalink)

4- Ao selecionar Reopen in Container  Lembrar de selecionar o docker-compose! (!)
    (!) A manha é que o vscode só esteja vendo a pasta backend

5- Se vc fez tudo certo! já deve ter o launch.json prontinho e já utilizando o vscode dentro do container.

5.5- Adicionar o campo "cwd": "${fileDirname}" no launch.json, para dizer que para o debug, de qual pasta é o working directory

6- Agora só falta vc rodar o código! Vc precisa achar o arquivo app/main.py, o abra e depois aperte f5! 

7- Agora vc está debugando! então o principal é que vc marque os pontos para debugar e acesse http://127.0.0.1:8000/docs para escolher qual endpoint vc vai debugar

8- Se vai debuggar os algoritimos de escalonamento, vc quer debuggar o endpoint de start_backend! E alguma hora ele vai chegar no seu breakpoint (se vc colocou)

9- Exemplo de body para o endpoint start_backend:

{
    "config":{
        "scale_algorithm": "FIFO",
        "quantum": 2,
        "overhead":2
    },
    "processes":[
        {
            "name":"1",
            "arrival_time":2,
            "execution_time":3,
            "deadline":4
        },
        {
            "name":"2",
            "arrival_time":2,
            "execution_time":3,
            "deadline":4
        }
    ]
}
