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
    <div className="h-screen overflow-hidden">
      <ResizablePanelGroup
        direction="horizontal"
        className="h-full w-full rounded-lg border"
      >
        <ResizablePanel defaultSize={50}>
          <div className="flex h-full items-center justify-center p-1">
            <span className="font-semibold">{page1}</span>
          </div>
        </ResizablePanel>
        <ResizableHandle />
        <ResizablePanel defaultSize={70}>
          <ResizablePanelGroup direction="vertical">
            <ResizablePanel defaultSize={50}>
              <div className="flex h-full items-center justify-center p-1">
                <span className="font-semibold">{page2}</span>
              </div>
            </ResizablePanel>
            <ResizableHandle />
            <ResizablePanel defaultSize={50}>
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


// export function ResizableDemo({
//   page1,
//   page2,
//   page3,
// }: {
//   page1: React.ReactNode;
//   page2: React.ReactNode;
//   page3: React.ReactNode;
// }) {
//   return (
//     <div className="h-screen overflow-hidden">
//       <ResizablePanelGroup
//         direction="horizontal"
//         className="h-full w-full rounded-lg border"
//       >
//         <ResizablePanel defaultSize="50%">
//           <div className="flex h-full items-center justify-center p-6">
//             <span className="font-semibold">{page1}</span>
//           </div>
//         </ResizablePanel>
//         <ResizableHandle />
//         <ResizablePanel defaultSize="50%">
//           <ResizablePanelGroup direction="vertical">
//             <ResizablePanel defaultSize="25%">
//               <div className="flex h-full items-center justify-center p-6">
//                 <span className="font-semibold">{page2}</span>
//               </div>
//             </ResizablePanel>
//             <ResizableHandle />
//             <ResizablePanel defaultSize="75%">
//               <div className="flex h-full items-center justify-center p-6">
//                 <span className="font-semibold">{page3}</span>
//               </div>
//             </ResizablePanel>
//           </ResizablePanelGroup>
//         </ResizablePanel>
//       </ResizablePanelGroup>
//     </div>
//   );
// }


