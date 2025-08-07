import React, { useEffect, useState } from "react";
import axios from "axios";
import { LineChart, Line, XAxis, YAxis, Tooltip, ReferenceDot } from "recharts";

export default function OilChart() {
  const [data, setData] = useState([]);
  const [events, setEvents] = useState([]);
  const [changePoint, setChangePoint] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/api/oil-prices")
      .then((res) => setData(res.data));
    axios
      .get("http://127.0.0.1:5000/api/events")
      .then((res) => setEvents(res.data));
    axios
      .get("http://127.0.0.1:5000/api/change-point")
      .then((res) => setChangePoint(res.data));
  }, []);

  return (
    <div>
      <h2>Brent Oil Prices Over Time</h2>
      <LineChart width={1000} height={400} data={data}>
        <XAxis dataKey="Date" />
        <YAxis dataKey="Price" />
        <Tooltip />
        <Line type="monotone" dataKey="Price" stroke="#8884d8" />

        {changePoint && (
          <ReferenceDot
            x={changePoint.change_date}
            y={data.find((d) => d.Date === changePoint.change_date)?.Price}
            r={5}
            fill="red"
            label="Change Point"
          />
        )}
      </LineChart>

      <div style={{ marginTop: "20px" }}>
        {changePoint && (
          <div>
            <strong>Detected Change Point:</strong> {changePoint.change_date}
            <br />
            Mean shifted from {changePoint.mu1.toFixed(5)} to{" "}
            {changePoint.mu2.toFixed(5)}
            <br />
            Percent change: <b>{changePoint.percent_change}%</b>
          </div>
        )}
      </div>
    </div>
  );
}
