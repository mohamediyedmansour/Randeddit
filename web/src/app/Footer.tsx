export default function Footer() {
  return (
    <footer
      className="mt-auto w-full text-center py-4 text-gray-700 text-sm"
      style={{ fontFamily: "inherit" }}
    >
      Made with <span className="text-red-500">❤️</span> by{" "}
      <a
        href="https://github.com/mohamediyedmansour"
        target="_blank"
        rel="noopener noreferrer"
        className="underline hover:text-orange-600"
      >
        Iyed
      </a>
    </footer>
  );
}
