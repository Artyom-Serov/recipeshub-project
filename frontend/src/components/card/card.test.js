import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AuthContext } from '../../contexts'
import Card from './index'

const defaultProps = {
  name: 'Борщ',
  id: 1,
  image: 'http://example.com/borsch.jpg',
  is_favorited: false,
  is_in_shopping_cart: false,
  tags: [{ id: 1, name: 'Завтрак', color: '#8775D2' }],
  cooking_time: 60,
  author: { id: 5, first_name: 'Иван', last_name: 'Петров' },
  handleLike: jest.fn(),
  handleAddToCart: jest.fn(),
  updateOrders: jest.fn()
}

const renderCard = (props = {}, loggedIn = true) => {
  return render(
    <MemoryRouter>
      <AuthContext.Provider value={loggedIn}>
        <Card {...defaultProps} {...props} />
      </AuthContext.Provider>
    </MemoryRouter>
  )
}

describe('Card', () => {
  it('renders recipe name', () => {
    renderCard()
    expect(screen.getByText('Борщ')).toBeInTheDocument()
  })

  it('renders cooking time', () => {
    renderCard()
    expect(screen.getByText('60 мин.')).toBeInTheDocument()
  })

  it('renders author name', () => {
    renderCard()
    expect(screen.getByText('Иван Петров')).toBeInTheDocument()
  })

  it('renders add to cart button when logged in', () => {
    renderCard()
    expect(screen.getByText(/Добавить в покупки/)).toBeInTheDocument()
  })

  it('shows "Рецепт добавлен" when in shopping cart', () => {
    renderCard({ is_in_shopping_cart: true })
    expect(screen.getByText(/Рецепт добавлен/)).toBeInTheDocument()
  })

  it('hides action buttons when not logged in', () => {
    renderCard({}, false)
    expect(screen.queryByText(/Добавить в покупки/)).not.toBeInTheDocument()
    expect(screen.queryByText(/Рецепт добавлен/)).not.toBeInTheDocument()
  })

  it('calls handleAddToCart when add button is clicked', () => {
    const handleAddToCart = jest.fn()
    renderCard({ handleAddToCart })
    fireEvent.click(screen.getByText(/Добавить в покупки/))
    expect(handleAddToCart).toHaveBeenCalledWith({
      id: 1,
      toAdd: 1,
      callback: defaultProps.updateOrders
    })
  })

  it('calls handleLike when star is clicked', () => {
    const handleLike = jest.fn()
    renderCard({ handleLike })
    const buttons = screen.getAllByRole('button')
    const starButton = buttons[1]
    fireEvent.click(starButton)
    expect(handleLike).toHaveBeenCalledWith({ id: 1, toLike: 1 })
  })

  it('renders link to recipe detail', () => {
    renderCard()
    const links = screen.getAllByRole('link')
    const recipeLink = links.find(l => l.getAttribute('href') === '/recipes/1')
    expect(recipeLink).toBeInTheDocument()
  })
})
