import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { X } from "lucide-react";

interface GameScreenProps {
  question: string | null;
  questionNumber: number;
  entropy?: number;
  guess: { name: string; probability: number } | null;
  onAnswer: (answer: string) => void;
  onGuessFeedback: (correct: boolean) => void;
  onQuit: () => void;
  isLoading?: boolean;
}

const answers = [
  { value: "yes", label: "Yes", color: "bg-primary hover:bg-primary/90 text-primary-foreground" },
  { value: "probably-yes", label: "Probably", color: "bg-primary/80 hover:bg-primary/70 text-primary-foreground" },
  { value: "maybe", label: "Maybe", color: "bg-muted hover:bg-muted/80 text-foreground" },
  { value: "probably-no", label: "Probably Not", color: "bg-muted hover:bg-muted/80 text-foreground" },
  { value: "no", label: "No", color: "bg-secondary hover:bg-secondary/80 text-secondary-foreground" },
];

const GameScreen = ({ 
  question, 
  questionNumber, 
  entropy = 0,
  guess,
  onAnswer, 
  onGuessFeedback,
  onQuit,
  isLoading = false
}: GameScreenProps) => {
  // Show guess screen if backend provided a guess
  if (guess) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-6 relative">
        {/* Quit button */}
        <Button
          variant="ghost"
          size="icon"
          onClick={onQuit}
          className="absolute top-4 right-4"
        >
          <X className="w-5 h-5" />
        </Button>

        {/* Guess */}
        <div className="max-w-2xl text-center mb-8 space-y-4">
          <h2 className="text-2xl font-semibold text-foreground">
            Is it {guess.name}?
          </h2>
          <p className="text-sm text-muted-foreground">
            Confidence: {Math.round(guess.probability * 100)}%
          </p>
        </div>

        {/* Feedback buttons */}
        <div className="flex gap-3">
          <Button
            onClick={() => onGuessFeedback(true)}
            size="lg"
            disabled={isLoading}
          >
            Yes, that's it
          </Button>
          <Button
            onClick={() => onGuessFeedback(false)}
            size="lg"
            variant="outline"
            disabled={isLoading}
          >
            No, keep going
          </Button>
        </div>
      </div>
    );
  }

  // Show question screen
  if (!question) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-muted-foreground">Loading...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 relative max-w-3xl mx-auto">
      {/* Quit button */}
      <Button
        variant="ghost"
        size="icon"
        onClick={onQuit}
        className="absolute top-4 right-4"
      >
        <X className="w-5 h-5" />
      </Button>

      {/* Progress */}
      <div className="w-full mb-8">
        <div className="flex justify-between items-center mb-2 text-sm text-muted-foreground">
          <span>Question {questionNumber}</span>
          {entropy > 0 && (
            <span>Uncertainty: {entropy.toFixed(2)}</span>
          )}
        </div>
        <Progress value={Math.max(0, Math.min(100, (1 - entropy / 10) * 100))} className="h-2" />
      </div>

      {/* Question */}
      <div className="text-center mb-12">
        <h2 className="text-2xl font-medium text-foreground mb-4">{question}</h2>
      </div>

      {/* Answer buttons */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-3 w-full">
        {answers.map((answer) => (
          <Button
            key={answer.value}
            onClick={() => onAnswer(answer.value)}
            className={`h-16 ${answer.color}`}
            disabled={isLoading}
          >
            {answer.label}
          </Button>
        ))}
      </div>
    </div>
  );
};

export default GameScreen;
