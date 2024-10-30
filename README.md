![Main Page](./media/documentation/mainpage.png)<br>

### The live link can be found here - [Crafted Nature](https://milestone-project-4-jp-01c67f637dac.herokuapp.com/)


# Crafted Nature

## Description

**Crafted Nature** is an e-commerce website dedicated to providing users with a seamless shopping experience for unique, handcrafted products. The website allows users to explore a diverse range of products, organized into various categories, and provides detailed information on each item, including descriptions, prices, and stock availability.

The site utilizes a **PostgreSQL database** to manage product data, user accounts, orders, and interactions. Key functionalities include browsing and searching for products, viewing detailed product information, managing user profiles, and securely processing payments through Stripe integration.

The application is built using **Django** as the backend framework, with **Django ORM** to manage database interactions. The frontend is styled with responsive CSS to ensure a seamless experience across various devices. The site is deployed on Heroku, allowing for scalability and easy access.

The main objective of Crafted Nature is to provide users with a smooth and enjoyable shopping experience, offering high-quality, handcrafted items while making the purchasing process as convenient and secure as possible.

## Site Owner Goals

As the owner of **Crafted Nature**, the primary goals of the site are:

1. **Provide a Wide Range of Products**: Offer a diverse selection of handcrafted products across various categories, ensuring that users can find unique and high-quality items. Each product listing includes detailed information to help users make informed purchasing decisions.

2. **Enhance User Engagement**: Create a user-friendly and interactive platform that encourages users to browse, discover, and engage with products. This includes features such as product browsing, detailed product pages.

3. **User Management and Personalization**: Allow users to create accounts, log in, and manage their profiles. Enable users to personalize their experience by adding products to their shopping cart, viewing their order history, and managing account information.

4. **Smooth Checkout Process**: Implement a secure and straightforward checkout process, including integration with Stripe for payment processing. This ensures a reliable and convenient purchasing experience for customers.

5. **Responsive Design**: Ensure the site is accessible and easy to use on both desktop and mobile devices, providing a seamless experience across all screen sizes.

6. **Scalability and Performance**: Utilize scalable technologies such as Heroku for deployment and PostgreSQL for data storage to handle a growing number of users and ensure the site performs well under load.

7. **Security**: Implement robust security measures to protect user data, including secure authentication, payment data encryption, and CSRF protection to ensure a safe shopping environment.

## Development Life Cycle

### Project Planning

During the project planning phase, the following steps were undertaken to ensure a structured and well-organized development process for **Crafted Nature**:

1. **Requirements Gathering**:

   - Identified the primary goals and objectives of the project, including providing a seamless shopping experience and secure payment processing.
   - Defined the core features and functionalities required for the application, such as product browsing, user authentication, shopping cart management, and order processing.

2. **Research and Analysis**:

   - Conducted research on e-commerce platforms to understand best practices for user experience, security, and product management.
   - Analyzed other handcrafted product sites to identify unique features and potential areas for improvement in user engagement and functionality.

3. **Technical Planning**:

   - Chose the Django framework for backend development due to its robust features for building e-commerce applications.
   - Selected PostgreSQL as the database system for its reliability and compatibility with Heroku for deployment.
   - Decided on using custom responsive CSS for frontend design to ensure a smooth and consistent user experience across all devices.

4. **Wireframing and Prototyping**:

   - Created wireframes and prototypes to visualize the layout and user flow of the website, including the product pages, shopping cart, and checkout process.
   - Collected feedback on the prototypes to make necessary adjustments before development commenced.

5. **Task Breakdown and Timeline**:

   - Broke down the project into manageable tasks and milestones, focusing on areas like database setup, frontend design, payment integration, and security.
   - Established a timeline for development, setting realistic deadlines for each phase to ensure steady progress.

6. **Setting Up the Development Environment**:

   - Configured version control using Git and set up a repository on GitHub for collaborative development and tracking changes.
   - Established a local development environment with necessary tools and libraries, including virtual environments, required Python packages, and PostgreSQL configuration.

