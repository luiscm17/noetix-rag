import { forwardRef, type ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

const variantStyles = {
  primary: `
    bg-brand text-[#0c0a09] font-semibold hover:bg-brand-hover/95
    shadow-md shadow-brand/15 hover:shadow-lg hover:shadow-brand/20 disabled:opacity-60
  `,
  secondary: `
    bg-[var(--bg-elevated)] border border-[var(--border-subtle)]
    text-[var(--text-primary)] hover:bg-[var(--bg-secondary)]/60 hover:border-[var(--border-default)]
  `,
  ghost: `
    bg-transparent text-[var(--text-secondary)] hover:text-[var(--text-primary)]
    hover:bg-[var(--bg-secondary)]/40
  `,
  danger: `
    bg-transparent text-red-500 hover:bg-red-500/10
    border border-transparent hover:border-red-500/20
  `,
};

const sizeStyles = {
  sm: 'h-8 px-3 text-xs rounded-lg gap-2',
  md: 'h-10 px-4 text-sm rounded-xl gap-2',
  lg: 'h-12 px-6 text-base rounded-2xl gap-3',
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'primary', size = 'md', className = '', isLoading, children, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={`
          inline-flex items-center justify-center font-medium
          transition-all duration-200 ease-out
          focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2 focus-visible:ring-offset-[var(--bg-primary)]
          disabled:cursor-not-allowed disabled:hover:opacity-50
          ${variantStyles[variant]}
          ${sizeStyles[size]}
          ${className}
        `}
        {...props}
      >
        {isLoading && (
          <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        )}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
