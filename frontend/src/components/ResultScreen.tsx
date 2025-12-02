import { Button } from "@/components/ui/button";
import { Share2 } from "lucide-react";

interface ResultScreenProps {
  characterName: string;
  characterQuote: string;
  onPlayAgain: () => void;
}

const ResultScreen = ({ characterName, characterQuote, onPlayAgain }: ResultScreenProps) => {
  const handleShare = () => {
    const text = `Ind-inator guessed I was thinking of ${characterName}! 🎯`;
    if (navigator.share) {
      navigator.share({ text });
    } else {
      navigator.clipboard.writeText(text);
      alert("Copied to clipboard!");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6">
      <div className="text-center max-w-2xl space-y-8">
        {/* Result */}
        <div className="space-y-4">
          <h2 className="text-xl font-medium text-foreground">
            I guessed:
          </h2>
          <div className="bg-card rounded-lg p-8 border">
            <h1 className="text-3xl font-semibold text-foreground mb-4">
              {characterName}
            </h1>
            <p className="text-muted-foreground italic">
              "{characterQuote}"
            </p>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Button
            onClick={onPlayAgain}
            size="lg"
          >
            Play Again
          </Button>
          <Button
            onClick={handleShare}
            size="lg"
            variant="outline"
          >
            <Share2 className="w-4 h-4 mr-2" />
            Share
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ResultScreen;
