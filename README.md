# RecipeHub

A full-stack recipe sharing platform built with Django and Django REST Framework. RecipeHub enables users to discover, create, manage, rate, comment on, and save recipes through a responsive web application and RESTful APIs.

The project demonstrates authentication, authorization, CRUD operations, media uploads, search, filtering, REST API development, and modern Django best practices.

---

## Overview

RecipeHub is designed as a community-driven platform where users can:

- Create and publish recipes
- Browse recipes by category
- Search and filter recipes
- Rate and review recipes
- Save favourite recipes
- Manage their own content
- Access recipe data through REST APIs

---

## Key Features

### Authentication & Authorization

- User Registration
- Secure Login & Logout
- Session Authentication
- JWT Authentication (REST API)
- Protected Routes
- Role-based Ownership (Users can edit/delete only their own recipes)

### Recipe Management

- Create Recipes
- Edit Recipes
- Delete Recipes
- Upload Recipe Images
- Category Management
- Difficulty Levels
- Preparation Time
- Cooking Time
- Servings Information
- Featured Recipes

### Community Features

- Recipe Rating System
- Comment System
- Save Favourite Recipes
- Recently Added Recipes
- Top Rated Recipes
- Related Recipes

### Search & Filtering

- Search by Recipe Title
- Search by Description
- Search by Ingredients
- Filter by Category
- Filter by Difficulty
- Sort by Latest
- Sort by Rating
- Sort by Cooking Time

### User Dashboard

- My Recipes
- Saved Recipes
- Manage Personal Recipes

### REST API

- Recipe CRUD API
- JWT Authentication
- Search API
- Ordering API
- Pagination
- Browsable API

---

## Technology Stack

| Category | Technologies |
|----------|--------------|
| Backend | Python, Django |
| API | Django REST Framework |
| Authentication | Django Authentication, JWT |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| UI | Bootstrap |
| Image Processing | Pillow |
| Version Control | Git & GitHub |

---

## Project Structure

```
RecipeHub_Django
│
├── recipehub/
│
├── recipes/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── api_urls.py
│   ├── api_views.py
│   ├── forms.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── media/
├── static/
├── templates/
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Database Models

- User
- Recipe
- Rating
- Comment
- SavedRecipe

---

## REST API

### Authentication

```
POST    /api/token/
POST    /api/token/refresh/
```

### Recipes

```
GET     /api/recipes/
GET     /api/recipes/{id}/
POST    /api/recipes/
PUT     /api/recipes/{id}/
PATCH   /api/recipes/{id}/
DELETE  /api/recipes/{id}/
```

### Search

```
GET /api/recipes/?search=pasta
```

### Ordering

```
GET /api/recipes/?ordering=-created_at
GET /api/recipes/?ordering=prep_time
GET /api/recipes/?ordering=cook_time
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Harshali-14/RecipeHub_Django.git

cd RecipeHub_Django
```

### Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### Apply Database Migrations

```bash
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```
http://127.0.0.1:8000/
```

---

## Security Features

- CSRF Protection
- Password Hashing
- JWT Authentication
- Session Authentication
- Login Required Views
- Object-level Authorization
- User Ownership Validation

---

## Future Improvements

- User Profile Management
- Password Reset via Email
- Email Verification
- Recipe Likes
- Social Sharing
- PostgreSQL Support
- Docker Support
- Swagger/OpenAPI Documentation
- Deployment on Render
- GitHub Actions CI/CD

---

## Author

**Harshali Kulkarni**

MCA Graduate | Python & Django Developer

GitHub: https://github.com/Harshali-14

LinkedIn: https://www.linkedin.com/in/harshali-kulkarni-54a822236

Email: harshaliak14@gmail.com

---

## License

This project is licensed under the MIT License.

---

## Support

If you found this project useful, please consider giving it a star.
