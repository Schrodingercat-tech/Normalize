import Card from 'react-bootstrap/Card';

const styles = {
    'color' : 'red',
    'opacity' : '0.5',
    'size' : '100px'
}
const girl = '/public/images/girl.jpg'
export function ImageAndTextExample() {
  return (
    <>
      <Card>
        <Card.Img variant="top" src={girl} />
        <Card.Body>
          <Card.Text>
          <Card.Title style={styles}>
            Image Prediction
            <Card.Header>
                Vision task
            </Card.Header>
          </Card.Title>
          </Card.Text>
        </Card.Body>
      </Card>
    </>
  );
}


export default ImageAndTextExample;