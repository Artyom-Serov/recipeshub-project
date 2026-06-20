import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AuthContext } from '../../contexts'
import Main from './index'

jest.mock('../../utils/index.js', () => ({
  hexToRgba: jest.fn(() => 'rgba(135, 117, 210, 0.1)'),
  useRecipes: () => ({
    recipes: [
      {
        id: 1,
        name: 'Борщ',
        image: 'img.jpg',
        cooking_time: 60,
        is_favorited: false,
        is_in_shopping_cart: false,
        tags: [{ id: 1, name: 'Завтрак', color: '#8775D2' }],
        author: { id: 1, first_name: 'Иван', last_name: 'Петров' }
      }
    ],
    setRecipes: jest.fn(),
    recipesCount: 1,
    setRecipesCount: jest.fn(),
    recipesPage: 1,
    setRecipesPage: jest.fn(),
    tagsValue: [{ id: 1, name: 'Завтрак', color: '#8775D2', value: true }],
    setTagsValue: jest.fn(),
    handleTagsChange: jest.fn(),
    handleLike: jest.fn(),
    handleAddToCart: jest.fn()
  })
}))

const renderMain = (updateOrders = jest.fn()) => {
  return render(
    <MemoryRouter>
      <AuthContext.Provider value={false}>
        <Main updateOrders={updateOrders} />
      </AuthContext.Provider>
    </MemoryRouter>
  )
}

describe('Main', () => {
  it('renders page title', () => {
    renderMain()
    expect(screen.getByText('Рецепты')).toBeInTheDocument()
  })

  it('renders recipe name', () => {
    renderMain()
    expect(screen.getByText('Борщ')).toBeInTheDocument()
  })

  it('renders tags', () => {
    renderMain()
    const tags = screen.getAllByText('Завтрак')
    expect(tags.length).toBeGreaterThanOrEqual(1)
  })
})
