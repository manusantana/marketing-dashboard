# Backend Improvement Program

This document outlines the plan to improve the backend with the following functionalities.

## User & Role Management

### Authentication/Authorization
We will implement JWT-based (JSON Web Tokens) authentication. It's a robust, stateless standard, perfect for communication between a React frontend and our API. For the future, if social media login is required, we'll integrate an OAuth 2.0 flow. We do not need LDAP.

### Roles
Roles should be hard-coded initially to simplify business logic and security. We will start with three base roles: **admin**, **editor**, and **viewer**. This gives us clear control over permissions from the start, and we can add a dynamic role system in a later phase if the product requires it.

## Frontend / Dashboard

### Framework
We will maintain the existing React setup. There's no compelling technical reason to migrate to another framework, and leveraging the current codebase will accelerate development.

### User-based 'Frontend Checks'
These checks primarily refer to conditional user interface (UI) rendering and form validation based on the user's role:

- **View/Component Access Control**: The frontend will hide UI routes and components (buttons, menus, entire pages) that the user's role does not have access to. For example, a viewer will not see the "Create New Post" button.
- **Field Validation**: Certain fields in forms may be disabled or read-only based on the role. An editor could modify the body of an article, but not its publication date, a field that only the admin can change.

## Database & Uploads

### Database
We will use PostgreSQL. Its reliability, scalability, and support for advanced data types like JSONB make it ideal for our application. Of course, the corresponding models and migrations must be generated for the users, roles, and the role_user pivot tables. This is fundamental for maintaining database schema integrity and versioning.

### "Remove Uploads Files"
We do not want to completely remove the file upload endpoints. The correct action is to restrict access. The upload endpoint must be protected and only accessible to authorized roles, such as admin and editor. A viewer attempting to access it will receive a **403 Forbidden** error.

## API Integrations

### Specific Endpoints
We need the following initial data flows:

- **Google Analytics**: User acquisition data, behavioral metrics (sessions, bounce rate), and goal conversions.
- **Google Ads / Meta Ads**: Key campaign performance metrics: impressions, clicks, CTR, cost per acquisition (CPA), and ROAS.
- **Social Media (e.g., Twitter, Instagram)**: Post engagement metrics: likes, comments, shares, reach.
- **Shopify**: Order synchronization (orders/create, orders/updated), product inventory updates (products/update), and basic customer information (customers).

### Integration Level
Let's start with placeholder code and well-defined API clients. This will allow us to build the frontend in parallel without depending on the OAuth authentications being complete. The first phase is to have a solid client architecture; the second will be to implement the full authentication flows and real data synchronization.

## Responsive Design

### Style Guides
The new design must follow Material-UI (MUI) guidelines. Its component system is very comprehensive, accelerates React development, and ensures excellent visual consistency. Additionally, the colors, typographies, and logos defined in our branding guide must be applied to customize the MUI components and align them with our brand identity.

