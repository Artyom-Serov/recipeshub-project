import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route } from 'react-router-dom'
import { UserContext } from '../../contexts'
import User from './index'
import api from '../../api'

jest.mock('../../utils/index.js', () => ({
  hexToRgba: jest.fn(() => 'rgba(0, 0, 0, 0.1)'),
  useRecipes: () => ({
    recipes: [],
    setRecipes: jest.fn(),
    recipesCount: 0,
    setRecipesCount: jest.fn(),
    recipesPage: 1,
    setRecipesPage: jest.fn(),
    tagsValue: [],
    setTagsValue: jest.fn(),
    handleTagsChange: jest.fn(),
    handleLike: jest.fn(),
    handleAddToCart: jest.fn()
  }),
  useTags: () => ({
    value: [],
    handleChange: jest.fn(),
    setValue: jest.fn()
  })
}))

jest.mock('../../api')

const renderUser = (currentUserId = 1) => {
  return render(
    <MemoryRouter initialEntries={['/user/5']}>
      <UserContext.Provider value={{ id: currentUserId }}>
        <Route path='/user/:id'>
          <User updateOrders={jest.fn()} />
        </Route>
      </UserContext.Provider>
    </MemoryRouter>
  )
}

describe('User', () => {
  beforeEach(() => {
    api.getUser.mockResolvedValue({
      id: 5,
      first_name: 'Иван',
      last_name: 'Петров',
      is_subscribed: false
    })
    api.getTags.mockResolvedValue([])
    api.getRecipes.mockResolvedValue({ results: [], count: 0 })
    api.deleteSubscriptions.mockResolvedValue({})
    api.subscribe.mockResolvedValue({})
  })

  it('renders user name from API', async () => {
    renderUser()
    expect(await screen.findByText('Иван Петров')).toBeInTheDocument()
  })

  it('renders subscribe button when viewing other user', async () => {
    renderUser(1)
    expect(await screen.findByText('Подписаться на автора')).toBeInTheDocument()
  })

  it('renders unsubscribe button when already subscribed', async () => {
    api.getUser.mockResolvedValue({
      id: 5,
      first_name: 'Иван',
      last_name: 'Петров',
      is_subscribed: true
    })
    renderUser(1)
    expect(await screen.findByText('Отписаться от автора')).toBeInTheDocument()
  })
})
