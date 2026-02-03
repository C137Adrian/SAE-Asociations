import React, { Suspense, lazy } from 'react';
import { createBrowserRouter } from 'react-router-dom';
import Layout from '../pages/Layout';
const Home = lazy(() => import('../pages/Home'));
const Login = lazy(() => import('../pages/Login'));
const RegisterUser = lazy(() => import('../pages/RegisterUser'));
const RegisterAssociation = lazy(() => import('../pages/RegisterAssociation'));
const EventDetail = lazy(() => import('../pages/EventDetail'));
const EventList = lazy(() => import('../pages/EventList'));
const EventCreation = lazy(() => import('../pages/EventCreation'));
const AssociationList = lazy(() => import('../pages/AssociationList'));
const AssociationDetail = lazy(() => import('../pages/AssociationDetail'));
const DonateForm = lazy(() => import('../pages/DonateForm'));
const Donations = lazy(() => import('../pages/Donations'));
const DonationSuccess = lazy(() => import('../pages/DonationSuccess'));
const DonationCancel = lazy(() => import('../pages/DonationCancel'));
const AccountSettings = lazy(() => import('../pages/AccountSettings'));
import AuthValidator from '../components/AuthValidator';
const ForgotPassword = lazy(() => import('../components/ForgotPassword'));
const ResetPassword = lazy(() => import('../components/ResetPassword'));

const ProtectedLayout = () => (
  <AuthValidator>
    <Suspense fallback={<div className="text-center py-5">Cargando...</div>}>
      <Layout />
    </Suspense>
  </AuthValidator>
);

const routerConfig = {
  future: {
    v7_startTransition: true,
    v7_relativeSplatPath: true
  },
  routes: [
    {
      path: "/",
      element: <ProtectedLayout />,
      children: [
        {
          index: true,
          element: (
            <Suspense fallback={<div className="text-center py-5">Cargando...</div>}>
              <Home />
            </Suspense>
          )
        },
        {
          path: "login",
          element: (
            <Suspense fallback={<div className="text-center py-5">Cargando...</div>}>
              <Login />
            </Suspense>
          )
        },
        {
          path: "register/user",
          element: <RegisterUser />
        },
        {
          path: "register/association",
          element: <RegisterAssociation />
        },
        // Password Recovery Routes
        {
          path: "forgot-password",
          element: <ForgotPassword />
        },
        {
          path: "reset-password/:token",
          element: <ResetPassword />
        },
        {
          path: "account/settings",
          element: <AccountSettings />
        },
        {
          path: "event/detail/:id",
          element: (
            <Suspense fallback={<div className="text-center py-5">Cargando evento...</div>}>
              <EventDetail />
            </Suspense>
          )
        },
        {
          path: "event/list",
          element: (
            <Suspense fallback={<div className="text-center py-5">Cargando lista...</div>}>
              <EventList />
            </Suspense>
          )
        },
        {
          path: "event/list/:association_id",
          element: <EventList />
        },
        {
          path: "event/creation",
          element: (
            <Suspense fallback={<div className="text-center py-5">Cargando editor...</div>}>
              <EventCreation />
            </Suspense>
          )
        },
        {
          path: "associations",
          element: (
            <Suspense fallback={<div className="text-center py-5">Cargando asociaciones...</div>}>
              <AssociationList />
            </Suspense>
          )
        },
        {
          path: "association/:id",
          element: (
            <Suspense fallback={<div className="text-center py-5">Cargando asociación...</div>}>
              <AssociationDetail />
            </Suspense>
          )
        },
        {
          path: "donations",
          element: (
            <Suspense fallback={<div className="text-center py-5">Cargando donaciones...</div>}>
              <Donations />
            </Suspense>
          )
        },
        {
          path: "donate/association/:id",
          element: (
            <Suspense fallback={<div className="text-center py-5">Cargando formulario de donación...</div>}>
              <DonateForm />
            </Suspense>
          )
        },
        {
          path: "donation-success",
          element: <DonationSuccess />
        },
        {
          path: "donation-cancel",
          element: <DonationCancel />
        },
        {
          path: "*",
          element: <Home />
        }
      ]
    }
  ]
};

export const router = createBrowserRouter(routerConfig.routes, routerConfig);