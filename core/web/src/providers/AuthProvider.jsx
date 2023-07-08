import React, { createContext, useContext, useMemo } from 'react';
import { Navigate, Outlet } from 'react-router-dom';

import {
  CircularProgress,
} from '@mui/material';

import useAxios from 'api/axios';
import ENDPOINTS from 'api/endpoints';
import handleErrors from 'api/errors';

const AuthContext = createContext(null);

const useAuth = () => useContext(AuthContext);

const AuthProvider = ({ children }) => {
  const [{ loading: loadingProfile, data: profile }, refetchProfile] = useAxios(
    {
      url: ENDPOINTS.profile,
      method: 'GET',
    },
  );

  const [{ loading }, execute] = useAxios(
    {
      method: 'POST',
    },
    {
      manual: true,
    },
  );

  const login = async (form, validation, setError, setAlert) => {
    setAlert(null);
    try {
      await execute({
        url: ENDPOINTS.authorization,
        data: form,
      });
      window.location.reload();
    } catch (err) {
      handleErrors(validation, err.response.data.details, setError, setAlert);
    }
  };

  const register = async (form, validation, setError, setAlert) => {
    setAlert(null);
    try {
      await execute({
        url: ENDPOINTS.registration,
        data: form,
      });
      await execute({
        url: ENDPOINTS.authorization,
        data: form,
      });
      window.location.reload();
    } catch (err) {
      handleErrors(validation, err.response.data.details, setError, setAlert);
    }
  };

  const logout = async () => {
    await execute({
      url: ENDPOINTS.deauthorization,
    });
    window.location.reload();
  };

  const value = useMemo(() => ({
    loading, loadingProfile, profile, refetchProfile, login, register, logout,
  }), [loading, loadingProfile, profile]);

  return (
    <AuthContext.Provider value={value}>
      {loadingProfile && !profile
        ? (
          <div
            style={{
              minHeight: '100dvh',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
            }}
          >
            <CircularProgress />
          </div>
        ) : children}
    </AuthContext.Provider>
  );
};

const GuestRoutes = () => {
  const { profile } = useAuth();
  return !profile ? <Outlet /> : <Navigate to="/" replace />;
};

const AuthorizedRoutes = () => {
  const { profile } = useAuth();
  return profile ? <Outlet /> : <Navigate to="/sign-in" replace />;
};

export {
  AuthProvider, AuthorizedRoutes, GuestRoutes, useAuth,
};
