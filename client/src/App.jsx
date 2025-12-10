import 'primereact/resources/themes/saga-blue/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
//https://primereact.org/theming/
import { Button } from 'primereact/button';
import React, {useState, useEffect} from 'react'
//Componenets used to make basic UI design structure
import { Card } from 'primereact/card';
import { Divider } from 'primereact/divider';
import { Panel } from 'primereact/panel';
import { Splitter, SplitterPanel } from 'primereact/splitter';

//Select AI
import { PanelMenu } from 'primereact/panelmenu';
import { CascadeSelect } from 'primereact/cascadeselect';
import { Carousel } from 'primereact/carousel';
        
//Charts
import { Chart } from 'primereact/chart';

//Governance warning messages
import { Messages } from 'primereact/messages';
        
//swapping between AI's
import { Skeleton } from 'primereact/skeleton';
import { ProgressSpinner } from 'primereact/progressspinner';
        
//Looks kinda cool myb a background toy
import { Ripple } from 'primereact/ripple';

import DoughnutChartDemo from './chart.jsx'
import ComboChartDemo from './combochart.jsx'
import LineGraphDemo from './linegraph.jsx';
import { Calendar } from 'primereact/calendar';
import { InputText } from "primereact/inputtext";
import { Dropdown } from 'primereact/dropdown';
import './App.css';
         
