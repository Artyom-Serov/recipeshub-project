import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AuthContext } from '../../contexts'
import SignUp from './index'

const renderSignUp = (loggedIn = false, onSignUp = jest.fn()) => {
  return render(
    <MemoryRouter>
      <AuthContext.Provider value={loggedIn}>
        <SignUp onSignUp={onSignUp} />
      </AuthContext.Provider>
    </MemoryRouter>
  )
}

describe('SignUp', () => {
  it('renders form title', () => {
    renderSignUp()
    expect(screen.getByText('Регистрация')).toBeInTheDocument()
  })

  it('renders all 5 form fields', () => {
    renderSignUp()
    expect(screen.getByText('Имя')).toBeInTheDocument()
    expect(screen.getByText('Фамилия')).toBeInTheDocument()
    expect(screen.getByText('Имя пользователя')).toBeInTheDocument()
    expect(screen.getByText('Адрес электронной почты')).toBeInTheDocument()
    expect(screen.getByText('Пароль')).toBeInTheDocument()
  })

  it('renders submit button', () => {
    renderSignUp()
    expect(screen.getByText('Создать аккаунт')).toBeInTheDocument()
  })

  it('submit button is disabled by default', () => {
    renderSignUp()
    expect(screen.getByText('Создать аккаунт')).toBeDisabled()
  })

  it('calls onSignUp with values on submit', () => {
    const onSignUp = jest.fn()
    renderSignUp(false, onSignUp)
    const form = screen.getByText('Регистрация').closest('form') || document.querySelector('form')
    fireEvent.submit(form)
    expect(onSignUp).toHaveBeenCalled()
  })
})
