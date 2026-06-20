import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Subscriptions from './index'

jest.mock('../../utils/index.js', () => ({
  useSubscriptions: () => ({
    subscriptions: [
      {
        id: 1,
        email: 'author@test.com',
        first_name: 'Иван',
        last_name: 'Петров',
        username: 'ivan',
        recipes_count: 2,
        recipes: [
          { id: 1, name: 'Recipe 1', image: 'img.jpg', cooking_time: 20 }
        ]
      }
    ],
    setSubscriptions: jest.fn(),
    subscriptionsCount: 1,
    setSubscriptionsCount: jest.fn(),
    removeSubscription: jest.fn(),
    subscriptionsPage: 1,
    setSubscriptionsPage: jest.fn()
  })
}))

const renderSubscriptions = () => {
  return render(
    <MemoryRouter>
      <Subscriptions />
    </MemoryRouter>
  )
}

describe('Subscriptions', () => {
  it('renders page title', () => {
    renderSubscriptions()
    expect(screen.getByText('Мои подписки')).toBeInTheDocument()
  })

  it('renders subscription author name', () => {
    renderSubscriptions()
    expect(screen.getByText('Иван Петров')).toBeInTheDocument()
  })
})