function App() {
  const [selectedAI, setSelectedAI] = useState("gemma3:1b");
  const [selectedTable, setSelectedTable] = useState("base");
  const [processData, setProcessData] = useState("process")
  const [AIs, setAIs] = useState([]);
  const [table, setTable] = useState([]);
  const [data, setData] = useState()
  const [Budget, setBudget] = useState(null);
  const [dates, setDates] = useState(null);

  const apiUrl = import.meta.env.VITE_API_URL;
  console.log(apiUrl)

  useEffect(() => {
    console.log("useEffect ran, apiUrl:", apiUrl);

    fetch(`${apiUrl}/models`)
      .then(res => {
        console.log("Got response:", res);
        return res.json();
      })
      .then(AIs => {
        console.log("Parsed JSON:", AIs);
        setAIs(AIs);
        setSelectedAI(AIs[0]);
      })
      .catch(err => {
        console.error("Error fetching models:", err);
      });
  }, []);

  useEffect(() => {
    fetch(`${apiUrl}/tables`)
      .then(res => res.json())
      .then(tables => {
        setTable(tables);
        console.log(tables)
        setSelectedTable(tables[0])
      })
      .catch(err => {
        console.error('Error fetching Tables:', err);
      });
  }, []);

  useEffect(() => {
    fetch(`${apiUrl}/data?model=${selectedAI.name}`).then(
      res => res.json()
    ).then(
      data => {
        setData(data[selectedTable.name])
      }).catch(err => {
        console.error('Error fetching Data:', err);
      });
   //https://stackoverflow.com/questions/45992682/calling-functions-after-state-change-occurs-in-reactjs Aishwarya Harpale
  }, [selectedAI, selectedTable])

  useEffect(() => {
    fetch(`${apiUrl}/processData?model=${selectedAI.name}&dates=${dates}`).then(
      res => res.json()
    ).then(
      processData => {
        console.log(dates)
        console.log(processData)
        setProcessData(processData)
      }).catch(err => {
        console.error('Error fetching Processing Data:', err);
      });
   //https://st, daackoverflow.com/questions/45992682/calling-functions-after-state-change-occurs-in-reactjs Aishwarya Harpale
  }, [selectedAI, dates])

  return (
    <div className = "Website">
      <main>
            <Dropdown value={selectedAI} onChange={(e) => setSelectedAI(e.value)} options={AIs} optionLabel="name"
              placeholder="Select an AI" className="dropdown"/>
            <Dropdown value={selectedTable} onChange={(e) => setSelectedTable(e.value)} options={table} optionLabel="name"
              placeholder="Select a Table" className="dropdown" />
            
            <Calendar value={dates} onChange={(e) => setDates(e.value)} showIcon selectionMode="range" readOnlyInput hideOnRangeSelection className = "calendar" />
            <InputText value={Budget} onChange={(e) => setBudget(e.target.value)} keyfilter="float
            " placeholder="Budget" className="budget"/>
            <Divider />
        <div className='UI'>
              <Card title="Accuracy" subTitle="How often a model's predictions are correct, incorrect or unattempted." className="graph">
                <DoughnutChartDemo 
                  correct={data?.[2] ?? 0}
                  incorrect={data?.[3] ?? 0}
                  unattempted={data?.[4] ?? 0}
                />
              </Card>
              <Card title="Cost" subTitle={`The cost associated to run a query on ${selectedAI.name}`} className="graph">               
                <ComboChartDemo
                  labels={processData?.[4] ?? []}
                  dataset={processData?.[1] ?? []}
                  budget={Budget ?? 0}
                />
              </Card>
        </div>
        <Divider />
        <div className="lowerrow">
          <Card title="Overall Correct" className="icard">
            <div className="infocard">
              <div className="infocard-inner">
                <div className="infocard-front">
                  <p>
                    {(data?.[2] ?? 0)} / {(data?.[2] ?? 0) + (data?.[3] ?? 0) + (data?.[4] ?? 0)}
                  </p>
                </div>
                <div className="infocard-back">
                  <p>Total number of questions that were answered correctly</p>
                </div>
              </div>
            </div>
          </Card>
          <Card title="Hallucination Rate" className="icard">
            <div className="infocard">
              <div className="infocard-inner">
                <div className="infocard-front">
                  <p>
                    {(data?.[3] ?? 0)} / {(data?.[2] ?? 0) + (data?.[3] ?? 0)}
                  </p>
                </div>
                <div className="infocard-back">
                  <p>The frequency at which an artificial intelligence (AI) system, particularly a large language model (LLM), generates incorrect, nonsensical, or misleading information</p>
                </div>
              </div>
            </div>
          </Card>
          <Card title="F Score" className="icard">
            <div className="infocard">
              <div className="infocard-inner">
                <div className="infocard-front">
                  <p>
                    {Number((2 * (data?.[2] ?? 0)) / ((data?.[4] ?? 0) + (data?.[2] ?? 0) + (data?.[3] ?? 0))*100).toPrecision(3)}%
                  </p>
                </div>
                <div className="infocard-back">
                  <p>Precision: Measures the proportion of positive identifications that were actually correct. A high precision means the model has fewer false positives.</p>
                </div>
              </div>
            </div>
          </Card>
          <Card title="Accuracy Rate" className="icard">
            <div className="infocard">
              <div className="infocard-inner">
                <div className="infocard-front">
                  <p>
                    {(data?.[2] ?? 0)} / {(data?.[2] ?? 0) + (data?.[3] ?? 0)}
                  </p>
                </div>
                <div className="infocard-back">
                  <p>The number of questions the model answered correctly, out of only questions that were attempted (i.e., questions answered correct and incorrectly).</p>
                </div>
              </div>
            </div>
          </Card>
        </div>
        <div className = "MidGraph">
          <Card title="Latency" subTitle="The time delay it takes between prompt and response, measured in milliseconds (ms)" className="largegraph">
            <LineGraphDemo
              title={"Latency"}
              labels={processData?.[4] ?? []}
              dataset={processData?.[0] ?? []}
              colour={'#00C5DE'}
            />        
          </Card>
        </div>
        <Divider />
        <div className="UI">
          <Card title="Memory Usage" subTitle="The amount of RAM (Random Access Memory) a program, process, or computer system is actively using to run in megabytes (mb)" className="graph">
            <LineGraphDemo
              title={"Memory Usage"}
              labels={processData?.[4] ?? []}
              dataset={processData?.[3] ?? []}
              colour={'#00C5DE'}
            /> 
          </Card>
          <Card title="CPU Usage" subTitle="CPU usage is the percentage of processor power being used to run instructions that is currently in use" className="graph">
            <LineGraphDemo
              title={"CPU Usage"}
              labels={processData?.[4] ?? []}
              dataset={processData?.[2] ?? []}
              colour={'#00C5DE'}
            /> 
          </Card>
        </div>
      </main>
    </div>
  );
}

export default App
