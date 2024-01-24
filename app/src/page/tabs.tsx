import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/components/ui/tabs"
// import { InputFile } from "./upload file"
// import { CheckboxDemo } from "./check box"
import { UploadPredict } from "./upload & predict"
import { VisionBar } from "./vision bar"
import { DataTableDemo } from "./data_table"
//import { InputFile } from "./select file"

//import image from '/images/fc41d371ceee48d3abb43750bdfdc0c6.jpeg'
// import { AspectRatio } from "@radix-ui/react-aspect-ratio"


export function TabsDemo({VisionTab}:{VisionTab: React.ReactNode;}
) {
  return (
    <Tabs defaultValue="account" className="w-[100%]">
      <TabsList className="grid w-full grid-cols-3">
        <TabsTrigger value="cv">Computer Vision</TabsTrigger>
        <TabsTrigger value="data">Vision Data</TabsTrigger>
        <TabsTrigger value="graph">Vision Graph</TabsTrigger>
      </TabsList>

      <TabsContent value="cv" >
        
        <Card>
          
          <CardHeader>
            <CardTitle>Norma Vision Transformers</CardTitle>
            
            
            <CardDescription >
              images are trained on yolov8 model and performs various on images like <br></br> 
              object detection
              image classification
              image segmentation 
              object detection
              pose detection
            </CardDescription>
            {VisionTab}
            
          </CardHeader>
          
          <CardFooter>
            <div className="grid grid-cols-2">
              <UploadPredict/>
              <VisionBar/>
            </div>
            
          </CardFooter>
        </Card>
      </TabsContent>
      <TabsContent value="data">
        <Card>
          <CardHeader>
            <DataTableDemo/>
            <CardTitle>Password</CardTitle>
            <CardDescription>
              Change your password here. After saving, you'll be logged out.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="space-y-1">
              <Label htmlFor="current">Current password</Label>
              <Input id="current" type="password" />
            </div>
            <div className="space-y-1">
              <Label htmlFor="new">New password</Label>
              <Input id="new" type="password" />
            </div>
          </CardContent>
          <CardFooter>
            <Button>Save password</Button>
          </CardFooter>
        </Card>
      </TabsContent>
    </Tabs>
  );
}
