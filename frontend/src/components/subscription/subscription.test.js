import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Subscription from './index'

const defaultProps = {
  email: 'author@test.com',
  first_name: 'Иван',
  last_name: 'Петров',
  username: 'ivan',
  removeSubscription: jest.fn(),
  recipes_count: 5,
  id: 1,
  recipes: [
    { id: 1, name: 'Recipe 1', image: 'img1.jpg', cooking_time: 20 },
    { id: 2, name: 'Recipe 2', image: 'img2.jpg', cooking_time: 30 },
    { id: 3, name: 'Recipe 3', image: 'img3.jpg', cooking_time: 10 }
  ]
}

const renderSubscription = (props = {}) => {
  return render(
    <MemoryRouter>
      <Subscription {...defaultProps} {...props} />
    </MemoryRouter>
  )
}

describe('Subscription', () => {
  it('renders author name', () => {
    renderSubscription()
    expect(screen.getByText('Иван Петров')).toBeInTheDocument()
  })

  it('renders unsubscribe button', () => {
    renderSubscription()
    expect(screen.getByText('Отписаться')).toBeInTheDocument()
  })

  it('calls removeSubscription on unsubscribe click', () => {
    const removeSubscription = jest.fn()
    renderSubscription({ removeSubscription })
    fireEvent.click(screen.getByText('Отписаться'))
    expect(removeSubscription).toHaveBeenCalledWith({ id: 1 })
  })

  it('shows "Еще N рецептов" when recipes_count > 3', () => {
    renderSubscription()
    expect(screen.getByText(/Еще 2 рецепта/)).toBeInTheDocument()
  })

  it('hides "Еще" link when recipes_count <= 3', () => {
    renderSubscription({ recipes_count: 3 })
    expect(screen.queryByText(/Еще/)).not.toBeInTheDocument()
  })

  it('renders all recipe names', () => {
    renderSubscription()
    expect(screen.getByText('Recipe 1')).toBeInTheDocument()
    expect(screen.getByText('Recipe 2')).toBeInTheDocument()
    expect(screen.getByText('Recipe 3')).toBeInTheDocument()
  })
})
