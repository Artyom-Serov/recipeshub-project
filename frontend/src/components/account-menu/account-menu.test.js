import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { AuthContext } from '../../contexts'
import AccountMenu from './index'

const renderMenu = (loggedIn, onSignOut) => {
  return render(
    <AuthContext.Provider value={loggedIn}>
      <MemoryRouter>
        <AccountMenu onSignOut={onSignOut} />
      </MemoryRouter>
    </AuthContext.Provider>
  )
}

describe('AccountMenu', () => {
  it('shows login and signup links when not authenticated', () => {
    renderMenu(false)
    expect(screen.getByText('Войти')).toBeInTheDocument()
    expect(screen.getByText('Создать аккаунт')).toBeInTheDocument()
  })

  it('shows change password and logout when authenticated', () => {
    renderMenu(true)
    expect(screen.getByText('Изменить пароль')).toBeInTheDocument()
    expect(screen.getByText('Выход')).toBeInTheDocument()
  })

  it('calls onSignOut when logout is clicked', () => {
    const onSignOut = jest.fn()
    renderMenu(true, onSignOut)
    fireEvent.click(screen.getByText('Выход'))
    expect(onSignOut).toHaveBeenCalledTimes(1)
  })

  it('does not show change password when not authenticated', () => {
    renderMenu(false)
    expect(screen.queryByText('Изменить пароль')).not.toBeInTheDocument()
  })

  it('does not show login when authenticated', () => {
    renderMenu(true)
    expect(screen.queryByText('Войти')).not.toBeInTheDocument()
  })
})
