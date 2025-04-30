import { useEffect, useState } from 'react';
import { useBackend } from './hooks/useBackend';

export default function App() {
  const [todoList, setTodoList] = useState(null);
  const backend = useBackend();

  useEffect(() => {
    if (!backend) return;
    backend.getTodoList().then((todoList) => {
      console.log("todo list:", JSON.stringify(todoList, null, 2));
      setTodoList(todoList);
    });
  }, [backend]);

  return (
    <div className="max-w-xl mx-auto mt-10 space-y-4">
      <h1 className="text-3xl font-bold mb-4">TODO List</h1>
      {todoList && todoList.map((todo) => (
        <div
          key={todo.id}
          className={`flex items-center justify-between p-4 rounded-2xl shadow-md ${
            todo.completed ? "bg-green-50" : "bg-yellow-50"
          }`}
        >
          <div>
            <h2 className="text-lg font-medium text-gray-900">{todo.title}</h2>
            <p className="text-sm text-gray-500">ID: {todo.id} | User: {todo.userId}</p>
          </div>
          <span
            className={`text-sm font-semibold px-3 py-1 rounded-full ${
              todo.completed
                ? "bg-green-100 text-green-700"
                : "bg-yellow-100 text-yellow-700"
            }`}
          >
            {todo.completed ? "Completed" : "Pending"}
          </span>
        </div>
      ))}
    </div>
  )
}