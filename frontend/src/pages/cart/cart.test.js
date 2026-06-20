import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Cart from './index'

jest.mock('../../utils/index.js', () => ({
  useRecipes: () => ({
    recipes: [
      {
        id: 1,
        name: 'Борщ',
        image: 'img.jpg',
        cooking_time: 60,
        is_in_shopping_cart: true
      },
      {
        id: 2,
        name: 'Салат',
        image: 'img2.jpg',
        cooking_time: 20,
        is_in_shopping_cart: true
      }
    ],
    setRecipes: jest.fn(),
    handleAddToCart: jest.fn()
  })
}))

const renderCart = (orders = 0, updateOrders = jest.fn()) => {
  return render(
    <MemoryRouter>
      <Cart orders={orders} updateOrders={updateOrders} />
    </MemoryRouter>
  )
}

describe('Cart', () => {
  it('renders page title', () => {
    renderCart()
    expect(screen.getByText('Список покупок')).toBeInTheDocument()
  })

  it('renders recipe names in cart', () => {
    renderCart()
    expect(screen.getByText('Борщ')).toBeInTheDocument()
    expect(screen.getByText('Салат')).toBeInTheDocument()
  })

  it('shows download button when orders > 0', () => {
    renderCart(2)
    expect(screen.getByText('Скачать список')).toBeInTheDocument()
  })

  it('hides download button when orders is 0', () => {
    renderCart(0)
    expect(screen.queryByText('Скачать список')).not.toBeInTheDocument()
  })
})
