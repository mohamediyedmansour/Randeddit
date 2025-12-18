export default function NSFWWarning() {
  return (
    <div className="transition-all duration-700 ease-out transform opacity-0 translate-y-4 animate-fadeIn text-center">
      <div
        className="bg-red-100 border border-red-400 text-red-700 px-4 py-2 rounded mb-4 text-sm font-medium"
        style={{ fontFamily: "inherit" }}
      >
        ⚠️ Warning: Some subreddits may be NSFW
      </div>
    </div>
  );
}
