
document.addEventListener('DOMContentLoaded', function () {
	// Get elements by ID
	const showRegisterLink = document.getElementById('show-register');
	const showLoginLink = document.getElementById('show-login');
	const loginForm = document.getElementById('login-form');
	const registerForm = document.getElementById('register-form');
	const offcanvasElement = document.getElementById('offcanvasRight');
	const offcanvasRegLog = document.getElementById('offcanvasRightLabel'); // Header label in offcanvas

	// Log initial elements to confirm they're detected correctly
	console.log('Initial Elements:', {
		showRegisterLink,
		showLoginLink,
		loginForm,
		registerForm,
		offcanvasElement,
		offcanvasRegLog
	});

	// Check if offcanvas element is defined and initialize it
	let offcanvas;
	if (offcanvasElement) {
		offcanvas = new bootstrap.Offcanvas(offcanvasElement);
		console.log("Bootstrap Offcanvas initialized successfully.");
	} else {
		console.error("Offcanvas element not found. Check the ID 'offcanvasRight'.");
	}

	// Confirm all required elements exist before adding event listeners
	if (showRegisterLink && showLoginLink && loginForm && registerForm && offcanvas && offcanvasRegLog) {
		console.log("All required elements are found.");

		// Toggle to show Register form and update header text
		showRegisterLink.addEventListener('click', function (e) {
			e.preventDefault();
			console.log('Switching to Register form'); // Log action
			loginForm.style.display = 'none';
			registerForm.style.display = 'block';
			offcanvasRegLog.textContent = 'Register';

			// Show the offcanvas
			offcanvas.show();
		});

		// Toggle to show Login form and update header text
		showLoginLink.addEventListener('click', function (e) {
			e.preventDefault();
			console.log('Switching to Login form'); // Log action
			loginForm.style.display = 'block';
			registerForm.style.display = 'none';
			offcanvasRegLog.textContent = 'Login';

			// Show the offcanvas
			offcanvas.show();
		});
	} else {
		console.error('One or more elements were not found. Check IDs and HTML structure.');
	}
});



// Function to handle form submissions
function handleFormSubmit(form, url, offcanvas) {
	if (!form) return;

	form.addEventListener('submit', async function (event) {
		event.preventDefault();
		console.log('Form submitted to URL:', url); // Debug log

		// Clear previous errors
		form.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
		form.querySelectorAll('.invalid-feedback').forEach(el => el.remove());
		const alertDiv = form.querySelector('.alert');
		if (alertDiv) alertDiv.remove();

		const submitButton = form.querySelector('button[type="submit"]');
		submitButton.disabled = true;

		try {
			const formData = new FormData(form);
			// Log form data for debugging
			for (let pair of formData.entries()) {
				console.log(pair[0] + ': ' + pair[1]);
			}

			const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
			console.log('CSRF Token present:', !!csrfToken); // Debug log

			if (!csrfToken) {
				throw new Error('CSRF token not found');
			}

			const response = await fetch(url, {
				method: 'POST',
				headers: {
					'X-CSRFToken': csrfToken,
					'X-Requested-With': 'XMLHttpRequest',
				},
				body: formData
			});

			console.log('Response status:', response.status); // Debug log
			// Log raw response for debugging
			const responseText = await response.text();
			console.log('Raw response:', responseText);

			let data;
			try {
				data = JSON.parse(responseText);
			} catch (e) {
				console.error('JSON parse error:', e);
				throw new Error('Invalid JSON response from server');
			}

			if (response.ok && data.success) {
				const successToast = new bootstrap.Toast(document.getElementById('successToast'));
				document.querySelector('#successToast .toast-body').textContent =
					data.message || 'Logged in successfully!';
				successToast.show();

				if (offcanvas) offcanvas.hide();

				setTimeout(() => {
					window.location.href = data.redirect_url || '/';
				}, 1000);
			} else {
				submitButton.disabled = false;

				if (data.errors) {
					Object.entries(data.errors).forEach(([field, errors]) => {
						const inputElement = form.querySelector(`[name="${field}"]`);
						if (inputElement) {
							inputElement.classList.add('is-invalid');
							const errorElement = document.createElement('div');
							errorElement.className = 'invalid-feedback';
							errorElement.textContent = Array.isArray(errors) ? errors[0] : errors;
							inputElement.parentNode.appendChild(errorElement);
						}
					});
				}

				// Display a general error message if it exists
				if (data.message) {
					const errorDiv = document.createElement('div');
					errorDiv.className = 'alert alert-danger mt-3';
					errorDiv.textContent = data.message;
					form.insertBefore(errorDiv, form.firstChild);
				}
			}
		} catch (error) {
			console.error('Detailed error:', error); // Detailed error logging
			submitButton.disabled = false;

			const errorDiv = document.createElement('div');
			errorDiv.className = 'alert alert-danger mt-3';
			errorDiv.textContent = 'An error occurred: ' + error.message;
			form.insertBefore(errorDiv, form.firstChild);
		}
	});
}


