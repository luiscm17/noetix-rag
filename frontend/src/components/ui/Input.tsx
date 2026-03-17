import { forwardRef, type InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  icon?: React.ReactNode;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, icon, className = '', ...props }, ref) => {
    return (
      <div className="space-y-2">
        {label && (
          <label className="text-xs font-semibold text-[var(--text-muted)] uppercase ml-1 tracking-wider">
            {label}
          </label>
        )}
        <div className="relative group">
          {icon && (
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-[var(--text-muted)] group-focus-within:text-brand transition-colors">
              {icon}
            </div>
          )}
          <input
            ref={ref}
            className={`
              w-full bg-[var(--bg-tertiary)] border border-[var(--border-default)] rounded-xl
              py-3.5 ${icon ? 'pl-11' : 'pl-4'} pr-4
              text-sm text-[var(--text-primary)] placeholder:text-[var(--text-muted)]
              focus:outline-none focus:border-brand/30 focus:ring-2 focus:ring-brand/10
              transition-colors duration-200
              disabled:opacity-50 disabled:cursor-not-allowed
              ${error ? 'border-red-500/50 focus:border-red-500/30 focus:ring-red-500/10' : ''}
              ${className}
            `}
            {...props}
          />
        </div>
        {error && (
          <p className="text-xs text-red-500 ml-1">{error}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
