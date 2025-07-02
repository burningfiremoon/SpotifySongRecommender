import React from 'react'
import Button from './Button'
import { useNavigate } from 'react-router-dom'

function ButtonLink({route, children, onClick}) {
    const navigate = useNavigate();
    const handleClick = (e) =>{
        if (onClick) onClick(e);
        navigate(route)
    };

  return (
    <Button onClick={handleClick} role='link'>
        {children}
    </Button>
  );
}

export default ButtonLink