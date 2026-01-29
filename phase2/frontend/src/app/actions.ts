'use server';

import { revalidatePath } from 'next/cache';

/**
 * Revalidates the dashboard path to refresh data
 */
export async function revalidateDashboard() {
  revalidatePath('/dashboard');
}

/**
 * Revalidates the todo path to refresh data
 */
export async function revalidateTodo() {
  revalidatePath('/todo');
}