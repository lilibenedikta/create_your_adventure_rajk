
# Create your adventure!
### Dokumentáció a saját szöveg alapú kalandjátékod létrehozásához
### Kofrán Dániel, Nádasy Lili 

Az alábbi dokumentáció egy szöveg alapú kalandjáték létrehozásához szükséges lépéseket tartalmazza. Ha végigcsinálod, a játékod a következő dolgokra lesz képes: 
- végig lehet játszani az általad írt, bármennyi szituációt és döntést tartalmazó kalandot
- böngészőn keresztül, PC-n játszható
- párhuzamosan több ember is tud vele játszani
- játék közben el lehet menteni az aktuális helyzetet, kilépni, és később onnan folytatni 

## Rövid összefoglaló

A saját kalandod létrehozásához a következő lépéseken kell végigmenned.
- A kitalált történetedet szituációkra és választási lehetőségekre bontva kell elmentened 2 külön, szigorú formai szabályokkal ellátott .csv fájlként.
- Klónolned ezt a Github repo-t, és átírni a megfelelő paramétereket az erre szentelt fájlban.
- Felraknod a .csv fájlokat a saját AWS fiókod S3 bucket-jába.
- Heroku-n deploy-olnod az applikációt

A következő részekben ezeket fejtjük ki.


## Történetírás, adatok


A kaland játékod alapja egy szöveges adatbázis lesz, amit te hozhatsz létre.

A játék struktúrája reprezentálható hálózatként, ahol a csomópontok a döntési helyzetek, az élek pedig a választási lehetőségek.

