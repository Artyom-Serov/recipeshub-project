import { render, screen, fireEvent } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import ChangePassword from './index'

const renderChangePassword = (onPasswordChange = jest.fn()) => {
  return render(
    <MemoryRouter>
      <ChangePassword onPasswordChange={onPasswordChange} />
    </MemoryRouter>
  )
}

describe('ChangePassword', () => {
  it('renders form title', () => {
    renderChangePassword()
    const titles = screen.getAllByText('Изменить пароль')
    expect(titles.length).toBe(2)
  })

  it('renders all 3 password fields', () => {
    renderChangePassword()
    expect(screen.getByText('Старый пароль')).toBeInTheDocument()
    expect(screen.getByText('Новый пароль')).toBeInTheDocument()
    expect(screen.getByText('Подтверждение нового пароля')).toBeInTheDocument()
  })

  it('renders submit button', () => {
    renderChangePassword()
    const buttons = screen.getAllByText('Изменить пароль')
    expect(buttons[1].tagName).toBe('BUTTON')
  })

  it('calls onPasswordChange on form submit', () => {
    const onPasswordChange = jest.fn()
    renderChangePassword(onPasswordChange)
    const form = document.querySelector('form')
    fireEvent.submit(form)
    expect(onPasswordChange).toHaveBeenCalled()
  })
})
