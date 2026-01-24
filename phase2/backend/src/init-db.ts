import { db, query } from './services/database';

async function initializeDatabase() {
  try {
    console.log('Initializing SQLite database...');

    // Create users table if it doesn't exist
    await query(`
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
    await query(`
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
    await query('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);');
    await query('CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);');
    await query('CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);');

    console.log('Indexes created for improved performance.');
    console.log('Database initialization completed successfully!');

    // Close the database connection
    if (db) {
      await db.close();
    }
  } catch (error) {
    console.error('Error initializing database:', error);
    process.exit(1);
  }
}

initializeDatabase();