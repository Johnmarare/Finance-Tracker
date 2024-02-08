import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Bar } from 'react-chartjs-2';
import Chart from 'chart.js/auto';
import 'chartjs-adapter-date-fns';

const baseurl = "http://localhost:5000";

const Budget = () => {
  const [category, setCategory] = useState("");
  const [asigned, setAsigned] = useState("");
  const [activity, setActivity] = useState("");
  const [available, setAvailable] = useState("");
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Asigned',
        data: [],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
    ],
  });
  const [loadingChartData, setLoadingChartData] = useState(false);
  const [error, setError] = useState(null);

  // Define chartCanvasRef
  const chartCanvasRef = useRef(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    if (name === 'category') {
      setCategory(value);
    } else if (name === 'asigned') {
      setAsigned(value);
    } else if (name === 'activity') {
      setActivity(value);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Input validation
      if (isNaN(parseFloat(asigned)) || isNaN(parseFloat(activity))) {
        setError("Please enter valid numeric values for Assigned and Activity.");
        return;
      }

      // Calculate available based on assigned and activity
      const calculatedAvailable = parseFloat(asigned) - parseFloat(activity);

      // Submit the budget data to the server
      const response = await axios.post(`${baseurl}/budget`, {
        category,
        asigned: parseFloat(asigned),
        activity: parseFloat(activity),
        available: calculatedAvailable,
      });

      // After creating/updating the budget, update the chart data
      const updatedLabels = [...chartData.labels, category];
      const updatedData = [...chartData.datasets[0].data, parseFloat(asigned)];

      setChartData({
        labels: updatedLabels,
        datasets: [
          {
            label: 'Assigned',
            data: updatedData,
            backgroundColor: 'rgba(75, 192, 192, 0.6)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
          },
        ],
      });

      // Clear the form fields
      setCategory("");
      setAsigned("");
      setActivity("");
      setAvailable(calculatedAvailable.toString()); // Set the calculated available value
    } catch (error) {
      setError("Error creating/updating budget. Please try again.");
      console.error("Error creating/updating budget:", error);
    }
  };

  useEffect(() => {
    // Fetch initial chart data
    const fetchChartData = async () => {
      setLoadingChartData(true);
      try {
        const response = await axios.get(`${baseurl}/budget/chart`);
        const { labels, data } = response.data;
        setChartData({
          labels,
          datasets: [
            {
              label: 'Assigned',
              data,
              backgroundColor: 'rgba(75, 192, 192, 0.6)',
              borderColor: 'rgba(75, 192, 192, 1)',
              borderWidth: 1,
            },
          ],
        });
      } catch (error) {
        setError("Error fetching chart data. Please try again.");
        console.error("Error fetching chart data:", error);
      } finally {
        setLoadingChartData(false);
      }
    };

    fetchChartData();
  }, []);

  return (
    <div className="container-fluid">
      <section>
        <form onSubmit={handleSubmit}>
          {/* ... (rest of the form remains unchanged) */}
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
            <label htmlFor='asigned'>Asigned</label>
            <input
              type='number'
              id='asigned'
              name='asigned'
              placeholder='Asigned amount...'
              value={asigned}
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
            <input
              type='number'
              id='available'
              name='available'
              placeholder='Available amount...'
              value={available}
              onChange={handleChange}
              readOnly
            />
          </div>
          <div>
            <button type='submit' className="btn btn-primary">Submit</button>
          </div>

          {/* Loading state */}
          {loadingChartData && <p>Loading chart data...</p>}

          {/* Error message */}
          {error && <p className="text-danger">{error}</p>}
        </form>
      </section>

      {/* Render Chart */}
      <div>
        <h2>Budget Chart</h2>
        <Bar ref={chartCanvasRef} data={chartData} />
      </div>
    </div>
  );
};

export default Budget;
