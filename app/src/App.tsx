import './App.css'
import { ImageCard } from './page/image card'
import { ResizableDemo } from './page/resizable window'
import { TabsDemo } from './page/tabs';
import image from '/images/nebula.jpg'
// import { TabsDemo } from './page/tabs'
// import { Button } from './components/ui/button'
// import { CardWithForm } from './page/card'
// import { DataTableDemo } from './page/data_table'
const Imgcontent = () => {
  return (
    <>
      <ImageCard
        children={
          <h1>
            Norma : Vision Transformers @__sAi__
            <></>
          </h1>
        }
        imgsrc={image}
      />
    </>
  );
};

function App() {
  return (
    <>
      
      <TabsDemo
      VisionTab={<ResizableDemo page1={<Imgcontent />} 
      page2={<Imgcontent />}
      page3={<Imgcontent />}
      
      />}
      />
    </>
  );
}

export default App



