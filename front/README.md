# Club  Task Manager Frontend

A Vue.js frontend for the Club Task Manager application.

## Features

- User authentication (login, register, password reset)
- Task management (create, read, update, delete)
- Drag and drop interface for task status updates
- Responsive design for mobile and desktop
- Modern UI with Quasar components and Tailwind CSS

## Tech Stack

- Vue.js 3 with Composition API
- TypeScript
- Pinia for state management
- Vue Router for routing
- Quasar Framework for UI components
- Tailwind CSS for styling
- Vite for build tooling

## Project Structure

```
src/
├── assets/         # Static assets like CSS, images
├── client/         # API client for backend communication
├── components/     # Reusable Vue components
├── composables/    # Vue composables (custom hooks)
├── router/         # Vue Router configuration
├── stores/         # Pinia stores for state management
├── types/          # TypeScript type definitions
└── views/          # Page components
```

## Development

### Prerequisites

- Node.js (v16+)
- pnpm (recommended) or npm

### Setup

1. Install dependencies:

```bash
pnpm install
```

2. Create a `.env` file with the following variables:

```
VITE_API_URL=http://localhost:5000
VITE_APP_TITLE=Club Task Manager
```

3. Start the development server:

```bash
pnpm dev
```

### Building for Production

```bash
pnpm build
```

## Docker

The application can be run using Docker:

```bash
docker-compose up -d
```

This will start the frontend, backend, MongoDB, and Redis services.