// Initialize form handlers
const loginFormElement = document.querySelector('#login-form form');
const registerFormElement = document.querySelector('#register-form form');

if (loginFormElement) {
	console.log('Login form found, action URL:', loginFormElement.action); // Debug log
	handleFormSubmit(loginFormElement, loginFormElement.action);
}
if (registerFormElement) {
	console.log('Register form found, action URL:', registerFormElement.action); // Debug log
	handleFormSubmit(registerFormElement, registerFormElement.action);
}



// DOM elements
const cartButton = document.getElementById('cart-button');
const cartOffCanvas = document.getElementById('cart-off-canvas');
const cartOverlay = document.getElementById('cart-overlay');
const cartItemsContainer = document.getElementById('cart-items-container');
const emptyCartMessage = document.getElementById('empty-cart-message');
const cartSubtotal = document.getElementById('cart-subtotal');
const closeCartBtn = document.getElementById('close-cart');
const checkoutBtn = document.getElementById('checkout-btn');

fetchCartDataOnPageLoad();

function formatPrice(price) {
	return `£${parseFloat(price).toFixed(2)}`;
}

// open close cart
function openCart() {
	cartOffCanvas.classList.add('show');
	cartOverlay.style.display = 'block';
	document.body.style.overflow = 'hidden';
	updateCart();
}

// Function to close cart
function closeCart() {
	cartOffCanvas.classList.remove('show');
	cartOverlay.style.display = 'none';
	document.body.style.overflow = '';
}

function updateCartTotalItems(totalItems) {
	const cartTotalItemsElement = document.getElementById('cart-total-items');
	cartTotalItemsElement.textContent = totalItems;  // Aktualizuje wyświetlaną liczbę produktów
}



// Function to fetch cart data when the page loads (added for initial load update)
async function fetchCartDataOnPageLoad() {
	try {
		const response = await fetch('/cart/get-items/'); // Fetch the current cart items
		const data = await response.json();

		// Calculate the total number of items in the cart and update the display
		const totalItems = data.items.reduce((total, item) => total + item.quantity, 0);
		updateCartTotalItems(totalItems);  // Update the number of items in the cart button
	} catch (error) {
		console.error('Error fetching cart data:', error);
	}
}


// Debounce function to prevent rapid firing of updates while the user is typing
function debounce(func, delay) {
	let timeout;
	return function (...args) {
		clearTimeout(timeout);
		timeout = setTimeout(() => func.apply(this, args), delay);
	};
}

// Function to render cart items in the DOM (dynamically)
function renderCartItems(items) {
	const cartItemsContainer = document.getElementById('cart-items-container');

	// Clear existing items
	cartItemsContainer.innerHTML = '';

	// If no items, show the empty cart message
	if (items.length === 0) {
		document.getElementById('empty-cart-message').style.display = 'block';
		document.getElementById('cart-subtotal').textContent = 'Subtotal: £0.00';
		return;
	} else {
		document.getElementById('empty-cart-message').style.display = 'none';
	}

	// Render each item
	items.forEach(item => {
		const itemElement = document.createElement('div');
		itemElement.classList.add('cart-item');
		itemElement.innerHTML = `
		<div class="cart-item-image">
			<img src="${item.image_url}" alt="${item.name}">
		</div>
		<div class="cart-item-details">
			<h4>${item.name}</h4>
			<p class="product-category">${item.category}</p>
			<p>£${item.price}</p>
			<div>
				<button class="remove-item" data-product-id="${item.product_id}">
			<i class="trash fa fa-trash"></i>
		</button>
			<div class="quantity-controls">
				<button class="decrease-quantity" data-product-id="${item.product_id}">-</button>
				<input type="number" class="quantity-input" value="${item.quantity}" min="1" data-product-id="${item.product_id}">
				<button class="increase-quantity" data-product-id="{{ item.product_id }}" data-stock="{{ item.stock }}">+</button>
			</div></div>
			<p class="subtotal">Subtotal: £${(item.price * item.quantity).toFixed(2)}</p>
		</div>
		<button class="remove-item" data-product-id="${item.product_id}">
			<i class="trash fa fa-trash"></i>
		</button>
	`;

		// Append item to cart
		cartItemsContainer.appendChild(itemElement);
	});
}



