import React from 'react';
import ReactDOM from 'react-dom/client';
import { RouterProvider } from 'react-router-dom';
import { router } from './routes/routes';
import { StoreProvider } from './hooks/useGlobalReducer';
import './styles/index.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import ErrorBoundary from './shared/components/ErrorBoundary';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <ErrorBoundary>
            <StoreProvider>
                <RouterProvider router={router} />
            </StoreProvider>
        </ErrorBoundary>
    </React.StrictMode>
);