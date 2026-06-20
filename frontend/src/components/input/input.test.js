import { render, screen, fireEvent } from '@testing-library/react'
import Input from './index'

describe('Input', () => {
  it('renders label text', () => {
    render(<Input label='Электронная почта' />)
    expect(screen.getByText('Электронная почта')).toBeInTheDocument()
  })

  it('renders input element', () => {
    render(<Input label='Email' />)
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('calls onChange when value changes', () => {
    const handleChange = jest.fn()
    render(<Input label='Email' onChange={handleChange} name='email' />)
    const input = screen.getByRole('textbox')
    fireEvent.change(input, { target: { value: 'test@test.com' } })
    expect(handleChange).toHaveBeenCalled()
  })

  it('sets name attribute on input', () => {
    render(<Input label='Email' name='email' />)
    expect(screen.getByRole('textbox')).toHaveAttribute('name', 'email')
  })

  it('sets required attribute', () => {
    render(<Input label='Email' required name='email' />)
    expect(screen.getByRole('textbox')).toBeRequired()
  })

  it('passes type attribute', () => {
    render(<Input label='Password' type='password' name='password' />)
    const input = screen.getByLabelText('Password')
    expect(input).toHaveAttribute('type', 'password')
  })

  it('starts with provided value', () => {
    render(<Input label='Email' value='test@test.com' name='email' />)
    expect(screen.getByRole('textbox')).toHaveValue('test@test.com')
  })
})
