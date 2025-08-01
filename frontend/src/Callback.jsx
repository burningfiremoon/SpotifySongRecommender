import React, { useEffect, useState } from "react";

const Callback = () => {
    const [message, setMessage] = useState('Loading...');
    useEffect(() => {
        const code = new URLSearchParams(window.location.search).get('code')

        if (!code && !sessionStorage.getItem('spotify_access_token')) {
            setMessage("No Code in URL. Authorization failed.");
            return;
        }

         if(sessionStorage.getItem('spotify_access_token')) {
            setMessage("Already logged In")
            return;
        }

        fetch('http://localhost:5000/api/exchange_token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        })
            .then(res => res.json())
            .then(data => {
                if (data.access_token) {
                    sessionStorage.setItem('spotify_access_token', data.access_token);
                    setMessage('Logged In! Token Stored.');

                    window.history.replaceState(null, "", "/");
                } else {
                    console.error(data);
                    setMessage('Failed to exchange token.');
                }
            })
            .catch(err => {
                console.error(err);
                setMessage('Error during token exchange.')
            });
    },[]);

    return(
        <h2>{message}</h2>
    );
}

export default Callback