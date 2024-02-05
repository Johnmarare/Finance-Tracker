import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './index.css';


const baseurl = "http://localhost:5000";

function Income() {
  const [description, setDescription] = useState("");
  const [amount, setAmount] = useState("");
  const [editingIncomeId, setEditingIncomeId] = useState(null);
  const [incomeList, setIncomeList] = useState([]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'description') {
      setDescription(value);
    } else if (name === 'amount') {
      setAmount(value);
    }
  };

  const fetchIncomes = async () => {
    try {
      const response = await axios.get(`${baseurl}/income`);
      const { incomes } = response.data;
      setIncomeList(incomes);
    } catch (error) {
      console.error("Error fetching incomes:", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingIncomeId) {
        // Update existing income
        await axios.put(`${baseurl}/income/${editingIncomeId}`, {
          description,
          amount: parseFloat(amount),
        });
        setEditingIncomeId(null);
      } else {
        // Create new income
        await axios.post(`${baseurl}/income`, {
          description,
          amount: parseFloat(amount),
        });
      }

      // After creating/updating the income, refetch the list
      fetchIncomes();
      // Clear the form fields
      setDescription("");
      setAmount("");
    } catch (error) {
      console.error("Error creating/updating income:", error);
    }
  };

  const handleUpdate = async (id) => {
    try {
      const response = await axios.get(`${baseurl}/income/${id}`);
      const { income } = response.data;
      setDescription(income.description);
      setAmount(income.amount);
      setEditingIncomeId(id);
    } catch (error) {
      console.error("Error fetching income for update:", error);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`${baseurl}/income/${id}`);
      const updatedList = incomeList.filter((income) => income.id !== id);
      setIncomeList(updatedList);
    } catch (err) {
      console.error(err.message);
    }
  };

  const handleCancelEdit = () => {
    setDescription("");
    setAmount("");
    setEditingIncomeId(null);
  };

  useEffect(() => {
    fetchIncomes();
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
              placeholder='income name'
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
            <button type='submit' className="btn btn-primary">{editingIncomeId ? 'Update' : 'Submit'}</button>
            {editingIncomeId && (
              <button type='button' className="btn btn-secondary ms-2" onClick={handleCancelEdit}>Cancel Edit</button>
            )}
          </div>
        </form>
      </section>

      {/* income List */}
      <div>
        <h2>income List</h2>
        <ul className="list-group">
          {incomeList.map((income) => (
            <li key={income.id} className="list-group-item d-flex justify-content-between align-items-center">
              {income.description} - {income.amount}
              <div>
                <button className="btn btn-warning me-2" onClick={() => handleUpdate(income.id)}>Edit</button>
                <button className="btn btn-danger" onClick={() => handleDelete(income.id)}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Income;
