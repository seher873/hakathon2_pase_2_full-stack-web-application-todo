import sqlite3 from 'sqlite3';
import { open, Database } from 'sqlite';

// Initialize database synchronously for the init script
async function initializeDatabase() {
  try {
    console.log('Initializing SQLite database for development...');
    sqlite3.verbose();
    
    // Open SQLite database (creates file if it doesn't exist)
    const db = await open({
      filename: './hackathon_dev.db', // Local SQLite file
      driver: sqlite3.Database,
    });

    // Create users table if it doesn't exist
    await db.exec(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      );
    `);

    console.log('Users table created or already exists.');

    // Create tasks table if it doesn't exist
    await db.exec(`
      CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        url TEXT, -- Optional URL field for running links
        status TEXT DEFAULT 'todo',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
      );
    `);

    console.log('Tasks table created or already exists.');

    // Create indexes
    await db.exec('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);');
    await db.exec('CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);');
    await db.exec('CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);');

    console.log('Indexes created for improved performance.');
    console.log('Database initialization completed successfully!');

    // Close the database connection
    await db.close();
    
    return true;
  } catch (error) {
    console.error('Error initializing database:', error);
    return false;
  }
}

// Run the initialization
initializeDatabase().then(success => {
  if (success) {
    console.log('Database setup completed successfully!');
    process.exit(0);
  } else {
    console.error('Database setup failed!');
    process.exit(1);
  }
}).catch(error => {
  console.error('Unexpected error during database setup:', error);
  process.exit(1);
});