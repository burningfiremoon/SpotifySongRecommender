import React from 'react'

function Button(props) {
  return (
    <button onClick={props.onClick} role={props.role}>
        {props.children}
    </button>
  )
}

export default Button