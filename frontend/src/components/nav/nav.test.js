import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Nav from './index'

const renderNav = (loggedIn, orders = 0) => {
  return render(
    <MemoryRouter>
      <Nav loggedIn={loggedIn} orders={orders} />
    </MemoryRouter>
  )
}

describe('Nav', () => {
  it('shows recipes link for all users', () => {
    renderNav(false)
    expect(screen.getByText('Рецепты')).toBeInTheDocument()
  })

  it('hides auth-required links when not logged in', () => {
    renderNav(false)
    expect(screen.queryByText('Мои подписки')).not.toBeInTheDocument()
    expect(screen.queryByText('Создать рецепт')).not.toBeInTheDocument()
    expect(screen.queryByText('Избранное')).not.toBeInTheDocument()
    expect(screen.queryByText('Список покупок')).not.toBeInTheDocument()
  })

  it('shows auth-required links when logged in', () => {
    renderNav(true)
    expect(screen.getByText('Рецепты')).toBeInTheDocument()
    expect(screen.getByText('Мои подписки')).toBeInTheDocument()
    expect(screen.getByText('Создать рецепт')).toBeInTheDocument()
    expect(screen.getByText('Избранное')).toBeInTheDocument()
    expect(screen.getByText('Список покупок')).toBeInTheDocument()
  })

  it('shows orders count badge when orders > 0', () => {
    const { container } = renderNav(true, 3)
    const badge = container.querySelector('.orders-count')
    expect(badge).toBeInTheDocument()
    expect(badge.textContent).toBe('3')
  })

  it('hides orders count badge when orders is 0', () => {
    const { container } = renderNav(true, 0)
    expect(container.querySelector('.orders-count')).not.toBeInTheDocument()
  })
})
