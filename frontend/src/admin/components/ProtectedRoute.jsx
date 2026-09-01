import { Navigate } from 'react-router-dom';
import { adminApi } from '../services/api';

export const ProtectedRoute = ({ children }) => {
  const token = adminApi.token;

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
};
