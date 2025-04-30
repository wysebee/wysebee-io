import { useEffect, useState } from 'react';
import { useBackend } from './hooks/useBackend';

export default function App() {
  const [imageList, setImageList] = useState('');
  const backend = useBackend();

  useEffect(() => {
    if (!backend) return;
    backend.getImages().then((images) => {
      console.log("image list:", JSON.stringify(images, null, 2));
      const list = [];
      images.forEach((image) => {
        console.log("image:", image);
        list.push(`wysebee://openfile/?file=${image}`);
      });
      setImageList(list);
    });
  }, [backend]);

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold mb-6 text-center">Image Gallery</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {imageList && imageList.map((img, index) => (
          <div key={index} className="overflow-hidden rounded-2xl shadow-md hover:shadow-xl transition-shadow duration-300">
            <img
              src={img}
              alt={`Gallery image ${index + 1}`}
              className="w-full h-64 object-cover hover:scale-105 transition-transform duration-300"
            />
          </div>
        ))}
      </div>
    </div>
  )
}