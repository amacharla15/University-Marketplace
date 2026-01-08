# University Marketplace

A full-stack marketplace for university students to buy/sell/exchange items within a verified campus community.

🎥 Demo (YouTube): https://youtu.be/dD_xrF4pGcw?si=RDeg5Il6kOBvUZpV

---

## Overview

University Marketplace is a Django + PostgreSQL web app inspired by how students often use social media stories to sell textbooks, electronics, furniture, or sublease apartments. This project centralizes that informal workflow into a structured platform where users can:

- Register/login (intended for university email-based access control)
- Create and manage listings (images, price, tags/categories)
- Browse a feed with search + filters
- Save favorites (wishlist)
- Message sellers in-app
- Schedule on-campus meetups (appointments)
- Leave ratings/reviews after transactions
- Report listings for moderation

It is containerized with Docker and designed to be deployable on Google Cloud with multiple app servers behind a load balancer. User-uploaded images are designed to be stored in GCP Storage Buckets, and `/server_info/` exposes runtime/server metadata for debugging.

---

## Tech Stack

- **Backend:** Python, Django
- **Database:** PostgreSQL
- **Frontend:** HTML, CSS, JavaScript, Bootstrap (templates)
- **Infra/DevOps:** Docker, deployment manifests/scripts for GCP, load-balancer-oriented setup
- **Diagnostics:** `/server_info/` endpoint for environment/config visibility

---

## Key Features

### Listings + Discovery
- Create/edit listings with images, descriptions, price, tags
- Home feed of listings
- Search + filters (keywords/category/tags)

### Trust + Workflow
- Verified user flow (university email-based access control intent)
- Favorites/Wishlist
- Ratings & reviews
- Report listing (moderation flow)

### Communication + Logistics
- In-app messaging between buyer/seller
- Appointment scheduling for meetups/pickup

### Deployment + Ops
- Dockerized app
- Designed for multi-instance deployment behind HTTPS Load Balancer
- `/server_info/` to surface server/environment details for debugging

---

## Routes / Pages

- `/` — Home feed (listings + search/filters)
- `/signup/` — Register
- `/login/` — Login
- `/logout/` — Logout
- `/about/` — About
- `/profile/` — Profile + listings + wishlist
- `/item/<id>/` — Item detail (view/chat/appointment)
- `/upload/` — Create listing
- `/messages/` — Inbox/chat
- `/appointments/` — Manage appointments
- `/report/<id>/` — Report listing
- `/server_info/` — Server metadata (diagnostics)

---

## Local Setup (Docker)

### Prerequisites
- Docker + Docker Compose (or Docker Desktop)

### Run
```bash
# build
docker build -t university-marketplace .

# run (example)
docker run -p 8000:8000 university-marketplace
