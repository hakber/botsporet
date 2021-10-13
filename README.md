# botsporet
A collection of apps to facilitate a type of game show on Twitch

Sorry, the rest of the documentation will be in Swedish :(

I detta repo finns som sagt ett par appar som är tilltänkta att underlätta för skapandet av en finfin gameshow på Twitch (vanligtvis hållen på Socialiseringskommittén/Vörttuben, men känn er fria att använda koden om ni lyckas förstå er på den).

## Användande

Tanken är ungefär att frågor och svar till att börja med ska matas in i Frågor/Frågor.xlsx. Webbappen/interfacet läser sedan in frågorna och låter en bestämma vilken fråga som är aktuell, och skriver det till CURRENT_QUESTION i database.db (se hur du kör en Flask-app [här](https://flask.palletsprojects.com/en/2.0.x/cli/)). Twitchbotten läser in vilket svar folk skickar, samt vilken fråga som är aktuell, och skriver svaret till ANSWERS i database.db. answersToExcel.py plockar ut svaren ur databasen och lägger dem i en excel-fil, och createLeaderBoard.py skapar en resultattabell.

Utöver apparna som faciliterar själva spelet i sig, så finns även en app för att tanka bilder från Google Streetview, till hjälp för att skapa hjälpmaterialet till frågorna.

### Noter om API-keys

För att skapa egen API-nyckel osv för twitch-boten, se dokumentationen [här](https://twitchio.readthedocs.io/en/latest/quickstart.html)

För att skapa egen API-nyckel osv för Google Streetview/Maps, se dokumentationen [här](https://developers.google.com/maps/documentation/streetview/get-api-key)

## Lite to-do

**Övergripande pga jag är keff:**
* Kommunikation mellan twitchbotten och interfacet sker just nu genom databasen. Funkar det eller bör programmen slås ihop och lagra nuvarande fråga i minnet? (Funkar det i sin tur eller blir det knas pga asyncio osv?)
* Öhm variabelnamn, kodstruktur, databasnamn, dokumentation osv osv FÖRLÅT jag läste typ 6hp programmering 2011.

**Annat övergripande**
* Google Spreadsheets-integrering för att möjliggöra att fler är med och rättar manuellt. Kanske kan leaderboard-funktionen isf lösas mha en enkel pivottabell? Om Google Spreadsheets integreras tror jag dock det fortfarande är bra att mellanlagra i databas, känns som det finns risk för att skriva över svar som kommer in samtidigt annars eller andra fel osv (?).

**Twitchbotten:**
* ~~Begränsa antal svar per fråga till 1~~ (Fixat, vilken king jag e)
* Felmeddelanden till användare m.a.p. ovan eller om det är stängt för frågor
* Svarsbekräftelse? (?)

**Interfacet:**
* Lite störigt att den laddas om varje gång man ställer in fråga. Går det åtminstone att göra nåt så att ens val är desamma efter sidan laddats om?

**Rättningsscriptet:**
* Nån lite fuzzy matchning på inkomma gissningar och svar, för att godkänna mindre stavfel?

**Kart-appen:**
* Begränsa antalet nedladdade bilder på något sätt? Kan dela bli onödigt många bilder och dels bränner det maps-api-quota
* Kameravinkeln skiftar massa nu. Kanske inte ett problem egentligen? Men om nån är flink på matte kanske det vore ballt med en funktion f(nuvarande latitud, nuvarande longitud, mållatitud, mållångitud)=kompassvinkel
