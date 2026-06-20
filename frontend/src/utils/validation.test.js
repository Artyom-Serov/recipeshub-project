import { renderHook, act } from '@testing-library/react-hooks'
import { useForm, useFormWithValidation } from './validation'

describe('useForm', () => {
  it('initializes with empty values', () => {
    const { result } = renderHook(() => useForm())
    expect(result.current.values).toEqual({})
  })

  it('updates values on handleChange', () => {
    const { result } = renderHook(() => useForm())
    act(() => {
      result.current.handleChange({
        target: { name: 'email', value: 'test@test.com' }
      })
    })
    expect(result.current.values).toEqual({ email: 'test@test.com' })
  })

  it('preserves existing values when adding new field', () => {
    const { result } = renderHook(() => useForm())
    act(() => {
      result.current.handleChange({
        target: { name: 'email', value: 'test@test.com' }
      })
    })
    act(() => {
      result.current.handleChange({
        target: { name: 'password', value: '123456' }
      })
    })
    expect(result.current.values).toEqual({
      email: 'test@test.com',
      password: '123456'
    })
  })

  it('overwrites existing field value', () => {
    const { result } = renderHook(() => useForm())
    act(() => {
      result.current.handleChange({
        target: { name: 'email', value: 'old@test.com' }
      })
    })
    act(() => {
      result.current.handleChange({
        target: { name: 'email', value: 'new@test.com' }
      })
    })
    expect(result.current.values).toEqual({ email: 'new@test.com' })
  })

  it('setValues updates values directly', () => {
    const { result } = renderHook(() => useForm())
    act(() => {
      result.current.setValues({ name: 'John', age: '30' })
    })
    expect(result.current.values).toEqual({ name: 'John', age: '30' })
  })
})

describe('useFormWithValidation', () => {
  it('initializes with empty values, errors, and isValid=false', () => {
    const { result } = renderHook(() => useFormWithValidation())
    expect(result.current.values).toEqual({})
    expect(result.current.errors).toEqual({})
    expect(result.current.isValid).toBe(false)
  })

  it('resets form with custom values', () => {
    const { result } = renderHook(() => useFormWithValidation())
    act(() => {
      result.current.resetForm(
        { email: 'test@test.com' },
        { email: '' },
        true
      )
    })
    expect(result.current.values).toEqual({ email: 'test@test.com' })
    expect(result.current.errors).toEqual({ email: '' })
    expect(result.current.isValid).toBe(true)
  })

  it('resets form to empty state by default', () => {
    const { result } = renderHook(() => useFormWithValidation())
    act(() => {
      result.current.resetForm()
    })
    expect(result.current.values).toEqual({})
    expect(result.current.errors).toEqual({})
    expect(result.current.isValid).toBe(false)
  })
})
