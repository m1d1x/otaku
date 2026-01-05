// API клиент для работы с нашим бэкендом

const API_BASE_URL = 'http://localhost:8000/api'

class AnimeAPI {
	/**
	 * Получить список аниме с фильтрами
	 */
	static async getAnimes(params = {}) {
		const {
			limit = 20,
			page = 1,
			order = 'popularity',
			kind = null,
			status = null,
			season = null,
			score = null,
			genre = null,
			search = null,
		} = params

		const queryParams = new URLSearchParams({
			limit: limit.toString(),
			page: page.toString(),
			order,
		})

		if (kind) queryParams.append('kind', kind)
		if (status) queryParams.append('status', status)
		if (season) queryParams.append('season', season)
		if (score) queryParams.append('score', score.toString())
		if (genre) queryParams.append('genre', genre)
		if (search) queryParams.append('search', search)

		try {
			const response = await fetch(`${API_BASE_URL}/animes?${queryParams}`)

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`)
			}

			const result = await response.json()
			return result.data
		} catch (error) {
			console.error('Ошибка получения аниме:', error)
			throw error
		}
	}

	/**
	 * Получить детальную информацию об аниме
	 */
	static async getAnimeById(id) {
		try {
			const response = await fetch(`${API_BASE_URL}/animes/${id}`)

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`)
			}

			const result = await response.json()
			return result.data
		} catch (error) {
			console.error(`Ошибка получения аниме ${id}:`, error)
			throw error
		}
	}

	/**
	 * Поиск аниме по названию
	 */
	static async searchAnimes(query, limit = 10) {
		try {
			const response = await fetch(
				`${API_BASE_URL}/search?q=${encodeURIComponent(query)}&limit=${limit}`
			)

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`)
			}

			const result = await response.json()
			return result.data
		} catch (error) {
			console.error('Ошибка поиска:', error)
			throw error
		}
	}

	/**
	 * Получить список жанров
	 */
	static async getGenres() {
		try {
			const response = await fetch(`${API_BASE_URL}/genres`)

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`)
			}

			const result = await response.json()
			return result.data
		} catch (error) {
			console.error('Ошибка получения жанров:', error)
			throw error
		}
	}

	/**
	 * Получить список студий
	 */
	static async getStudios() {
		try {
			const response = await fetch(`${API_BASE_URL}/studios`)

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`)
			}

			const result = await response.json()
			return result.data
		} catch (error) {
			console.error('Ошибка получения студий:', error)
			throw error
		}
	}
}

export default AnimeAPI
