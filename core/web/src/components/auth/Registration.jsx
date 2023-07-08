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

const Registration = () => {
  const { loading, register } = useAuth();

  const validation = {
    username: {
      required: 'This field may not be blank.',
      maxLength: 'No more than 150 characters.',
      pattern: 'Provide the valid username.',
    },
    password: {
      required: 'This field may not be blank.',
      minLength: 'At least 8 characters.',
      maxLength: 'No more than 128 characters.',
      pattern: 'Provide the valid password.',
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
          Sign Up
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Controller
                name="username"
                control={control}
                defaultValue=""
                rules={{
                  required: true,
                  maxLength: 150,
                  pattern: /^[\w]+$/,
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
                  minLength: 8,
                  maxLength: 128,
                  pattern: /^(?=.*\d)(?=.*[A-Za-z]).{8,128}$/,
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
                    autoComplete="new-password"
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
              onClick={handleSubmit((form) => register(form, validation, setError, setAlert))}
            >
              Sign Up
            </LoadingButton>
          </Grid>
          <Grid container justifyContent="flex-end">
            <Grid item>
              <Link href="/sign-in" variant="body2">
                Already have an account? Sign In
              </Link>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
};

export default Registration;