document.querySelectorAll('.quantity-input').forEach(input => {
	input.addEventListener('change', (e) => {
		const newQuantity = parseInt(e.target.value, 10);  // Parse the new quantity as an integer

		// Debugging: Log the quantity input change event
		console.log(`Quantity input change for product ID ${e.target.dataset.productId}: New Quantity: ${newQuantity}`);

		if (isNaN(newQuantity) || newQuantity <= 0) {
			// Invalid quantity, show an error and reset to 1
			e.target.value = 1;
			showToast('Quantity must be at least 1.', 'error');
		} else {
			// Update the quantity for this product in the cart
			updateCartQuantity(e.target.dataset.productId, newQuantity);
		}
	});
});

// Function to dynamically update the quantity of an item in the cart
async function updateCartQuantity(productId, newQuantity) {
	// Ensure newQuantity is valid
	if (newQuantity <= 0 || isNaN(newQuantity)) {
		console.log(`Invalid quantity for product ID ${productId}. Quantity: ${newQuantity}.`);
		showToast('Invalid quantity. Quantity must be at least 1.', 'error');
		return;
	}

	// Debugging: Log the quantity to be sent to the server
	console.log(`Sending request to update quantity of product ID ${productId} to ${newQuantity}.`);

	try {
		const response = await fetch(`/cart/update/${productId}/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCsrfToken(),  // Include CSRF token
			},
			body: JSON.stringify({ quantity: newQuantity })  // Send the new valid quantity
		});

		const data = await response.json();

		if (response.ok) {
			console.log(`Quantity update successful for product ID ${productId}:`, data);
			showToast('Quantity updated!');
			await updateCart();  // Refresh the cart
		} else {
			console.log('Error response from server:', response);
			showToast('Error updating quantity', 'error');
		}
	} catch (error) {
		console.error('Error updating cart quantity:', error);
		showToast('Error updating quantity', 'error');
	}
}


async function removeFromCart(productId) {
	console.log(`Sending request to remove product ID ${productId} from cart.`);

	try {
		const response = await fetch(`/cart/remove/${productId}/`, {
			method: 'POST',
			headers: {
				'X-CSRFToken': getCsrfToken(),
				'Content-Type': 'application/json'
			}
		});

		if (!response.ok) {
			console.error('Error response from server:', response);
			showToast('Error removing item from cart', 'error');
			return;
		}

		const data = await response.json();
		console.log(`Product ID ${productId} removed successfully:`, data);

		showToast('Item removed from cart');
		await updateCart();  // Refresh cart
	} catch (error) {
		console.error('Error removing from cart:', error);
		showToast('Error removing item from cart', 'error');
	}
}




// Function to update and re-render the cart (ensure it properly updates the quantity)
async function updateCart() {
	try {
		const response = await fetch('/cart/get-items/');
		const data = await response.json();

		// Debugging: Log the received cart data from the server
		console.log('Cart data received from server:', data);

		// Clear the current cart items
		cartItemsContainer.innerHTML = '';  // Make sure this clears the cart first

		if (data.items.length === 0) {
			cartSubtotal.textContent = 'Subtotal: £0.00';
			emptyCartMessage.style.display = 'block';
		} else {
			emptyCartMessage.style.display = 'none';

			// Re-render each item in the cart
			data.items.forEach(item => {
				const itemElement = document.createElement('div');
				itemElement.classList.add('cart-item');

				itemElement.innerHTML = `
				<div class="cart-item">
					<!-- Left: Product Image -->
					<div class="cart-item-image">
						<img src="${item.image_url}" alt="${item.name}">
					</div>

					<!-- Right: Product Details -->
					<div class="cart-item-details">
						<h4 class="product-name">${item.name}</h4>
						<p class="product-category">${item.category ? item.category : 'Unknown Category'}</p>
						<p class="product-price">£${item.price}</p>

						<!-- Quantity Controls -->
						<div class="cart-one-line">
							<!-- Remove Button -->
							<div>
								<button class="remove-item" data-product-id="${item.product_id}">
									<i class="trash fa fa-trash"></i>
								</button>
							</div>
							<div class="quantity-controls">
								<button class="decrease-quantity" data-product-id="${item.product_id}">-</button>
								<input type="number" class="quantity-input" value="${item.quantity}" min="1" data-product-id="${item.product_id}">
								<button class="increase-quantity" data-product-id="${item.product_id}" data-stock="${item.stock}">+</button>
							</div>
						</div>

						<!-- Subtotal -->
						<p class="subtotal">Subtotal: £${(item.price * item.quantity).toFixed(2)}</p>
					</div>
				</div>
			`;

				// Append item to the cart container
				cartItemsContainer.appendChild(itemElement);

				// Add event listeners for quantity change
				const quantityInput = itemElement.querySelector('.quantity-input');
				quantityInput.addEventListener('change', (e) => {
					const newQuantity = parseInt(e.target.value, 10);
					if (isNaN(newQuantity) || newQuantity <= 0) {
						e.target.value = 1;
						showToast('Quantity must be at least 1.', 'error');
					} else {
						updateCartQuantity(item.product_id, newQuantity);
					}
				});

				// Add event listeners for increasing quantity
				const increaseButton = itemElement.querySelector('.increase-quantity');
				increaseButton.addEventListener('click', () => {
					let currentQuantity = parseInt(quantityInput.value);
					const stock = parseInt(increaseButton.getAttribute('data-stock'));

					if (currentQuantity < stock) {
						currentQuantity++;
						quantityInput.value = currentQuantity;
						updateCartQuantity(item.product_id, currentQuantity);
					} else {
						console.log(`Cannot increase, stock limit reached: ${stock}`);
						showToast('Stock limit reached.', 'error');
					}
				});

				// Add event listeners for decreasing quantity
				const decreaseButton = itemElement.querySelector('.decrease-quantity');
				decreaseButton.addEventListener('click', () => {
					let currentQuantity = parseInt(quantityInput.value);
					if (currentQuantity > 1) {
						currentQuantity--;
						quantityInput.value = currentQuantity;
						updateCartQuantity(item.product_id, currentQuantity);
					}
				});

				// Add event listeners for removing an item
				const removeButton = itemElement.querySelector('.remove-item');
				removeButton.addEventListener('click', () => {
					removeFromCart(item.product_id);
				});
			});

			// Update the subtotal with the new total from the server response
			cartSubtotal.textContent = `Subtotal: £${data.total}`;
			const totalQuantity = data.items.reduce((sum, item) => sum + item.quantity, 0); // Calculate total quantity
			document.getElementById('cart-total-items').textContent = totalQuantity;  // Update cart icon
		}
	} catch (error) {
		console.error('Error updating cart:', error);
		showToast('Error updating cart', 'error');
	}
}

// Ensure updateCartQuantity is also called correctly with the right product and quantity
async function updateCartQuantity(productId, newQuantity) {
	console.log(`Sending request to update quantity of product ID ${productId} to ${newQuantity}`);

	try {
		const response = await fetch(`/cart/update/${productId}/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCsrfToken(),  // Ensure the CSRF token is sent
			},
			body: JSON.stringify({ quantity: newQuantity })  // Send the new valid quantity
		});

		const data = await response.json();
		if (response.ok) {
			console.log(`Quantity update successful for product ID ${productId}:`, data);
			showToast('Quantity updated!');
			await updateCart();  // Refresh the cart after updating quantity
		} else {
			console.log('Error response from server:', data);
			showToast('Error updating quantity', 'error');
		}
	} catch (error) {
		console.error('Error updating cart quantity:', error);
		showToast('Error updating quantity', 'error');
	}
}





