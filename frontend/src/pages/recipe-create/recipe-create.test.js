import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import RecipeCreate from './index'

jest.mock('../../utils/index.js', () => ({
  useTags: () => ({
    value: [{ id: 1, name: 'Завтрак', color: '#8775D2', value: true }],
    handleChange: jest.fn(),
    setValue: jest.fn()
  })
}))

const renderRecipeCreate = () => {
  return render(
    <MemoryRouter>
      <RecipeCreate />
    </MemoryRouter>
  )
}

describe('RecipeCreate', () => {
  it('renders page title', () => {
    renderRecipeCreate()
    expect(screen.getByText('Создание рецепта')).toBeInTheDocument()
  })

  it('renders recipe name input', () => {
    renderRecipeCreate()
    expect(screen.getByText('Название рецепта')).toBeInTheDocument()
  })

  it('renders tags', () => {
    renderRecipeCreate()
    expect(screen.getByText('Завтрак')).toBeInTheDocument()
  })

  it('submit button is disabled by default', () => {
    renderRecipeCreate()
    expect(screen.getByText('Создать рецепт')).toBeDisabled()
  })
})
