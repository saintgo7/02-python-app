import React, { useState } from 'react';
import { useQuery } from 'react-query';
import api from '../api/client';
import toast from 'react-hot-toast';

interface Item {
  id: number;
  name: string;
  description: string;
  created_at: string;
}

export default function ItemsPage() {
  const [skip, setSkip] = useState(0);
  const [limit, setLimit] = useState(10);
  const [newItemName, setNewItemName] = useState('');
  const [newItemDesc, setNewItemDesc] = useState('');

  const { data: items, isLoading, refetch } = useQuery<Item[]>(
    ['items', skip, limit],
    () => api.get('/items', { params: { skip, limit } }).then((res) => res.data),
    { staleTime: 30000 }
  );

  const handleCreateItem = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/items', {
        name: newItemName,
        description: newItemDesc,
      });
      toast.success('Item created!');
      setNewItemName('');
      setNewItemDesc('');
      refetch();
    } catch (error: any) {
      toast.error('Failed to create item');
    }
  };

  const handleDeleteItem = async (id: number) => {
    try {
      await api.delete(`/items/${id}`);
      toast.success('Item deleted!');
      refetch();
    } catch (error: any) {
      toast.error('Failed to delete item');
    }
  };

  return (
    <div className="items-page">
      <h1>Items</h1>

      <form onSubmit={handleCreateItem} className="create-form">
        <input
          type="text"
          placeholder="Item name"
          value={newItemName}
          onChange={(e) => setNewItemName(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Description"
          value={newItemDesc}
          onChange={(e) => setNewItemDesc(e.target.value)}
        />
        <button type="submit">Add Item</button>
      </form>

      {isLoading ? (
        <p>Loading items...</p>
      ) : (
        <div className="items-list">
          {items?.map((item) => (
            <div key={item.id} className="item-card">
              <h3>{item.name}</h3>
              <p>{item.description}</p>
              <small>{new Date(item.created_at).toLocaleDateString()}</small>
              <button
                onClick={() => handleDeleteItem(item.id)}
                className="delete-btn"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
