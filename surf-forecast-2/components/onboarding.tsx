"use client"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { MapPin, User, Waves } from "lucide-react"
import { useState } from "react"

interface OnboardingProps {
  onComplete: (beach: string, skill: string) => void
}

const beaches = [
  {
    name: "Bondi",
    description: "Famous beach with consistent waves",
    difficulty: "Intermediate",
    image: "/bondi-beach-aerial-view.jpg",
  },
  {
    name: "Maroubra",
    description: "Powerful waves for experienced surfers",
    difficulty: "Advanced",
    image: "/maroubra-beach-waves.jpg",
  },
]

const skillLevels = [
  { level: "Beginner", description: "Just starting out, learning basics" },
  { level: "Intermediate", description: "Can catch waves consistently" },
  { level: "Advanced", description: "Experienced surfer, all conditions" },
]

export default function Onboarding({ onComplete }: OnboardingProps) {
  const [selectedBeach, setSelectedBeach] = useState<string>("")
  const [selectedSkill, setSelectedSkill] = useState<string>("")

  const handleComplete = () => {
    if (selectedBeach && selectedSkill) {
      onComplete(selectedBeach, selectedSkill)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-primary text-primary-foreground p-4 shadow-lg">
        <div className="flex items-center justify-center max-w-md mx-auto">
          <div className="flex items-center gap-2">
            <Waves className="w-6 h-6" />
            <h1 className="text-xl font-bold">Doctor Surf</h1>
          </div>
        </div>
      </header>

      <div className="max-w-md mx-auto p-4 space-y-6">
        {/* Welcome Section */}
        <div className="text-center py-6">
          <h2 className="text-2xl font-bold text-foreground mb-2">Welcome to Doctor Surf</h2>
          <p className="text-muted-foreground">Let's personalize your surf forecast experience</p>
        </div>

        {/* Beach Selection */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 mb-3">
            <MapPin className="w-5 h-5 text-accent" />
            <h3 className="text-lg font-semibold text-foreground">Choose Your Beach</h3>
          </div>

          <div className="space-y-3">
            {beaches.map((beach) => (
              <Card
                key={beach.name}
                className={`cursor-pointer transition-all ${
                  selectedBeach === beach.name ? "ring-2 ring-accent bg-accent/5" : "hover:bg-muted/50"
                }`}
                onClick={() => setSelectedBeach(beach.name)}
              >
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <img
                      src={beach.image || "/placeholder.svg"}
                      alt={beach.name}
                      className="w-16 h-16 rounded-lg object-cover"
                    />
                    <div className="flex-1">
                      <h4 className="font-semibold text-foreground">{beach.name}</h4>
                      <p className="text-sm text-muted-foreground">{beach.description}</p>
                      <Badge variant="secondary" className="mt-1 text-xs">
                        {beach.difficulty}
                      </Badge>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Skill Level Selection */}
        <div className="space-y-4">
          <div className="flex items-center gap-2 mb-3">
            <User className="w-5 h-5 text-accent" />
            <h3 className="text-lg font-semibold text-foreground">Your Skill Level</h3>
          </div>

          <div className="space-y-3">
            {skillLevels.map((skill) => (
              <Card
                key={skill.level}
                className={`cursor-pointer transition-all ${
                  selectedSkill === skill.level ? "ring-2 ring-accent bg-accent/5" : "hover:bg-muted/50"
                }`}
                onClick={() => setSelectedSkill(skill.level)}
              >
                <CardContent className="p-4">
                  <h4 className="font-semibold text-foreground">{skill.level}</h4>
                  <p className="text-sm text-muted-foreground">{skill.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Continue Button */}
        <div className="pt-6">
          <Button
            onClick={handleComplete}
            disabled={!selectedBeach || !selectedSkill}
            className="w-full bg-accent hover:bg-accent/90 text-accent-foreground"
            size="lg"
          >
            Get My Surf Forecast
          </Button>
        </div>
      </div>
    </div>
  )
}
