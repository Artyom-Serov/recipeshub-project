import { renderHook, act } from '@testing-library/react-hooks'
import useRecipes from './use-recipes'

jest.mock('../api', () => ({
  __esModule: true,
  default: {
    addToFavorites: jest.fn(),
    removeFromFavorites: jest.fn(),
    addToOrders: jest.fn(),
    removeFromOrders: jest.fn()
  }
}))

const api = require('../api').default

describe('useRecipes', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    jest.spyOn(window, 'alert').mockImplementation(() => {})
  })

  it('initializes with empty state', () => {
    const { result } = renderHook(() => useRecipes())
    expect(result.current.recipes).toEqual([])
    expect(result.current.recipesCount).toBe(0)
    expect(result.current.recipesPage).toBe(1)
    expect(result.current.tagsValue).toEqual([])
  })

  it('setRecipes updates recipes', () => {
    const { result } = renderHook(() => useRecipes())
    const recipes = [{ id: 1, name: 'Test' }]
    act(() => {
      result.current.setRecipes(recipes)
    })
    expect(result.current.recipes).toEqual(recipes)
  })

  it('setRecipesCount updates count', () => {
    const { result } = renderHook(() => useRecipes())
    act(() => {
      result.current.setRecipesCount(10)
    })
    expect(result.current.recipesCount).toBe(10)
  })

  it('setRecipesPage updates page', () => {
    const { result } = renderHook(() => useRecipes())
    act(() => {
      result.current.setRecipesPage(3)
    })
    expect(result.current.recipesPage).toBe(3)
  })

  describe('handleLike', () => {
    it('calls addToFavorites and updates recipe is_favorited on success', async () => {
      api.addToFavorites.mockResolvedValue({})
      const { result } = renderHook(() => useRecipes())
      act(() => {
        result.current.setRecipes([
          { id: 1, name: 'Test', is_favorited: false }
        ])
      })
      await act(async () => {
        await result.current.handleLike({ id: 1, toLike: true })
      })
      expect(api.addToFavorites).toHaveBeenCalledWith({ id: 1 })
      expect(result.current.recipes[0].is_favorited).toBe(true)
    })

    it('calls removeFromFavorites and updates recipe is_favorited on success', async () => {
      api.removeFromFavorites.mockResolvedValue({})
      const { result } = renderHook(() => useRecipes())
      act(() => {
        result.current.setRecipes([
          { id: 1, name: 'Test', is_favorited: true }
        ])
      })
      await act(async () => {
        await result.current.handleLike({ id: 1, toLike: false })
      })
      expect(api.removeFromFavorites).toHaveBeenCalledWith({ id: 1 })
      expect(result.current.recipes[0].is_favorited).toBe(false)
    })

    it('shows alert on API error with errors field', async () => {
      api.addToFavorites.mockRejectedValue({ errors: 'Server error' })
      const { result } = renderHook(() => useRecipes())
      act(() => {
        result.current.setRecipes([
          { id: 1, name: 'Test', is_favorited: false }
        ])
      })
      await act(async () => {
        await result.current.handleLike({ id: 1, toLike: true })
      })
      expect(window.alert).toHaveBeenCalledWith('Server error')
    })
  })

  describe('handleAddToCart', () => {
    it('calls addToOrders and updates recipe is_in_shopping_cart on success', async () => {
      api.addToOrders.mockResolvedValue({})
      const { result } = renderHook(() => useRecipes())
      act(() => {
        result.current.setRecipes([
          { id: 1, name: 'Test', is_in_shopping_cart: false }
        ])
      })
      await act(async () => {
        await result.current.handleAddToCart({ id: 1, toAdd: true })
      })
      expect(api.addToOrders).toHaveBeenCalledWith({ id: 1 })
      expect(result.current.recipes[0].is_in_shopping_cart).toBe(true)
    })

    it('calls removeFromOrders and updates recipe is_in_shopping_cart on success', async () => {
      api.removeFromOrders.mockResolvedValue({})
      const { result } = renderHook(() => useRecipes())
      act(() => {
        result.current.setRecipes([
          { id: 1, name: 'Test', is_in_shopping_cart: true }
        ])
      })
      await act(async () => {
        await result.current.handleAddToCart({ id: 1, toAdd: false })
      })
      expect(api.removeFromOrders).toHaveBeenCalledWith({ id: 1 })
      expect(result.current.recipes[0].is_in_shopping_cart).toBe(false)
    })

    it('calls callback after successful add', async () => {
      api.addToOrders.mockResolvedValue({})
      const callback = jest.fn()
      const { result } = renderHook(() => useRecipes())
      act(() => {
        result.current.setRecipes([
          { id: 1, name: 'Test', is_in_shopping_cart: false }
        ])
      })
      await act(async () => {
        await result.current.handleAddToCart({ id: 1, toAdd: true, callback })
      })
      expect(callback).toHaveBeenCalledWith(true)
    })

    it('shows alert on API error', async () => {
      api.addToOrders.mockRejectedValue({ errors: 'Error' })
      const { result } = renderHook(() => useRecipes())
      await act(async () => {
        await result.current.handleAddToCart({ id: 1, toAdd: true })
      })
      expect(window.alert).toHaveBeenCalledWith('Error')
    })
  })
})
