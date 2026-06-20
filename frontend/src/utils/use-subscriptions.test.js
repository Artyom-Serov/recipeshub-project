import { renderHook, act } from '@testing-library/react-hooks'
import useSubscriptions from './use-subscriptions'

jest.mock('../api', () => ({
  __esModule: true,
  default: {
    deleteSubscriptions: jest.fn()
  }
}))

const api = require('../api').default

describe('useSubscriptions', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    jest.spyOn(window, 'alert').mockImplementation(() => {})
  })

  it('initializes with empty state', () => {
    const { result } = renderHook(() => useSubscriptions())
    expect(result.current.subscriptions).toEqual([])
    expect(result.current.subscriptionsPage).toBe(1)
    expect(result.current.subscriptionsCount).toBe(0)
  })

  it('setSubscriptions updates subscriptions', () => {
    const { result } = renderHook(() => useSubscriptions())
    const subs = [{ id: 1, name: 'Author' }]
    act(() => {
      result.current.setSubscriptions(subs)
    })
    expect(result.current.subscriptions).toEqual(subs)
  })

  it('setSubscriptionsPage updates page', () => {
    const { result } = renderHook(() => useSubscriptions())
    act(() => {
      result.current.setSubscriptionsPage(3)
    })
    expect(result.current.subscriptionsPage).toBe(3)
  })

  describe('removeSubscription', () => {
    it('removes subscription from list and decrements count on success', async () => {
      api.deleteSubscriptions.mockResolvedValue({})
      const { result } = renderHook(() => useSubscriptions())
      act(() => {
        result.current.setSubscriptions([
          { id: 1, name: 'Author 1' },
          { id: 2, name: 'Author 2' }
        ])
        result.current.setSubscriptionsCount(2)
      })
      await act(async () => {
        await result.current.removeSubscription({ id: 1 })
      })
      expect(api.deleteSubscriptions).toHaveBeenCalledWith({ author_id: 1 })
      expect(result.current.subscriptions).toEqual([
        { id: 2, name: 'Author 2' }
      ])
      expect(result.current.subscriptionsCount).toBe(1)
    })

    it('shows alert on API error', async () => {
      api.deleteSubscriptions.mockRejectedValue({ errors: 'Error' })
      const { result } = renderHook(() => useSubscriptions())
      await act(async () => {
        await result.current.removeSubscription({ id: 1 })
      })
      expect(window.alert).toHaveBeenCalledWith('Error')
    })

    it('does nothing on API error without errors field', async () => {
      api.deleteSubscriptions.mockRejectedValue({})
      const { result } = renderHook(() => useSubscriptions())
      act(() => {
        result.current.setSubscriptions([
          { id: 1, name: 'Author 1' }
        ])
        result.current.setSubscriptionsCount(1)
      })
      await act(async () => {
        await result.current.removeSubscription({ id: 1 })
      })
      expect(window.alert).not.toHaveBeenCalled()
    })
  })
})