[Ezen a linken](https://docs.google.com/spreadsheets/d/15zoYvlXV7RlHADRWOu5du17LMPyK_JtH257VcmXiH8E/edit?usp=sharing) találod a példa játékot, ami segít neked, hogy hiba nélkül megadd a szituációkat (nodes) és a választási lehetőségeket (edges) tartalmazó adatbázisokat, amelyek felépítik a játékot. 



A spreadsheetben találsz néhány beépített függvényt (zöld oszlopok fekete betűvel). Ezeknek mindenhol OK-t kell mutatniuk, különben a játékod hibára fog jutni. Ha mégis hibára fut valamelyik, akkor a hibaüzenetből tudsz következtetni a hiba okára.


Egy szabály nincs befüggvényezve, ami az, hogy minden node csak egyszer fordulhat elő a történetben, tehát **nem lehetnek loopok**. Máshogy fogalmazva egy játék során minden megtörtént helyzet ID-ja egyedi.


A problémamentes futtatáshoz fontos továbbá, hogy az utolsó szituációnál, a finish page előtti utolsó állomásodnál is meg kell adnod választási lehetőségeket, a választási lehetőségeket tartalmazó file-ban. A jelen repóban lévő segédadatbázis szemlélteti ezt a kitételt. Ennél az állomásnál érdemes a “TEXT_E” oszlopba beírni, hogy “VÉGE”. Az utolsó “FROM” node-okat pedig lista formában be kell majd illeszteni a kódba - erre második pontban visszatérünk.


**A történetedet mindenképp ebben a formátumban írd meg**, és másold le, illetve használd bátran ellenőrzésre ezt a Google Sheetet. Amikor csv formátumban exportálod az adatot, figyelj rá, hogy az ellenőrző függvények oszlopai már ne legyenek benne. 


Az első pont végén két .csv fájlod lesz - ebben a dokumentációban így hívják ezeket: 
- RAJK_ZORK_edges.csv
- RAJK_ZORK_nodes.csv


## GitHub Repository


A kreatív írói energiák kiélése után jöhet a kód összerakása. Ehhez a kiindulópontot a [create_your_adventure_rajk GitHub repository](https://github.com/lilibenedikta/create_your_adventure_rajk) adja. 

Az első lépés ennek a repositorynak a klónolása, [amihez itt találsz egy hasznos leírást](https://www.educative.io/answers/how-to-clone-a-git-repository-using-the-command-line), ha kell egy kis segítség.

Röviden összefoglalva a tartalmukat, a következő fájlokat találod a repository-ban: 

- assets/style.css - az app-ban található dash elemek formázási adatai, beállításai
- pages/home_page.py - a nyitóoldal dash kódja
- pages/chapter_1.py - a szituációk és választási lehetőségek dash kódja
- pages/finish_page.py - a zárólap kódja
- .gitignore - az itt szereplő, felesleges fájlokat figyelmen kívül hagyja a verziókövető rendszer
- Procfile - a Herokun való deployment-hez szükséges fájl
- README.md - a repository leírása
- app.py - ennek futtatásával indul el az app
- authentication_and_parameters.py - az AWS serverrel való kommunikációhoz szükséges és játékspecifikus paramétereket tartalmazó kód
- requirements.txt - szükséges packagek
- runtime.txt - a szükséges python verzió nevét tartalmazza
- session_state.py - a játék aktuális státuszának követéséhez kell

Miután sikerült klónolnod a repositoryt, néhány dolgot módosítani kell a kódban, hogy az működjön a te történeteddel. Ezeket a módosítandó dolgokat az authentication_and_parameters.py fájlban találod, és az alábbi kép ismerteti őket.

![alt text](https://github.com/lilibenedikta/create_your_adventure_rajk/blob/update_markdown/docu_image.png?raw=true)


## AWS szerver fiók

Szükséged lesz egy AWS fiókra, ahol egy [S3 bucket nevű eszközt](https://towardsdatascience.com/how-to-upload-and-download-files-from-aws-s3-using-python-2022-4c9b787b15f2) fogsz tárolásra használni. Ide kell feltölteni az első pontban letöltött .csv fájlokat, és a játék itt fogja követni az egyedi felhasználók játék folyamatait, tehát a mentésben és a párhuzamos játékban is fontos szerepe van.

Itt generálni kell egy ún. secret access key-t, ami a szerverre való belépéshez szükséges azonosításhoz kell. Sarkalatos pontja a folyamatnak a bucket-hoz tartozó titkos azonosítók tárolása. Főbűn kategóriába tartozik, ha ezeket az azonosítókat úgy tárolod, hogy valaki meg tudja találni a GitHubon, úgyhogy ennek kikerüléséhez ún. environment variable-eket fogsz létrehozni virtuális környezet segítségével. Hogy ezt valahogy meg tudd találni, érdemes elmenteni egy .txt fájlba a gépeden. 
Két bucket-ra lesz szükség, az egyikbe a .csv fájlokat kell feltölteni, a másikba pedig a párhuzamos játékhoz szükséges user session-ök adatai fognak kerülni.


## Heroku fiók

Egy Heroku fiókra mindenképpen szükséged lesz. Ha még nem rendelkezel vele, [ilyet itt tudsz létrehozni](https://signup.heroku.com/login). A Heroku egy felhőplatform, amely több programozási nyelvet is támogat. Herokut modern alkalmazások telepítésére, kezelésére és skálázására használják. 
Más megfogalmazásban ahhoz kell, hogy az appot ne csak lokálisan lehessen elérni, hanem egy linken keresztül bárhonnan, szóval nagyon egyszerűen meg tudod majd osztani a játékodat másokkal. 


## Environment variables, deployment

Az app deployment a [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) segítségével történik. Szükséged lesz python-3.10.-es (virtuális) környezetre, hogy hozzá tudj férni a heroku fiókodhoz a command line-on keresztül. Ennek létrehozásának egy (és ajánlott) módja az Anaconda, és azon belül az [Anaconda Prompt](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) használata. 
Ha mindez sikerült, a következő parancsokat kell beírni a command promptba amit használsz (itt Anaconda Promptba), mielőtt kalandra lehet kelni:

- conda env list → milyen környezetek elérhetők? (ez a parancs csak a tájékozódáshoz szükséges)
- cd path/a/klónolt/GitHub/repohoz → elnavigálás a repository mappájába
- conda activate heroku → belépés a heroku környezetbe
- heroku login → átirányít a böngészőbe, belépés a fiókba
- heroku create az-appod-neve → létrehozza az applikációt, itt fogod látni a linket hozzá
- heroku config:set AWS_ACCESS_KEY_ID=érték → megadod a secret key azonosítóját
- heroku config:set AWS_SECRET_ACCESS_KEY=érték → megadod a secret key értékét
- git push heroku main → updateled a main branchet a heroku által létrehozott új repository-n (ezt bármilyen változtatás után meg kell csinálni)
- heroku open → megnyitod az applikációt
- (heroku logs --tail → ha valamilyen okból Application Errort kapsz, így tudod megnézni a hibaüzenetet)

# Gratulálunk, kész is vagy!