function getCsrfToken() {
	return document.querySelector('[name=csrfmiddlewaretoken]').value;
}


// add to cart
async function addToCart(productId, quantity = 1, stock = 0) {
	if (quantity > stock) {
		showToast(`Only ${stock} items available in stock`, 'error');
		return;
	}

	try {
		const response = await fetch(`/cart/add/${productId}/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCsrfToken(),
			},
			body: JSON.stringify({ quantity: quantity })
		});

		if (response.ok) {
			const data = await response.json();
			showToast('Product added to cart successfully!');
			await updateCart();
			openCart();
		} else {
			const errorData = await response.json();
			showToast(errorData.message, 'error');
		}
	} catch (error) {
		console.error('Error adding to cart:', error);
		showToast('Error adding product to cart', 'error');
	}
}

// validation for "Add to Cart"
document.querySelectorAll('.add-to-cart').forEach(button => {
	button.addEventListener('click', (e) => {
		const productId = e.target.dataset.productId;
		const stock = e.target.dataset.stock;
		const quantity = 1;
		addToCart(productId, quantity, stock);
	});
});



// Function to show toast
function showToast(message, type = 'success') {
	const toast = new bootstrap.Toast(document.getElementById('successToast'));
	const toastBody = document.querySelector('.toast-body');
	toastBody.textContent = message;
	toast.show();
}

// Event Listeners
cartButton.addEventListener('click', openCart);
closeCartBtn.addEventListener('click', closeCart);
cartOverlay.addEventListener('click', closeCart);

// Init
document.addEventListener('DOMContentLoaded', () => {
	// Dodaj obsługę kliknięcia dla wszystkich przycisków "Add to Cart"
	document.querySelectorAll('.add-to-cart').forEach(button => {
		button.addEventListener('click', (e) => {
			const productId = e.target.dataset.productId;
			addToCart(productId);
		});
	});
});

async function logCartState() {
	try {
		const response = await fetch('/cart/get-items/');
		const data = await response.json();

		console.log("=== Aktualny stan koszyka ===");
		console.log(`Liczba przedmiotów: ${data.items.length}`);
		console.log(`Łączna wartość: ${data.total}`);


		data.items.forEach((item, index) => {
			console.log(`Produkt #${index + 1}:`);
			console.log(`  Nazwa: ${item.name}`);
			console.log(`  Ilość: ${item.quantity}`);
			console.log(`  Cena: ${item.price}`);
			console.log(`  Wartość całkowita: ${item.total}`);
		});

	} catch (error) {
		console.error('Błąd podczas pobierania stanu koszyka:', error);
	}
}


