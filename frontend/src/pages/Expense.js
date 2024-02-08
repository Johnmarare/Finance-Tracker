import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './../components/index.css';


const baseurl = "http://localhost:5000";

function Expense() {
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const [editingExpenseId, setEditingExpenseId] = useState(null);
  const [expenseList, setExpenseList] = useState([]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'description') {
      setDescription(value);
    } else if (name === 'amount') {
      setAmount(value);
    }
  };

  const fetchExpenses = async () => {
    try {
      const response = await axios.get(`${baseurl}/expense`);
      const { expenses } = response.data;
      setExpenseList(expenses);
    } catch (error) {
      console.error("Error fetching expenses:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingExpenseId) {
        // Update existing expense
        await axios.put(`${baseurl}/expense/${editingExpenseId}`, {
          description,
          amount: parseFloat(amount),
        });
        setEditingExpenseId(null);
      } else {
        // Create new expense
        await axios.post(`${baseurl}/expense`, {
          description,
          amount: parseFloat(amount),
        });
      }

      // After creating/updating the expense, refetch the list
      fetchExpenses();
      // Clear the form fields
      setDescription("");
      setAmount("");
    } catch (error) {
      console.error("Error creating/updating expense:", error);
    }
  };

  const handleUpdate = async (id) => {
    try {
      const response = await axios.get(`${baseurl}/expense/${id}`);
      const { expense } = response.data;
      setDescription(expense.description);
      setAmount(expense.amount);
      setEditingExpenseId(id);
    } catch (error) {
      console.error("Error fetching expense for update:", error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${baseurl}/expense/${id}`);
      const updatedList = expenseList.filter((expense) => expense.id !== id);
      setExpenseList(updatedList);
    } catch (err) {
      console.error(err.message);
    }
  };

  const handleCancelEdit = () => {
    setDescription("");
    setAmount("");
    setEditingExpenseId(null);
  };

  useEffect(() => {
    fetchExpenses();
  }, []);

  return (
    <div className="container-fluid">
      <section>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor='description'>Description</label>
            <input
              type='text'
              id='description'
              name='description'
              placeholder='Expense name'
              value={description}
              onChange={handleChange}
            />
            <label htmlFor='amount'>Amount</label>
            <input
              type='number'
              id='amount'
              name='amount'
              placeholder='Amount...'
              value={amount}
              onChange={handleChange}
            />
          </div>
          <div>
            <button type='submit' className="btn btn-primary">{editingExpenseId ? 'Update' : '+ Add Expense'}</button>
            {editingExpenseId && (
              <button type='button' className="btn btn-secondary ms-2" onClick={handleCancelEdit}>Cancel Edit</button>
            )}
          </div>
        </form>
      </section>

      {/* Expense List */}
      <div>
        <h2>Expense List</h2>
        <ul className="list-group">
          {expenseList.map((expense) => (
            <li key={expense.id} className="list-group-item d-flex justify-content-between align-items-center">
              {expense.description} - {expense.amount}
              <div>
                <button className="btn btn-warning me-2" onClick={() => handleUpdate(expense.id)}>Edit</button>
                <button className="btn btn-danger" onClick={() => handleDelete(expense.id)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Expense;
