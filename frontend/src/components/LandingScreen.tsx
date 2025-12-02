import { Button } from "@/components/ui/button";
import { Info } from "lucide-react";

interface LandingScreenProps {
  onStart: () => void;
  onOpenAbout: () => void;
}

const LandingScreen = ({ onStart, onOpenAbout }: LandingScreenProps) => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4">
      {/* About button */}
      <Button
        variant="ghost"
        size="icon"
        onClick={onOpenAbout}
        className="absolute top-4 right-4"
      >
        <Info className="w-5 h-5" />
      </Button>

      {/* Content */}
      <div className="text-center space-y-6 max-w-md">
        <h1 className="text-4xl font-semibold text-foreground mb-2">
          Ind-inator
        </h1>
        <p className="text-muted-foreground mb-8">
          Think of a character and I'll try to guess who it is.
        </p>
        <Button
          onClick={onStart}
          size="lg"
          className="px-8 py-6 text-base"
        >
          Start Game
        </Button>
      </div>
    </div>
  );
};

export default LandingScreen;
