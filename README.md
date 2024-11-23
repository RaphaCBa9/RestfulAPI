# Projeto Computação em Nuvem - Insper 2024.2
**Autoria de:** Raphael Cavalcanti Banov

**Link para o DockerHub do projeto:**
[Repositório Docker Hub](https://hub.docker.com/repository/docker/raphaba9/restfulapi-app/)

**Link para vídeo-demonstração da dockerização do projeto:**  [Vídeo-demonstração](https://youtu.be/HM9yQYtUGzY)

## 📄 Explicação do Projeto
O projeto se trata de uma API RESTful que é capaz de cadastrar e autenticar usuários, ou seja, validar a infraestrutura de um aplicativo. Após a construção da API, o projeto foi dockerizado e, então, implantado no AWS.

O endpoint de consulta utilizado é uma API de fatos/piadas envolvendo o artista marcial, ator, produtor de cinema e roteirista americano Chuck Norris.
Para saber mais sobre essa API, acesse [este link](https://api.chucknorris.io/).

# Como executar a api via Docker

## 0) Pré-requisitos

### Docker
Para executar a API, você precisará instalar o docker no seu sistema operacional, veja a instalação do docker para:
- [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Mac-OS](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Linux](https://docs.docker.com/desktop/setup/install/linux/)

### Postgres
É necessário, també configurar o framework da base de dados do **PostgreSQL**

Confira a instalação e configuração acessando a [documentação oficial](https://www.postgresql.org/download/).


## 1) Preparando o ambiente

### 1.1) Inicie o Docker em sua máquina

![tela do docker dektop](imgs/print_docker.png)
Não é necessário realizar login ou criar uma conta

### 1.2) Crie e acesse um novo diretório

```
$ mkdir novaPasta
$ cd novaPasta
```

### 1.3) Coloque o arquivo ```compose.yml``` no diretório criado

Baixe o arquivo, clicando [aqui](./compose.yaml)

Ou clone [este repositório](https://github.com/RaphaCBa9/RestfulAPI) do GitHub (caso possua git em sua máquina)

```git
$ git clone https://github.com/RaphaCBa9/RestfulAPI
```
O arquivo ``compose.yml`` estará na raiz do repositório.

## 2) Rode o docker compose

```bash
$ docker compose up --build
```

### 2.1) Verificando se rodou corretamente
Para conferir se o arquivo foi rodado corretamente:

a) Verifique a aba "Images" do seu Docker Desktop
![alt text](imgs/print_docker_images.png)

b) Rode o comando:

```
$ docker images
```
A saída deve ser algo parecido com isso:
```
REPOSITORY                TAG       IMAGE ID       CREATED      SIZE
raphaba9/restfulapi-app   latest    48509b9908a9   4 days ago   238MB
postgres                  15        53432d8e87c9   8 days ago   426MB
```

## 3) Acesse a API e teste!

### 3.1) Testando via <img src="imgs/FastAPI.svg" alt="FastAPI Icon" width="16"/> FastAPI Swagger

Abra um navegador e acesse: http://0.0.0.0:8000/docs

### 3.2) Testando via CLI


### Endpoint ```./registrar```
Em um terminal, execute:

```
$ curl -X 'POST' \
  'http://0.0.0.0:8000/registrar' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "nome": "Seu Nome",
  "email": "SeuEmail@exemplo.com",
  "senha": "SuaSenha"
}'
```
#### A saída esperada é:

```
{
  "jwt": "seuTokenDeAcesso"
}
```

### Endpoint ```./login```
```
curl -X 'POST' \
  'http://0.0.0.0:8000/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "seuEmailCadastrado@exemplo.com",
  "senha": "SuaSenha"
}'
```

#### A saída esperada é:

```
{
  "jwt": "seuTokenDeAcesso"
}
```
### Endpoint ```./consultar```

```
curl -X 'GET' \
  'http://0.0.0.0:8000/consultar?authorization=seuTokenDeAcesso' \
  -H 'accept: application/json'
```
## 4) Finalizando o conteiner
Para finalizar o conteiner do docker, rode o comando:
```
docker compose down --volumes
```
___

# Teste dos endpoints do projeto

### Registro de usuários
![gif_consulta](imgs/gif_registrar.gif)

### Validação de usuários (Login)
![gif_consulta](imgs/gif_login.gif)

### Consulta a API
![gif_consulta](imgs/gif_consultar.gif)



# Implementação do projeto na AWS

## Interação via **FastAPI Swagger**


http://a91098edad62a4d1ba4cf2b2e1b7a0d8-1412143645.us-east-1.elb.amazonaws.com/docs

## Interação via CLI

### Endpoint `/registrar`
```
$ curl -X 'POST' \
  'http://a91098edad62a4d1ba4cf2b2e1b7a0d8-1412143645.us-east-1.elb.amazonaws.com/registrar' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "nome": "Seu Nome",
  "email": "SeuEmail@exemplo.com",
  "senha": "SuaSenha"
}'
```


### Endpoint ```./login```
```
curl -X 'POST' \
  'http://a91098edad62a4d1ba4cf2b2e1b7a0d8-1412143645.us-east-1.elb.amazonaws.com/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "seuEmail@exemplo.com",
  "senha": "SuaSenha"
}'
```

#### A saída esperada é:

```
{
  "jwt": "seuTokenDeAcesso"
}
```



### Endpoint ```./consultar```

```
curl -X 'GET' \
  'http://a91098edad62a4d1ba4cf2b2e1b7a0d8-1412143645.us-east-1.elb.amazonaws.com/consultar?authorization=seuTokenDeAcesso' \
  -H 'accept: application/json'
```

#### A saída esperada é:
```
{
"id":"z-sPdqWoRtaXiMLbozz2Tg",
"fact":"Fato sobre o Chuck Norris"
}
```

# Processo para hospedar um cluster Kubernetes na AWS

## 0) Pré-requisitos

### AWS CLI
O **AWS CLI** uma ferramenta de código aberto da Amazon Web Services (AWS) que permite interagir com a plataforma por meio de uma interface de linha de comando.

Para instalar a interface, acesse a [documentação oficial.](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

Verifique a instalação executando no terminal:
```bash
aws --version
```
O resultado esperado deve ser semelhante a:
```bash
aws-cli/2.22.3 Python/3.12.6 Linux/6.8.0-49-generic exe/x86_64.ubuntu.22
```

### Kubectl

Kubectl é uma ferramenta de linha de comando que permite interagir com clusters do Kubernetes

Para instalar a interface, acesse a [documentação oficial.](https://kubernetes.io/docs/tasks/tools/)

Verifique a instalação executando no terminal:
```bash
kubectl version
```
O resultado esperado deve ser semelhante a:
```bash
Client Version: v1.31.2
Kustomize Version: v5.4.2
Server Version: v1.30.6-eks-7f9249a
```

### Eksctl
Eksctl é uma ferramenta de linha de comando (CLI) oficial do Amazon Elastic Kubernetes Service (Amazon EKS)

Para instalar a interface, acesse a [documentação oficial.](https://eksctl.io/installation/)

Verifique a instalação executando no terminal:
```bash
eksctl version
```
O resultado esperado deve ser semelhante a:
```bash
0.194.0
```

## 1) Configuração da AWS

### 1.1) Chave de acesso
As chaves de acesso são necessárias para que o AWS CLI possa executar os comandos em nome da sua conta AWS

Acesse o console IAM: [IAM Console](https://us-east-1.console.aws.amazon.com/iam/home?region=us-east-1#/users)

## 2) Criando o cluster e configurando o kubectl

Criação do cluster EKS com dois nós.
```bash
eksctl create cluster --name api-restful --region us-east-1 --nodes 2 --node-type t3.medium
```

Conexão do kubectl com o cluster
```bash
aws eks --region us-east-1 update-kubeconfig --name api-restful
```

Verificando os clusters:
```
eksctl get cluster
```

Se os clusters foram criados corretamente, a saída deve ser algo parecido com:

```
NAME		  REGION		EKSCTL CREATED
api-restful	  us-east-1	    True
```

## 3) Montagem dos arquivos ``deployment.yaml``

### 3.1) web-deployment.yaml

Este arquivo é responsável por realizar a configuração do Deployment da Aplicação (FastAPI):
- Utiliza a imagem Docker raphaba9/restfulapi-app:latest.
- Define variáveis de ambiente para configuração da aplicação

Configuração do serviço de LoadBalancing.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
      - name: fastapi
        image: raphaba9/restfulapi-app:latest
        env:
          - name: SQLALCHEMY_DATABASE_URL
            value: "postgresql://postgres:admin@postgres:5432/cloud"
          - name: SECRET_KEY
            value: "SuperHiperMegaChaveSecreta123123"
        ports:
          - containerPort: 8000
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-service
spec:
  type: LoadBalancer
  ports:
    - port: 80
      targetPort: 8000
  selector:
    app: fastapi
```
### 3.2) db-deployment.yaml

Realização da configuração do Deployment do Banco de Dados (PostgreSQL):

- Cria um Deployment para um banco de dados PostgreSQL.
- Utiliza a imagem Docker postgres:15.
- Define variáveis de ambiente para configurar o banco de dados

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15
        env:
          - name: POSTGRES_USER
            value: "postgres"
          - name: POSTGRES_PASSWORD
            value: "admin"
          - name: POSTGRES_DB
            value: "cloud"
        ports:
          - containerPort: 5432
---
apiVersion: v1
kind: Service
metadata:
  name: postgres
spec:
  ports:
    - port: 5432
  selector:
    app: postgres
```

## 4) Realizando o deployment da base de dados e da aplicação

Para criar os recursos no cluster com base nas definições dos arquivos `.yaml`, execute estes comandos:

```
kubectl apply -f db-deployment.yaml 
kubectl apply -f web-deployment.yaml
```

## 5) Verificando os pods

Para verificar os pods em execução no cluster, execute:
```bash
kubectl get pods
```
Se os pods foram criados corretamente, a saída deve ser algo parecido com:

```
NAME                        READY   STATUS    RESTARTS   AGE
fastapi-5fb7fcc74-lt9ws     1/1     Running   0          30h
postgres-7c9d46fff9-z6p8m   1/1     Running   0          30h
```

## 6) Conseguindo o link de acesso
O link de acesso é providenciado pelo serviço de LoadBalancing.

```bash
kubectl get svc fastapi-service
```

```
NAME              TYPE           CLUSTER-IP      EXTERNAL-IP                                                               PORT(S)        AGE
fastapi-service   LoadBalancer   10.100.230.34   a91098edad62a4d1ba4cf2b2e1b7a0d8-1412143645.us-east-1.elb.amazonaws.com   80:32543/TCP   30h

```

## 7) Para acessar o Swagger da Fastapi:

```
http://a91098edad62a4d1ba4cf2b2e1b7a0d8-1412143645.us-east-1.elb.amazonaws.com/docs
```