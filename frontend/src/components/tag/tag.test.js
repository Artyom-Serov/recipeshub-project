import { render, screen } from '@testing-library/react'
import Tag from './index'

describe('Tag', () => {
  it('renders tag name', () => {
    render(<Tag name='Завтрак' />)
    expect(screen.getByText('Завтрак')).toBeInTheDocument()
  })

  it('uses default color when not provided', () => {
    const { container } = render(<Tag name='Завтрак' />)
    const tag = container.firstChild
    expect(tag.style.color).toBe('rgb(135, 117, 210)')
  })

  it('uses custom color', () => {
    const { container } = render(<Tag name='Обед' color='#FF0000' />)
    const tag = container.firstChild
    expect(tag.style.color).toBe('rgb(255, 0, 0)')
  })
})
