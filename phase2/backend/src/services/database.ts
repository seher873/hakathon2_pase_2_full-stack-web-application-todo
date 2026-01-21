import sqlite3 from 'sqlite3';
import { open, Database } from 'sqlite';
import dotenv from 'dotenv';

dotenv.config();

// Determine if we're using PostgreSQL or SQLite based on environment
const USE_POSTGRES = process.env.USE_POSTGRES === 'true';

// Global database instance
let db: Database | null = null;
let dbInitialized = false;
let dbInitializationPromise: Promise<void> | null = null;

// Initialize database connection
async function initializeDatabase() {
  if (USE_POSTGRES) {
    // Use PostgreSQL (original implementation)
    console.log('Using PostgreSQL database');
    // Note: In a real implementation, you would use the pg library here
    // For now, we'll throw an error if PostgreSQL is requested but not available
    throw new Error('PostgreSQL support requires additional setup');
  } else {
    // Use SQLite for development
    console.log('Using SQLite database for development');
    sqlite3.verbose();

    // Open SQLite database (creates file if it doesn't exist)
    const database = await open({
      filename: './hackathon_dev.db', // Local SQLite file
      driver: sqlite3.Database,
    });

    // Create tables if they don't exist
    await database.exec(`
      CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      );
    `);

    await database.exec(`
      CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        url TEXT, -- Added for link functionality
        status TEXT DEFAULT 'todo',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
      );
    `);

    // Create indexes
    await database.exec('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);');
    await database.exec('CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);');
    await database.exec('CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);');

    console.log('SQLite database initialized successfully');

    // Assign to global variable
    db = database;
    dbInitialized = true;
  }
}

// Initialize the database when module loads (only if not already initialized)
if (!dbInitialized) {
  dbInitializationPromise = initializeDatabase().catch(error => {
    console.error('Error initializing database:', error);
    process.exit(1);
  });
}

// Helper function to run queries (mimics the pg.Pool.query interface)
export async function query(text: string, params?: any[]) {
  // Wait for database to be initialized
  if (!dbInitialized && dbInitializationPromise) {
    await dbInitializationPromise;
  }

  if (!db) {
    throw new Error('Database not initialized');
  }

  // Convert PostgreSQL-style parameter placeholders ($1, $2, etc.) to SQLite-style (?)
  let sql = text;
  if (params && params.length > 0) {
    // Replace $1, $2, etc. with ?
    sql = text.replace(/\$\d+/g, '?');
  }

  try {
    if (params && params.length > 0) {
      const result = await db.all(sql, params);
      return { rows: result, rowCount: result.length };
    } else {
      const result = await db.all(sql);
      return { rows: result, rowCount: result.length };
    }
  } catch (error) {
    console.error('Database query error:', error);
    throw error;
  }
}

// Helper function to run insert/update/delete queries
export async function run(text: string, params?: any[]) {
  // Wait for database to be initialized
  if (!dbInitialized && dbInitializationPromise) {
    await dbInitializationPromise;
  }

  if (!db) {
    throw new Error('Database not initialized');
  }

  // Convert PostgreSQL-style parameter placeholders ($1, $2, etc.) to SQLite-style (?)
  let sql = text.replace(/\$\d+/g, '?');

  try {
    if (params && params.length > 0) {
      return await db.run(sql, params);
    } else {
      return await db.run(sql);
    }
  } catch (error) {
    console.error('Database run error:', error);
    throw error;
  }
}

// Export a pool-like object for compatibility with existing code
export const pool = {
  query: query,
  run: run
};

// Export the database instance and initialization function for direct access
export { db, initializeDatabase };