# payments

### Para subir a aplicação localmente os seguintes passos são necessários:
#### Pré-requisitos
- [docker-compose](https://docs.docker.com/compose/install)
- [asdf](https://asdf-vm.com/guide/getting-started.html)


#### Rodando via docker

```bash
make docker_run

```

#### Rodando local

```bash
asdf plugin-add python
asdf plugin-add poetry https://github.com/asdf-community/asdf-poetry.git
asdf install

poetry install
poetry shell
make run
```

#### Rodando os testes local
```bash
make test
make integration_test
```

acessar: http://localhost:8000/docs


#### Documentação arquitetural

![Documentação arquitetural](https://github.com/davisnog/payments/blob/main/images/kanastra-payments.drawio.png?raw=true)