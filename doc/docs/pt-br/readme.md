# Pylax

[Read this document in other languages](../global_docs.md)

O Pylax é um projeto [Open Source](https://pt.wikipedia.org/wiki/C%C3%B3digo_aberto) de um bot para ajudar a administrar a brincadeira de **Verdade ou Desafio** em comunidades do [Discord](https://discord.com/). O projeto criado inicialmente para ser utilizado na [Comunidade Ballerini](https://discord.gg/wagxzStdcR), mas hoje está disponível de maneira aberta. O Pylax é a versão **2.0** do projeto que anteriormente se chamava [Calax](https://github.com/MateusSantosMeuBem/calax_v_python), cujo nome é baseado no personagem demoníaco do filme [Truth or Dare](https://pt.wikipedia.org/wiki/Truth_or_Dare_(2018)).

## Configurações do bot
Para rodar esse projeto, primeiro você precisa criar uma aplicação no [Developer Portal](https://discord.com/developers/applications). Na aba `Informações gerais` preencha os campos **Nome**, **Descrição** e **Icone do App**. Na aba `Robô` clique no botão **Adicionar bot** e adicione seu bot. Prencha os campos **Username** e **ícone**. Agora vamos setar as configurações do bot, marque os seguintes campos e em seguida salve as alterações:

**Authorization Flow**
- [X] PUBLIC BOT
- [ ] REQUIRES OAUTH2 CODE GRANT

**Privileged Gateway Intents**
- [X] PRESENCE INTENT
- [X] SERVER MEMBERS INTENT
- [X] MESSAGE CONTENT INTENT

No diretório `pylax/` duplique o arquivo `example.env` e renomeie como `.env` e preencha seus campos.
No seu servidor, crie um canal de texto chamado `autenticação` e coloque seu id no arquivo citado acima. Cada jogo acontece em uma sala, cada sala é composto por um par de canais (1 de voz e 1 de texto), crie o número de salas dependendo do número de jogos que você queira. Não esqueça de editar as permissões dos membros para essas salas (isso é com você =D).

Na diretório `pylax/src/json` duplique o arquivo `example.rooms.json` e renomeie como `rooms.json` e preencha seus campos.
Esse arquivo contém uma lista que guarda quais são as salas ondem irão ocorrer os jogos. Exemplo de preenchimento:
```json
[
    {
        "bot_master": "123456789",
        "id_text_channel": "75656456745",
        "id_voice_channel": "25435498675687"
    },
    {
        "bot_master": "987654321",
        "id_text_channel": "567453563",
        "id_voice_channel": "656754674"
    }
]
```
`bot_master` se trata da pessoa que irá gerenciar determinada sala, use o padrão *snowflake*.

**Agora vamos trazer o bot para o seu servidor!**

Na página da sua aplicação em na aba `OAuth2 > Gerador de url` selecione o **Escopo** `robô` e em **Permissão de Bot** selecione todas as permissões abaixo:

**Permissões gerais**
- [X] Gerenciar servidor
- [X] Gerenciar canais
- [X] Gerenciar emojis e stickers
- [X] Ler mensagens/ver canais
- [X] Membros moderados

**Permissões de texto**
- [X] Enviar mensagens
- [X] Gerenciar mensagens
- [X] Incorporar links
- [X] Anexar arquivos
- [X] Ler histórico de mensagens
- [X] Usar emojis externos
- [X] Usar stickers externos
- [X] Adicionar reações

**Permissões de voz**
- [X] Conectar
- [X] Usar atividades de voz
- [X] Usar atividades incorporadas

Essas permissões são necessárias para que o bot funcione corretamente. Agora copie a url gerada e cole no seu navegador, selecione o servidor que você deseja adicionar o bot e clique em **Autorizar**. Quando o bot estiver online, um dos `bot masters` deve entrar em uma sala de voz e digitar na sua sala o comando ??add_auth_message para que o bot envie uma mensagem de autenticação para o canal de texto `autenticação`. Os membros devem reagir com o emoji de verificação para que o bot os adicione na sala de voz.

## Colocando o bot online
Para colocar o bot online, você precisa ter o [Python](https://www.python.org/downloads/) instalado na sua máquina. Depois de instalado, abra o terminal e execute o seguinte comando:
```bash
pip install -r requirements.txt
```
Esse comando irá instalar todas as dependências necessárias para rodar o projeto. Agora vamos rodar o bot, execute o seguinte comando:
```bash
python pylax
```
Pronto! O bot está online e pronto para ser usado.

## Comandos
Os comandos do bot são executados através de mensagens enviadas no canal de texto da sala de voz. Os comandos são iniciados com `??` e seguido do nome do comando. Exemplo: `??add_auth_message`. Os comandos são:

**Comandos para o jogo**
- `??iniciar` - Inicia o jogo.
- `??girar` - Gira a garrafa e escolhe uma vítima.
- `??op [o] [v]` - Seleciona a opção da vítima.
- `??ajuda` - O Pylax seleciona uma pergunta do banco de dados.
- `??feito` - A vítima indica que respondeu a pergunta.

**Comandos para os bot masters**
- `??add_auth_message` - Envia uma mensagem de autenticação para o canal de texto `autenticação`.
- `??kick <id_membro> [0] [1] [2]` - Remove o membro da sala de voz e da sala de texto. `0` para remover apenas do jogo, `1` para remover apenas da sala `2` para remover de ambos.
- `??next` - Passa a vez para o próximo membro.
- `??restart` - Reinicia o jogo.
- `??rules` - Mostra as regras do jogo.
- `??show_players` - Mostra os jogadores da sala.
- `??status` - Mostra o status do jogo.

## Sobre o jogo
**Script do jogo**
- O jogo começa quando o bot master digita o comando `??iniciar`.
- A pessoa na vez (asker) deve girar a garrafa para escolher uma vítima.
- A vítima deve escolher uma opção entre as 2 disponíveis (v: verdade, c: consequência).
- Baseado no que a vítmia escolheu, o asker deve fazer uma pergunta.
- Após a vítima responder a pergunta, ela deve digitar o comando `??feito`.
- Irá acontecer uma votação para decidir se a vítima está mentindo ou não.
- Em seguinda, a próxima pessoa na vez (asker) deve girar a garrafa para escolher uma nova vítima.

**Regras do jogo**
- Para jogar o jogo, você precisa estar em uma sala de voz do jogo e ter reagido com o emoji de verificação na mensagem de autenticação.
- Apenas o bot master pode iniciar o jogo.
- O jogo não tem fim.
- Se um jogador escolher 3 vezes a opção `v`, ele será forçado a escolher a opção `c`.
- Se as pessoas decidirem que a vítima está mentindo, ela receberá uma flag. Com 2 flags, a vítima fica impossibilitada de jogar por duas rodadas. Se elas decidirem que a vítima está falando a verdade, ela ganha uma estrela.

## Contribuindo

[Quero contribuir!](contributing.md)

## [LICENÇA](../../../LICENSE)
