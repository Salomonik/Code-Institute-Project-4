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

### Non-Functional Requirements

1. **Performance**:

   - Database queries should be optimized for efficient data retrieval to ensure fast loading times.
   - The application should minimize resource usage and optimize images and other assets for quicker page loading.

2. **Reliability**:

   - The application should have minimal downtime, with robust error handling and stability under normal usage conditions.

3. **Usability**:

   - The user interface should be intuitive and easy to navigate, guiding users seamlessly through browsing, adding items to the cart, and completing checkout.
   - Forms, buttons, and other interactive elements should provide clear, immediate feedback to the user.

4. **Security**:

   - Sensitive data, such as user passwords and payment information, should be securely encrypted.

5. **Accessibility**:

   - The application should adhere to accessibility guidelines, including providing descriptive alt text for images, ensuring readable font sizes, and maintaining high contrast between text and background colors for users with visual impairments.
   - Navigation should be keyboard-friendly, allowing users to access all content without a mouse.

   ### Out of Scope

The following features are not included in the current scope of the **Crafted Nature** project:


1. **Product Reviews and Ratings**:

   - The functionality for users to leave reviews or rate products is not available in this version. Future updates may include features for product reviews or ratings.

2. **Advanced Inventory Management**:

   - While basic stock levels are displayed, there is no in-depth inventory management system, such as tracking product variants or supplier information.

3. **Wishlist Functionality**:

   - The option for users to save products to a wishlist is not available in the current scope. Users can add products to their cart, but wishlist features are out of scope for this release.

4. **Multiple Shipping Options**:

   - The checkout process does not offer multiple shipping options or estimated delivery times. Shipping details are handled at a basic level, with one standard shipping method available.

5. **International Currency Support**:

   - The application currently supports only one currency and does not include multi-currency or localization options.

## User Experience

### User Stories

1. **As a visitor**, I want to be able to search for products by name so that I can easily find items of interest.

2. **As a visitor**, I want to view detailed information about a product, including its description, price, and stock availability, so that I can make informed purchasing decisions.

3. **As a visitor**, I want to be able to register for an account so that I can save my details for faster checkout and track my orders.

4. **As a registered user**, I want to be able to log in and log out of my account to keep my personal information secure.

5. **As a registered user**, I want to update my profile information, such as my email or password, to keep my account information up to date.

6. **As a registered user**, I want to add items to my shopping cart to keep track of products I intend to purchase.

7. **As a registered user**, I want to view and manage items in my cart, including adjusting quantities and removing items, before completing my purchase.

8. **As a registered user**, I want to securely proceed through checkout, entering my payment and shipping details with confidence.

9. **As a registered user**, I want to view my past orders and order status on my profile page, so that I can keep track of my purchases.

10. **As a registered user**, I want to be able to contact customer support if I have questions about my order or products.

## Returning User Experience

1. **Seamless Login**:

   - Returning users can easily log in to their accounts using their registered email and password to access their shopping and profile information.

2. **Profile Management**:

   - Returning users can view and update their account information.
   - Users can see a summary of their past orders.

3. **Cart Management**:

   - Returning users can view and manage items in their shopping cart, which remains saved in their profile for easy access during their next visit.
   - They can add new items to their cart or remove items they are no longer interested in purchasing.

4. **Order History**:

   - Returning users can view their past orders directly from their profile page, allowing them to track previous purchases and order statuses.

5. **Product Search and Discovery**:

   - Users can continue to search for products by name using the search functionality.


6. **Personalized Experience**:

   - Notifications or flash messages provide feedback to users for successful actions, such as adding a product to the cart, updating profile information, or completing a purchase.


## Design

### Color Scheme

The color scheme is designed to be visually engaging and comfortable for users, creating a cohesive and modern look throughout the application. The palette includes:

- **Primary Color**: `#333`
- **Secondary Color**: `#555`
- **Accent Color**: `#007acc`
- **Background Color**: `#f4f4f9`
- **Text Color**: `#222`

