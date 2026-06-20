import { render, screen, fireEvent } from '@testing-library/react'
import Textarea from './index'

describe('Textarea', () => {
  it('renders label text', () => {
    render(<Textarea label='Описание' />)
    expect(screen.getByText('Описание')).toBeInTheDocument()
  })

  it('renders textarea element', () => {
    render(<Textarea label='Описание' />)
    expect(screen.getByRole('textbox')).toBeInTheDocument()
  })

  it('calls onChange when value changes', () => {
    const handleChange = jest.fn()
    render(<Textarea label='Описание' onChange={handleChange} />)
    const textarea = screen.getByRole('textbox')
    fireEvent.change(textarea, { target: { value: 'new text' } })
    expect(handleChange).toHaveBeenCalled()
  })

  it('starts with provided value', () => {
    render(<Textarea label='Описание' value='initial' />)
    expect(screen.getByRole('textbox')).toHaveValue('initial')
  })
})
