import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Purchase from './index'

const defaultProps = {
  image: 'http://example.com/img.jpg',
  name: 'Test Recipe',
  cooking_time: 30,
  id: 1,
  handleRemoveFromCart: jest.fn(),
  is_in_shopping_cart: true,
  updateOrders: jest.fn()
}

const renderPurchase = (props = {}) => {
  return render(
    <MemoryRouter>
      <Purchase {...defaultProps} {...props} />
    </MemoryRouter>
  )
}

describe('Purchase', () => {
  it('renders recipe name', () => {
    renderPurchase()
    expect(screen.getByText('Test Recipe')).toBeInTheDocument()
  })

  it('renders cooking time', () => {
    renderPurchase()
    expect(screen.getByText('30 мин.')).toBeInTheDocument()
  })

  it('renders remove link', () => {
    renderPurchase()
    expect(screen.getByText('Удалить')).toBeInTheDocument()
  })

  it('calls handleRemoveFromCart when remove is clicked', () => {
    const handleRemoveFromCart = jest.fn()
    renderPurchase({ handleRemoveFromCart })
    fireEvent.click(screen.getByText('Удалить'))
    expect(handleRemoveFromCart).toHaveBeenCalledWith({
      id: 1,
      toAdd: false,
      callback: defaultProps.updateOrders
    })
  })

  it('returns null when is_in_shopping_cart is false', () => {
    const { container } = renderPurchase({ is_in_shopping_cart: false })
    expect(container.innerHTML).toBe('')
  })
})
