const mockFetch = (responseData, status = 200) => {
  const ok = status < 400
  global.fetch = jest.fn().mockResolvedValue({
    status,
    ok,
    json: () => ok ? Promise.resolve(responseData) : Promise.reject(responseData),
    blob: () => Promise.resolve(new Blob(['test']))
  })
}

beforeEach(() => {
  jest.restoreAllMocks()
  localStorage.clear()
})

describe('Api', () => {
  let api
  beforeEach(() => {
    api = require('./index').default
  })

  describe('checkResponse', () => {
    it('resolves with data for status < 400', async () => {
      const res = { status: 200, json: () => Promise.resolve({ key: 'value' }) }
      const result = await api.checkResponse(res)
      expect(result).toEqual({ key: 'value' })
    })

    it('resolves with response for status 204', async () => {
      const res = { status: 204 }
      const result = await api.checkResponse(res)
      expect(result).toBe(res)
    })

    it('rejects with data for status >= 400', async () => {
      const res = { status: 400, json: () => Promise.resolve({ error: 'bad request' }) }
      await expect(api.checkResponse(res)).rejects.toEqual({ error: 'bad request' })
    })
  })

  describe('checkFileDownloadResponse', () => {
    it('rejects for status >= 400', async () => {
      const res = { status: 500, blob: () => Promise.resolve(new Blob()) }
      await expect(api.checkFileDownloadResponse(res)).rejects.toBeUndefined()
    })
  })

  describe('signin', () => {
    it('makes POST request to login endpoint', async () => {
      mockFetch({ auth_token: 'token123' })
      const result = await api.signin({ email: 'test@test.com', password: 'pass' })
      expect(fetch).toHaveBeenCalledWith('/api/auth/token/login/', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ email: 'test@test.com', password: 'pass' })
      })
      expect(result).toEqual({ auth_token: 'token123' })
    })
  })

  describe('signout', () => {
    it('makes POST request with auth token', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({})
      await api.signout()
      expect(fetch).toHaveBeenCalledWith('/api/auth/token/logout/', {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        }
      })
    })
  })

  describe('signup', () => {
    it('makes POST request to users endpoint', async () => {
      mockFetch({ id: 1 })
      const data = {
        email: 'test@test.com',
        password: 'pass',
        username: 'testuser',
        first_name: 'Test',
        last_name: 'User'
      }
      await api.signup(data)
      expect(fetch).toHaveBeenCalledWith('/api/users/', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify(data)
      })
    })
  })

  describe('getUserData', () => {
    it('makes GET request with auth token', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({ id: 1, email: 'test@test.com' })
      const result = await api.getUserData()
      expect(fetch).toHaveBeenCalledWith('/api/users/me/', {
        method: 'GET',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        }
      })
      expect(result).toEqual({ id: 1, email: 'test@test.com' })
    })
  })

  describe('changePassword', () => {
    it('makes POST request with auth token and body', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({})
      await api.changePassword({ current_password: 'old', new_password: 'new' })
      expect(fetch).toHaveBeenCalledWith('/api/users/set_password/', {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        },
        body: JSON.stringify({ current_password: 'old', new_password: 'new' })
      })
    })
  })

  describe('getRecipes', () => {
    it('makes GET request with query params', async () => {
      mockFetch({ results: [], count: 0 })
      await api.getRecipes({ page: 2, limit: 10 })
      const url = fetch.mock.calls[0][0]
      expect(url).toContain('page=2')
      expect(url).toContain('limit=10')
    })

    it('includes auth header when token exists', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({ results: [], count: 0 })
      await api.getRecipes({ page: 1 })
      expect(fetch).toHaveBeenCalledWith(
        expect.any(String),
        expect.objectContaining({
          headers: expect.objectContaining({
            'authorization': 'Token mytoken'
          })
        })
      )
    })

    it('adds tags params when tags are active', async () => {
      mockFetch({ results: [], count: 0 })
      const tags = [
        { slug: 'breakfast', value: true },
        { slug: 'lunch', value: false },
        { slug: 'dinner', value: true }
      ]
      await api.getRecipes({ page: 1, tags })
      const url = fetch.mock.calls[0][0]
      expect(url).toContain('tags=breakfast')
      expect(url).toContain('tags=dinner')
      expect(url).not.toContain('tags=lunch')
    })
  })

  describe('getRecipe', () => {
    it('makes GET request with recipe_id', async () => {
      mockFetch({ id: 1, name: 'Test' })
      await api.getRecipe({ recipe_id: 1 })
      expect(fetch).toHaveBeenCalledWith('/api/recipes/1/', {
        method: 'GET',
        headers: { 'content-type': 'application/json' }
      })
    })
  })

  describe('createRecipe', () => {
    it('makes POST request with all fields', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({ id: 1 })
      const data = {
        name: 'Test',
        image: 'data:image/png;base64,abc',
        tags: [1, 2],
        cooking_time: 30,
        text: 'Description',
        ingredients: [{ id: 1, amount: 100 }]
      }
      await api.createRecipe(data)
      expect(fetch).toHaveBeenCalledWith('/api/recipes/', {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        },
        body: JSON.stringify(data)
      })
    })
  })

  describe('addToFavorites', () => {
    it('makes POST request with auth token', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({})
      await api.addToFavorites({ id: 1 })
      expect(fetch).toHaveBeenCalledWith('/api/recipes/1/favorite/', {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        }
      })
    })
  })

  describe('removeFromFavorites', () => {
    it('makes DELETE request', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({})
      await api.removeFromFavorites({ id: 1 })
      expect(fetch).toHaveBeenCalledWith('/api/recipes/1/favorite/', {
        method: 'DELETE',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        }
      })
    })
  })

  describe('subscribe', () => {
    it('makes POST request to subscribe endpoint', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({})
      await api.subscribe({ author_id: 5 })
      expect(fetch).toHaveBeenCalledWith('/api/users/5/subscribe/', {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        }
      })
    })
  })

  describe('deleteSubscriptions', () => {
    it('makes DELETE request to unsubscribe endpoint', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({})
      await api.deleteSubscriptions({ author_id: 5 })
      expect(fetch).toHaveBeenCalledWith('/api/users/5/subscribe/', {
        method: 'DELETE',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        }
      })
    })
  })

  describe('getSubscriptions', () => {
    it('makes GET request with pagination params', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({ results: [], count: 0 })
      await api.getSubscriptions({ page: 1, limit: 6, recipes_limit: 3 })
      const url = fetch.mock.calls[0][0]
      expect(url).toContain('page=1')
      expect(url).toContain('limit=6')
      expect(url).toContain('recipes_limit=3')
    })
  })

  describe('getIngredients', () => {
    it('makes GET request with name query', async () => {
      mockFetch([{ id: 1, name: 'Tomato' }])
      await api.getIngredients({ name: 'Tom' })
      expect(fetch).toHaveBeenCalledWith('/api/ingredients/?name=Tom', {
        method: 'GET',
        headers: { 'content-type': 'application/json' }
      })
    })
  })

  describe('getTags', () => {
    it('makes GET request without auth', async () => {
      mockFetch([{ id: 1, name: 'Breakfast' }])
      const result = await api.getTags()
      expect(fetch).toHaveBeenCalledWith('/api/tags/', {
        method: 'GET',
        headers: { 'content-type': 'application/json' }
      })
      expect(result).toEqual([{ id: 1, name: 'Breakfast' }])
    })
  })

  describe('addToOrders / removeFromOrders', () => {
    it('addToOrders makes POST request', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({})
      await api.addToOrders({ id: 1 })
      expect(fetch).toHaveBeenCalledWith('/api/recipes/1/shopping_cart/', {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        }
      })
    })

    it('removeFromOrders makes DELETE request', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({})
      await api.removeFromOrders({ id: 1 })
      expect(fetch).toHaveBeenCalledWith('/api/recipes/1/shopping_cart/', {
        method: 'DELETE',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        }
      })
    })
  })

  describe('deleteRecipe', () => {
    it('makes DELETE request to recipe endpoint', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({})
      await api.deleteRecipe({ recipe_id: 1 })
      expect(fetch).toHaveBeenCalledWith('/api/recipes/1/', {
        method: 'DELETE',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        }
      })
    })
  })

  describe('downloadFile', () => {
    it('makes GET request with auth token', async () => {
      localStorage.setItem('token', 'mytoken')
      global.URL.createObjectURL = jest.fn()
      global.fetch = jest.fn().mockResolvedValue({
        status: 200,
        blob: () => new Promise(() => {})
      })
      api.downloadFile()
      expect(fetch).toHaveBeenCalledWith('/api/recipes/download_shopping_cart/', {
        method: 'GET',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        }
      })
    })
  })

  describe('getUser', () => {
    it('makes GET request with user id', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({ id: 1, email: 'user@test.com' })
      const result = await api.getUser({ id: 1 })
      expect(fetch).toHaveBeenCalledWith('/api/users/1/', {
        method: 'GET',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        }
      })
      expect(result).toEqual({ id: 1, email: 'user@test.com' })
    })
  })

  describe('getUsers', () => {
    it('makes GET request with pagination', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({ results: [], count: 0 })
      await api.getUsers({ page: 1, limit: 6 })
      const url = fetch.mock.calls[0][0]
      expect(url).toContain('page=1')
      expect(url).toContain('limit=6')
    })
  })

  describe('updateRecipe', () => {
    it('makes PATCH request with image when updated', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({ id: 1 })
      await api.updateRecipe({
        name: 'Updated',
        recipe_id: 1,
        image: 'data:image/png;base64,abc',
        tags: [1],
        cooking_time: 30,
        text: 'Desc',
        ingredients: []
      }, true)
      expect(fetch).toHaveBeenCalledWith('/api/recipes/1/', {
        method: 'PATCH',
        headers: {
          'content-type': 'application/json',
          'authorization': 'Token mytoken'
        },
        body: expect.stringContaining('"image":"data:image/png;base64,abc"')
      })
    })

    it('makes PATCH request with undefined image when not updated', async () => {
      localStorage.setItem('token', 'mytoken')
      mockFetch({ id: 1 })
      await api.updateRecipe({
        name: 'Updated',
        recipe_id: 1,
        image: 'http://example.com/img.jpg',
        tags: [1],
        cooking_time: 30,
        text: 'Desc',
        ingredients: []
      }, false)
      const body = JSON.parse(fetch.mock.calls[0][1].body)
      expect(body.image).toBeUndefined()
    })
  })
})
