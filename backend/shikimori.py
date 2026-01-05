from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests


class ShikimoriAPI:
    """Клиент для работы с Shikimori API"""
    
    BASE_URL = "https://shikimori.one/api"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AnimeTracker/1.0',
            'Accept': 'application/json'
        })
    
    def get_animes(
        self,
        limit: int = 20,
        page: int = 1,
        order: str = "popularity",
        kind: Optional[str] = None,
        status: Optional[str] = None,
        season: Optional[str] = None,
        score: Optional[int] = None,
        genre: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict]:
        """
        Получить список аниме с фильтрами
        
        Args:
            limit: Количество результатов (max 50)
            page: Номер страницы
            order: Сортировка (id, ranked, kind, popularity, name, aired_on, episodes, status, random)
            kind: Тип (tv, movie, ova, ona, special, music)
            status: Статус (anons, ongoing, released)
            season: Сезон (например: 2024_fall, summer_2023)
            score: Минимальный рейтинг
            genre: ID жанра (можно через запятую)
            search: Поиск по названию
        """
        params = {
            'limit': min(limit, 50),
            'page': page,
            'order': order
        }
        
        if kind:
            params['kind'] = kind
        if status:
            params['status'] = status
        if season:
            params['season'] = season
        if score:
            params['score'] = score
        if genre:
            params['genre'] = genre
        if search:
            params['search'] = search
        
        try:
            response = self.session.get(
                f"{self.BASE_URL}/animes",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return []
    
    def get_anime_by_id(self, anime_id: int) -> Optional[Dict]:
        """Получить детальную информацию об аниме"""
        try:
            response = self.session.get(
                f"{self.BASE_URL}/animes/{anime_id}",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка получения аниме {anime_id}: {e}")
            return None
    
    def search_animes(self, query: str, limit: int = 10) -> List[Dict]:
        """Поиск аниме по названию"""
        return self.get_animes(search=query, limit=limit)
    
    def get_genres(self) -> List[Dict]:
        """Получить список всех жанров"""
        try:
            response = self.session.get(
                f"{self.BASE_URL}/genres",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка получения жанров: {e}")
            return []
    
    def get_studios(self) -> List[Dict]:
        """Получить список студий"""
        try:
            response = self.session.get(
                f"{self.BASE_URL}/studios",
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка получения студий: {e}")
            return []


# Пример использования ZHOPA
if __name__ == "__main__":
    client = ShikimoriAPI()
    
    # Получить топ 10 популярных аниме
    print("Топ 10 популярных аниме:")
    animes = client.get_animes(limit=10, order="popularity")
    for anime in animes:
        print(f"- {anime.get('russian', anime['name'])} (Score: {anime['score']})")
    
    # Поиск аниме
    print("\nПоиск 'Naruto':")
    results = client.search_animes("Naruto", limit=5)
    for anime in results:
        print(f"- {anime['name']}")