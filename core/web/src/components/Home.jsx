import React from 'react';

import {
  Container,
} from '@mui/material';

import { LoadingButton } from '@mui/lab';

import { useAuth } from 'providers/AuthProvider';

const Home = () => {
  const { loading, logout } = useAuth();

  return (
    <Container>
      <LoadingButton
        type="button"
        variant="contained"
        loading={loading}
        sx={{ mt: 3, mb: 2 }}
        onClick={logout}
      >
        Logout
      </LoadingButton>
    </Container>
  );
};

export default Home;
