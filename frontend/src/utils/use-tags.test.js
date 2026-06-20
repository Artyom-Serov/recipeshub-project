import { renderHook, act } from '@testing-library/react-hooks'
import { useTags } from './use-tags'

describe('useTags', () => {
  it('initializes with empty array', () => {
    const { result } = renderHook(() => useTags())
    expect(result.current.value).toEqual([])
  })

  it('setValue sets tags array', () => {
    const { result } = renderHook(() => useTags())
    const tags = [
      { id: 1, name: 'Завтрак', value: true },
      { id: 2, name: 'Обед', value: false }
    ]
    act(() => {
      result.current.setValue(tags)
    })
    expect(result.current.value).toEqual(tags)
  })

  it('handleChange toggles tag value from true to false', () => {
    const { result } = renderHook(() => useTags())
    act(() => {
      result.current.setValue([
        { id: 1, name: 'Завтрак', value: true }
      ])
    })
    act(() => {
      result.current.handleChange(1)
    })
    expect(result.current.value[0].value).toBe(false)
  })

  it('handleChange toggles tag value from false to true', () => {
    const { result } = renderHook(() => useTags())
    act(() => {
      result.current.setValue([
        { id: 1, name: 'Завтрак', value: false }
      ])
    })
    act(() => {
      result.current.handleChange(1)
    })
    expect(result.current.value[0].value).toBe(true)
  })

  it('handleChange toggles only the specified tag', () => {
    const { result } = renderHook(() => useTags())
    act(() => {
      result.current.setValue([
        { id: 1, name: 'Завтрак', value: true },
        { id: 2, name: 'Обед', value: false }
      ])
    })
    act(() => {
      result.current.handleChange(1)
    })
    expect(result.current.value[0].value).toBe(false)
    expect(result.current.value[1].value).toBe(false)
  })

  it('handleChange with non-existent id does nothing', () => {
    const { result } = renderHook(() => useTags())
    act(() => {
      result.current.setValue([
        { id: 1, name: 'Завтрак', value: true }
      ])
    })
    act(() => {
      result.current.handleChange(999)
    })
    expect(result.current.value[0].value).toBe(true)
  })
})
