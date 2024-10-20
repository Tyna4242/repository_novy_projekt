# Online obchod

## Stručný popis systému

## Project Tasks

### Admin Functionalities

- [ ] **Add Category**:
  - [ ] Category name
  - [ ] Parent ID (for category tree)
  - [ ] Implement category search
  - [ ] Allow dragging categories to change position
  
- [ ] **Category Tree Overview**:
  - [ ] Display category tree structure
  - [ ] Include drag-and-drop functionality for reordering
  
- [ ] **Add Product**:
  - [ ] Product name
  - [ ] Description
  - [ ] Picture URL
  - [ ] Availability
  - [ ] Price
  - [ ] Product type (dropdown)
  - [ ] Category selection (dropdown)
  - [ ] Author selection (dropdown)

- [ ] **Product List and Edit**:
  - [ ] Display a list of all products with details
  - [ ] Implement a button to edit product details
  - [ ] Add product search functionality

---

### User Functionalities

- [ ] **User Registration**:
  - [ ] Form with field validation (email, password, city, address)
  
- [ ] **User Login**:
  - [ ] Implement user login functionality
  - [ ] Provide option for user logout

- [ ] **Product List**:
  - [ ] Display products as a list or grid
  - [ ] Enable product search functionality
  - [ ] Implement AJAX product search
  
- [ ] **Pagination**:
  - [ ] Display products in a table with pagination
  - [ ] Enable sorting of products in the table

- [ ] **Cart Management**:
  - [ ] Display products added to the cart
  - [ ] Enable users to order products from the cart
  - [ ] Redirect to static "Thank You" page after order submission
  - [ ] Reduce product availability after ordering
  
---

### Weather Widget

- [ ] **Weather Widget**:
  - [ ] Display weather based on the city of the currently logged-in user

---

### Additional Functionalities

- [ ] **User Account Editing**:
  - [ ] Allow users to edit their account data (address, email, etc.)

- [ ] **Order Overview**:
  - [ ] Implement order overview for users
  - [ ] Allow admins to view all user orders

- [ ] **Add Author in Admin Panel**:
  - [ ] Allow admin to assign authors to products

---

### General Requirements

- [ ] **Security**:
  - [ ] Use `django.contrib.auth` to secure access to the application
  - [ ] Ensure proper validation for data entered by users

- [ ] **Aesthetic Presentation**:
  - [ ] Ensure the website is aesthetically pleasing and user-friendly

- [ ] **Pre-validation of User Data**:
  - [ ] Validate all data collected from users
