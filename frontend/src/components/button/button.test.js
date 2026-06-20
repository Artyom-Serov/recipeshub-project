import { render, screen, fireEvent } from '@testing-library/react'
import Button from './index'

describe('Button', () => {
  it('renders children text', () => {
    render(<Button>Войти</Button>)
    expect(screen.getByText('Войти')).toBeInTheDocument()
  })

  it('calls clickHandler on click', () => {
    const handleClick = jest.fn()
    render(<Button clickHandler={handleClick}>Click</Button>)
    fireEvent.click(screen.getByText('Click'))
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('renders as anchor tag when href is provided', () => {
    render(<Button href="/test">Link</Button>)
    const link = screen.getByText('Link')
    expect(link.tagName).toBe('A')
    expect(link).toHaveAttribute('href', '/test')
  })

  it('renders as button when no href', () => {
    render(<Button>Click</Button>)
    const btn = screen.getByText('Click')
    expect(btn.tagName).toBe('BUTTON')
  })

  it('applies disabled class when disabled prop is true', () => {
    const { container } = render(<Button disabled>Click</Button>)
    const button = container.querySelector('button')
    expect(button).toBeDisabled()
    expect(button.className).toContain('button_disabled')
  })

  it('does not call clickHandler when button is disabled', () => {
    const handleClick = jest.fn()
    render(<Button disabled clickHandler={handleClick}>Click</Button>)
    const button = screen.getByText('Click')
    fireEvent.click(button)
    expect(handleClick).not.toHaveBeenCalled()
  })

  it('uses default modifier when none provided', () => {
    const { container } = render(<Button>Click</Button>)
    const button = container.querySelector('button')
    expect(button.className).toContain('button_style_light-blue')
  })

  it('uses custom modifier', () => {
    const { container } = render(<Button modifier='style_dark-blue'>Click</Button>)
    const button = container.querySelector('button')
    expect(button.className).toContain('button_style_dark-blue')
  })

  it('applies custom className', () => {
    const { container } = render(<Button className='my-class'>Click</Button>)
    const button = container.querySelector('button')
    expect(button.className).toContain('my-class')
  })
})
