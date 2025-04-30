import { useEffect, useState } from 'react';
import { useBackend } from './hooks/useBackend';

export default function App() {
  const [user, setUser] = useState('');
  const [imageSrc, setImageSrc] = useState(null);
  const backend = useBackend();

  useEffect(() => {
    if (!backend) return;
    backend.getUserInfo("1234567890").then((userInfo) => {
      console.log("user info:", JSON.stringify(userInfo, null, 2));
      setUser(userInfo);
      setImageSrc(`wysebee://openfile/?file=${userInfo.avatar}`);
    });
  }, [backend]);

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center flex-col">
      <h1 className="text-3xl font-bold mb-4">User Info</h1>
      <div className="max-w-sm mx-auto mt-10 p-6 bg-white rounded-2xl shadow-lg flex items-center space-x-4">
        <img
          className="h-16 w-16 rounded-full object-cover"
          src={imageSrc}
          alt={user.name}
        />
        <div>
          <div className="text-xl font-medium text-gray-900">{user.name}</div>
          <p className="text-gray-500">{user.email}</p>
        </div>
      </div>
    </div>
  )
}