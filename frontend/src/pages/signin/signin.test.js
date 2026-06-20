import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AuthContext } from '../../contexts'
import SignIn from './index'

const renderSignIn = (loggedIn = false, onSignIn = jest.fn()) => {
  return render(
    <MemoryRouter>
      <AuthContext.Provider value={loggedIn}>
        <SignIn onSignIn={onSignIn} />
      </AuthContext.Provider>
    </MemoryRouter>
  )
}

describe('SignIn', () => {
  it('renders form title', () => {
    renderSignIn()
    expect(screen.getByText('Войти на сайт')).toBeInTheDocument()
  })

  it('renders email and password inputs', () => {
    renderSignIn()
    expect(screen.getByText('Электронная почта')).toBeInTheDocument()
    expect(screen.getByText('Пароль')).toBeInTheDocument()
  })

  it('renders submit button', () => {
    renderSignIn()
    expect(screen.getByText('Войти')).toBeInTheDocument()
  })

  it('submit button is disabled by default (isValid=false)', () => {
    renderSignIn()
    expect(screen.getByText('Войти')).toBeDisabled()
  })

  it('calls onSignIn with values on submit', () => {
    const onSignIn = jest.fn()
    renderSignIn(false, onSignIn)
    const emailInput = screen.getByLabelText('Электронная почта')
    const passwordInput = screen.getByLabelText('Пароль')

    fireEvent.change(emailInput, { target: { value: 'test@test.com', name: 'email' } })
    fireEvent.change(passwordInput, { target: { value: 'password123', name: 'password' } })
    fireEvent.submit(emailInput.closest('form'))

    expect(onSignIn).toHaveBeenCalledWith(
      expect.objectContaining({
        email: 'test@test.com',
        password: 'password123'
      })
    )
  })
})
