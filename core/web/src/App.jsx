import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import {
  createTheme,
  ThemeProvider,
} from '@mui/material/styles';

import { AuthorizedRoutes, AuthProvider, GuestRoutes } from 'providers/AuthProvider';

import Authorization from 'components/auth/Authorization';
import Registration from 'components/auth/Registration';
import Home from 'components/Home';
import NotFound from 'components/NotFound';

import styles from 'styles/colors.scss';

import 'App.scss';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: styles.red,
    },
    background: {
      default: styles.dark,
    },
  },
});

const App = () => (
  <ThemeProvider theme={theme}>
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route element={<GuestRoutes />}>
            <Route path="/sign-in" element={<Authorization />} />
            <Route path="/sign-up" element={<Registration />} />
          </Route>
          <Route element={<AuthorizedRoutes />}>
            <Route path="/" element={(<Home />)} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  </ThemeProvider>
);

export default App;