### Content Requirements

_Pages and Features_

1. **Home Page**:

   - Introduction to the site and its main offerings.
   - Search bar for users to search for products by name or category.

2. **Product Details Page**:

   - Detailed information about a specific product, including:
     - Name
     - Description
     - Price
     - Stock availability
     - Product images
   - Option to add the product to the shopping cart.

3. **User Profile Page**:

   - Display user information.
   - List of past orders with order details and statuses.
   - Option to update user profile information.

4. **Shopping Cart Page**:

   - Overview of items added to the cart, with options to:
     - Adjust item quantities
     - Remove items from the cart
     - View subtotal and total prices
   - Proceed to checkout button.

5. **Checkout Page**:

   - Form for users to enter shipping and payment information.
   - Summary of items in the cart and total cost.
   - Stripe payment integration to securely handle payments.

6. **Login Page**:

   - Form for users to log in with their email and password.

7. **Registration Page**:

   - Form for new users to sign up with their username, email, and password.
   - Validation for unique usernames and emails.


### Development Life Cycle

## Development

1. **Setting Up Django Application**:
   - Initialized a Django application.
   - Configured the app with necessary settings, including database configuration for PostgreSQL and CSRF protection for secure transactions.

2. **Defining Database Models**:
   - Created Django models for `User`, `Product`, `Category`, `Cart`, `Order`, `OrderItem`, and `CartItem` to manage product listings, user shopping cart, and order processing.
   - Defined relationships between models, such as foreign keys for user accounts and products.

3. **Payment Integration**:
   - Integrated with Stripe API to securely handle payment processing during checkout.
   - Implemented functionality to validate payments and update order statuses after successful transactions.

4. **Frontend Development**:
   - Created HTML templates using Django's templating engine.
   - Styled the frontend with custom CSS to ensure responsive design across different devices, providing a smooth shopping experience for users.


## Requirements

### Functional Requirements

1. **User Authentication**:

   - Users should be able to register, log in, and log out.
   - Registered users should have a unique username and email.
   - Passwords should be hashed and stored securely to ensure user data protection.

2. **User Profile**:

   - Users should be able to view and update their profile information, including changing details like email and password.
   - Profiles should display past orders and order statuses to help users keep track of their purchases.
   - Users should have access to their profile where they can manage account information and view order history.

3. **Product Search and Display**:

   - Users should be able to search for products by name.
   - The application should display product details, including name, description, price, and stock status.
   - Product data should be organized into categories, making browsing and searching intuitive for users.

4. **Shopping Cart Management**:

   - Users should be able to add products to their shopping cart.
   - Users should be able to view and manage items in their cart, including adjusting quantities or removing items.
   - The cart should display the total cost and allow users to proceed to checkout.

5. **Checkout and Payment**:

   - Users should be able to securely enter shipping and payment information during checkout.
   - Integration with Stripe API should enable secure payment processing.
   - After successful payment, users should receive a confirmation, and order details should be saved in the database.

6. **Main Page**:

   - The main page should direct users to the product catalog.
   - Users should have immediate access to browse all available products.
   - A prominent link or button should guide users to explore product categories or search for specific items.


7. **Product Details Page**:

   - The product details page should display all relevant information about the product.
   - Users should have the option to add the product to their cart directly from this page.
   - If a product is out of stock, the page should clearly indicate this status.

8. **Responsive Design**:

   - The application should be responsive, ensuring optimal viewing on both desktop and mobile devices.
   - The layout should adapt to different screen sizes to provide a seamless shopping experience across devices.

9. **Error Handling**:

   - The application should handle errors gracefully, providing users with helpful feedback if something goes wrong.
   - User-friendly error messages should be displayed for issues such as invalid inputs, out-of-stock items, or failed payment attempts.

10. **Security**:

    - CSRF protection should be implemented to prevent cross-site request forgery.
    - All user input should be validated to prevent SQL injection, XSS, and other security vulnerabilities.
    - Passwords and sensitive user data should be securely hashed and encrypted where necessary.
