import { render, screen, fireEvent } from '@testing-library/react'
import CheckboxGroup from './index'

const tags = [
  { id: 1, name: 'Завтрак', value: true, color: '#8775D2' },
  { id: 2, name: 'Обед', value: false, color: '#F1C40F' }
]

describe('CheckboxGroup', () => {
  it('renders label when provided', () => {
    render(<CheckboxGroup label='Теги' values={tags} />)
    expect(screen.getByText('Теги')).toBeInTheDocument()
  })

  it('renders all tag checkboxes', () => {
    render(<CheckboxGroup values={tags} />)
    expect(screen.getByText('Завтрак')).toBeInTheDocument()
    expect(screen.getByText('Обед')).toBeInTheDocument()
  })

  it('calls handleChange when checkbox button is clicked', () => {
    const handleChange = jest.fn()
    render(<CheckboxGroup values={tags} handleChange={handleChange} />)
    const buttons = screen.getAllByRole('button')
    fireEvent.click(buttons[0])
    expect(handleChange).toHaveBeenCalledWith(1)
  })

  it('does not render label when not provided', () => {
    const { container } = render(<CheckboxGroup values={tags} />)
    const labels = container.querySelectorAll('.label')
    expect(labels.length).toBe(0)
  })
})
