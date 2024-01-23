export function ImageCard({
  children,
  imgsrc,
  ...props
}: {
  children: React.ReactNode;
  imgsrc: string;
}) {
  return (
    <>
    <div {...props} className="relative max-w-xl overflow-hidden rounded-2xl shadow-lg group">
      <img src={imgsrc} alt="image" 
      className="transition-transform 
      group-hover:scale-110 duration-300
      "
      />
    <div className="absolute inset-0 flex  items-end bg-gradient-to-t from-black/60 to-transparent"> 
        <div className="p-4 text-white">
            {children}
        </div>
    </div>
    </div>
    </>
  );
}