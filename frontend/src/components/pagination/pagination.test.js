import { render, screen, fireEvent } from '@testing-library/react'
import Pagination from './index'

describe('Pagination', () => {
  it('renders null when count is 0', () => {
    const { container } = render(<Pagination count={0} />)
    expect(container.innerHTML).toBe('')
  })

  it('renders null when pagesCount <= 1', () => {
    const { container } = render(<Pagination count={5} limit={6} />)
    expect(container.innerHTML).toBe('')
  })

  it('renders page numbers', () => {
    render(<Pagination count={12} limit={6} />)
    expect(screen.getByText('1')).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
  })

  it('calls onPageChange when page number is clicked', () => {
    const onPageChange = jest.fn()
    render(<Pagination count={18} limit={6} onPageChange={onPageChange} />)
    fireEvent.click(screen.getByText('2'))
    expect(onPageChange).toHaveBeenCalledWith(2)
  })

  it('renders arrow images', () => {
    const { container } = render(<Pagination count={18} limit={6} />)
    const images = container.querySelectorAll('img')
    expect(images.length).toBe(2)
  })
})
