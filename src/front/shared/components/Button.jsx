import React from 'react'
import PropTypes from 'prop-types'

/**
 * Componente Button reutilizable
 * Uso:
 * <Button onClick={...} variant="primary">Aceptar</Button>
 */
const Button = ({ children, onClick, className = '', type = 'button' }) => {
  return (
    <button type={type} onClick={onClick} className={`btn ${className}`}>
      {children}
    </button>
  )
}

Button.propTypes = {
  children: PropTypes.node.isRequired,
  onClick: PropTypes.func,
  className: PropTypes.string,
  type: PropTypes.oneOf(['button', 'submit', 'reset'])
}

export default Button