### Typography

The application’s font choices ensure readability and a clean, modern look:

- **Header Font**: `'Arial'`, sans-serif
- **Body Font**: `'Inter'`

### Layout

The layout is responsive, adjusting gracefully to different screen sizes for a seamless user experience. Key design principles include:

- **Max Width**: The primary content container is set to a maximum width of `1200px` to maintain readability and a structured layout on larger screens.
- **Padding and Margin**: Consistent padding and margin ensure balanced spacing between elements, creating a clean and organized look.
- **Box Shadow**: Subtle shadows provide depth to elements, distinguishing them from the background and enhancing the visual hierarchy.

## Wireframe

<details>
<summary>Wireframe</summary>

<details>

<summary>Main Page</summary>

![Main Page Wireframe](./media/documentation/main-big.png)

</details>

<details>
<summary>Category</summary>

![Product Category](./media/documentation/productsandcategory.png)

</details>

<details>
<summary>Profile</summary>

![Profile Wireframe](./media/documentation/profile-big.png)

</details>

</details>

## Screenshots

<details>
<summary>Screenshots</summary>

<details>

<summary>Main Page</summary>

![Main Page ](./media/documentation/screen-main.png)
![Main Page ](./media/documentation/screen-main-mobile.png)

</details>

<details>
<summary>Game Details</summary>

![Products](./media/product_images/documentation/screen-products.png)
![Products](./media/documentation/screen-products-mobile.png)

</details>

<details>
<summary>Profile</summary>

![Profile](./media/documentation/screen-profile.png)
![Profile](./media/documentation/screen-profile-mobile.png)

</details>

</details>

## Features

### Homepage

- **Product Search**: Users can search for products by name or category using the search bar on the homepage.
- **User Authentication**: Users can log in or register directly from the navigation bar on the homepage for quick access to their accounts.

### User Authentication

- **User Registration**: New users can create an account by providing a username, email, and password, enabling them to save profile and order information.
- **User Login**: Registered users can log in to their accounts securely using their email and password.
- **User Logout**: Logged-in users have the option to securely log out from their accounts.

### User Profile

- **Profile Page**: Users have access to a personal profile page where they can view and update their account information.
- **Order History**: Users can view a list of their past orders, with details such as order dates and statuses to help them track purchases.

### Product Details

- **Detailed Product Information**: Clicking on a product provides detailed information, including a description, price, available stock, and high-quality images.
- **Add to Cart**: Users can add products to their shopping cart directly from the product page.

### Shopping Cart

- **View Cart**: Users can view all items in their shopping cart, including item quantities and subtotal costs, with options to adjust quantities or remove items.
- **Cart Summary**: The cart displays the total cost of all items, allowing users to review their order before proceeding to checkout.

### Flash Messages

- **Feedback Messages**: Users receive feedback messages for important actions, such as adding items to the cart, successful login/logout, and completed purchases, to confirm actions.

### Responsive Design

- **Mobile-Friendly**: The application is fully responsive, ensuring a consistent and optimized experience across desktops, tablets, and mobile devices.

### Checkout and Payment

- **Secure Checkout**: Users proceed through a secure checkout where they can enter shipping and payment details.
- **Stripe Integration**: Stripe is integrated for secure and streamlined payment processing, ensuring user data security and payment reliability.


### Security

- **CSRF Protection**: The application employs CSRF tokens to guard against Cross-Site Request Forgery attacks, ensuring secure form submissions.
- **Password Hashing**: User passwords are securely hashed, with additional layers of security applied to protect sensitive information.

### Additional Features

- **Product Filtering and Sorting**: Users can filter products by category and sort items by price or popularity to streamline their shopping experience.

## Implementation Details

### Technology Stack

- **Frontend**: HTML, CSS (Bootstrap), JavaScript
- **Backend**: Python, Django
- **Database**: PostgreSQL
- **APIs**: Stripe API for payment processing
- **Hosting**: Heroku

