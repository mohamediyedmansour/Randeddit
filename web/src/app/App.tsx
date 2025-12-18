import { useEffect, useState } from "react";
import GitHubRibbon from "./GitHubStar";
import Footer from "./Footer";
import NSFWWarning from "./NSFWWarning";

interface Subreddit {
  subreddit: string;
  line_number: number;
}

export default function App() {
  const [subreddits, setSubreddits] = useState<Subreddit[]>([]);
  const [showWarning, setShowWarning] = useState(false);

  // Animate NSFW warning on mount
  useEffect(() => {
    const timer = setTimeout(() => setShowWarning(true), 300);
    return () => clearTimeout(timer);
  }, []);

  // Fetch subreddits
  const fetchSubreddits = async (count = 10) => {
    try {
      const res = await fetch(
        `https://randeddit-api.iyed.space/get_sub?count=${count}`
      );
      const data: Subreddit[] = await res.json();
      setSubreddits((prev) => [...prev, ...data]);
    } catch (error) {
      console.error("Failed to fetch subreddits:", error);
    }
  };

  useEffect(() => {
    fetchSubreddits();
  }, []);

  // Ensure at least 5 subreddits
  useEffect(() => {
    if (subreddits.length < 5) {
      fetchSubreddits();
    }
  }, [subreddits]);

  // Handle logo click
  const handleClick = () => {
    if (subreddits.length === 0) return;
    const sub = subreddits.shift();
    setSubreddits([...subreddits]);
    if (sub) {
      window.open(`https://reddit.com/r/${sub.subreddit}`, "_blank");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center bg-gradient-to-br from-orange-50 to-red-50 relative">
      {/* Centered logo container */}
      <div className="flex flex-col items-center justify-center flex-1 w-full">
        <div
          className="mb-8 inline-block cursor-pointer animate-breathe"
          onClick={handleClick}
        >
          <svg
            width="300"
            height="300"
            viewBox="0 0 300 300"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="drop-shadow-2xl"
          >
            {/* Background circle */}
            <circle cx="150" cy="150" r="140" fill="white" />

            {/* Reddit alien body */}
            <ellipse cx="150" cy="160" rx="60" ry="65" fill="#FF4500" />

            {/* Reddit alien head */}
            <circle cx="150" cy="120" r="45" fill="#FF4500" />

            {/* Eyes */}
            <circle cx="135" cy="115" r="8" fill="white" />
            <circle cx="165" cy="115" r="8" fill="white" />
            <circle cx="137" cy="115" r="4" fill="#1a1a1b" />
            <circle cx="167" cy="115" r="4" fill="#1a1a1b" />

            {/* Smile */}
            <path
              d="M 135 130 Q 150 140 165 130"
              stroke="#1a1a1b"
              strokeWidth="3"
              fill="none"
              strokeLinecap="round"
            />

            {/* Antenna */}
            <line
              x1="150"
              y1="75"
              x2="150"
              y2="45"
              stroke="#FF4500"
              strokeWidth="4"
            />

            {/* Dice as antenna ball - creative twist! */}
            <g transform="rotate(25 150 30)">
              <rect
                x="135"
                y="15"
                width="30"
                height="30"
                rx="4"
                fill="#FFD635"
                stroke="#1a1a1b"
                strokeWidth="2"
              />
              {/* Dice dots showing "6" */}
              <circle cx="142" cy="22" r="2.5" fill="#1a1a1b" />
              <circle cx="142" cy="30" r="2.5" fill="#1a1a1b" />
              <circle cx="142" cy="38" r="2.5" fill="#1a1a1b" />
              <circle cx="158" cy="22" r="2.5" fill="#1a1a1b" />
              <circle cx="158" cy="30" r="2.5" fill="#1a1a1b" />
              <circle cx="158" cy="38" r="2.5" fill="#1a1a1b" />
            </g>

            {/* Left arm holding a die */}
            <ellipse
              cx="95"
              cy="160"
              rx="15"
              ry="30"
              fill="#FF4500"
              transform="rotate(-30 95 160)"
            />
            <g transform="rotate(-15 75 155)">
              <rect
                x="60"
                y="140"
                width="28"
                height="28"
                rx="3"
                fill="#FFD635"
                stroke="#1a1a1b"
                strokeWidth="2"
              />
              {/* Dice showing "3" */}
              <circle cx="67" cy="147" r="2" fill="#1a1a1b" />
              <circle cx="74" cy="154" r="2" fill="#1a1a1b" />
              <circle cx="81" cy="161" r="2" fill="#1a1a1b" />
            </g>

            {/* Right arm holding a die */}
            <ellipse
              cx="205"
              cy="160"
              rx="15"
              ry="30"
              fill="#FF4500"
              transform="rotate(30 205 160)"
            />
            <g transform="rotate(15 225 155)">
              <rect
                x="212"
                y="140"
                width="28"
                height="28"
                rx="3"
                fill="#FFD635"
                stroke="#1a1a1b"
                strokeWidth="2"
              />
              {/* Dice showing "5" */}
              <circle cx="219" cy="147" r="2" fill="#1a1a1b" />
              <circle cx="233" cy="147" r="2" fill="#1a1a1b" />
              <circle cx="226" cy="154" r="2" fill="#1a1a1b" />
              <circle cx="219" cy="161" r="2" fill="#1a1a1b" />
              <circle cx="233" cy="161" r="2" fill="#1a1a1b" />
            </g>

            {/* Ears */}
            <circle cx="110" cy="100" r="12" fill="#FF4500" />
            <circle cx="190" cy="100" r="12" fill="#FF4500" />

            {/* Feet */}
            <ellipse cx="130" cy="215" rx="20" ry="12" fill="#FF4500" />
            <ellipse cx="170" cy="215" rx="20" ry="12" fill="#FF4500" />

            {/* Floating dice around for extra fun */}
            <g opacity="0.8">
              <rect
                x="35"
                y="220"
                width="20"
                height="20"
                rx="2"
                fill="#FFD635"
                stroke="#1a1a1b"
                strokeWidth="1.5"
                transform="rotate(20 45 230)"
              />
              <circle cx="45" cy="230" r="1.5" fill="#1a1a1b" />
            </g>

            <g opacity="0.8">
              <rect
                x="245"
                y="220"
                width="20"
                height="20"
                rx="2"
                fill="#FFD635"
                stroke="#1a1a1b"
                strokeWidth="1.5"
                transform="rotate(-20 255 230)"
              />
              <circle cx="250" cy="225" r="1.5" fill="#1a1a1b" />
              <circle cx="260" cy="225" r="1.5" fill="#1a1a1b" />
              <circle cx="255" cy="235" r="1.5" fill="#1a1a1b" />
            </g>
          </svg>
        </div>

        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          Random<span className="text-orange-600">dit</span>
        </h1>

        <p className="text-xl text-gray-600 mb-4">
          Roll the dice, discover a new subreddit! 🎲
        </p>

        {showWarning && <NSFWWarning />}
      </div>

      <Footer />
    </div>
  );
}
