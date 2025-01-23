# Cafe Booking

## Overview

Cafe Booking is a Django-based application for managing cafe orders. It includes features for creating, listing, updating, and deleting orders, as well as filtering and pagination.

## Features

- Create, list, update, and delete orders
- Filter orders by table number and status
- Pagination for order lists
- Detailed order views
- Admin interface for managing orders

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/cafe-booking.git
    cd cafe-booking
    ```

2. Create and activate a virtual environment:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:

    ```sh
    pip install -r requirements.txt
    ```

4. Apply migrations:

    ```sh
    python manage.py migrate
    ```

5. Create a superuser:

    ```sh
    python manage.py createsuperuser
    ```

6. Run the development server:

    ```sh
    python manage.py runserver
    ```

## Usage

### API Endpoints

- List Orders: `GET /api/orders/`
- Create Order: `POST /api/orders/`
- Retrieve Order: `GET /api/orders/{id}/`
- Update Order: `PUT /api/orders/{id}/`
- Delete Order: `DELETE /api/orders/{id}/`

### Admin Interface

Access the admin interface at `/admin/` to manage orders.

### Filtering and Pagination

Use query parameters to filter and paginate orders:

- `table_number`: Filter by table number
- `status`: Filter by status (`pending`, `ready`, `paid`)
- `page`: Specify the page number
- `page_size`: Specify the number of items per page

## Documentation

### Typing Annotations

The project uses typing annotations for functions and variables to improve code readability and maintainability. For example:

```python
from typing import List

def get_order_items(order_id: int) -> List[dict]:
    # Function implementation
    pass
```

### Function and Code Block Descriptions

Each function and major code block includes detailed descriptions to explain its purpose and functionality. For example:

```python
def create_order(data: dict) -> Order:
    """
    Create a new order with the given data.

    Args:
        data (dict): The data for the new order.

    Returns:
        Order: The created order instance.
    """
    # Function implementation
    pass
```

## Running Tests

To run the tests, use the following command:

```sh
python manage.py test
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
