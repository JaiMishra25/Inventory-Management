# Inventory Management Frontend

A modern React frontend for the Inventory Management Tool with beautiful UI and intuitive user experience.

## Features

- **Modern UI**: Built with React 18 and Tailwind CSS
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Authentication**: Secure login/logout with JWT tokens
- **Product Management**: Add, view, and update products
- **Real-time Updates**: Live inventory tracking
- **Search & Filter**: Find products quickly
- **Beautiful Components**: Modern, accessible UI components

## Tech Stack

- **React 18**: Modern React with hooks
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **Axios**: HTTP client for API calls
- **Lucide React**: Beautiful icons
- **React Hot Toast**: Toast notifications

## Quick Start

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm start
   ```

3. **Open your browser**:
   Navigate to `http://localhost:3000`

## Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/         # Page components
├── context/       # React context providers
├── services/      # API services
├── hooks/         # Custom React hooks
└── utils/         # Utility functions
```

## Backend Integration

The frontend connects to the FastAPI backend running on `http://localhost:8080`. Make sure the backend is running before using the frontend.

## Environment Variables

Create a `.env` file in the root directory:

```env
REACT_APP_API_URL=http://localhost:8080
```

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder. 