import React, { useState, useEffect } from 'react';
import { useApi } from '../contexts/ApiProvider';
import 'bootstrap/dist/css/bootstrap.min.css';

const Budget = () => {
  const [category, setCategory] = useState("");
  const [assigned, setAssigned] = useState("");
  const [activity, setActivity] = useState("");
  const [available, setAvailable] = useState("");
  const [editingBudgetId, setEditingBudgetId] = useState(null);
  const [budgetList, setBudgetList] = useState([]);
  const [error, setError] = useState(null);
  const api = useApi();

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'category') {
      setCategory(value);
    } else if (name === 'assigned') {
      setAssigned(value);
    } else if (name === 'activity') {
      setActivity(value);
    }
  };

  const fetchBudgets = async () => {
    try {
      const response = await api.get('/budget');
      const { budgets } = response.body;
      setBudgetList(budgets);
    } catch (error) {
      console.error("Error fetching budgets:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Input validation
      if (isNaN(parseFloat(assigned)) || isNaN(parseFloat(activity))) {
        setError("Please enter valid numeric values for Assigned and Activity.");
        return;
      }

      // Calculate available based on assigned and activity
      available = parseFloat(assigned) - parseFloat(activity);
      setAvailable = available;

      if (editingBudgetId) {
        // Update existing budget
        await api.put(`/budget/${editingBudgetId}`, {
          category,
          assigned: parseFloat(assigned),
          activity: parseFloat(activity),
          available: available,
        });
        setEditingBudgetId(null);
      } else {
        // Create new budget
        await api.post('/budget', {
          category,
          assigned: parseFloat(assigned),
          activity: parseFloat(activity),
          available: available,
        });
      }

      // After creating/updating the budget, refetch the list
      fetchBudgets();
      // Clear the form fields and error state
      setCategory("");
      setAssigned("");
      setActivity("");
      setError(null);
    } catch (error) {
      console.error("Error creating/updating budget:", error);
    }
  };

  const handleUpdate = async (id) => {
    try {
      const response = await api.get(`/budget/${id}`);
      const { budget } = response.body;
      setCategory(budget.category);
      setAssigned(budget.assigned);
      setActivity(budget.activity);
      setEditingBudgetId(id);
    } catch (error) {
      console.error("Error fetching budget for update:", error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await api.delete(`/budget/${id}`);
      const updatedList = budgetList.filter((budget) => budget.id !== id);
      setBudgetList(updatedList);
    } catch (err) {
      console.error(err.message);
    }
  };

  const handleCancelEdit = () => {
    setCategory("");
    setAssigned("");
    setActivity("");
    setEditingBudgetId(null);
  };

  useEffect(() => {
    const fetchBudgets = async () => {
      try {
        const response = await api.get('/budget');
        const { budgets } = response.body;
        setBudgetList(budgets);
      } catch (error) {
        console.error("Error fetching budgets:", error);
      }
    };

    fetchBudgets();
}, [api]);
  

  return (
    <div className="container-fluid">
      <section>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor='category'>Category</label>
            <input
              type='text'
              id='category'
              name='category'
              placeholder='Budget category'
              value={category}
              onChange={handleChange}
            />
            <label htmlFor='assigned'>Assigned</label>
            <input
              type='number'
              id='assigned'
              name='assigned'
              placeholder='Assigned amount...'
              value={assigned}
              onChange={handleChange}
            />
            <label htmlFor='activity'>Activity</label>
            <input
              type='number'
              id='activity'
              name='activity'
              placeholder='Activity amount...'
              value={activity}
              onChange={handleChange}
            />
            <label htmlFor='available'>Available</label>
            <output value={available} id='available' name='available'>{available}</output>
          </div>
          <div>
            <button type='submit' className="btn btn-primary">Submit</button>
            {editingBudgetId && (
              <button type='button' className="btn btn-secondary ms-2" onClick={handleCancelEdit}>Cancel Edit</button>
            )}
          </div>
        </form>
      </section>

      {/* Budget List */}
      <div>
        <h2>Budget List</h2>
        <ul className="list-group">
          {budgetList && budgetList.map((budget) => (
            <li key={budget.id}>
              {budget.category} - Assigned: {budget.assigned}, Activity: {budget.activity}, Available: {budget.available}
              <div>
                <button className="btn btn-warning me-2" onClick={() => handleUpdate(budget.id)}>Edit</button>
                <button className="btn btn-danger" onClick={() => handleDelete(budget.id)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Budget;