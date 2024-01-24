import { Button } from "@/components/ui/button"
import { InputFile } from "./upload file"
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
  } from "@/components/ui/tooltip"
  
export function UploadPredict() {
  return (
    <div className="flex  items-center space-x-1">
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger>
            <InputFile />
          </TooltipTrigger>
          <TooltipContent className="p-3">
              Choose an image file
              <br />
              image.jpg etc
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>

      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger>
            <Button className=''>Predict</Button>
          </TooltipTrigger>

          <TooltipContent className="p-3">
            Click to make image prediction
            <br />
            please make sure to check the check-box
            <br />
            for example ✅Detection ✅Segmentation
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </div>
  );
}
