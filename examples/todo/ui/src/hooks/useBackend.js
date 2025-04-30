import { useEffect, useState } from 'react';

export function useBackend() {
  const [backend, setBackend] = useState(null);

  useEffect(() => {
    if (window.wysebee) {
      setBackend(window.wysebee);
      return;
    }

    const interval = setInterval(() => {
      if (window.wysebee) {
        setBackend(window.wysebee);
        clearInterval(interval);
        console.log('Backend connection established');
      } else {
        console.log('Waiting for backend to become available...');
      }
    }, 1000); // Poll every second

    const timeout = setTimeout(() => {
      if (!window.wysebee) {
        console.error('Failed to connect to backend after 30 seconds');
        clearInterval(interval);
      }
    }, 30000);

    // Clean up on unmount
    return () => {
      clearInterval(interval);
      clearTimeout(timeout);
    };
  }, []);

  return backend;
}