document.querySelectorAll('.decrease-quantity').forEach(button => {
	button.addEventListener('click', function () {
		const input = this.nextElementSibling;  // Target the input element next to the button
		let currentValue = parseInt(input.value);
		const productId = input.getAttribute('data-product-id');

		console.log(`Decrease button clicked for product ID ${productId}, current value: ${currentValue}`);

		if (currentValue > parseInt(input.min)) {
			input.value = currentValue - 1;
			console.log(`Decreased quantity to: ${input.value}`);
			// Update the cart on server-side
			updateCartQuantity(productId, parseInt(input.value));
		} else {
			console.log(`Cannot decrease further, current value is ${currentValue}`);
		}

		// Re-enable the increase button if the quantity is less than stock
		const increaseButton = this.parentElement.querySelector('.increase-quantity');
		increaseButton.disabled = false;
	});
});

document.querySelectorAll('.increase-quantity').forEach(button => {
	button.addEventListener('click', function () {
		const input = this.previousElementSibling;  // Target the input element previous to the button
		let currentValue = parseInt(input.value);
		const productId = input.getAttribute('data-product-id');
		const stock = this.getAttribute('data-stock');  // Assume we have the stock in a data attribute

		console.log(`Increase button clicked for product ID ${productId}, current value: ${currentValue}, stock available: ${stock}`);

		if (currentValue < stock) {
			input.value = currentValue + 1;  // Update the input field's value
			console.log(`Increased quantity to: ${input.value}`);

			// Call the server to update the cart
			updateCartQuantity(productId, parseInt(input.value));
		} else {
			console.log(`Cannot increase, stock limit reached: ${stock}`);
		}
	});
});

