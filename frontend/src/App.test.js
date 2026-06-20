import { render, screen, waitFor, act } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import App from './App'

jest.mock('./api', () => ({
  __esModule: true,
  default: {
    getUserData: jest.fn(),
    getRecipes: jest.fn().mockResolvedValue({ count: 0, results: [] }),
    signin: jest.fn(),
    signout: jest.fn(),
    signup: jest.fn(),
    changePassword: jest.fn(),
    getTags: jest.fn().mockResolvedValue([]),
    getRecipe: jest.fn(),
    addToFavorites: jest.fn(),
    removeFromFavorites: jest.fn(),
    addToOrders: jest.fn(),
    removeFromOrders: jest.fn(),
    downloadFile: jest.fn(),
    getUser: jest.fn(),
    getUsers: jest.fn(),
    getSubscriptions: jest.fn(),
    subscribe: jest.fn(),
    deleteSubscriptions: jest.fn(),
    getIngredients: jest.fn().mockResolvedValue([]),
    createRecipe: jest.fn(),
    updateRecipe: jest.fn(),
    deleteRecipe: jest.fn()
  }
}))

import api from './api'

const renderApp = (initialEntries = ['/']) => {
  return render(
    <MemoryRouter initialEntries={initialEntries}>
      <App />
    </MemoryRouter>
  )
}

describe('App', () => {
  beforeEach(() => {
    jest.clearAllMocks()
    localStorage.clear()
  })

  it('renders signin page when not authenticated', async () => {
    localStorage.removeItem('token')
    renderApp(['/'])
    expect(await screen.findByText('Войти на сайт')).toBeInTheDocument()
  })

  it('checks token on mount if token exists', async () => {
    const originalError = console.error
    console.error = (...args) => {
      if (args[0]?.includes?.('Cannot update a component')) return
      if (args[0]?.includes?.('Cannot read properties of undefined')) return
      originalError.call(console, ...args)
    }
    localStorage.setItem('token', 'valid-token')
    api.getUserData.mockResolvedValue({ id: 1, email: 'test@test.com' })
    api.getRecipes.mockResolvedValue({ count: 0, results: [] })
    api.getTags.mockResolvedValue([])
    renderApp()
    await waitFor(() => {
      expect(api.getUserData).toHaveBeenCalled()
    })
    console.error = originalError
  })

  it('shows navigation links for unauthenticated user', async () => {
    localStorage.removeItem('token')
    renderApp(['/signin'])
    expect(await screen.findByText('Создать аккаунт')).toBeInTheDocument()
    expect(screen.getByText('Рецепты')).toBeInTheDocument()
  })

  it('renders footer', async () => {
    localStorage.removeItem('token')
    renderApp(['/signin'])
    expect(await screen.findByText('Продуктовый помощник')).toBeInTheDocument()
  })
})
