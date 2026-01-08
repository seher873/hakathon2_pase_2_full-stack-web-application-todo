'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../../hooks/useAuth';
import AuthForm from '../../components/AuthForm';

const SignupPage = () => {
  const router = useRouter();
  const { signup, isLoading, error } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    passwordConfirm: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    if (!formData.passwordConfirm) {
      newErrors.passwordConfirm = 'Please confirm your password';
    } else if (formData.password !== formData.passwordConfirm) {
      newErrors.passwordConfirm = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    try {
      await signup(formData.email, formData.password, formData.passwordConfirm);
      router.push('/dashboard');
    } catch (err) {
      console.error('Signup failed:', err);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (errors[name as keyof typeof errors]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name as keyof typeof errors];
        return newErrors;
      });
    }
  };

  return (
    <AuthForm
      title="Create your account"
      subtitle="Already have an account?"
      linkText="Sign in here"
      linkHref="/login"
      error={error}
      isLoading={isLoading}
      buttonText="Creating account..."
      onSubmit={handleSubmit}
    >
      <div>
        <label htmlFor="email" className="sr-only">
          Email address
        </label>
        <input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          required
          value={formData.email}
          onChange={handleChange}
          className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
            errors.email ? 'border-red-300' : 'border-gray-300'
          } placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
          placeholder="Email address"
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600">{errors.email}</p>
        )}
      </div>
      <div>
        <label htmlFor="password" className="sr-only">
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="new-password"
          required
          value={formData.password}
          onChange={handleChange}
          className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
            errors.password ? 'border-red-300' : 'border-gray-300'
          } placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
          placeholder="Password"
        />
        {errors.password && (
          <p className="mt-1 text-sm text-red-600">{errors.password}</p>
        )}
      </div>
      <div>
        <label htmlFor="passwordConfirm" className="sr-only">
          Confirm Password
        </label>
        <input
          id="passwordConfirm"
          name="passwordConfirm"
          type="password"
          autoComplete="new-password"
          required
          value={formData.passwordConfirm}
          onChange={handleChange}
          className={`appearance-none rounded-none relative block w-full px-3 py-2 border ${
            errors.passwordConfirm ? 'border-red-300' : 'border-gray-300'
          } placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm`}
          placeholder="Confirm Password"
        />
        {errors.passwordConfirm && (
          <p className="mt-1 text-sm text-red-600">{errors.passwordConfirm}</p>
        )}
      </div>
    </AuthForm>
  );
};

export default SignupPage;