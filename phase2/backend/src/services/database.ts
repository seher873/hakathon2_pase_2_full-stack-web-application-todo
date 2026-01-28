import sqlite3 from 'sqlite3';
import { open, Database } from 'sqlite';
import dotenv from 'dotenv';
import { Pool } from 'pg';

dotenv.config();

// Determine if we're using PostgreSQL or SQLite based on environment
const IS_POSTGRES_ENABLED = process.env.USE_POSTGRES === 'true';

// Global database instance
let db: Database | null = null;
let pgPool: Pool | null = null;
let dbInitialized = false;
let dbInitializationPromise: Promise<void> | null = null;

// Initialize database connection
async function initializeDatabase() {
  if (IS_POSTGRES_ENABLED) {
    console.log('--- DB INFO: Using PostgreSQL ---');
    pgPool = new Pool({
      connectionString: process.env.DATABASE_URL,
      user: process.env.DB_USER,
      host: process.env.DB_HOST,
      database: process.env.DB_NAME,
      password: process.env.DB_PASSWORD,
      port: parseInt(process.env.DB_PORT || '5432'),
      ssl: process.env.DB_SSL === 'true' ? { rejectUnauthorized: false } : false
    });

    try {
      const client = await pgPool.connect();
      console.log('--- DB INFO: PostgreSQL connected ---');
      client.release();
      dbInitialized = true;
    } catch (err) {
      console.error('--- DB ERROR: PostgreSQL connection failed ---', err);
      throw err;
    }
  } else {
    console.log('--- DB INFO: Using SQLite ---');
    sqlite3.verbose();
    const database = await open({
      filename: './hackathon_dev.db',
      driver: sqlite3.Database,
    });

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
        url TEXT,
        status TEXT DEFAULT 'todo',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
      );
    `);

    await database.exec('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);');
    await database.exec('CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);');
    await database.exec('CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);');

    console.log('--- DB INFO: SQLite initialized ---');
    db = database;
    dbInitialized = true;
  }
}

if (!dbInitialized) {
  dbInitializationPromise = initializeDatabase().catch(error => {
    console.error('--- DB ERROR: Critical Init Failure ---', error);
    process.exit(1);
  });
}

/**
 * Universal query function that handles Postgres vs SQLite differences
 */
export async function query(text: string, params?: any[]) {
  if (!dbInitialized && dbInitializationPromise) await dbInitializationPromise;

  if (IS_POSTGRES_ENABLED) {
    if (!pgPool) throw new Error('Postgres pool not initialized');
    return await pgPool.query(text, params);
  }

  if (!db) throw new Error('Database not initialized');

  // SQLite Logic
  let sql = text.replace(/\$\d+/g, '?');
  const isReturning = sql.toUpperCase().includes('RETURNING');

  if (isReturning) {
    sql = sql.replace(/RETURNING \*/gi, '').trim();
  }

  console.log(`[SQL DEBUG] ${sql}`, params || []);

  try {
    if (sql.toUpperCase().startsWith('SELECT')) {
      const rows = params ? await db.all(sql, params) : await db.all(sql);
      return { rows, rowCount: rows.length };
    } else {
      // For INSERT/UPDATE/DELETE
      const result = params ? await db.run(sql, params) : await db.run(sql);

      let rows: any[] = [];
      if (isReturning && sql.toUpperCase().startsWith('INSERT')) {
        const lastId = result.lastID;
        const inserted = await db.get('SELECT * FROM tasks WHERE id = ?', [lastId]);
        rows = inserted ? [inserted] : [];
      } else if (isReturning && (sql.toUpperCase().startsWith('UPDATE') || sql.toUpperCase().startsWith('PATCH'))) {
        // Fallback: for updates, we try to return the row using the ID if it's in params
        // This is specifically for your task routes
        const id = params ? params.find(p => typeof p === 'number' || (typeof p === 'string' && !isNaN(Number(p)))) : null;
        if (id) {
          const updated = await db.get('SELECT * FROM tasks WHERE id = ?', [id]);
          rows = updated ? [updated] : [];
        }
      }

      return { rows, rowCount: result.changes || rows.length };
    }
  } catch (error) {
    console.error(`[SQL ERROR] ${sql}`, error);
    throw error;
  }
}

/**
 * Compatibility wrapper for .run()
 */
export async function run(text: string, params?: any[]) {
  return query(text, params);
}

export const pool = { query, run };
export { db, pgPool, initializeDatabase };