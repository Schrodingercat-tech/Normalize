import { Card } from "@/components/ui/card";
import { CheckboxDemo } from "./check box";
import { ComboboxPopover } from "./combo box";

export function VisionBar() {
    return (
      <>
        <Card className="flex gap-3  p-1 overflow-x-auto">
          <CheckboxDemo checkName="Detection" />
          <CheckboxDemo checkName="Segmentation" />
          <CheckboxDemo checkName="Pose" />
          <CheckboxDemo checkName="Text" />
          <ComboboxPopover />
        </Card>
      </>
    );
  }
  

{/* <Card 
style={{textAlign:"center", alignItems:"center", backgroundColor:'rgba(203, 159, 159, 0.5)'}} 
className="flex w-full p-2 overflow-x-auto">

<div className="flex space-x-5">
<CheckboxDemo checkName="Detection" />
<CheckboxDemo checkName="Pose" />
<CheckboxDemo checkName="Segmentation" />
<CheckboxDemo checkName="text" />
</div>

</Card> */}