import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route } from 'react-router-dom'
import ProtectedRoute from './index'

describe('ProtectedRoute', () => {
  const MockComponent = () => <div>Protected Content</div>

  it('renders component when loggedIn is true', () => {
    render(
      <MemoryRouter initialEntries={['/protected']}>
        <ProtectedRoute
          exact
          path='/protected'
          component={MockComponent}
          loggedIn={true}
        />
      </MemoryRouter>
    )
    expect(screen.getByText('Protected Content')).toBeInTheDocument()
  })

  it('redirects to /signin when loggedIn is false', () => {
    render(
      <MemoryRouter initialEntries={['/protected']}>
        <ProtectedRoute
          exact
          path='/protected'
          component={MockComponent}
          loggedIn={false}
        />
        <Route path='/signin'>
          <div>Sign In Page</div>
        </Route>
      </MemoryRouter>
    )
    expect(screen.getByText('Sign In Page')).toBeInTheDocument()
    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument()
  })
})
