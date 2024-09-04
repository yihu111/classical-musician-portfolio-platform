# Classical Musician Portfolio Platform

### Description:

This repository contains my final project for **CS50: Introduction to Computer Science** offered by Harvard University. The project is a web-based classical musician portfolio platform designed to allow musicians to showcase the pieces they have performed, and for other users to discover, view, and explore these musical portfolios.

The platform provides an intuitive and streamlined user experience where musicians can easily register, log in, and manage their own profiles. Each musician can build a personal portfolio by adding, updating, or deleting pieces they have played, which can include details such as the title, composer, and year of performance. The goal is to offer a digital space for classical musicians to exhibit their work and share their journey with others.

Users, even without logging in, can browse through the profiles of different musicians using the search functionality, which allows for filtering by username. This makes it easy for music enthusiasts, colleagues, or other musicians to search for specific performers, view their repertoire, and learn more about the pieces they have performed. Each profile is unique to the individual and includes personal details like the musician's name, instrument, and a short bio.

In its current form, the platform offers essential functionality like user registration, authentication, and portfolio management. However, it is designed as a foundation that can be extended with additional features such as social interactions, performance reviews, multimedia uploads (audio or video of performances), and even collaborative features for musicians to engage with each other.

While this platform represents a basic starting point, the potential for expansion is vast. It can grow into a full-featured social network for classical musicians, helping them connect with other professionals, music enthusiasts, or potential employers, all while showcasing their talents through a dynamic online presence.

This project exemplifies the core principles and skills learned throughout the CS50 course, including web development with Python and Flask, database management with SQLite, user authentication, and more. It is a demonstration of both technical skills and a passion for the classical music community.

### Features:

- **User Authentication**: Musicians can register, log in, and manage their own portfolios.
- **Profile Management**: Users can add a short bio, list their instruments, and store their played pieces.
- **Music Portfolio**: Musicians can add details about the pieces they have played (title, composer, and year).
- **Search for Musicians**: Anyone, logged in or not, can search for a musician's profile by username.
- **View Public Profiles**: Non-authenticated users can view any musician's public profile.
- **Session Management**: Users can log out securely, and session data is cleared.
- **Edit Profile**: Musicians can update their bio, password, and other details.
- **Delete Pieces**: Musicians can remove pieces from their portfolio.

### Code Structure

The folders are structured as follows:

```
.
├── app.py
├── music_portfolio.db
├── templates/
│   ├── add_piece.html
│   ├── edit_profile.html
│   ├── index.html
│   ├── layout.html
│   ├── login.html
│   ├── own_profile.html
│   ├── profile.html
│   └── register.html
├── static/
|   └── style.css
├── requirements.txt
└── README.md
```
