import { useState } from "react";
import LandingScreen from "@/components/LandingScreen";
import GameScreen from "@/components/GameScreen";
import ResultScreen from "@/components/ResultScreen";
import AboutModal from "@/components/AboutModal";
import { startGame, submitAnswer, submitGuessFeedback, getNextQuestion, type GameState } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

type GameStateType = "landing" | "playing" | "result";

const Index = () => {
  const { toast } = useToast();
  const [gameState, setGameState] = useState<GameStateType>("landing");
  const [currentState, setCurrentState] = useState<GameState | null>(null);
  const [guessedCharacter, setGuessedCharacter] = useState<{ name: string; quote?: string } | null>(null);
  const [showAbout, setShowAbout] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleStartGame = async () => {
    try {
      setIsLoading(true);
      const state = await startGame();
      setCurrentState(state);
      setGameState("playing");
      setGuessedCharacter(null);
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to start game",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleQuitGame = () => {
    setGameState("landing");
    setCurrentState(null);
    setGuessedCharacter(null);
  };

  const handleAnswer = async (answer: string) => {
    if (!currentState?.question || isLoading) return;

    try {
      setIsLoading(true);
      const newState = await submitAnswer(currentState.question.id, answer);
      setCurrentState(newState);

      // If backend provided a guess, we'll show it in GameScreen
      // The GameScreen component will handle showing the guess UI
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to submit answer",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleGuessFeedback = async (correct: boolean) => {
    if (!currentState?.guess || isLoading) return;

    try {
      setIsLoading(true);
      
      if (correct) {
        // User confirmed the guess is correct
        setGuessedCharacter({
          name: currentState.guess.name,
          // You can add quote lookup here if needed
        });
        setGameState("result");
      } else {
        // Wrong guess - get next question
        await submitGuessFeedback(false);
        const newState = await getNextQuestion();
        setCurrentState(newState);
      }
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to submit feedback",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      {gameState === "landing" && (
        <LandingScreen 
          onStart={handleStartGame} 
          onOpenAbout={() => setShowAbout(true)} 
        />
      )}

      {gameState === "playing" && currentState && (
        <GameScreen
          question={currentState.question?.text || null}
          questionNumber={currentState.questionNumber}
          entropy={currentState.entropy}
          guess={currentState.guess}
          onAnswer={handleAnswer}
          onGuessFeedback={handleGuessFeedback}
          onQuit={handleQuitGame}
          isLoading={isLoading}
        />
      )}

      {gameState === "result" && guessedCharacter && (
        <ResultScreen
          characterName={guessedCharacter.name}
          characterQuote={guessedCharacter.quote || `I knew it was ${guessedCharacter.name}!`}
          onPlayAgain={handleStartGame}
        />
      )}

      <AboutModal open={showAbout} onOpenChange={setShowAbout} />
    </div>
  );
};

export default Index;
