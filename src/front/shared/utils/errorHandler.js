// Centralized frontend error handler
// Integrate with notification system here (useNotification) if available

function handleError(error, info) {
  try {
    // Basic logging
    // Send to remote logging endpoint in production if configured
    console.error('Captured frontend error:', error);
    if (info) console.error('Error info:', info);

    // Fallback notification: use window.alert if no notification system
    if (typeof window !== 'undefined' && window.alert) {
      try {
        window.alert('Se ha producido un error en la aplicación. Revisa la consola para más detalles.');
      } catch (e) {
        // ignore
      }
    }
  } catch (e) {
    // prevent handler from throwing
    console.error('Error inside errorHandler:', e);
  }
}

export default handleError;
