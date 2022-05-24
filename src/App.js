import './App.css';
import { Gantt } from 'gantt-task-react';
import "gantt-task-react/dist/index.css";
import { useEffect, useState } from 'react';

function App() {
  const [processList, setProcessList] = useState();
  const [cicle, setCicle] = useState(1);
  // const [cicleExists, setCicleExists] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:8000/cicle/get/${cicle}`)
    .then(res => res.json())
    .then(data => setProcessList(data));
  }, [cicle]);

  console.log(processList);

  // do {
  //   cicleCount++;
  //   setCicle(cicleCount);
  // }while(cicleExists);

  return (
    <div className="App">
      {processList ? <Gantt tasks={
        [
          {
            start: new Date(2020, 1, processList.started_time), 
            end: new Date(2020, 1, processList.started_time + processList.time),
            name: 'Processo ' + processList.process.A.name,
            id: 'task0',
            type:'task',
            progress: 100,
            isDisabled: true,
            styles: { progressColor: '#ffbb54', progressSelectedColor: '#ff9e0d' },
          },
          {
            start: new Date(2020, 1, processList.started_time + 4), 
            end: new Date(2020, 1, processList.started_time + processList.time + 4),
            name: 'Processo ' + processList.process.A.name,
            id: 'task0',
            type:'task',
            progress: 100,
            isDisabled: true,
            styles: { progressColor: '#ffbb54', progressSelectedColor: '#ff9e0d' },
          },
        ]
      } /> : <p>Não há processos em execução.</p>}
      
    </div>
  );
}

export default App;