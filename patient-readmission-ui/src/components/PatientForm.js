import React, { useState } from "react";
import axios from "axios";

const API_URL = "https://0fut5yz7b4.execute-api.us-east-1.amazonaws.com/prod/predict";

export default function PatientForm({ onResult }) {
  // Example features — adapt to your model features
  const [form, setForm] = useState({
    age: 45,
    gender: 0, // 0=M,1=F – your encoding may differ
    num_prior_admissions: 1,
    lab_result_1: 100,
    lab_result_2: 5,
    vital_bp: 120,
    length_of_stay: 3
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((s) => ({ ...s, [name]: value }));
  };

  const buildCsv = (f) => {
    // build CSV string in the model's expected order
    return [
      f.age,
      f.gender,
      f.num_prior_admissions,
      f.lab_result_1,
      f.lab_result_2,
      f.vital_bp,
      f.length_of_stay
    ].join(",");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const csv = buildCsv(form);

      // Our Lambda expects JSON with "body": JSON-string (if proxy), but endpoint accepts direct too.
      // We will send the body wrapper (works with your Lambda)
      const payload = { body: JSON.stringify({ input: csv }) };

      const res = await axios.post(API_URL, payload);
      // Lambda returns { statusCode:200, body: '{"prediction":"0.23\n"}' }
      let body = res.data;
      if (body.body) body = JSON.parse(body.body);

      const prediction = parseFloat(body.prediction);
      onResult({ prediction, raw: body.prediction });
    } catch (err) {
      console.error(err);
      setError(err.message || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h4 className="text-lg font-semibold mb-4">Patient Input</h4>

      <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="text-sm font-medium">Age</label>
          <input name="age" type="number" value={form.age} onChange={handleChange}
                 className="w-full mt-1 p-2 border rounded" />
        </div>

        <div>
          <label className="text-sm font-medium">Gender (0=M,1=F)</label>
          <input name="gender" type="number" value={form.gender} onChange={handleChange}
                 className="w-full mt-1 p-2 border rounded" />
        </div>

        <div>
          <label className="text-sm font-medium">Prior admissions</label>
          <input name="num_prior_admissions" type="number" value={form.num_prior_admissions} onChange={handleChange}
                 className="w-full mt-1 p-2 border rounded" />
        </div>

        <div>
          <label className="text-sm font-medium">Length of stay (days)</label>
          <input name="length_of_stay" type="number" value={form.length_of_stay} onChange={handleChange}
                 className="w-full mt-1 p-2 border rounded" />
        </div>

        <div>
          <label className="text-sm font-medium">Lab test 1</label>
          <input name="lab_result_1" type="number" value={form.lab_result_1} onChange={handleChange}
                 className="w-full mt-1 p-2 border rounded" />
        </div>

        <div>
          <label className="text-sm font-medium">Lab test 2</label>
          <input name="lab_result_2" type="number" value={form.lab_result_2} onChange={handleChange}
                 className="w-full mt-1 p-2 border rounded" />
        </div>

        <div>
          <label className="text-sm font-medium">Vital BP</label>
          <input name="vital_bp" type="number" value={form.vital_bp} onChange={handleChange}
                 className="w-full mt-1 p-2 border rounded" />
        </div>

        <div className="md:col-span-2 flex items-center gap-3">
          <button type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded font-semibold disabled:opacity-50"
                  disabled={loading}>
            {loading ? "Predicting…" : "Predict Readmission Risk"}
          </button>

          {error && <div className="text-sm text-red-600">{error}</div>}
        </div>
      </form>
    </div>
  );
}
