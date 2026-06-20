import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route } from 'react-router-dom'
import { AuthContext, UserContext } from '../../contexts'
import SingleCard from './index'

jest.mock('../../utils/index.js', () => ({
  hexToRgba: jest.fn(() => 'rgba(135, 117, 210, 0.1)'),
  useRecipe: () => ({
    recipe: {
      id: 1,
      name: 'Борщ',
      image: 'http://example.com/borsch.jpg',
      tags: [{ id: 1, name: 'Завтрак', color: '#8775D2' }],
      cooking_time: 60,
      text: 'Описание рецепта',
      is_favorited: false,
      is_in_shopping_cart: false,
      ingredients: [
        { id: 1, name: 'Свекла', amount: 2, measurement_unit: 'шт' }
      ],
      author: {
        id: 5,
        first_name: 'Иван',
        last_name: 'Петров',
        is_subscribed: false
      }
    },
    setRecipe: jest.fn(),
    handleLike: jest.fn(),
    handleAddToCart: jest.fn(),
    handleSubscribe: jest.fn()
  })
}))

const renderSingleCard = (loggedIn = false, currentUserId = 1) => {
  return render(
    <MemoryRouter initialEntries={['/recipes/1']}>
      <AuthContext.Provider value={loggedIn}>
        <UserContext.Provider value={{ id: currentUserId }}>
          <Route path='/recipes/:id'>
            <SingleCard
              loggedIn={loggedIn}
              loadItem={jest.fn()}
              updateOrders={jest.fn()}
            />
          </Route>
        </UserContext.Provider>
      </AuthContext.Provider>
    </MemoryRouter>
  )
}

describe('SingleCard', () => {
  it('renders recipe name', () => {
    renderSingleCard()
    expect(screen.getByText('Борщ')).toBeInTheDocument()
  })

  it('renders cooking time', () => {
    renderSingleCard()
    expect(screen.getByText('60 мин.')).toBeInTheDocument()
  })

  it('renders ingredient', () => {
    renderSingleCard()
    expect(screen.getByText('Свекла - 2 шт')).toBeInTheDocument()
  })

  it('renders author name', () => {
    renderSingleCard()
    expect(screen.getByText('Иван Петров')).toBeInTheDocument()
  })

  it('renders subscribe button when not own page', () => {
    renderSingleCard(true, 1)
    expect(screen.getByText('Подписаться на автора')).toBeInTheDocument()
  })

  it('does not render subscribe button on own recipe', () => {
    renderSingleCard(true, 5)
    expect(screen.queryByText('Подписаться на автора')).not.toBeInTheDocument()
  })

  it('renders edit link on own recipe', () => {
    renderSingleCard(true, 5)
    expect(screen.getByText('Редактировать рецепт')).toBeInTheDocument()
  })
})
