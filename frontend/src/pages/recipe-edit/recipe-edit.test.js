import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route } from 'react-router-dom'
import RecipeEdit from './index'

jest.mock('../../utils/index.js', () => ({
  useTags: () => ({
    value: [{ id: 1, name: 'Завтрак', color: '#8775D2', value: true }],
    handleChange: jest.fn(),
    setValue: jest.fn()
  })
}))

const renderRecipeEdit = (onItemDelete = jest.fn()) => {
  return render(
    <MemoryRouter initialEntries={['/recipes/1/edit']}>
      <Route path='/recipes/:id/edit'>
        <RecipeEdit onItemDelete={onItemDelete} />
      </Route>
    </MemoryRouter>
  )
}

describe('RecipeEdit', () => {
  it('renders page title', () => {
    renderRecipeEdit()
    expect(screen.getByText('Редактирование рецепта')).toBeInTheDocument()
  })

  it('renders tags', () => {
    renderRecipeEdit()
    expect(screen.getByText('Завтрак')).toBeInTheDocument()
  })

  it('renders delete button', () => {
    renderRecipeEdit()
    expect(screen.getByText('Удалить')).toBeInTheDocument()
  })

  it('submit button is disabled by default', () => {
    renderRecipeEdit()
    expect(screen.getByText('Редактировать рецепт')).toBeDisabled()
  })
})
