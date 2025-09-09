"use client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Clock } from "lucide-react"

interface BestSurfTime {
  timeRange: string
  description: string
  stars: number
}

interface DayForecast {
  day: string
  date: string
  aiOverview: string
  conditions: {
    waveHeight: string
    waveDirection: string
    windSpeed: string
    windDirection: string
    tideStatus: "High" | "Low" | "Rising" | "Falling"
    rating: "Poor" | "Fair" | "Good" | "Excellent"
    nextTide: string
  }
  bestSurfTimes: BestSurfTime[]
}

const mockForecastData: DayForecast[] = [
  {
    day: "Monday",
    date: "Dec 9",
    aiOverview:
      "Solid start to the week with consistent 3-4ft waves building through the day. Light northwest winds will keep conditions clean, especially in the afternoon when waves peak at 4-5ft. Rising tide creates perfect timing for an afternoon session.",
    conditions: {
      waveHeight: "3-4 ft",
      waveDirection: "SW",
      windSpeed: "8 mph",
      windDirection: "NW",
      tideStatus: "Rising",
      rating: "Good",
      nextTide: "High at 2:30 PM",
    },
    bestSurfTimes: [
      { timeRange: "7:00 - 9:00", description: "Small waves, high tide, offshore wind", stars: 3 },
      { timeRange: "14:00 - 16:00", description: "Good size waves, rising tide", stars: 4 },
    ],
  },
  // ... existing forecast data ...
]

const beachData = {
  Bondi: mockForecastData,
  Maroubra: [
    // ... existing Maroubra data ...
  ],
}

interface ThisWeekProps {
  beach: string
}

function getRatingColor(rating: string) {
  switch (rating) {
    case "Excellent":
      return "bg-green-500"
    case "Good":
      return "bg-blue-500"
    case "Fair":
      return "bg-yellow-500"
    case "Poor":
      return "bg-red-500"
    default:
      return "bg-gray-500"
  }
}

function renderStars(count: number) {
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map((star) => (
        <div key={star} className={`w-3 h-3 ${star <= count ? "text-yellow-400" : "text-gray-300"}`}>
          ★
        </div>
      ))}
    </div>
  )
}

export default function ThisWeek({ beach }: ThisWeekProps) {
  const currentForecastData = beachData[beach as keyof typeof beachData]

  return (
    <div className="space-y-4">
      {/* Weekly Summary */}
      <div className="bg-muted rounded-lg p-4 border-border border">
        <h2 className="font-semibold text-foreground mb-2">This Week's Best Surf</h2>
        <p className="text-sm text-muted-foreground leading-relaxed">
          Wednesday looks exceptional with 4-6ft waves and light offshore winds at both beaches. Tuesday afternoon shows
          promise for Maroubra with clean 5-6ft sets. Avoid Thursday - small waves and strong onshore winds will make
          conditions poor across all spots.
        </p>
      </div>

      {/* Forecast Cards */}
      <div className="space-y-4">
        {currentForecastData.map((dayData, index) => (
          <Card key={index} className="bg-card border-border">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-lg text-foreground">{dayData.day}</CardTitle>
                  <p className="text-sm text-muted-foreground">{dayData.date}</p>
                </div>
                <Badge className={`${getRatingColor(dayData.conditions.rating)} text-white`}>
                  {dayData.conditions.rating}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* AI Overview section */}
              <div className="bg-accent/10 rounded-lg p-3 border-l-4 border-accent">
                <p className="text-sm text-foreground leading-relaxed">{dayData.aiOverview}</p>
              </div>

              {/* Best Surf Times section */}
              <div className="border-t border-border pt-3">
                <div className="flex items-center gap-2 mb-3">
                  <Clock className="w-4 h-4 text-muted-foreground" />
                  <span className="text-sm font-medium text-foreground">Best Surf Times</span>
                </div>
                <div className="space-y-3">
                  {dayData.bestSurfTimes.map((surfTime, timeIndex) => (
                    <div key={timeIndex} className="flex items-center justify-between p-3 bg-muted rounded-lg">
                      <div className="flex-1">
                        <div className="font-medium text-foreground mb-1">{surfTime.timeRange}</div>
                        <div className="text-sm text-muted-foreground">{surfTime.description}</div>
                      </div>
                      <div className="ml-3">{renderStars(surfTime.stars)}</div>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
