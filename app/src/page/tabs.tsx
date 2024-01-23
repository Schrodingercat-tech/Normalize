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
//import { InputFile } from "./select file"

//import image from '/images/fc41d371ceee48d3abb43750bdfdc0c6.jpeg'
// import { AspectRatio } from "@radix-ui/react-aspect-ratio"

const Vision=()=>{
  return(
    <div className="flex sapce-x-2">
      
    </div>
  );
}

export function TabsDemo() {
  return (
    <Tabs defaultValue="account" className="w-[100%]">
      <TabsList className="grid w-full grid-cols-3">
        <TabsTrigger value="account">Computer Vision</TabsTrigger>
        <TabsTrigger value="password">Vision Data</TabsTrigger>
        <TabsTrigger value="graph">Vision Graph</TabsTrigger>
      </TabsList>

      <TabsContent value="account" >
        
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
            <Card className="h-[500px] w-[100%]">
              <Vision/>
              
            </Card>
            
          </CardHeader>
          
          <CardContent className="space-y-1">
            <div className="space-y-1">
              <Label htmlFor="name">Name</Label>
              <Input id="name" defaultValue="Pedro Duarte" />
            </div>
            <div className="space-y-1">
              <Label htmlFor="username">Username</Label>
              <Input id="username" defaultValue="@peduarte" />
            </div>
          </CardContent>
          <CardFooter>
            <Button>Save changes</Button>
          </CardFooter>
        </Card>
      </TabsContent>
      <TabsContent value="password">
        <Card>
          <CardHeader>
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
