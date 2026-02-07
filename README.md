# UpBID 🚀

UpBID is a full-stack auction web application inspired by eBay, built using **Django**. It allows users to list items for auction, place competitive bids, manage personal watchlists, and receive real-time feedback on auction outcomes.

The project focuses on user authentication, relational data modeling, and interactive auction logic while maintaining a clean and intuitive user experience.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Django (Python) |
| **Database** | Django ORM |
| **Auth** | Django Built-in Authentication |
| **Frontend** | Jinja, Django Templates

---

## ✨ Core Features

### 🔐 User Authentication
Secure user registration, login, and logout functionality powered by Django’s robust auth system.

### 🏷️ Create Auction Listings
Authenticated users can create detailed listings, upload item descriptions, and set a starting bid price.

### 📈 Bidding System
* **Dynamic Bidding:** Users can place bids on active listings.
* **Validation:** Each bid must be strictly higher than the current highest bid to be accepted.
* **Control:** Listings remain active until the owner chooses to close the auction.

### 🗂️ Active Listings & Categories
* **Discovery:** A dedicated page displays all currently open auctions.
* **Organization:** Listings are grouped by category for easy navigation (e.g., Electronics, Fashion, Home).

### ⭐ Watchlist
* Users can add or remove listings from their personal watchlist.
* Quickly access interested items directly from the navigation bar.

### 🔔 Auction Notifications
Real-time feedback for users when an auction is closed:
* They successfully win an auction.
* They have been outbid by another user.

---
