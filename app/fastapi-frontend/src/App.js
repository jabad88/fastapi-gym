import { useState } from "react";

function App() {
  const [exercises, setExercises] = useState([]);
  const [exerciseId, setExerciseId] = useState("");
  const [exercise, setExercise] = useState(null);
  const [newName, setNewName] = useState("");
  const [newReps, setNewReps] = useState("");
  
  async function loadExercises() {
    try {
      const res = await fetch("http://localhost:8000/get_exercise");
      const data = await res.json();
      setExercises(data);
    } catch (error) {
      console.error("Error fetching exercises:", error);
    }
  }

  async function loadExerciseById() {
    if (!exerciseId) return;

    try {
      const res = await fetch(`http://localhost:8000/exercise/${exerciseId}`);
      if (!res.ok) {
        setExercise({ error: "Exercise not found!" });
        return;
      }
      const data = await res.json();
      setExercise(data);
    } catch (error) {
      console.error("Error fetching exercise by ID:", error);
    }
  }

    async function addExercise() {
    if (!newName || !newReps) return;

    try {
      const res = await fetch("http://localhost:8000/exercise", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newName, reps: parseInt(newReps) }),
      });

      if (!res.ok) {
        alert("Failed to add exercise");
        return;
      }

      const data = await res.json();
      alert(`Exercise added: ${data.name} (${data.reps} reps)`);

      // Clear form fields
      setNewName("");
      setNewReps("");

      // Optionally reload exercises list
      loadExercises();
    } catch (error) {
      console.error("Error adding exercise:", error);
    }
  }


  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h1>FastAPI Test Frontend (React)</h1>

      <div style={{ marginBottom: "20px" }}>
        <button onClick={loadExercises}>Load Exercises</button>
        <pre>{JSON.stringify(exercises, null, 2)}</pre>
      </div>

      <div style={{ marginBottom: "20px" }}>
        <h2>Add New Exercise</h2>
        <input
          type="text"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          placeholder="Exercise Name"
        />
        <input
          type="number"
          value={newReps}
          onChange={(e) => setNewReps(e.target.value)}
          placeholder="Reps"
        />
        <button onClick={addExercise}>Add Exercise</button>
      </div>


      <div>
        <h2>Get Exercise by ID</h2>
        <input
          type="number"
          value={exerciseId}
          onChange={(e) => setExerciseId(e.target.value)}
          placeholder="Enter exercise ID"
        />
        <button onClick={loadExerciseById}>Load Exercise</button>
        <pre>{JSON.stringify(exercise, null, 2)}</pre>
      </div>
    </div>
  );
}

export default App;
