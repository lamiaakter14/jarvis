# JARVIS Frontend Dashboard

A modern, responsive web dashboard for the JARVIS AI Cognitive Assistant built with React, TypeScript, and Tailwind CSS.

## 🚀 Features

- **Modern UI**: Built with React 18 and Tailwind CSS for a sleek, responsive design
- **Dark Mode**: Full dark mode support with theme persistence
- **Real-time Updates**: Polling-based updates to keep data fresh
- **Type-Safe**: Written in TypeScript for better development experience
- **Responsive**: Mobile-first design that works on all screen sizes
- **Performance Analytics**: Visualize productivity metrics with Recharts
- **5 Cognitive Agents**: Interact with Strategist, Mentor, Executor, Innovator, and Amplifier agents

## 📋 Pages

1. **Dashboard** - Overview with stats, system status, and quick actions
2. **Cognitive Loop** - Run and monitor all 5 cognitive agents
3. **Plans** - View and generate daily plans with tasks
4. **Tasks** - Task management (coming soon)
5. **Knowledge Gaps** - Track identified learning areas
6. **Innovations** - Browse creative ideas and innovations
7. **Performance** - Analytics and productivity metrics with charts
8. **Settings** - Configure API, theme, and agent settings

## 🛠️ Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Fast build tool and dev server
- **React Router v6** - Client-side routing
- **Tailwind CSS** - Utility-first styling
- **Axios** - API client
- **Recharts** - Data visualization
- **Lucide React** - Icon library
- **React Hot Toast** - Toast notifications
- **Radix UI** - Accessible component primitives

## 📦 Installation

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your backend API URL
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

   The app will be available at http://localhost:3000

## 🔧 Available Scripts

- `npm run dev` - Start development server with HMR
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally
- `npm run lint` - Run ESLint

## 🏗️ Project Structure

```
frontend/
├── public/              # Static assets
│   └── jarvis-logo.svg
├── src/
│   ├── api/            # API client and endpoints
│   ├── components/     # React components
│   │   ├── common/     # Reusable UI components
│   │   ├── dashboard/  # Dashboard-specific components
│   │   └── layout/     # Layout components
│   ├── contexts/       # React contexts
│   ├── pages/          # Page components
│   ├── styles/         # Global styles
│   ├── types/          # TypeScript type definitions
│   ├── utils/          # Utility functions
│   ├── App.tsx         # Main app component
│   └── main.tsx        # Entry point
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## 🌐 API Integration

The frontend connects to the JARVIS FastAPI backend. By default, it expects the backend at `http://localhost:8000`.

### API Endpoints Used

- `GET /health` - Health check
- `POST /api/cognitive-loop` - Run cognitive loop
- `GET /api/plan/today` - Get today's plan
- `POST /api/plan/generate` - Generate new plan
- `GET /api/gaps` - Get knowledge gaps
- `GET /api/innovations` - Get innovations
- `GET /api/performance` - Get performance metrics

### Configuring Backend URL

Set the `VITE_API_URL` environment variable:

```bash
# .env
VITE_API_URL=http://localhost:8000
```

Or configure the proxy in `vite.config.ts` for development.

## 🎨 Customization

### Theme Colors

Edit `tailwind.config.js` to customize colors:

```javascript
theme: {
  extend: {
    colors: {
      primary: '#3B82F6',    // Blue
      secondary: '#8B5CF6',  // Purple
    },
  },
}
```

### Dark Mode

Dark mode is implemented using Tailwind's `class` strategy. Toggle with the moon/sun icon in the header.

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized build in the `dist/` directory.

### Serve Static Files

You can serve the `dist/` directory with any static file server:

```bash
npm run preview  # Preview locally
```

Or use a service like Vercel, Netlify, or serve with Nginx.

### Docker Deployment

To deploy with Docker alongside the backend, update `docker-compose.yml`:

```yaml
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
```

## 🧪 Development Tips

1. **Backend Must Be Running**: Ensure the FastAPI backend is running at the configured URL
2. **Hot Module Replacement**: Vite provides instant HMR for rapid development
3. **TypeScript**: Use proper types to catch errors early
4. **Dark Mode Testing**: Test both light and dark modes
5. **Responsive Testing**: Check mobile, tablet, and desktop layouts

## 🐛 Troubleshooting

### API Connection Issues

If you see API errors:
1. Verify the backend is running: `curl http://localhost:8000/health`
2. Check the `VITE_API_URL` in your `.env` file
3. Check browser console for CORS errors
4. Verify proxy configuration in `vite.config.ts`

### Build Errors

If the build fails:
1. Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
2. Clear Vite cache: `rm -rf node_modules/.vite`
3. Check for TypeScript errors: `npm run lint`

## 📚 Resources

- [React Documentation](https://react.dev/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Vite Guide](https://vitejs.dev/guide/)
- [React Router](https://reactrouter.com/)

## 📄 License

Same as the main JARVIS project.

## 🤝 Contributing

Contributions are welcome! Please ensure your code:
- Follows the existing code style
- Includes proper TypeScript types
- Is responsive and accessible
- Works in both light and dark modes
