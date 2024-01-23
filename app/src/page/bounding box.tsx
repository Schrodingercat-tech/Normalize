import React from 'react';

interface BoundingBoxProps {
  xmin: number;
  xmax: number;
  ymin: number;
  ymax: number;
  imageWidth: number;
  imageHeight: number;
}

const BoundingBox: React.FC<BoundingBoxProps> = ({
  xmin,
  xmax,
  ymin,
  ymax,
  imageWidth,
  imageHeight,
}) => {
  // Calculate the width and height of the bounding box
  const boxWidth = xmax - xmin;
  const boxHeight = ymax - ymin;

  // Calculate the percentage width and height relative to the image size
  const percentWidth = (boxWidth / imageWidth) * 100;
  const percentHeight = (boxHeight / imageHeight) * 100;

  // Calculate the percentage left and top based on xmin and ymin
  const percentLeft = (xmin / imageWidth) * 100;
  const percentTop = (ymin / imageHeight) * 100;

  // Inline styles for the bounding box
  const boundingBoxStyles: React.CSSProperties = {
    position: 'absolute',
    left: `${percentLeft}%`,
    top: `${percentTop}%`,
    width: `${percentWidth}%`,
    height: `${percentHeight}%`,
    border: '2px solid red', // Adjust the border style as needed
    boxSizing: 'border-box',
  };

  return <div style={boundingBoxStyles}></div>;
};