### Environment Configuration

The application utilizes environment variables to securely manage configuration settings. These variables are stored in a `.env` file and include:

- `DJANGO_SECRET_KEY`: A secret key used for Django session management and CSRF protection.
- `DATABASE_URL`: The URL for connecting to the PostgreSQL database.
- `DEBUG`: A flag to enable/disable debug mode in the development environment.
- `STRIPE_SECRET_KEY`: The secret key for processing payments through the Stripe API.
- `STRIPE_PUBLISHABLE_KEY`: The publishable key used for the frontend Stripe integration.
- `ALLOWED_HOSTS`: Hosts allowed to access the application in production.

### Database Models

The application uses Django ORM to define the following database models:

- **User**: Stores user account information, including username, email, and password hash.
- **Product**: Stores information about each product, including name, description, price, stock, category, and images.
- **Category**: Organizes products into categories, aiding in filtering and browsing.
- **Order**: Stores order information for each transaction, including user, order date, total amount, and status.
- **OrderItem**: Links products to orders, storing quantity and price per item.
- **Cart**: Tracks items added by the user before checkout, containing a list of `CartItem` entries.
- **CartItem**: Associates products with the shopping cart, including quantity and date added.

![database Wireframe](./media/documentation/graphviz.svg)

### Table Relationships

1. **User - Order**:

   - **Relationship**: One-to-Many
   - **Description**: A user can have many orders associated with their account. The `user_id` foreign key in the `order` table references the `id` in the `user` table.
   - **Diagram**: `USER ||--o{ ORDER : places`

2. **Order - OrderItem**:

   - **Relationship**: One-to-Many
   - **Description**: Each order can have multiple items. The `order_id` foreign key in the `order_item` table references the `id` in the `order` table.
   - **Diagram**: `ORDER ||--o{ ORDER_ITEM : contains`

3. **Product - OrderItem**:

   - **Relationship**: One-to-Many
   - **Description**: Each product can be included in many order items. The `product_id` foreign key in the `order_item` table references the `id` in the `product` table.
   - **Diagram**: `PRODUCT ||--o{ ORDER_ITEM : part of`

4. **User - Cart**:

   - **Relationship**: One-to-One
   - **Description**: Each user has one cart associated with their account. The `user_id` foreign key in the `cart` table references the `id` in the `user` table.
   - **Diagram**: `USER ||--o| CART : owns`

5. **Cart - CartItem**:

   - **Relationship**: One-to-Many
   - **Description**: A cart can have multiple items in it. The `cart_id` foreign key in the `cart_item` table references the `id` in the `cart` table.
   - **Diagram**: `CART ||--o{ CART_ITEM : holds`

6. **Product - CartItem**:

   - **Relationship**: Many-to-One
   - **Description**: A product can be added to many carts as separate cart items. The `product_id` foreign key in the `cart_item` table references the `id` in the `product` table.
   - **Diagram**: `PRODUCT ||--o{ CART_ITEM : included in`


## Manual Testing

### 1. Home Page
- **Objective**: Verify that the home page loads correctly and displays featured products.
- **Steps**:
  1. Navigate to the home page.
  2. Check if featured products are displayed.
  3. Verify the accuracy of images, titles, and descriptions for each product.
- **Expected Result**: The home page loads without errors, and featured products are displayed correctly.

### 2. User Registration
- **Objective**: Ensure a new user can register successfully.
- **Steps**:
  1. Go to the registration page.
  2. Fill in the registration form with valid data.
  3. Submit the form.
  4. Check that a success message appears, and the user is redirected to the login page.
- **Expected Result**: The user registers successfully, with a success message displayed.

### 3. User Login
- **Objective**: Ensure registered users can log in without issues.
- **Steps**:
  1. Go to the login page.
  2. Enter valid credentials.
  3. Submit the form.
  4. Check that the user is redirected to the home page and that user-specific options (e.g., “My Account,” “Favorites”) are visible.