// Function to dynamically update the quantity of an item in the cart
async function updateCartQuantity(productId, newQuantity, stock) {
	// Ensure newQuantity is valid
	if (newQuantity <= 0 || isNaN(newQuantity)) {
		console.log(`Invalid quantity for product ID ${productId}. Quantity: ${newQuantity}.`);
		showToast('Invalid quantity. Quantity must be at least 1.', 'error');
		return;
	}

	if (newQuantity > stock) {
		console.log(`Cannot add more than ${stock} items for product ID ${productId}.`);
		showToast(`Only ${stock} items available in stock`, 'error');
		return;
	}

	// Debugging: Log the quantity to be sent to the server
	console.log(`Sending request to update quantity of product ID ${productId} to ${newQuantity}.`);

	try {
		const response = await fetch(`/cart/update/${productId}/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCsrfToken(),  // Include CSRF token
			},
			body: JSON.stringify({ quantity: newQuantity })  // Send the new valid quantity
		});

		const data = await response.json();

		if (response.ok) {
			console.log(`Quantity update successful for product ID ${productId}:`, data);
			showToast('Quantity updated!');

			// Update the subtotal and cart UI
			await updateCart();  // Refresh the cart and update subtotal
		} else {
			console.log('Error response from server:', response);
			showToast('Error updating quantity', 'error');
		}
	} catch (error) {
		console.error('Error updating cart quantity:', error);
		showToast('Error updating quantity', 'error');
	}
}

// Function to update subtotal
function updateSubtotal(totalPrice) {
	const subtotalElement = document.querySelector('#cart-subtotal span:last-child');

	console.log(`Updating subtotal to: £${totalPrice}`);
	subtotalElement.textContent = `£${parseFloat(totalPrice).toFixed(2)}`;
}

// Function to get token
function getCsrfToken() {
	return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Debug
document.getElementById('cart-button').addEventListener('click', function () {
	console.log('Cart button clicked, opening cart...');
	openCart();
});


document.addEventListener('DOMContentLoaded', function () {
	const checkoutBtn = document.querySelector('.btn-checkout'); // Upewnij się, że `checkoutBtn` odpowiada Twojemu przyciskowi Check Out.

	if (checkoutBtn) { // Sprawdź, czy przycisk istnieje
		checkoutBtn.addEventListener('click', async function (e) {
			e.preventDefault();  // Zapobiega domyślnemu działaniu
			console.log('Checkout button clicked. Starting to check cart contents.'); // Debug log

			try {
				// Sprawdź, czy są produkty w koszyku
				const response = await fetch('/cart/get-items/');
				console.log('Response from server received:', response); // Debug log
				const data = await response.json();

				console.log('Cart data:', data); // Debug log - wyświetlenie zawartości koszyka

				if (data.items && data.items.length === 0) {
					// Wyświetl komunikat, jeśli koszyk jest pusty
					console.log('Cart is empty. Showing toast notification.'); // Debug log
					showToast('Your cart is empty. Add items before proceeding to checkout.', 'error');
				} else {
					// Przejdź do checkout, jeśli koszyk zawiera produkty
					console.log('Cart has items. Redirecting to checkout page.'); // Debug log
					window.location.href = '/checkout/';
				}
			} catch (error) {
				console.error('Error checking cart contents:', error); // Detailed error log
				showToast('An error occurred. Please try again.', 'error');
			}
		});
	} else {
		console.error('Checkout button not found. Ensure it exists in the HTML with class="btn-checkout".'); // Debug log
	}
});



// Pobierz element paska nawigacji
const navbar = document.querySelector('.navbar');
let lastScrollY = window.scrollY;

window.addEventListener('scroll', () => {
    if (window.scrollY > lastScrollY) {
        // Jeśli przewijamy w dół, ukryj nawigację
        navbar.classList.add('hide');
    } else {
        // Jeśli przewijamy w górę, pokaż nawigację
        navbar.classList.remove('hide');
    }
    // Zaktualizuj wartość ostatniej pozycji przewijania
    lastScrollY = window.scrollY;
});
