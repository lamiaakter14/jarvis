export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validateRequired = (value: string): boolean => {
  return value.trim().length > 0;
};

export const validateMinLength = (value: string, minLength: number): boolean => {
  return value.trim().length >= minLength;
};

export const validateMaxLength = (value: string, maxLength: number): boolean => {
  return value.trim().length <= maxLength;
};

export const validateNumber = (value: string): boolean => {
  return !isNaN(Number(value));
};

export const validatePositiveNumber = (value: string): boolean => {
  const num = Number(value);
  return !isNaN(num) && num > 0;
};

export const validateRange = (value: number, min: number, max: number): boolean => {
  return value >= min && value <= max;
};