- **Expected Result**: Successful login with user-specific options displayed.

### 4. Checkout Process
- **Objective**: Confirm the checkout process is functional, including payment and order confirmation.
- **Steps**:
  1. Add products to the cart.
  2. Go to the checkout page.
  3. Fill in payment and shipping details.
  4. Confirm the order.
- **Expected Result**: The order is processed successfully, with a confirmation message displayed and payment recorded.

## Automated Tests

The **checkout** app includes automated tests covering key functionalities of the checkout process, such as payment handling, order confirmation, and validation of customer information. These tests ensure the reliability and security of the checkout flow.


## Browser Testing

### 1. Cross-browser Testing
- **Objective**: Ensure the application works correctly across different browsers.
- **Steps**:
  1. Test the application in different browsers (Chrome, Firefox, Safari, Edge).
  2. Verify that all features work as expected.
- **Expected Result**: The application works correctly across all tested browsers.

### 2. Responsive Design Testing
- **Objective**: Verify that the application is responsive and works well on different screen sizes.
- **Steps**:
  1. Test the application on different devices (desktop, tablet, mobile).
  2. Verify that the layout adjusts correctly to different screen sizes.
- **Expected Result**: The application is responsive and works well on different devices.

## Bug Tracking and Fixes

### Overview

During the development and testing phases, the application was rigorously tested to identify and resolve any potential bugs. The following outlines the process used for tracking and fixing bugs.

### Bug Tracking Process

1. **Identification**: Bugs were identified through manual testing, automated testing, and user feedback.
2. **Logging**: Identified bugs were logged.
5. **Resolution**: investigated and fixed the bugs.
6. **Verification**: Fixed bugs were tested to ensure they were resolved and did not introduce new issues.

### Fixed Bugs

- **User Registration Issues**: Fixed an issue where users could register with an existing email address, causing database conflicts.
- **Login Problems**: Resolved an issue where users were unable to log in due to incorrect password hash comparison.

### Known Issues

- **Cart issue**: There is an unresolved issue where "Your cart is empty." doesnt show after item is deleted from cart due to JS rendering"

## Technologies Used

### Frontend Technologies

- **HTML5**: Markup language used for structuring content on the web.
- **CSS3**: Stylesheet language used for describing the presentation of web pages.
- **JavaScript**: Programming language used to create dynamic and interactive elements on web pages.
- **Bootstrap CSS**: A modern responsive front-end framework based on Material Design.
- **Font Awesome**: A popular icon toolkit for adding scalable vector icons to the UI.

### Backend Technologies

- **Python**: Programming language used for backend development.
- **Django**: A high-level Python web framework that enables rapid development of secure and maintainable websites.
- **Django ORM**: Provides an Object-Relational Mapping (ORM) layer for interacting with the database.
- **Gunicorn**: A Python WSGI HTTP server for deploying the web application.

### Database

- **PostgreSQL**: An advanced, open-source relational database management system used to store and manage the application's data.

### APIs and Libraries

- **Stripe API**: Used to handle secure payment processing.
- **Requests**: A simple HTTP library for Python used to make API requests.
- **Jinja2**: A templating engine for Python used to render HTML templates in Django.
- **Font Awesome**: Library used for adding icons to the application for improved UI/UX.

### Deployment

- **Heroku**: A cloud platform used to deploy, manage, and scale the application.
- **Git**: Version control system used for tracking changes in the source code.

### Other Tools

- **Django Admin**: Built-in admin interface for managing application data and users.


# Pre-Deployment Checklist

Before deploying the application, ensure that the following tasks are completed:

### Code Quality and Testing

- [x] **Code Review**: Ensure all code has been reviewed and adheres to the project's coding standards.

### Application Configuration

