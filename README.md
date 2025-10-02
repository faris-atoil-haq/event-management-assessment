```markdown
# Event Management System

A Django-based event management system that allows users to create, manage, and track events with user authentication and a responsive web interface.

## 🚀 Features

- **User Authentication**: Complete signup, login, and logout functionality with email verification
- **Event Management**: Create, view, edit, and delete events
- **Responsive Design**: Modern UI using Tailwind CSS and Flowbite components
- **Dashboard Interface**: Clean and intuitive dashboard for managing events
- **Email System**: Password reset and account verification via email
- **Custom User Backend**: Extended authentication system supporting email/username login
- **Static File Management**: Optimized static file serving with WhiteNoise
- **Dark Mode Support**: Built-in dark/light theme toggle

## 🛠️ Technology Stack

- **Backend**: Django 5.2.6
- **Frontend**: HTML5, Tailwind CSS, Flowbite, JavaScript
- **Database**: PostgreSQL-compatible
- **Authentication**: Custom Django authentication backend
- **Static Files**: WhiteNoise for production static file serving
- **Email**: Django email backend
- **Deployment**: Vercel-ready configuration

## 📁 Project Structure

```
event-management-assessment/
├── app/                           # Main application
│   ├── models/                    # Database models
│   ├── views/                     # View controllers
│   ├── templatetags/              # Custom template tags
│   └── migrations/                # Database migrations
├── event_management/              # Project configuration
│   ├── settings.py                # Django settings
│   ├── urls.py                    # URL routing
│   └── views/                     # Project-level views
├── templates/                     # HTML templates
│   ├── app/templates/             # App-specific templates
│   ├── main/templates/            # Main templates
│   └── _base.html                 # Base template
├── static/                        # Static files (development)
├── staticfiles/                   # Collected static files (production)
├── utils/                         # Utility functions
└── requirements.txt               # Python dependencies
```

## 🔧 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js (for frontend dependencies)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd event-management-assessment
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js dependencies**
   ```bash
   npm install
   ```

5. **Environment Configuration**
   - Copy `.env.example` to `.env`
   - Configure the following variables:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=your-database-url
   SITE_URL=http://localhost:8000
   ```

6. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. **Collect Static Files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` to access the application.

## 🌐 Deployment

### Vercel Deployment

This project is configured for easy deployment on Vercel:

1. **Connect to Vercel**
   - Import your repository to Vercel
   - Configure environment variables in Vercel dashboard

2. **Environment Variables (Production)**
   ```env
   SECRET_KEY=your-production-secret-key
   DEBUG=False
   PROD=True
   DATABASE_URL=your-production-database-url
   ALLOWED_HOSTS=your-domain.vercel.app
   ```

3. **Automatic Deployment**
   - Push to main branch triggers automatic deployment
   - Static files are automatically collected and served

## 📱 Key Features

### Authentication System
- User registration with email verification
- Login/logout functionality  
- Custom authentication backend supporting email or username login

### Event Management
- Create new events with details (title, description, date, etc.)
- View all events in a timeline format
- Edit and delete existing events
- Dashboard with event overview

### User Interface
- Responsive design that works on all devices
- Modern UI components using Flowbite
- Dark/light mode toggle
- Clean and intuitive navigation

### Technical Features
- Custom template tags for enhanced functionality
- Middleware for request processing
- Custom context processors
- Optimized static file handling

## 🎯 Usage

### For Users
1. **Sign Up**: Create an account with email verification
2. **Login**: Access your dashboard
3. **Create Events**: Add new events with all necessary details
4. **Manage Events**: View, edit, or delete your events
5. **Dashboard**: Overview of all your events in timeline format

### For Administrators
- Access Django admin panel at `/admin/`
- Manage users and events
- View system statistics
- Configure site settings

## 🔐 Security Features

- CSRF protection enabled
- Secure password hashing
- Email verification for new accounts
- Session-based authentication
- SQL injection protection via Django ORM
- XSS protection with template escaping

## 🎨 Frontend Components

- **Tailwind CSS**: Utility-first CSS framework
- **Flowbite**: Component library for enhanced UI
- **Custom JavaScript**: Theme toggle and interactive features
- **Responsive Design**: Mobile-first approach
- **Dark Mode**: Automatic theme switching

## 🆘 Support

For support and questions:
- Open an issue on GitHub
- Contact the development team
- Check the documentation

## 🔧 Development Notes

- Uses Django's built-in development server for local development
- Static files are served via WhiteNoise in production
- Database migrations are handled automatically
- Custom management commands available for various tasks

---

**Built with ❤️ using Django and modern web technologies**
```

This README provides a comprehensive overview of your event management system, including installation instructions, features, deployment guidelines, and technical details. You can customize it further based on any specific requirements or additional features you want to highlight.