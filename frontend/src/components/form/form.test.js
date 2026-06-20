import { render, screen, fireEvent } from '@testing-library/react'
import Form from './index'

describe('Form', () => {
  it('renders children', () => {
    render(<Form><button>Submit</button></Form>)
    expect(screen.getByText('Submit')).toBeInTheDocument()
  })

  it('calls onSubmit when form is submitted', () => {
    const handleSubmit = jest.fn(e => e.preventDefault())
    render(<Form onSubmit={handleSubmit}><button type='submit'>Submit</button></Form>)
    fireEvent.submit(screen.getByRole('button'))
    expect(handleSubmit).toHaveBeenCalledTimes(1)
  })

  it('applies custom className', () => {
    const { container } = render(<Form className='my-form'>Content</Form>)
    expect(container.querySelector('form').className).toContain('my-form')
  })

  it('renders as form element', () => {
    const { container } = render(<Form>Content</Form>)
    expect(container.querySelector('form')).toBeInTheDocument()
  })
})
