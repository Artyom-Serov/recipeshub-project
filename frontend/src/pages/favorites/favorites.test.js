import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AuthContext } from '../../contexts'
import Favorites from './index'

jest.mock('../../utils/index.js', () => ({
  useRecipes: () => ({
    recipes: [
      {
        id: 1,
        name: 'Избранный рецепт',
        image: 'img.jpg',
        cooking_time: 30,
        is_favorited: true,
        is_in_shopping_cart: false,
        tags: [],
        author: { id: 1, first_name: 'Иван', last_name: 'Петров' }
      }
    ],
    setRecipes: jest.fn(),
    recipesCount: 1,
    setRecipesCount: jest.fn(),
    recipesPage: 1,
    setRecipesPage: jest.fn(),
    tagsValue: [],
    setTagsValue: jest.fn(),
    handleTagsChange: jest.fn(),
    handleLike: jest.fn(),
    handleAddToCart: jest.fn()
  })
}))

const renderFavorites = (updateOrders = jest.fn()) => {
  return render(
    <MemoryRouter>
      <AuthContext.Provider value={true}>
        <Favorites updateOrders={updateOrders} />
      </AuthContext.Provider>
    </MemoryRouter>
  )
}

describe('Favorites', () => {
  it('renders page title', () => {
    renderFavorites()
    expect(screen.getByText('Избранное')).toBeInTheDocument()
  })

  it('renders favorite recipe name', () => {
    renderFavorites()
    expect(screen.getByText('Избранный рецепт')).toBeInTheDocument()
  })
})
