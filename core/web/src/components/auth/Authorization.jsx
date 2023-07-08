import React, { useState } from 'react';
import { Controller, useForm } from 'react-hook-form';

import {
  Alert,
  Box,
  Container,
  CssBaseline,
  Grid,
  Link,
  TextField,
  Typography,
} from '@mui/material';

import { LoadingButton } from '@mui/lab';

import { useAuth } from 'providers/AuthProvider';

const Authorization = () => {
  const { loading, login } = useAuth();

  const validation = {
    username: {
      required: 'This field may not be blank.',
    },
    password: {
      required: 'This field may not be blank.',
    },
  };

  const [alert, setAlert] = useState(null);
  const { control, handleSubmit, setError } = useForm();

  return (
    <Container
      maxWidth="xs"
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        verticalAlign: 'center',
        minHeight: '100dvh',
      }}
    >
      <CssBaseline />
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography component="h1" variant="h5">
          Sign In
        </Typography>
        <Box component="form" sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Controller
                name="username"
                control={control}
                defaultValue=""
                rules={{
                  required: true,
                }}
                render={({
                  field: { onChange, value },
                  fieldState: { error: fieldError },
                }) => (
                  <TextField
                    onChange={onChange}
                    value={value}
                    required
                    fullWidth
                    id="username"
                    label="Username"
                    name="username"
                    autoComplete="off"
                    error={fieldError !== undefined}
                    helperText={fieldError ? fieldError.message || validation.username[fieldError.type] : ''}
                  />
                )}
              />
            </Grid>
            <Grid item xs={12}>
              <Controller
                name="password"
                control={control}
                defaultValue=""
                rules={{
                  required: true,
                }}
                render={({
                  field: { onChange, value },
                  fieldState: { error: fieldError },
                }) => (
                  <TextField
                    onChange={onChange}
                    value={value}
                    required
                    fullWidth
                    name="password"
                    label="Password"
                    type="password"
                    id="password"
                    autoComplete="current-password"
                    error={fieldError !== undefined}
                    helperText={fieldError ? fieldError.message || validation.password[fieldError.type] : ''}
                  />
                )}
              />
            </Grid>
          </Grid>
          <Grid item xs={12}>
            {alert && <Alert severity={alert.type} sx={{ mt: 2 }}>{alert.message}</Alert>}
          </Grid>
          <Grid item xs={12}>
            <LoadingButton
              type="submit"
              variant="contained"
              fullWidth
              loading={loading}
              sx={{ my: 2 }}
              onClick={handleSubmit((form) => login(form, validation, setError, setAlert))}
            >
              Sign In
            </LoadingButton>
          </Grid>
          <Grid container justifyContent="flex-end">
            <Grid item>
              <Link href="/sign-up" variant="body2">
                {'Don\'t have an account? Sign Up'}
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
};

export default Authorization;
