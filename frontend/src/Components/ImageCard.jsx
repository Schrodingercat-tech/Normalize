// import Button from 'react-bootstrap/Button';
// import 'bootstrap/dist/css/bootstrap.min.css';
// import 'bootstrap/dist/js/bootstrap.min.js';
// import Card from 'react-bootstrap/Card';


const cardStyle = {
    'color':'red',
    'opacity': '0.5',
   'size': '100px'
}
const img = '/public/images/girl.jpg';

export function ImageCard() {

    return(
        <div className="card">
            <div className="image-container">
                <img  src={img}/>
            </div>
            <div className="text-container">
                <h1>Image Prediction</h1>
            </div>
        </div>
    );

}
