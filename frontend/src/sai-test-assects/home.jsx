import { useState,useEffect} from 'react';
import Papa from 'papaparse'; 

const img = '/public/images/girl.jpg'
const apiUrl = 'http://127.0.0.1:8000/';

export const FetchData = async ({ url = apiUrl }) => {
  try {
    const response = await fetch(url);
    const data = await response.json();  // Use .json() to parse JSON response
    return data;
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error;
  }
};

export function Wish(apiUrl) {
  const [data, setData] = useState(null);

  const handleButtonClick = async () => {
    try {
      const result = await FetchData({apiUrl });  // Pass apiUrl as an object property
      setData(result);
    } catch (error) {
      // Handle error, e.g., show an error message
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div>
      <h2>Fetch Data from fast api</h2>
      <button onClick={handleButtonClick}>Fetch Data</button>
      {data ? (
        <p>{data.hi}</p>  // Access the 'hi' property from the response
      ) : (
        <p>Click the button to fetch data</p>
      )}
    </div>
  );
}


export function Test(){
    return(
        <div>
            <p> this task is to crop image with in react</p>
            <img src={img} alt="description" />
        </div>
    );
}



export function CSVTable() {

  const [data, setData] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const response = await fetch('/data.csv');
      const reader = response.body.getReader();
      const result = await reader.read(); // raw array buffer
     
      const parsed = Papa.parse(result.value, {header: true}); // parse csv
      const rows = parsed.data;
      setData(rows);
    }

    fetchData();
  }, []);

  return (
    <table>
      <thead>
        <tr>
          {data[0] && Object.keys(data[0]).map(key => (
            <th key={key}>{key}</th>  
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map(row => (
          <tr key={row.id}>
            {Object.values(row).map(val => (
              <td key={val}>{val}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );

}
