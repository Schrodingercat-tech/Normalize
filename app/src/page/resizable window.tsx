import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";

export function ResizableDemo({
  page1,
  page2,
  page3,
}: {
  page1: React.ReactNode;
  page2: React.ReactNode;
  page3: React.ReactNode;
}) {
  return (
    <div className="h-[70vh] overflow-hidden">
      <ResizablePanelGroup
        direction="horizontal"
        className="h-[80px] w-full rounded-lg border"
      >
        <ResizablePanel defaultSize={50}>
          <div className="flex h-full items-center justify-center p-1">
            <span className="font-semibold">
              <h1>Original Image</h1>
              <br></br>
              {page1}
              </span>
          </div>
        </ResizablePanel>
        <ResizableHandle />
        <ResizablePanel defaultSize={55}>
          <ResizablePanelGroup direction="vertical">
            <ResizablePanel defaultSize={50}>
              <div className="flex h-full items-center justify-center p-1">
                <span className="font-semibold">{page2}</span>
              </div>
            </ResizablePanel>
            <ResizableHandle />
            <ResizablePanel defaultSize={30}>
              <div className="flex h-full items-center justify-center p-1 m-0">
                <span className="font-semibold">{page3}</span>
              </div>
            </ResizablePanel>
          </ResizablePanelGroup>
        </ResizablePanel>
      </ResizablePanelGroup>
    </div>
  );
}


