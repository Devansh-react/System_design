## Functional Requirements

- **User Management**
  - Users can search for restaurants based on their location.

- **Restaurant Management**
  - Restaurants have menus with various food items.

- **Cart System**
  - Users can add food items to a cart.

- **Ordering System**
  - Users can place orders for **delivery** or **pickup**.
  - Use a **Factory Pattern** to handle different order types (e.g., _Now_ vs. _Scheduled_).

- **Payment System**
  - Use a **Strategy Pattern** for processing payments:
    - UPI
    - Card
    - Net Banking

- **Notification System**
  - Send notifications once the order is placed successfully.

## Non-Functional Requirements

- **Code Maintainability**
  - Use design patterns for clean, scalable code:
    - **Singleton** for Managers
    - **Strategy** for Payments
    - **Factory** for Orders

- **Loose Coupling**
  - Use Manager classes as a single point of contact
  - Avoid tight coupling between objects  
    (e.g., `RestaurantManager` for handling Restaurants).

- **Scalability**
  - The design should allow for future extensions, such as:
    - Adding new payment methods
    - Adding new order types  
      without major code changes.
