const express = require('express');
const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'OK', timestamp: new Date().toISOString() });
});

// Main endpoint
app.get('/', (req, res) => {
  res.status(200).json({ 
    message: 'Phase-4 Backend Service', 
    status: 'Running',
    port: PORT 
  });
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Phase-4 Backend service listening at http://0.0.0.0:${PORT}`);
});