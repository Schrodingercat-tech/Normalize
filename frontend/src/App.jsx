// import {CroppedImage} from "./sai-test-assects/home";
// const img = '/public/images/girl.jpg'


const img2 = '/public/images/gather.jpg'
function App() {
  return (
    <div className="cropped-container">
      <h1 className='text-3xl font-bold underline text-center'>Normalize</h1>
      <img className="cropped-image" src={img2}/>
    </div>
  );
}

export default App;
