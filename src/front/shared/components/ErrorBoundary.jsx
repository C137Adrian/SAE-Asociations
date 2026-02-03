import React from 'react';
import handleError from '../utils/errorHandler';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    // Log the error to consol and to centralized handler
    handleError(error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="container py-5 text-center">
          <h2>Ha ocurrido un error inesperado</h2>
          <p>Lo sentimos. Puedes recargar la página o intentar más tarde.</p>
          <button className="btn btn-primary" onClick={() => window.location.reload()}>
            Recargar
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
