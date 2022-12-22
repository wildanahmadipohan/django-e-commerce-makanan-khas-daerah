const updateButtons = document.querySelectorAll('.update-cart');
const deleteCartButtons = document.querySelectorAll('.delete-cart');
const deleteAllCart = document.querySelector('#delete-all-cart');

const hrefLogin = currentUrl === '/' ? '/login/' : `/login/?next=${currentUrl}`;

deleteCartButtons.forEach((button) => {
  button.addEventListener('click', () => {
    const productId = button.dataset.item;
    const action = button.dataset.action;
    const dataFrom = button.dataset.from;

    if (user === 'AnonymousUser') {
      location.href = hrefLogin;
    } else {
      updateCart(productId, action, dataFrom);
    }
  });
});

updateButtons.forEach((button, index) => {
  button.addEventListener('click', () => {
    const productId = button.dataset.product;
    const action = button.dataset.action;
    const dataFrom = button.dataset.from;

    if (user === 'AnonymousUser') {
      location.href = hrefLogin;
    } else {
      updateCart(productId, action, dataFrom);
    }
  });
});

const updateCart = (productId, action, dataFrom = null, qty = 1) => {
  const url = '/update_cart/';

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
    body: JSON.stringify({ productId, action, dataFrom, qty }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(`Data: ${data}`);
      location.reload();
    });
};

if (deleteAllCart) {
  deleteAllCart.addEventListener('click', () => {
    deleteCart();
  });
}

const deleteCart = () => {
  const url = '/delete_cart/';

  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    },
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(`Data: ${data}`);
      location.reload();
    });
};
