import { renderHook, act } from '@testing-library/react-hooks'
import useRecipe from './use-recipe'

jest.mock('../api', () => ({
  __esModule: true,
  default: {
    addToFavorites: jest.fn(),
    removeFromFavorites: jest.fn(),
    addToOrders: jest.fn(),
    removeFromOrders: jest.fn(),
    subscribe: jest.fn(),
    deleteSubscriptions: jest.fn()
  }
}))

const api = require('../api').default

describe('useRecipe', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    jest.spyOn(window, 'alert').mockImplementation(() => {})
  })

  it('initializes with empty recipe object', () => {
    const { result } = renderHook(() => useRecipe())
    expect(result.current.recipe).toEqual({})
  })

  it('setRecipe updates recipe', () => {
    const { result } = renderHook(() => useRecipe())
    const recipe = { id: 1, name: 'Test', is_favorited: 0 }
    act(() => {
      result.current.setRecipe(recipe)
    })
    expect(result.current.recipe).toEqual(recipe)
  })

  describe('handleLike', () => {
    it('calls addToFavorites and updates is_favorited to 1', async () => {
      api.addToFavorites.mockResolvedValue({})
      const { result } = renderHook(() => useRecipe())
      await act(async () => {
        await result.current.handleLike({ id: 1, toLike: 1 })
      })
      expect(api.addToFavorites).toHaveBeenCalledWith({ id: 1 })
      expect(result.current.recipe.is_favorited).toBe(1)
    })

    it('calls removeFromFavorites and updates is_favorited to 0', async () => {
      api.removeFromFavorites.mockResolvedValue({})
      const { result } = renderHook(() => useRecipe())
      await act(async () => {
        await result.current.handleLike({ id: 1, toLike: 0 })
      })
      expect(api.removeFromFavorites).toHaveBeenCalledWith({ id: 1 })
      expect(result.current.recipe.is_favorited).toBe(0)
    })
  })

  describe('handleAddToCart', () => {
    it('calls addToOrders and updates is_in_shopping_cart to 1', async () => {
      api.addToOrders.mockResolvedValue({})
      const { result } = renderHook(() => useRecipe())
      await act(async () => {
        await result.current.handleAddToCart({ id: 1, toAdd: 1 })
      })
      expect(api.addToOrders).toHaveBeenCalledWith({ id: 1 })
      expect(result.current.recipe.is_in_shopping_cart).toBe(1)
    })

    it('calls removeFromOrders and updates is_in_shopping_cart to 0', async () => {
      api.removeFromOrders.mockResolvedValue({})
      const { result } = renderHook(() => useRecipe())
      await act(async () => {
        await result.current.handleAddToCart({ id: 1, toAdd: 0 })
      })
      expect(api.removeFromOrders).toHaveBeenCalledWith({ id: 1 })
      expect(result.current.recipe.is_in_shopping_cart).toBe(0)
    })

    it('calls callback after success', async () => {
      api.addToOrders.mockResolvedValue({})
      const callback = jest.fn()
      const { result } = renderHook(() => useRecipe())
      await act(async () => {
        await result.current.handleAddToCart({ id: 1, toAdd: 1, callback })
      })
      expect(callback).toHaveBeenCalledWith(1)
    })
  })

  describe('handleSubscribe', () => {
    it('calls subscribe and updates author.is_subscribed to 1', async () => {
      api.subscribe.mockResolvedValue({})
      const { result } = renderHook(() => useRecipe())
      act(() => {
        result.current.setRecipe({
          author: { id: 5, is_subscribed: 0 }
        })
      })
      await act(async () => {
        await result.current.handleSubscribe({ author_id: 5, toSubscribe: 1 })
      })
      expect(api.subscribe).toHaveBeenCalledWith({ author_id: 5 })
      expect(result.current.recipe.author.is_subscribed).toBe(1)
    })

    it('calls deleteSubscriptions and updates author.is_subscribed to 0', async () => {
      api.deleteSubscriptions.mockResolvedValue({})
      const { result } = renderHook(() => useRecipe())
      act(() => {
        result.current.setRecipe({
          author: { id: 5, is_subscribed: 1 }
        })
      })
      await act(async () => {
        await result.current.handleSubscribe({ author_id: 5, toSubscribe: 0 })
      })
      expect(api.deleteSubscriptions).toHaveBeenCalledWith({ author_id: 5 })
      expect(result.current.recipe.author.is_subscribed).toBe(0)
    })
  })
})
