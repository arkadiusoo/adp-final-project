# 🗺️ Optimal Polish City Selection – Spatial Data Analysis Project

This project focuses on selecting the optimal city for young professionals in the IT industry who are considering relocating within Poland. The analysis combines rental prices, job offers, and the availability of basic services (Żabka convenience stores) using spatial data techniques.

## 🎯 Project Objective

To build a practical tool to help young individuals with a computer science background make informed decisions about where to live, based on:
- IT job offer density
- Rental costs
- Access to essential services

## 📊 Datasets Used

All datasets are from late 2023:
- **Apartment rental prices** – November 2023  
  Source: [Kaggle – Apartments](https://www.kaggle.com/datasets/krzysztofjamroz/apartment-prices-in-poland)
- **IT job offers** – September 2023  
  Source: [Kaggle – JustJoinIT Offers](https://www.kaggle.com/datasets/jszafranqb/justjoinit-job-offers-data-2021-10-2023-09)
- **Żabka store locations** – November 2023  
  Source: [Kaggle – Żabka Shops](https://www.kaggle.com/datasets/michaltajchert/zabka-shop-location-data)

Assumption: Job offers from September 2023 remain valid for November 2023 to align all datasets temporally.

## 🛠️ Technologies Used

- Python
- Pandas & GeoPandas
- Folium (for map visualizations)
- Shapely
- Geopy
- Matplotlib
- Contextily

## 🧭 Methodology

1. Load and preprocess rental, job, and Żabka data.
2. Filter data for major Polish cities: Warsaw, Kraków, Wrocław, Katowice.
3. Use spatial joins to compute distances from apartments to:
   - Closest job offers
   - Closest Żabka stores
4. Generate maps and statistical plots showing:
   - Apartment cost vs proximity to jobs and services
   - City-wise comparisons

---

# 🗺️ Wybór optymalnego miasta w Polsce – Projekt analizy danych przestrzennych

Projekt koncentruje się na wyborze optymalnego miasta do życia dla młodych specjalistów z branży IT rozważających przeprowadzkę w obrębie Polski. Analiza łączy dane o cenach wynajmu mieszkań, ofertach pracy oraz dostępności podstawowych usług (sklepy Żabka) z wykorzystaniem technik analizy danych przestrzennych.

## 🎯 Cel projektu

Stworzenie praktycznego narzędzia wspierającego młode osoby z wykształceniem informatycznym w podejmowaniu świadomych decyzji dotyczących miejsca zamieszkania, na podstawie:
- zagęszczenia ofert pracy w IT
- kosztów wynajmu mieszkań
- dostępu do podstawowych usług

## 📊 Wykorzystane zbiory danych

Wszystkie zbiory pochodzą z końca 2023 roku:
- **Ceny wynajmu mieszkań** – listopad 2023  
  Źródło: [Kaggle – Mieszkania](https://www.kaggle.com/datasets/krzysztofjamroz/apartment-prices-in-poland)
- **Oferty pracy w IT** – wrzesień 2023  
  Źródło: [Kaggle – JustJoinIT](https://www.kaggle.com/datasets/jszafranqb/justjoinit-job-offers-data-2021-10-2023-09)
- **Lokalizacje sklepów Żabka** – listopad 2023  
  Źródło: [Kaggle – Żabka](https://www.kaggle.com/datasets/michaltajchert/zabka-shop-location-data)

Założenie: oferty pracy z września 2023 uznaje się za aktualne w listopadzie 2023, co umożliwia spójną analizę czasową.

## 🛠️ Zastosowane technologie

- Python
- Pandas i GeoPandas
- Folium (wizualizacje mapowe)
- Shapely
- Geopy
- Matplotlib
- Contextily

## 🧭 Metodologia

1. Wczytanie i wstępne przetworzenie danych o wynajmie, ofertach pracy i sklepach Żabka.
2. Filtrowanie danych dla głównych miast Polski: Warszawa, Kraków, Wrocław, Katowice.
3. Wykorzystanie operacji przestrzennych do obliczenia odległości mieszkań od:
   - Najbliższych ofert pracy
   - Najbliższych sklepów Żabka
4. Generowanie map i wykresów pokazujących:
   - Koszt wynajmu względem bliskości pracy i usług
   - Porównania między miastami
