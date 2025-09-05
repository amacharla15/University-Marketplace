Project Title: University Marketplace

Project Description:
University Marketplace is a full-stack web application built to provide university students
with a dedicated platform to buy, sell, or exchange goods and services within their academic
community. Inspired by students using social media stories to sell textbooks, electronics,
furniture, or sublease apartments, this platform aims to centralize and streamline that
informal process into a secure and organized online marketplace.
Students must register and log in using official university email addresses to ensure that
only verified users can participate. Once authenticated, users can manage their profiles and
item listings. Each listing includes images, descriptions, prices, and tags for easier discovery
by others.
The homepage will display an updated feed of all items, with a search bar and category
filters to help users find what they need. Users can also favorite listings, contact sellers via
in-app chat, and schedule appointments to meet on campus for item inspection and pickup.
After each transaction, users may leave ratings and reviews to build trust in the community
and improve accountability.
The platform will be developed using HTML, CSS, JavaScript, Bootstrap, Django, and
PostgreSQL. It will be containerized with Docker and deployed to Google Cloud Platform
behind a load balancer with at least two app servers. User-uploaded images will be stored
using GCP Buckets. The /server_info/ path will show configuration and server environment
details for debugging purposes.
Advanced features include a wishlist, real-time notifications, a basic item recommender
system, and optional dark mode. These additions will improve user experience, encourage
engagement, and differentiate the platform from basic listing boards.
The responsive design will ensure accessibility across both mobile and desktop devices.
University Marketplace empowers students to engage in secure, efficient, and communitydriven exchanges while solving a real problem faced by students in everyday campus life.

Feature List: 
• • University email authentication (Join/Login)
• • User profile creation
• • Post, view, and edit item listings
• • Upload item images
• • Homepage listing feed
• • Search and filter by keywords, category, and tags
• • In-app messaging between users
• • Book Appointment for offline meetups
• • Wishlist (save favorite items)
• • Ratings and reviews for sellers
• • Notifications for chat, appointments, and updates
• • Report listing (moderation)
• • Responsive Bootstrap UI
• • REST API endpoints
• • Recommender system for item suggestions
• • Dark mode toggle
• • /server_info/ view for server metadata
• • Dockerized deployment to GCP
• • PostgreSQL database with 3+ related models
• • GCP Bucket for storing uploaded images

UI Navigation / Pages:
• • / → Home page: Feed of listings + search and filters
• • /signup/ → Join page: Register with university email
• • /login/ → Login page
• • /logout/ → Logout page
• • /about/ → About the platform
• • /profile/ → User profile: User info + listed items + wishlist
• • /item/<id>/ → Item detail page: View + chat + appointment
• • /upload/ → Upload item: Listing form
• • /messages/ → Chat interface: All messages
• • /appointments/ → View & manage appointments
• • /server_info/ → Server info endpoint for diagnostics
• • /report/<id>/ → Report listing 