- [x] **Environment Variables**: Ensure all necessary environment variables are set, including `DJANGO_SETTINGS_MODULE`, `DATABASE_URL`, `SECRET_KEY`, `STRIPE_PUBLIC_KEY`, and `STRIPE_SECRET_KEY`.
- [x] **Configuration Files**: Verify that configuration files such as `settings.py` and `.env` are correctly set up for the production environment.
- [x] **Database Migrations**: Run database migrations to ensure the production database schema is up-to-date.


### Deployment Steps

1. **Set Up Heroku CLI**: Make sure you have the Heroku CLI installed on your local machine. If not, you can install it from [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

2. **Log In to Heroku**:
    ```sh
    heroku login
    ```

3. **Create a New Heroku Application**:
    ```sh
    heroku create your-app-name
    ```

4. **Set Environment Variables** on Heroku:
    ```sh
    heroku config:set SECRET_KEY=your_secret_key
    heroku config:set DATABASE_URL=your_database_url
    heroku config:set STRIPE_PUBLIC_KEY=your_stripe_public_key
    heroku config:set STRIPE_SECRET_KEY=your_stripe_secret_key
    ```

5. **Push Code to Heroku**:
    ```sh
    git push heroku main
    ```

6. **Run Database Migrations**:
    ```sh
    heroku run python manage.py migrate
    ```

8. **Collect Static Files**:
    ```sh
    heroku run python manage.py collectstatic --noinput
    ```

9. **Open the Application**:
    ```sh
    heroku open
    ```

### Post-Deployment

1. **Monitor Logs**: Use Heroku logs to monitor the application for any errors or issues.
    ```sh
    heroku logs --tail
    ```

2. **Testing**: Perform final testing in the production environment to ensure everything is working as expected.

## Version Control

### GitHub Repository

The project's source code is hosted on GitHub, providing version control and collaboration features. The repository contains all code, documentation, and configuration files necessary to run the application.

### Repository Structure

- **`main` branch**: Contains the stable version of the application. All new features and bug fixes are merged into this branch after thorough testing.

### Version Control Practices

1. **Commits**: Commits are made frequently with clear, concise messages describing changes made, aiding in tracking the project’s history and purpose of each change.


## Reflections

### Achievements

Developing this project has led to several key achievements:

1. **Feature Implementation**: Successfully implemented core features such as user authentication, product management, and order processing.
2. **Integration with Stripe API**: Seamlessly integrated with the Stripe API to handle secure payment processing, enhancing the user experience.
3. **Responsive Design**: Ensured full responsiveness, providing an optimal viewing experience across devices.
4. **User Profiles and Comments**: Implemented user profiles and review features, fostering user engagement and interaction.
5. **Database Management**: Efficiently managed database migrations and relationships using Django ORM, ensuring data integrity and ease of development.

### Challenges

1. **Database Migrations**: Managing database migrations and ensuring data consistency during schema updates.
2. **User Authentication**: Implementing secure user authentication.
3. **Bug Fixes**: Debugging and resolving issues, such as the inconsistent display of flash messages after page reloads.

### Learning Experience

This project has provided valuable insights into various aspects of web development:

2. **Database Management**: Learned about designing and managing relational databases, creating efficient table relationships, and handling migrations.
3. **User Experience (UX)**: Emphasized the importance of UX in application design, resulting in a more intuitive and user-friendly interface.
4. **Version Control**: Enhanced skills in version control using Git and GitHub.
5. **Deployment**: Acquired knowledge in deploying Django applications to Heroku, managing environment variables, and ensuring smooth production deployment.

### Future Enhancements

1. **Bug Fixes and Improvements**: Continue identifying and fixing bugs, such as the flash message issue, and making continuous improvements based on user feedback.

### Conclusion

This project has been a rewarding experience, contributing to both personal and professional growth as a developer. The lessons learned and achievements gained will serve as a solid foundation for future projects.

---

## Acknowledgments

Thank you to the Slack and Reddit web development communities for their support and insights.





