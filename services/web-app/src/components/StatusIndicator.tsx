import React, { useState, useEffect } from 'react';
import { Activity, AlertCircle, CheckCircle } from 'lucide-react';

interface StatusIndicatorProps {
  apiBaseUrl: string;
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({ apiBaseUrl }) => {
  const [status, setStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const response = await fetch(`${apiBaseUrl}/health`);
        setStatus(response.ok ? 'online' : 'offline');
      } catch {
        setStatus('offline');
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30 seconds

    return () => clearInterval(interval);
  }, [apiBaseUrl]);

  const getStatusConfig = () => {
    switch (status) {
      case 'online':
        return {
          icon: CheckCircle,
          text: 'API Online',
          color: 'text-green-600',
          bgColor: 'bg-green-100',
        };
      case 'offline':
        return {
          icon: AlertCircle,
          text: 'API Offline',
          color: 'text-red-600',
          bgColor: 'bg-red-100',
        };
      default:
        return {
          icon: Activity,
          text: 'Checking...',
          color: 'text-yellow-600',
          bgColor: 'bg-yellow-100',
        };
    }
  };

  const config = getStatusConfig();
  const Icon = config.icon;

  return (
    <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-sm font-medium ${config.color} ${config.bgColor}`}>
      <Icon className="h-4 w-4" />
      <span>{config.text}</span>
    </div>
  );
};