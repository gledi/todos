
fetch(PUB_KEY_URL)
    .then(resp => resp.json())
    .then(data => {
        console.log('Received data:', data);
        const stripe = Stripe(data.publishableKey);

        const btn = document.querySelector(".btn-buy");

        btn.addEventListener("click", event => {
            fetch(CHECKOUT_SESSION_URL)
                .then(resp => resp.json())
                .then(data => {
                    return stripe.redirectToCheckout({sessionId: data.sessionId})
                });
        });
    });