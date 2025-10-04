from django.shortcuts import render
from django.http import HttpResponse
import markdown

def documentation(request):
    """
    Comprehensive documentation for the Event Management System workflow
    """
    documentation_content = """
# Event Management System - Complete User Guide

Welcome to the comprehensive guide for our Event Management System! This documentation covers the complete workflow from event creation to attendee registration and management.

## 🎯 System Overview

The Event Management System is designed to streamline the entire process of organizing, managing, and attending events. Whether you're an event organizer or an attendee, this guide will walk you through every feature.

### **User Roles**

- **👤 Member (Attendee)**: Can browse events, register for events, and manage their registrations
- **👨‍💼 Manager (Organizer)**: Can create, edit, and manage events, tracks, sessions, and view attendee lists
- **🛡️ Admin**: Full system access with user management capabilities

---

## 🚀 Getting Started

### **1. Account Creation & Authentication**

#### Registration Process
1. **Sign Up**: Visit `/signup/` to create your account
   - Provide username, email, first name, last name, and password
   - System automatically assigns "Member" role initially
   - Email verification may be required

2. **Login**: Access `/login/` with your credentials
   - Support for both username and email login
   - **"Remember Me"** option extends session to 30 days
   - Forgot password recovery available

3. **Profile Management**: Update your information and role requests

### **2. Dashboard Navigation**

After login, you'll access the main dashboard with:
- **📊 Dashboard**: Overview of upcoming events and your registrations
- **📅 Events**: Browse all available events
- **⚙️ Management**: Create and manage events (Manager role)
- **📖 Documentation**: This guide you're reading

---

## 📅 Event Management Workflow

### **For Event Organizers (Managers)**

#### **Step 1: Create an Event**

1. **Navigate to Management**
   - Click "Management" in the navigation
   - Select "Create New Event"

2. **Fill Event Details**
   ```
   ✅ Event Title (required)
   ✅ Description (optional but recommended)
   ✅ Start Date & Time (required)
   ✅ End Date & Time (required)
   ✅ Venue & Address (required)
   ✅ Capacity (required - max attendees)
   ```

3. **Event Status Options**
   - **Draft**: Visible only to you, allows editing
   - **Published**: Public and accepting registrations
   - **Cancelled**: Stops new registrations, notifies attendees

#### **Step 2: Create Event Tracks**

Tracks help organize your event into different themes or streams:

1. **Add Tracks**
   - In event management, click "Add Track"
   - Provide track name and description
   - Set track order (for display purposes)

2. **Track Examples**
   ```
   🎯 Technical Track
   💼 Business Track  
   🎨 Design Track
   🍽️ Networking Track
   ```

#### **Step 3: Create Sessions**

Sessions are specific activities within tracks:

1. **Session Details**
   - Session title and description
   - Start and end time (within event duration)
   - Assign to specific track
   - Speaker information (optional)

2. **Session Types**
   ```
   🎤 Keynote Presentation
   💬 Panel Discussion
   🛠️ Workshop
   🤝 Networking Session
   ☕ Coffee Break
   ```

#### **Step 4: Manage Registrations**

1. **View Attendee List**
   - Access registered attendees
   - Filter by registration status
   - Export attendee data

2. **Registration Status**
   - **Pending**: Default status upon registration
   - **Confirmed**: Manually confirm attendees
   - **Cancelled**: Handle cancellations

---

## 👥 Attendee Registration Workflow

### **For Event Attendees (Members)**

#### **Step 1: Browse Events**

1. **Dashboard View**
   - See timeline of upcoming events
   - View your registered events
   - Check event status and availability

2. **Events List**
   - Filter events by date, category, or status
   - See availability: "Available Slots: X/Y"
   - Identify fully booked events

#### **Step 2: Event Details**

1. **Click "Check This Event"** to view:
   - Complete event description
   - Date, time, and venue information
   - Available tracks and sessions
   - Current registration count

2. **Visual Indicators**
   ```
   🟢 Available - Open for registration
   🔴 Fully Booked - No slots available
   ✅ Registered - You're already registered
   ```

#### **Step 3: Registration Process**

1. **Register for Event**
   - Click "Register" button
   - Confirm your registration
   - Receive confirmation message

2. **Registration Confirmation**
   - Status changes to "Registered"
   - Event appears in "My Events"
   - Email confirmation (if configured)

#### **Step 4: Manage Your Registrations**

1. **View Registered Events**
   - Access "My Events" section
   - See all your upcoming events
   - Track event details and schedules

2. **Cancel Registration** (if needed)
   - Click event details
   - Select "Cancel Registration"
   - Confirm cancellation

---

## 🔧 Advanced Features

### **Event Status Management**

#### **Event Lifecycle**
```
📝 Draft → 🚀 Published → ✅ Completed
              ↓
            ❌ Cancelled
```

#### **Capacity Management**
- **Automatic Tracking**: System tracks registrations vs. capacity
- **Full Event Handling**: Prevents over-registration
- **Waitlist** (future feature): Queue attendees when full

### **Track & Session Organization**

#### **Track Benefits**
- **Organization**: Group related sessions
- **Navigation**: Help attendees find relevant content
- **Scheduling**: Avoid conflicts between similar topics

#### **Session Scheduling**
- **Time Validation**: Prevents overlapping sessions
- **Track Assignment**: Organize by theme
- **Speaker Management**: Track presenter information

### **User Experience Features**

#### **HTMX Integration**
- **Dynamic Updates**: Content loads without page refresh
- **Modal Dialogs**: Quick event details and registration
- **Real-time Feedback**: Instant status updates

#### **Responsive Design**
- **Mobile Friendly**: Works on all devices
- **Dark Mode**: Toggle between light and dark themes
- **Accessibility**: Screen reader friendly

---

## 🛠️ Technical Integration

### **API Endpoints**

The system provides RESTful APIs for integration:

#### **Authentication**
```
POST /api/auth/login/     - User login
POST /api/auth/refresh/   - Token refresh
GET  /api/profile/        - User profile
```

#### **Events**
```
GET  /api/events/              - List all events
POST /api/events/              - Create new event
GET  /api/events/{id}/         - Event details
PUT  /api/events/{id}/         - Update event
DELETE /api/events/{id}/       - Delete event
```

#### **Registration**
```
POST /api/events/{id}/register/ - Register for event
GET  /api/my-events/           - User's registered events
```

### **API Documentation**
- **Complete Reference**: Available at `/api/doc/`
- **Interactive Examples**: JSON request/response samples
- **Authentication Guide**: JWT token usage

---

## 📊 Dashboard & Analytics

### **Dashboard Features**

#### **For Attendees**
- **Event Timeline**: Chronological view of upcoming events
- **Registration Status**: Quick status overview
- **Event Recommendations**: Based on interests

#### **For Managers**
- **Event Statistics**: Registration counts and trends
- **Attendee Management**: Quick access to attendee lists
- **Event Performance**: Popular events and tracks

### **Reporting (Future)**
- **Attendance Reports**: Track actual vs. registered
- **Popular Tracks**: Most attended sessions
- **User Engagement**: Registration patterns

---

## 🔐 Security & Privacy

### **Data Protection**
- **Secure Authentication**: JWT tokens with expiration
- **Password Security**: Hashed storage, reset functionality
- **Session Management**: Configurable timeout periods

### **Privacy Features**
- **Data Control**: Users can update their information
- **Registration Privacy**: Attendee lists visible only to organizers
- **Email Protection**: No spam, only event-related communications

---

## 🚀 Deployment & Docker

### **Docker Support**
The system includes complete Docker configuration:

#### **Development Environment**
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up --build

# Your app will be available at: http://localhost:8000
```

#### **Production Environment**
```bash
# Start production environment with Nginx, PostgreSQL, Redis
docker-compose up --build

# Includes: Load balancing, caching, database optimization
```

#### **Services Included**
- **🐳 Django Web Application**: Main application server
- **🗄️ PostgreSQL Database**: Reliable data storage
- **⚡ Redis Cache**: Performance optimization
- **🌐 Nginx Reverse Proxy**: Load balancing and static files

---

## 🆘 Troubleshooting

### **Common Issues**

#### **Login Problems**
- **Forgot Password**: Use "Forgot Password" link
- **Account Locked**: Contact administrator
- **Email Not Verified**: Check spam folder

#### **Registration Issues**
- **Event Full**: Check for cancellations or contact organizer
- **Already Registered**: Check "My Events" section
- **Technical Error**: Refresh page and try again

#### **Performance Issues**
- **Slow Loading**: Check internet connection
- **Browser Compatibility**: Use modern browsers (Chrome, Firefox, Safari)
- **Mobile Issues**: Try desktop version for complex operations

### **Getting Help**

#### **Support Channels**
- **Documentation**: This comprehensive guide
- **API Reference**: `/api/doc/` for developers
- **Contact Support**: Through system messaging (future feature)

#### **Best Practices**
- **Regular Logout**: For security on shared computers
- **Update Profile**: Keep information current
- **Event Planning**: Create events well in advance
- **Capacity Planning**: Set realistic attendee limits

---

## 🔮 Future Enhancements

### **Planned Features**
- **📧 Email Notifications**: Automated event reminders
- **📱 Mobile App**: Native iOS/Android applications
- **💬 Live Chat**: Real-time event communication
- **📊 Advanced Analytics**: Detailed reporting dashboard
- **🎟️ QR Code Check-in**: Streamlined event entry
- **🔔 Push Notifications**: Real-time updates
- **🗓️ Calendar Integration**: Google Calendar, Outlook sync
- **💳 Payment Processing**: Paid event support

### **Integration Possibilities**
- **Video Conferencing**: Zoom, Teams integration
- **Social Media**: Event sharing and promotion
- **Survey Tools**: Post-event feedback collection
- **CRM Systems**: Customer relationship management

---

## 📞 Support & Contact

### **System Information**
- **Version**: 1.0.0
- **Technology Stack**: Django 5.2.6, PostgreSQL, Redis, Tailwind CSS
- **Browser Support**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### **Developer Resources**
- **API Documentation**: `/api/doc/`
- **Source Code**: GitHub repository
- **Docker Guide**: `/DOCKER_GUIDE.md`
- **Contributing**: Guidelines for development contributions

---

*This documentation is regularly updated. Last updated: October 2025*

---

**🎉 Thank you for using our Event Management System!**

We're committed to making event organization and attendance as smooth as possible. Whether you're organizing a small workshop or a large conference, our system provides the tools you need for success.

*Happy Event Managing! 🎪*
"""

    # Convert markdown to HTML
    html_content = markdown.markdown(documentation_content, extensions=['codehilite', 'tables', 'toc'])
    
    # Create styled HTML page
    styled_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Event Management System - User Guide</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
                background-color: #f8f9fa;
                color: #333;
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            }}
            .nav-header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px 0;
                margin: -40px -40px 30px -40px;
                border-radius: 12px 12px 0 0;
                text-align: center;
            }}
            .nav-header h1 {{
                margin: 0;
                font-size: 2.5rem;
                font-weight: 300;
            }}
            .nav-header p {{
                margin: 10px 0 0 0;
                opacity: 0.9;
                font-size: 1.1rem;
            }}
            h1 {{
                color: #000000;
                border-bottom: 3px solid #3b82f6;
                padding-bottom: 10px;
                margin-top: 40px;
            }}
            h2 {{
                color: #1e40af;
                margin-top: 35px;
                border-left: 5px solid #3b82f6;
                padding-left: 15px;
                background: linear-gradient(90deg, #eff6ff 0%, transparent 100%);
                padding: 10px 15px;
                border-radius: 0 8px 8px 0;
            }}
            h3 {{
                color: #1e3a8a;
                margin-top: 25px;
                border-bottom: 2px solid #e5e7eb;
                padding-bottom: 5px;
            }}
            h4 {{
                color: #312e81;
                margin-top: 20px;
            }}
            .toc {{
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
            }}
            .toc h2 {{
                margin-top: 0;
                color: #1e40af;
                border: none;
                background: none;
                padding: 0;
            }}
            .toc ul {{
                list-style-type: none;
                padding-left: 0;
            }}
            .toc ul li {{
                margin: 8px 0;
            }}
            .toc ul li a {{
                color: #3b82f6;
                text-decoration: none;
                padding: 5px 10px;
                border-radius: 4px;
                transition: background-color 0.2s;
            }}
            .toc ul li a:hover {{
                background-color: #dbeafe;
            }}
            code {{
                background-color: #f1f5f9;
                padding: 3px 8px;
                border-radius: 4px;
                font-family: 'Monaco', 'Menlo', monospace;
                color: #dc2626;
                font-size: 0.9em;
            }}
            pre {{
                background-color: #1e293b;
                color: #f8fafc;
                padding: 20px;
                border-radius: 8px;
                overflow-x: auto;
                border-left: 4px solid #3b82f6;
                margin: 20px 0;
            }}
            pre code {{
                background: none;
                color: inherit;
                padding: 0;
                font-size: 0.9em;
            }}
            .highlight {{
                background: linear-gradient(120deg, #fef3c7 0%, #fcd34d 100%);
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #f59e0b;
                margin: 20px 0;
            }}
            .info-box {{
                background: linear-gradient(120deg, #dbeafe 0%, #bfdbfe 100%);
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #3b82f6;
                margin: 20px 0;
            }}
            .warning-box {{
                background: linear-gradient(120deg, #fef2f2 0%, #fecaca 100%);
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #ef4444;
                margin: 20px 0;
            }}
            .success-box {{
                background: linear-gradient(120deg, #f0fdf4 0%, #bbf7d0 100%);
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #22c55e;
                margin: 20px 0;
            }}
            blockquote {{
                background: #f8fafc;
                border-left: 4px solid #64748b;
                margin: 20px 0;
                padding: 15px 20px;
                border-radius: 0 8px 8px 0;
                font-style: italic;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            th, td {{
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #e2e8f0;
            }}
            th {{
                background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                color: white;
                font-weight: 600;
            }}
            tr:hover {{
                background-color: #f8fafc;
            }}
            .emoji-large {{
                font-size: 1.5em;
                margin-right: 10px;
            }}
            .back-to-top {{
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: #3b82f6;
                color: white;
                padding: 12px 16px;
                border-radius: 50%;
                text-decoration: none;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
                transition: all 0.3s ease;
            }}
            .back-to-top:hover {{
                background: #1d4ed8;
                transform: translateY(-2px);
            }}
            @media (max-width: 768px) {{
                .container {{
                    padding: 20px;
                    margin: 10px;
                }}
                .nav-header {{
                    margin: -20px -20px 20px -20px;
                }}
                .nav-header h1 {{
                    font-size: 1.8rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav-header">
                <h1>📚 Event Management System</h1>
                <p>Complete User Guide & Documentation</p>
            </div>
            {html_content}
            <a href="#top" class="back-to-top">↑</a>
        </div>
        
        <script>
            // Smooth scrolling for anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
                anchor.addEventListener('click', function (e) {{
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {{
                        target.scrollIntoView({{
                            behavior: 'smooth',
                            block: 'start'
                        }});
                    }}
                }});
            }});
            
            // Show/hide back to top button
            window.addEventListener('scroll', function() {{
                const backToTop = document.querySelector('.back-to-top');
                if (window.pageYOffset > 300) {{
                    backToTop.style.display = 'block';
                }} else {{
                    backToTop.style.display = 'none';
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    return HttpResponse(styled_html)