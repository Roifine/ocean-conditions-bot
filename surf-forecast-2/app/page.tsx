"use client"
import { useState, useEffect } from "react"
import { Waves, Clock, Calendar } from "lucide-react"
import Onboarding from "@/components/onboarding"
import RightNow from "@/components/right-now"
import ThisWeek from "@/components/this-week"

type AppState = "onboarding" | "main"
type MainView = "right-now" | "this-week"

export default function SurfForecast() {
  const [appState, setAppState] = useState<AppState>("onboarding")
  const [currentView, setCurrentView] = useState<MainView>("right-now")
  const [selectedBeach, setSelectedBeach] = useState<string>("")
  const [userSkill, setUserSkill] = useState<string>("")

  // Check if user has completed onboarding
  useEffect(() => {
    const hasOnboarded = localStorage.getItem("surf-app-onboarded")
    const savedBeach = localStorage.getItem("surf-app-beach")
    const savedSkill = localStorage.getItem("surf-app-skill")

    if (hasOnboarded && savedBeach && savedSkill) {
      setSelectedBeach(savedBeach)
      setUserSkill(savedSkill)
      setAppState("main")
    }
  }, [])

  const handleOnboardingComplete = (beach: string, skill: string) => {
    setSelectedBeach(beach)
    setUserSkill(skill)
    setAppState("main")

    // Save to localStorage
    localStorage.setItem("surf-app-onboarded", "true")
    localStorage.setItem("surf-app-beach", beach)
    localStorage.setItem("surf-app-skill", skill)
  }

  if (appState === "onboarding") {
    return <Onboarding onComplete={handleOnboardingComplete} />
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-primary text-primary-foreground p-4 shadow-lg">
        <div className="flex items-center justify-between max-w-md mx-auto">
          <div className="flex items-center gap-2">
            <Waves className="w-6 h-6" />
            <h1 className="text-xl font-bold">Doctor Surf</h1>
          </div>
          <div className="text-sm">
            {selectedBeach} • {userSkill}
          </div>
        </div>
      </header>

      {/* Bottom Navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-card border-t border-border">
        <div className="max-w-md mx-auto flex">
          <button
            onClick={() => setCurrentView("right-now")}
            className={`flex-1 flex flex-col items-center gap-1 py-3 px-4 transition-colors ${
              currentView === "right-now" ? "text-accent bg-accent/10" : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <Clock className="w-5 h-5" />
            <span className="text-xs font-medium">Right Now</span>
          </button>
          <button
            onClick={() => setCurrentView("this-week")}
            className={`flex-1 flex flex-col items-center gap-1 py-3 px-4 transition-colors ${
              currentView === "this-week" ? "text-accent bg-accent/10" : "text-muted-foreground hover:text-foreground"
            }`}
          >
            <Calendar className="w-5 h-5" />
            <span className="text-xs font-medium">This Week</span>
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-md mx-auto p-4 pb-20">
        {currentView === "right-now" && <RightNow beach={selectedBeach} />}
        {currentView === "this-week" && <ThisWeek beach={selectedBeach} />}
      </div>
    </div>
  )
}
