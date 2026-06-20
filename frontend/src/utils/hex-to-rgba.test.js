import hexToRgba from './hex-to-rgba'

describe('hexToRgba', () => {
  it('converts hex to rgba with default alpha', () => {
    expect(hexToRgba('#8775D2')).toBe('rgba(135, 117, 210, 1')
  })

  it('converts hex to rgba with custom alpha', () => {
    expect(hexToRgba('#8775D2', 0.1)).toBe('rgba(135, 117, 210, 0.1')
  })

  it('converts hex without hash', () => {
    expect(hexToRgba('FF0000')).toBe('rgba(255, 0, 0, 1')
  })

  it('returns null for invalid hex', () => {
    expect(hexToRgba('xyz')).toBeNull()
  })

  it('handles black color', () => {
    expect(hexToRgba('#000000')).toBe('rgba(0, 0, 0, 1')
  })

  it('handles white color', () => {
    expect(hexToRgba('#FFFFFF')).toBe('rgba(255, 255, 255, 1')
  })

  it('handles lowercase hex', () => {
    expect(hexToRgba('#ffffff')).toBe('rgba(255, 255, 255, 1')
  })
})
