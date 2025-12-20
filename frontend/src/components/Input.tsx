import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

const Input: React.FC<InputProps> = ({ label, error, className = '', ...props }) => {
  return (
    <div className="space-y-2">
      {label && (
        <label className="block text-body font-medium text-neutral-700">
          {label}
        </label>
      )}
      <input
        className={`
          w-full px-4 py-3 min-h-touch
          text-body bg-white border rounded-lg
          border-neutral-300
          focus-ring
          placeholder:text-neutral-400
          disabled:bg-neutral-100 disabled:text-neutral-500 disabled:cursor-not-allowed
          ${error ? 'border-red-500' : ''}
          ${className}
        `}
        {...props}
      />
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

export default Input;
