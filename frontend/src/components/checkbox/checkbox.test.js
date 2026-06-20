import { render, screen, fireEvent } from '@testing-library/react'
import Checkbox from './index'

describe('Checkbox', () => {
  it('renders name text', () => {
    render(<Checkbox name='Завтрак' id={1} />)
    expect(screen.getByText('Завтрак')).toBeInTheDocument()
  })

  it('shows check icon when value is true', () => {
    const { container } = render(<Checkbox name='Завтрак' id={1} value={true} />)
    expect(container.querySelector('svg')).toBeInTheDocument()
  })

  it('hides check icon when value is false', () => {
    const { container } = render(<Checkbox name='Завтрак' id={1} value={false} />)
    expect(container.querySelector('svg')).not.toBeInTheDocument()
  })

  it('calls onChange with id when clicked', () => {
    const handleChange = jest.fn()
    render(<Checkbox name='Завтрак' id={5} onChange={handleChange} />)
    fireEvent.click(screen.getByRole('button'))
    expect(handleChange).toHaveBeenCalledWith(5)
  })

  it('applies active class when value is true', () => {
    const { container } = render(<Checkbox name='Завтрак' id={1} value={true} />)
    const button = container.querySelector('button')
    expect(button.className).toContain('checkbox_active')
  })

  it('does not apply active class when value is false', () => {
    const { container } = render(<Checkbox name='Завтрак' id={1} value={false} />)
    const button = container.querySelector('button')
    expect(button.className).not.toContain('checkbox_active')
  })
})
