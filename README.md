<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** banjoanton, repo, twitter_handle, email
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">Begagnat-bevakning</h3>

  <p align="center">
    Bevaka begagnathandeln i Sverige med hjälp av Telegram och Google Cloud functions.
    <br />
    <a href="https://github.com/banjoanton/begagnat-bevakning/issues">Rapportera ett fel</a>
    ·
    <a href="https://github.com/banjoanton/begagnat-bevakning/issues">Begär en funktion</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->

## Innehållsförtäckning

- [Innehållsförtäckning](#innehållsförtäckning)
- [Om projektet](#om-projektet)
  - [Byggt med](#byggt-med)
- [Startguide](#startguide)
  - [Förutsättningar](#förutsättningar)
    - [Moduler](#moduler)
    - [Databas](#databas)
    - [Telegram](#telegram)
  - [Installation](#installation)
- [Användning](#användning)

<!-- ABOUT THE PROJECT -->

## Om projektet

Detta är ett projekt som jag skapade för att lära mig hantera [Google Cloud Functions](https://cloud.google.com/functions/), web scraping med [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) och API-hantering med [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot).

Google Cloud tar emot HTTP GET förfrågningar med sökord och geografisk avgränsning, varpå den läser av [Blocket](https://www.blocket.se) och [Tradera](https://www.tradera.se) efter artiklar som matchar sökordet. Nya artiklar sparas och skickas till en egenskapad Telegramgrupp med information om objektet, länk och foto. Ett ID för annonsen sparas också i en SQL-databas så att det ej skickas en notis för samma produkt två gånger.

[Google Cloud Scheduler](https://cloud.google.com/scheduler/) kan användas för att schemalägga HTTP GET-förfrågningar. Alltså, för att bestämma hur ofta den ska söka igenom hemsidorna.

Detta projektet bör ej användas utan skapades endast i utbildningssyfte.

### Byggt med

-   [Google Cloud Functions](https://cloud.google.com/functions/)
-   [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
-   [Python Telegram Bot](https://github.com/python-telegram-bot/python-telegram-bot)
-   [Google Cloud Scheduler](https://cloud.google.com/scheduler/)
-   [Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts)
-   [MySQL](https://www.mysql.com/)

<!-- GETTING STARTED -->

## Startguide

### Förutsättningar

#### Moduler

Samtliga moduler finns angedda i `requirements.txt`-filen och kan installeras med:

```sh
pip -r install requirements.txt
```

#### Databas

Programmet använder sig av en Remote SQL-databas. Denna bör innehålla följande:

-   En databas som heter `begagnat`.
-   Ett table vid namn `tradera` som innehåller:
    -   Text som heter `id`
    -   Boolean som heter `has_viewed`
-   Ett table vid namn `blocket` som innehåller:
    -   Text som heter `id`
    -   Boolean som heter `has_viewed`

En databas kan skapas gratis på [följande hemsida](https://www.freesqldatabase.com/).

#### Telegram

Programmet använder sig av telegram för att skicka notiser så fort en ny annons har dykt upp. Skapa en ny telegram-bot på [följande länk](https://telegram.me/BotFather).

-   Ladda hem desktop-appen om du är på dator.
-   Skriv `/newbot` för att skapa en ny bot.
-   Spara ditt token, det borde se ut ungefär såhär:

```
704418931:AAEtcZ*************
```

-   Skriv något till boten för att bli tilldelad ett chat id.
-   Få tag på chat id genom att gå till följande länk:

```
https://api.telegram.org/bot<ditt_bot_token>/getUpdates
```

### Installation

1. Klona repot

```sh
git clone https://github.com/banjoanton/begagnat-bevakning.git
```

2. Installera alla moduler

```sh
pip -r install requirments.txt
```

3. Lägg till miljövariabler som kommer användas senare i `.env.yaml`.
4. Ladda hem och installera [Google Cloud SDK](https://cloud.google.com/sdk/docs/quickstarts)
5. Ladda upp programmet till Cloud Functions med SDK.

```
gcloud functions deploy begagnat-bevakning --entry-point main --runtime python37 --trigger-http --env-vars-file .env.yaml
```

6. Få adressen genom att besöka [Cloud Functions-konsolen](https://console.cloud.google.com/functions) eller skriva in:

```
gcloud functions describe begagnat-bevakning
```

<!-- USAGE EXAMPLES -->

## Användning

Sökningen aktiveras genom HTTP GET förfrågningar, genom att besöka adressen från steg 6 i webläsaren. Med hjälp av GET parametrar kan man justera sökningen:

-   q - sökordet, måste anges för att det ska fungera.
-   lan - används på blocket, om det ska vara lokalt, i angränsande län eller i hela Sverige.
    -   1 = lokalt (Älvsborg som default, kan ändras i `blocket.py`)
    -   2 = angränsade län
    -   3 = hela Sverige

Exempel - sök efter iPhone i hela Sverige.

```
https://us-central1-projekt-namn.cloudfunctions.net/begagnat-bevakning?q=iPhone&lan=3
```

Vid första sökningen kommer alla resultat att visas, vid varje efterkommande sökning visas bara de nya annonserna. Därav blir det en bevakning.

Processen kan automatiseras med [Google Cloud Scheduler](https://cloud.google.com/scheduler/).
