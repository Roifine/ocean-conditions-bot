"use client"
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Waves, Wind, TrendingUp, TrendingDown } from "lucide-react"

interface RightNowProps {
  beach: string
}

const currentConditions = {
  Bondi: {
    status: "Good",
    waveHeight: "3-4 ft",
    windSpeed: "8 mph",
    windDirection: "NW",
    tideStatus: "Rising",
    nextTide: "High at 2:30 PM",
    summary: "Solid 3-4ft waves with light offshore winds. Perfect for an afternoon session!",
    color: "good",
  },
  Maroubra: {
    status: "Excellent",
    waveHeight: "4-5 ft",
    windSpeed: "6 mph",
    windDirection: "NE",
    tideStatus: "Rising",
    nextTide: "High at 2:45 PM",
    summary: "Premium conditions with 4-5ft waves and light offshore winds. Get out there now!",
    color: "excellent",
  },
}

function getStatusColor(status: string) {
  switch (status) {
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

function getTideIcon(status: string) {
  return status === "Rising" || status === "High" ? (
    <TrendingUp className="w-4 h-4" />
  ) : (
    <TrendingDown className="w-4 h-4" />
  )
}

export default function RightNow({ beach }: RightNowProps) {
  const conditions = currentConditions[beach as keyof typeof currentConditions]

  return (
    <div className="space-y-4">
      {/* Current Status Card */}
      <Card className="bg-card border-border">
        <CardContent className="p-6 text-center">
          <div className="space-y-4">
            <div>
              <h2 className="text-sm font-medium text-muted-foreground mb-2">Right Now at {beach}</h2>
              <div className="flex items-center justify-center gap-3">
                <Badge className={`${getStatusColor(conditions.status)} text-white text-lg px-4 py-2`}>
                  {conditions.status}
                </Badge>
              </div>
            </div>

            <p className="text-foreground text-balance leading-relaxed">{conditions.summary}</p>
          </div>
        </CardContent>
      </Card>

      {/* Quick Conditions */}
      <div className="grid grid-cols-2 gap-3">
        <Card className="bg-card border-border">
          <CardContent className="p-4">
            <div className="flex items-center gap-2 mb-2">
              <Waves className="w-4 h-4 text-accent" />
              <span className="text-sm font-medium text-foreground">Waves</span>
            </div>
            <p className="text-lg font-semibold text-foreground">{conditions.waveHeight}</p>
          </CardContent>
        </Card>

        <Card className="bg-card border-border">
          <CardContent className="p-4">
            <div className="flex items-center gap-2 mb-2">
              <Wind className="w-4 h-4 text-accent" />
              <span className="text-sm font-medium text-foreground">Wind</span>
            </div>
            <p className="text-lg font-semibold text-foreground">
              {conditions.windSpeed} {conditions.windDirection}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Tide Info */}
      <Card className="bg-card border-border">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {getTideIcon(conditions.tideStatus)}
              <span className="text-sm font-medium text-foreground">Tide</span>
            </div>
            <div className="text-right">
              <p className="font-semibold text-foreground">{conditions.tideStatus}</p>
              <p className="text-sm text-muted-foreground">{conditions.nextTide}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
