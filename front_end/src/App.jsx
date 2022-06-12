import './App.css';
import { Gantt } from 'gantt-task-react';
import "gantt-task-react/dist/index.css";
import { useEffect, useState, useRef } from 'react';

const cores = {
  A: "#9400D3",
  B: "#1E90FF",
  C: "#228B22",
  D: "#008B8B",
  E: "#00FF00",
  F: "#7FFFD4",
  G: "#DAA520",
  H: "#CD5C5C",
  I: "#4B0082",
  J: "#F08080",
  K: "#8B008B",
  L: "#FF8C00",
  N: "#40E0D0",
  M: "#FF4500",
  O: "#A0522D",
  P: "#800080",
  Q: "#00FF00"
}

function App() {
  const [processList, setProcessList] = useState([]);
  const [cicle, setCicle] = useState(1);
  const [stopTimer, setStopTimer] = useState(false)
  const [start, setStart] = useState(false)

  const inputRef = useRef(null);
  const timer = useRef(null);

  useEffect(() => {
    if (start)
      fetch(`http://localhost:8030/cicle/get/${cicle}`)
        .then(res => res.json())
        .then(data => {
          if (data.detail === "Item not found")
            setStopTimer(true)
          else
            setProcessList(t => [...t, data])
        })
  }, [cicle, start]);


  useEffect(() => {
    if (stopTimer === false && start === true) {
      timer.current = setInterval(() => {
        setCicle(cicle => cicle + 1)
      }, inputRef.current.value);
    }
    return () => clearInterval(timer.current)
  }, [stopTimer, start]);

  useEffect(() => {
    if (stopTimer) {
      clearInterval(timer.current)
    }
  }, [stopTimer])

  const tasks = processList.map((process, idx) => {
    return {
      start: new Date(2020, 1, process.started_time),
      end: new Date(2020, 1, process.time),
      name: 'Processo ' + process.process.name,
      id: idx,
      type: 'task',
      progress: 100,
      isDisabled: true,
      styles: { progressColor: cores[process.process.name], progressSelectedColor: '#ff9e0d' },
    }
  })

  const actualProcess = processList[processList.length - 1]
  const processName = actualProcess?.process.name
  const real_virtual_map = actualProcess?.real_virtual_map[processName].real

  const processMap = Object.entries(actualProcess?.real_virtual_map ?? {})
    .reduce((previa, [key, value]) => {
      if (value.real === null) return previa;
      for (const num of value.real) {
        previa[num] = key;
      }
      return previa
    }, {})

  return (
    <div className="App">
      {processList.length > 0
        ? <Gantt
          tasks={tasks}
          listCellWidth=""
          TooltipContent={({ task }) => <div>Duração: {Math.abs(new Date(task.start).getDay() - new Date(task.end).getDay())}</div>}
        />
        : <p>Não há processos em execução.</p>
      }
      <div className='processin_container'>
        <div className='processin_left'>
          <p>Ultimo processo no ciclo {cicle}</p>
          <pre>
            <code>
              {actualProcess && (
                JSON.stringify({
                  done_in_this_cicle: actualProcess.done_in_this_cicle,
                  memory_counter: actualProcess.memory_counter,
                  process: actualProcess.process,
                  quantum: actualProcess.quantum,
                  overhead: actualProcess.overhead,
                  started_time: actualProcess.started_time,
                  time: actualProcess.time,
                }, null, 2)
              )}
            </code>
          </pre>
        </div>
        <div className='processin_right'>
          {Array.from({ length: 100 }, (_, idx) => (
            <div key={idx} className="memory_item">
              <span className="memory_number">{idx}</span>
              <div
                className="memory_process"
                style={{
                  background: idx in processMap && stopTimer === false
                    ? cores[processMap[idx]]
                    : "white"
                }}
              />
            </div>
          ))}
        </div>
        <label>
          <input type="number" name="cicle_time" defaultValue="2000" ref={inputRef} />
          <button onClick={() => setStart(true)} >iniciar</button>
        </label>
      </div>
    </div>
  );
}

export default App;
