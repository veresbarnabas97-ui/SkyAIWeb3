# SkyAI Ultimate Web3 Terminál

## 🚀 Áttekintés
A **SkyAI Ultimate Web3 Terminál** egy forradalmi, AI-vezérelt platform, amely a hagyományos pénzügyi piacok professzionális kereskedési eszközeit hozza el a decentralizált Web3 ökoszisztémába. A terminál fő fókuszában a **BNB Chain** (EVM) és a **Solana** hálózatok állnak.

Célunk, hogy a felhasználók számára a leggyorsabb, legátfogóbb és legbiztonságosabb platformot biztosítsuk a DeFi hozamgeneráláshoz és az AI-alapú kereskedéshez.

## ✨ Főbb Funkciók

| Funkció | Leírás | Kulcsszavak |
| :--- | :--- | :--- |
| **🎯 SNIPER HUD** | AI-vezérelt bot, amely a mempool figyelésével a leggyorsabb be- és kilépést biztosítja a tokenek piacán. | `AI`, `Mempool`, `Sebesség`, `Bot` |
| **👑 WHALE VAULT** | Intézményi szintű, biztonságos hozamgeneráló tárca (pl. Conservative/Aggressive Stratégiák). | `Staking`, `Yield`, `Hosszú Táv`, `BNB/SOL` |
| **💰 DeFi Protokollok** | 10 különböző bevételtermelő okosszerződés: Staking, $SKY Token Pre-Sale, NFT Mint. | `NFT`, `Pre-Sale`, `APY`, `Staking` |
| **🔗 Multichain Támogatás** | Zökkenőmentes kommunikáció a BNB és a Solana hálózatokkal egyetlen felületen. | `EVM`, `Solana`, `Phantom`, `MetaMask` |

## 🛠️ Technológiai Stílus

A projekt alapja a modern, futurisztikus felhasználói felület és a robusztus, blokklánc-specifikus frontend/backend kommunikáció.

### 🌐 Frontend
* **Dizájn:** Sötét téma, cián és neonzöld kiemelésekkel (`var(--cyan)`, `var(--solana)`).
* **Chartok:** TradingView Widgetek (`BINANCE:SOLUSDC`, `BINANCE:BNBUSDC`).

### ⚙️ Web3 Integráció (A Két Lánc Kezelése)
* **BNB Chain (EVM):** **Ethers.js** könyvtár a tárca (MetaMask/Trust Wallet) csatlakoztatásához és a tranzakciók küldéséhez.
* **Solana:** **`@solana/web3.js`** könyvtár a Phantom tárcával való interakcióhoz és a Lamports-alapú tranzakciók kezeléséhez.

## 🚀 Telepítés és Futtatás (Helyi Tesztkörnyezet)

A terminál egy HTML/JS/CSS alapú webes felület, mely közvetlenül kommunikál a böngészőben lévő Web3 tárcákkal.

1.  **Klónozás:** Klónozd a projekt fájljait (pl. `ALL.html`, `ProfileWeb3.html`) egy helyi mappába.
2.  **Web Szerver:** Egy lokális web szerver (pl. VS Code Live Server extension vagy Python `http.server`) szükséges az aszinkron funkciók (Fetch, Web3) futtatásához.
3.  **Tárca:** Győződj meg róla, hogy a böngésződben telepítve van a **MetaMask** (BNB Chainhez) és a **Phantom** (Solanához).
4.  **Futtatás:** Nyisd meg a `ALL.html` fájlt a lokális szervereden keresztül.

> **FIGYELEM:** A HTML fájlok tartalmaznak fejlesztői címeket a tranzakciókhoz (`MY_BNB_ADDRESS`, `MY_SOL_ADDRESS`). Ne futtasd a kódot nyilvános hálózaton ezen címek módosítása nélkül, ha a kód alapvető tranzakciókat indít.

## 🔗 Roadmap
A teljes fejlesztési ütemterv a `ROADMAP.txt` fájlban található.

## 📞 Kapcsolat
* **Alapító:** Veres Barnabás
* **Címek (BNB/SOL):** Lásd a `ProfileWeb3.html` fájlt (pl. `0xbb6433...`, `4iubzdpP...`).
